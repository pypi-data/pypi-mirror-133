import os
import logging
from datetime import datetime
import tempfile
from pyopereto.client import OperetoClient
from optparse import OptionParser
import importlib

logger = logging.getLogger(__name__)
TEMP_DIR = tempfile.gettempdir()
HOME_DIR = os.path.expanduser("~")
final_default_pdf = os.path.join(HOME_DIR, 'opereto_diagnostics_final.pdf')


def parse_options():
    usage = "%prog -s START_TIME -e END_TIME"

    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--start", dest="start_time", help="start time in the datetime ISO format")
    parser.add_option("-e", "--end", dest="end_time", help="end time in the datetime ISO format")
    parser.add_option("-f", "--file", dest="output_file", help="optional output file name", default=final_default_pdf)
    (options, args) = parser.parse_args()
    if not options.start_time or not options.end_time:
        parser.error('Time range must be provided.')
    return (options, args)


def remove_file_if_exists(file):
    if os.path.exists(file):
        os.remove(file)

def run_diagnostics(start_date, end_date, output_file=final_default_pdf):

    # requires also https://wkhtmltopdf.org
    required_packages = ['matplotlib', 'pandas', 'numpy', 'pdfkit', 'PyPDF2']
    for package in required_packages:
        if not importlib.util.find_spec(package):
            raise Exception(f'Opereto diagnostics requires the following python packages {str(required_packages)}. In addition it requres the wkhtmltopdf executable. Please install them and then re-run this command.')

    import pdfkit
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.backends.backend_pdf

    def create_report(data={}):
        temp_files = []

        def create_temp_file():
            fd, path = tempfile.mkstemp()
            temp_files.append(path)
            return path

        try:
            remove_file_if_exists(output_file)
            title = data['title']
            if 'tables' in data:
                for table in data['tables']:
                    temp_file = create_temp_file()
                    main_title = ''
                    if data['tables'].index(table)==0:
                        main_title = f'<h1>{title}</h1>'
                    html_table = table['df'].to_html()
                    table_title = table['title']
                    body = f"""
                        <html><body>
                        {main_title}
                        <h2>{table_title}</h2>
                        <head>
                            <meta name="pdfkit-page-size" content="Legal"/>
                            <meta name="pdfkit-orientation" content="Landscape"/>
                        </head>
                        {html_table}
                        </body></html>"""
                    pdfkit.from_string(body, temp_file)

            if 'plots' in data:
                pdf_doc = matplotlib.backends.backend_pdf.PdfPages
                for plot in data['plots']:
                    temp_file = create_temp_file()
                    with pdf_doc(temp_file) as pdf:
                        fig, axs = plt.subplots(figsize=(8, 4))
                        axs.set_title(plot['title'])
                        axs.set_xlabel(plot.get('xlabel') or 'Time')
                        axs.set_ylabel(plot.get('ylabel') or 'Value')
                        axs.plot(plot['df']['value'])
                        plt.tight_layout()
                        pdf.savefig(fig)
                        plt.close()

            # Merge all PDFs
            import PyPDF2
            pdfWriter = PyPDF2.PdfFileWriter()
            pdfWriter.addMetadata({
                '/Author': 'Dror Russo',
                '/Title': 'Opereto Diagnostics',
                '/CreationDate': str(datetime.today())
            })

            for filename in temp_files:
                pdf_reader = PyPDF2.PdfFileReader(filename)
                for page_num in range(pdf_reader.numPages):
                    page_obj = pdf_reader.getPage(page_num)
                    pdfWriter.addPage(page_obj)
            pdfOutputFile = open(output_file, 'wb')
            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()

        finally:
            for filename in temp_files:
                remove_file_if_exists(filename)

    final_results = []
    client = OperetoClient()

    start_time = datetime.fromisoformat(str(start_date))
    end_time = datetime.fromisoformat(str(end_date))
    timedelta = end_time - start_time
    if timedelta.total_seconds() > 60 * 60 * 24:
        raise Exception('Time range must not exceed 24 hours')

    main_title = f'Diagnostics KPI for the period of {start_date} to {end_date}. Measure intervals: 1 minute.'
    print(main_title)

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
        print(f'Total search entries found: {len(all_diagnostics)}\n')
        for entry in all_diagnostics:
            for kpi, kpivalue in entry['value'].items():
                final_results.append({'kpi': kpi, 'time': np.datetime64(entry['orig_date']), 'value': int(kpivalue)})

        df = pd.DataFrame(final_results)
        all_calls_per_url = df.groupby([pd.Grouper(key='time', freq='1min'), 'kpi']).sum()

        data = {
            'title': main_title,
            'tables': [
                {
                    'df': all_calls_per_url['value'].round(2).groupby('kpi').describe().reset_index(level='kpi'),
                    'title': 'API calls per URL'
                }
            ],
            'plots': [
                {
                    'df': df.groupby([pd.Grouper(key='time', freq='1min')]).sum(),
                    'title': 'API Calls Over Time'
                }
            ]
        }
        create_report(data)
        print(f'Generated diagnostics file: {output_file}')

    else:
        logger.error('No diagnostics data found for this time range')


if __name__ == "__main__":
    (options, args) = parse_options()
    run_diagnostics(str(options.start_time), str(options.end_time), str(options.output_file))