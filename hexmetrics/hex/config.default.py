import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

if not DEBUG:
    # Your server name, i.e. example.com
    SERVER_NAME = ''
    # I have my MySQL db details here, mysql://user:pass@mysql.server/db_name
    SQLALCHEMY_DATABASE_URI = ''
else:
    SERVER_NAME = '127.0.0.1:5000'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(basedir, os.pardir, 'hexmetrics.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True

# Used for CSRF - put something unique and hard to guess here
SECRET_KEY = ''

# Database table prefix
TABLE_PREFIX = 'hex'

# List of all administrators that will get user signup, error, etc. emails
EMAIL_ADMINS = ['']

# The from address for the site
EMAIL_FROM = ''
# The name the emails come from
EMAIL_FROM_NAME = 'HEX Metrics'

# If using Mailgun:
EMAIL_MAILGUN_API_KEY = '' # Your own API Key
EMAIL_MAILGUN_API_URL = '' # Your own API endpoint URL
EMAIL_MAILGUN_USER = '' # Your mailgun username for the above key/url
EMAIL_MAILGUN_PASSWORD = '' # The password for the above user

# Needed if you are using Mailgun, in case of error
EMAIL_SMTP_USER = '' # Your SMTP username
EMAIL_SMTP_PASS = '' # Your SMTP password
EMAIL_SMTP_SERVER = '' # Your SMTP server

# Twitter - for twitter feed; get these details from twitter dev. portal
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET=''
TWITTER_ACCESS_TOKEN_KEY='' 
TWITTER_ACCESS_TOKEN_SECRET=''

# The location of your cache directory
CACHE_FILE_LOCATION = os.path.join(basedir, os.pardir, 'public', 'static', 'cache')

# The URL (after /static/) for your cache
CACHE_URL_LOCATION = 'cache'