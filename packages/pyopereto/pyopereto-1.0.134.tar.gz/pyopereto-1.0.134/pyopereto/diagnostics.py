import logging
from datetime import datetime
import tempfile
from pyopereto.client import OperetoClient
from optparse import OptionParser
import importlib
logger = logging.getLogger(__name__)
TEMP_DIR = tempfile.gettempdir()


def parse_options():
    usage = "%prog -s START_TIME -e END_TIME"

    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--start", dest="start_time", help="start time in the datetime ISO format")
    parser.add_option("-e", "--end", dest="end_time", help="end time in the datetime ISO format")

    (options, args) = parser.parse_args()
    if not options.start_time or not options.end_time:
        parser.error('Time range must be provided.')
    return (options, args)


def run_diagnostics(start_date, end_date):
    pandas_exist = importlib.util.find_spec("pandas")
    numpy_exist = importlib.util.find_spec("numpy")
    if not pandas_exist or not numpy_exist:
        raise Exception('Opereto diagnostics requires python pandas and numpy libs. Please install them and then re-run this command.')
    else:
        import pandas as pd
        import numpy as np

    final_results = []
    client = OperetoClient()

    start_time = datetime.fromisoformat(str(start_date))
    end_time = datetime.fromisoformat(str(end_date))
    timedelta = end_time - start_time
    if timedelta.total_seconds() > 60 * 60 * 24:
        raise Exception('Time range must not exceed 24 hours')

    print(f'API call per second for the perios of {start_date} to {end_date}. Measure intervals: 1 minute.')

    start = 0
    size = 10000
    request_data = {'start': start, 'limit': size,
                    'filter': {'datetime_range': {'from': str(start_date), 'to': str(end_date)}}}
    res = client._call_rest_api('post', '/search/diagnostics', data=request_data, error='Cannot fetch diagnostics data')
    all_diagnostics = res
    while len(res) == size:
        start = start + size
        request_data = {'start': start, 'limit': size,
                        'filter': {'datetime_range': {'from': str(start_date), 'to': str(end_date)}}}
        res = client._call_rest_api('post', '/search/diagnostics', data=request_data,
                                    error='Cannot fetch diagnostics data')
        all_diagnostics += res

    if all_diagnostics:
        print(f'\nTotal search entries found: {len(all_diagnostics)}\n')
        for entry in all_diagnostics:
            for url, calls in entry['value'].items():
                final_results.append({'url': url, 'orig_date': np.datetime64(entry['orig_date']), 'calls': int(calls)})

        df = pd.DataFrame(final_results)
        all_calls = df.groupby([pd.Grouper(key='orig_date', freq='1min')]).sum()
        print('Total API calls')
        all_calls_describe = all_calls['calls'].div(60).round().describe().fillna(0).astype(int)
        with pd.option_context("display.max_rows", 1000):
            print(all_calls_describe)

        print('\nAPI calls per URL')
        all_calls_per_url = df.groupby([pd.Grouper(key='orig_date', freq='1min'), 'url']).sum()
        all_calls_per_url_describe = all_calls_per_url['calls'].div(60).round(2).groupby('url').describe()
        with pd.option_context("display.max_rows", 1000):
            print(all_calls_per_url_describe)
    else:
        logger.error('No diagnostics data found for this time range')


if __name__ == "__main__":
    (options, args) = parse_options()
    run_diagnostics(str(options.start_time), str(options.end_time))