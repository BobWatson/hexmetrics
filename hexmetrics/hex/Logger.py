import os
import logging
from logging import FileHandler
from logging.handlers import SMTPHandler

class HexLogger():
    
    level = logging.DEBUG
    
    mail_handler = None
    file_handler = None
    
    def getLogFile(self):
        from datetime import datetime
        logging_dir = os.path.join(os.path.dirname(__file__), 'logs')
        log_file = os.path.join(logging_dir, 'hex.%s.log' % datetime.utcnow().date().isoformat())
        return log_file
    
    def attach(self, app):
        # app.logger.addHandler(self.mail_handler);
        app.logger.addHandler(self.file_handler);
    
    def __init__(self, app):
        
        self.mail_handler = SMTPHandler(app.config['EMAIL_SMTP_SERVER'],
                           app.config['EMAIL_FROM'],
                           app.config['EMAIL_ADMINS'], '%s: Application Failure' % app.config['SERVER_NAME'],
                           credentials=(app.config['EMAIL_SMTP_USER'], app.config['EMAIL_SMTP_PASS']))
    
        self.file_handler = FileHandler(self.getLogFile(), mode='a')
    
        self.mail_handler.setLevel(self.level)
        self.file_handler.setLevel(self.level)
        from logging import Formatter
        self.mail_handler.setFormatter(Formatter('''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s
             
            Message:
 
            %(message)s
            '''))
        self.file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s'))
        
        #self.attach(app)