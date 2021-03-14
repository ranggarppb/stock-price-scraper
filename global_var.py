"""

Collection of configuration variables

"""
from utils import config_reader
import json
import os
CONFIG_FILE="config.ini"

config_google_storage = config_reader(CONFIG_FILE, section="google_storage")
config_rapid_api = config_reader(CONFIG_FILE, section="rapid_api")

# configuration of google cloud storage to read and store raw sentiment data
if config_google_storage["env"] != "local" :
    SERVICE_ACCOUNT_CREDENTIAL = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
else :
    SERVICE_ACCOUNT_CREDENTIAL = config_google_storage["local_credential"]
STORAGE_BUCKET = config_google_storage["storage_bucket"]
DATA_FILE = config_google_storage["data_file"]
GOOGLE_STORAGE_CONFIG = {
    "SERVICE_ACCOUNT_CREDENTIAL":SERVICE_ACCOUNT_CREDENTIAL,
    "STORAGE_BUCKET":STORAGE_BUCKET,
    "DATA_FILE":DATA_FILE
}

# configuration of xrapid api
URL = config_rapid_api["url"]
X_RAPID_KEY = config_rapid_api["x_rapidapi_key"]
LIST_STOCKS = config_rapid_api["list_stocks"].split(",")
SENTIMENT_DB_TMP = config_rapid_api["sentiment_db_tmp"]
X_RAPID_CONFIG = {
    "URL":URL,
    "X_RAPID_KEY":X_RAPID_KEY,
    "LIST_STOCKS":LIST_STOCKS,
    "SENTIMENT_DB_TMP":SENTIMENT_DB_TMP
}
