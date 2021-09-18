from bs4 import BeautifulSoup
import requests 
import pandas as pd
import json
from .Notation import notation_code



def get_code(name):
    nottation_code=notation_code()
    for action in nottation_code :
        if action["name"]==name :
            code=action['ISIN']
            return code

def get_data(soup):
    table= json.loads(soup.text)
    row_data=pd.DataFrame(table["result"])
    date=row_data['date']
    row_data.drop(['date'],axis=1,inplace=True)
    row_data.index=date
    row_data.columns=["Value","Low","High","Variation (%)","Volume"]
    return row_data

def intradata(soup):
    table= json.loads(soup.text)
    row_data=pd.DataFrame(table["result"][0])
    index=row_data['labels'].values
    row_data.drop(['labels'],axis=1,inplace=True)
    row_data.index=index
    row_data.columns=["Value"]
    return row_data


def get_masi(soup):
    table= json.loads(soup.text)
    row_data=pd.DataFrame(table["result"])
    date=row_data['labels']
    row_data.drop(['labels'],axis=1,inplace=True)
    row_data.index=date.apply(lambda x :datetime.datetime.fromtimestamp(x).date())
    row_data.columns=["Value"]
    return row_data


def produce_data(data,start,end):
    start=pd.to_datetime(start).date()
    end=pd.to_datetime(end).date()
    return data.loc[start:end]
