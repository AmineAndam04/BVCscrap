import requests 
from bs4 import BeautifulSoup
import pandas as pd
import json
import datetime
from .utils import *

def loadata(name, start=None,end=None):
	"""
	Load Data 
	Inputs: 
			Input   | Type                             | Description
			=================================================================================
			 name   |string                            | You must respect the notation. To see the notation see BVCscrap.notation
	         start  |string "YYYY-MM-DD"               | starting date Must respect the notation
	         end    |string "YYYY-MM-DD"               | Must respect the notation
	Outputs:
	        Output | Type                             | Description
	       ================================================================================= 
	               | pandas.DataFrame (4 columns)     | Value	Low	High	Variation (%)	Volume 
		                           		   * !! For MASI you get JUST "Value"
	Exemple :
	import BVCscrap  as load
	data=load.loadata('BCP',start='2021-09-01',end='2021-09-10')
	"""
	code=get_code(name)
	if name!="MASI":
		if start and end:
			link="https://www.leboursier.ma/api?method=getPriceHistory&ISIN="+code+"&format=json&from="+start+"&to=" +end
		else :
			start='2011-09-18'      
			link="https://www.leboursier.ma/api?method=getPriceHistory&ISIN="+code+"&format=json&from="+start+"&to=" +end 
		request_data = requests.get(link)
		soup = BeautifulSoup(request_data.text,features="lxml")
		data=get_data(soup)
	else:
		link="https://www.leboursier.ma/api?method=getMasiHistory&periode=10y&format=json"
		request_data = requests.get(link)
		soup = BeautifulSoup(request_data.text,features="lxml")
		data_all=get_masi(soup)
		if start and end :
			data=produce_data(data_all,start,end)
		else: 
			data=data_all
	return data 

def loadmany(*args,start=None,end=None):
	"""
	Load the data of many equities  
	Inputs: 
			Input   | Type                             | Description
			=================================================================================
			 *args  |strings                           | You must respect the notation. To see the notation see BVCscrap.notation
	         start  |string "YYYY-MM-DD"               | starting date Must respect the notation
	         end    |string "YYYY-MM-DD"               | Must respect the notation
	Outputs:
	        Output | Type                                 | Description
	       ================================================================================= 
	               | pandas.DataFrame (len(args) columns) | close prices of selected equities
	Exemple :
	import BVCscrap as load
	data=load.loadmany('BCP','BMCI',start="2021-08-30",end='2021-09-04')
	"""
	data=[]
	for i in args:
		provisoir=loadata(i,start,end)
		row=provisoir["Value"]
		data.append(row)
	data=pd.concat(data,axis=1,sort="False")
	data.columns=args
	return data


def getIntraday(name):
    """
	Load the intraday data  
	Inputs: 
			Input   | Type                             | Description
			=================================================================================
			 name  |strings                           | You must respect the notation. To see the notation see BVCscrap.notation
	       
	Outputs:
	        Output | Type                                 | Description
	       ================================================================================= 
	               | pandas.DataFrame                     | Intraday data
	Exemple :
	import BVCscrap as load
	data=load.getIntraday('MASI')
    """
    if name!='MASI':
        code=get_code(name)
        link="https://www.leboursier.ma/api?method=getStockIntraday&ISIN="+code+"&format=json"
    else :
        link="https://www.leboursier.ma/api?method=getMarketIntraday&format=json"
    request_data = requests.get(link)
    soup = BeautifulSoup(request_data.text,features="lxml")
    data=intradata(soup)
    return data
