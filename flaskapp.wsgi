import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/")
from userApp import userApp as application
application.secret_key = '2240641'
