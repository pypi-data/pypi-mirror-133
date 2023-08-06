import json
import os
import sys
import time

import pandas as pd

from datupapi.extract.io import IO


def main():
    io = IO(config_file='config.yml', logfile='data_io', log_path='output/logs')

    io.logger.debug('Data extraction starting...')
    df_xls = io.download_excel(q_name='Base de Datos CNCH_3.xlsx',
                               sheet_name='Venta 2015-2021',
                               datalake_path='dev/ramiro/as-is',
                               types={'Mes': str, 'Semana': str},
                               header_=0, num_records=10)
    io.upload_csv(df_xls,
                  q_name='Qraw',
                  datalake_path='dev/ramiro/output/sales')
    io.logger.debug('Data extraction completed...')
    io.upload_log()
    # Microservice response
    response = {
        'ConfigFileUri': os.path.join('s3://', io.datalake, io.config_path, 'config.yml')
    }
    io.upload_json_file(message=response, json_name='extract_response', datalake_path=io.response_path)


if __name__ == '__main__':
    main()
    sys.exit(0)