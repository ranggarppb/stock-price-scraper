import requests
import json
from datetime import datetime
import pandas as pd
from google.cloud import storage
from global_var import GOOGLE_STORAGE_CONFIG, X_RAPID_CONFIG

X_RAPID_KEY = X_RAPID_CONFIG["X_RAPID_KEY"]
with open(X_RAPID_KEY,'r') as f:
    x_rapid_config = f.readlines()

HEADERS = {
    'x-rapidapi-key': x_rapid_config[0][:-1],
    'x-rapidapi-host': x_rapid_config[1]
    }

def get_sentiment_data(response_xrapid, stock, database_input):

    prices = pd.DataFrame(response_xrapid['prices'])
    prices["date"] = prices["date"].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'))
    prices['open-1'] = prices['open'].shift(periods=-1)
    prices['diff'] = prices['open'] - prices['open-1']
    prices['positive_sentiment'] = prices['diff'].apply(lambda x : 1 if x > 0 else 0)
    prices['stock'] = stock.split('.')[0]
    sentiment = prices[['date','positive_sentiment','stock']]

    database_result = pd.concat([database_input,sentiment], axis=0)
    database_result = database_result.drop_duplicates(subset=['date','positive_sentiment','stock'])

    return database_result
    
if __name__ == '__main__' :

    storage_client = storage.Client.from_service_account_json(GOOGLE_STORAGE_CONFIG["SERVICE_ACCOUNT_CREDENTIAL"])
    bucket = storage_client.get_bucket(GOOGLE_STORAGE_CONFIG["STORAGE_BUCKET"])
    blob_input = bucket.get_blob(GOOGLE_STORAGE_CONFIG["DATA_FILE"])
    blob_input.download_to_filename(X_RAPID_CONFIG["SENTIMENT_DB_TMP"])

    database_input = pd.read_csv(X_RAPID_CONFIG["SENTIMENT_DB_TMP"], encoding='utf-8')
    database_result = database_input.copy()

    for stock in X_RAPID_CONFIG['LIST_STOCKS'] :
        querystring = {"symbol":stock,"region":"Indonesia"}
        response = requests.request("GET", X_RAPID_CONFIG["URL"], headers=HEADERS, params=querystring)
        response = json.loads(response.text)
        database_result = get_sentiment_data(response, stock, database_result)
        database_result.reset_index(drop=True, inplace=True)

    database_result.to_csv(X_RAPID_CONFIG["SENTIMENT_DB_TMP"], encoding='utf-8')

    blob_output = bucket.get_blob(GOOGLE_STORAGE_CONFIG["DATA_FILE"])
    blob_output.upload_from_filename(X_RAPID_CONFIG["SENTIMENT_DB_TMP"])
