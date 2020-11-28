from bs4 import BeautifulSoup
import requests 
import pandas as pd
import json
import datetime
from .Notation import notation_code



# Get the code of the asset to acces data
def get_code(name):
	notation_code=notation_code()
    for action in notation_code:
        if action["name"]==name:
            code=action['ISIN']
            return code

# Get data from json file
def get_data(soup):
	table= json.loads(soup.text)
	row_data=pd.DataFrame(table)
	result=row_data["result"]
	date=[]
	ouverture=[]
	plus_haut=[]
	plus_bas=[]
	fermeture=[]
	volume=[]
	for row in result:
		date_pro=datetime.datetime.fromtimestamp(row[0]/1000.0)
		date.append(str(date_pro.date()))
		ouverture.append(row[1])
		plus_haut.append(row[2])
		plus_bas.append(row[3])
		fermeture.append(row[4])
		volume.append(row[5])
	data=pd.DataFrame()
	data["Clôture"]=fermeture
	data["Plus_haut"]=plus_haut
	data["Plus_bas"]=plus_bas
	data["Ouverture"]=ouverture
	data["Volume"]=volume
	data.index=date
	return data 

# Produce data from the date strat until the date end
def produce_data(data,start,end):
	return data.loc[start:end]