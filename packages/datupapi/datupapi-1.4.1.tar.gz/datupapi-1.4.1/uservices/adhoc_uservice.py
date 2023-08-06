import os
import sys

from datupapi.utils.utils import Utils



def main():
    utls = Utils(config_file='config.yml', logfile='data_ranking', log_path='output/logs')
    message = '<p>Hola Equipo,</p> \
                <p>Datup te informa que nuestra plataforma ha finalizado tus pronosticos. Ingresa a este <a href="http://www.datup.ai">link</a> para descargarlos.</p> \
                <p>Cordialmente,</p> \
                <p>Datup Team</p> \
                <p><a href="http://www.datup.ai">www.datup.ai</a></p>'
    response = utls.send_email_notification(to_emails=['neosagan@gmail.com'],
                                            cc_emails=[],
                                            bcc_emails=['ramiro@datup.ai'],
                                            html_message=message)

if __name__ == '__main__':
    main()
    sys.exit(0)