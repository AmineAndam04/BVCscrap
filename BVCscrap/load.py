import requests 
from bs4 import BeautifulSoup
import pandas as pd
import json
import datetime
from .utils import *

def loadata(name, start=None,end=None,decode="utf-8"):
	"""
	Load Data 
	Inputs: 
			Input   | Type                             | Description
			=================================================================================
			 name   |string                            | You must respect the notation. To see the notation see BVCscrap.notation()
	         start  |string "YYYY-MM-DD"               | starting date Must respect the notation
	         end    |string "YYYY-MM-DD"               | Must respect the notation
	         decode |string                            | type of decoder. default value is utf-8. If it is not working use utf-8-sig
	Outputs:
	        Output | Type                             | Description
	       ================================================================================= 
	               | pandas.DataFrame (4 columns)     |Value	Min	Max	Variation	Volume
	"""
	code=get_code(name)
	if name != "MASI" and name != "MSI20":
		if start and end:
			link="https://medias24.com/content/api?method=getPriceHistory&ISIN="+ code+"&format=json&from="+start +"&to=" + end
		else :
			start='2011-09-18'
			end= str(datetime.datetime.today().date())    
			link="https://medias24.com/content/api?method=getPriceHistory&ISIN="+ code+"&format=json&from="+start +"&to=" + end 
		request_data = requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(request_data.text,features="lxml")
		data=get_data(soup,decode)
	else:
		if name=="MASI" :
			link="https://medias24.com/content/api?method=getMasiHistory&periode=10y&format=json"
		else:
			link="https://medias24.com/content/api?method=getIndexHistory&ISIN=msi20&periode=10y&format=json"
		request_data = requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})
		soup = BeautifulSoup(request_data.text,features="lxml")
		data_all=get_index(soup,decode)
		if start and end :
			data=produce_data(data_all,start,end)
		else: 
			data=data_all
	return data   

def loadmany(*args,start=None,end=None,feature="Value",decode="utf-8"):
	"""
	Load the data of many equities  
	Inputs: 
			Input   | Type                             | Description
			=================================================================================
			 *args  |strings                           | You must respect the notation. To see the notation see BVCscrap.notation
	         start  |string "YYYY-MM-DD"               | starting date Must respect the notation
	         end    |string "YYYY-MM-DD"               | Must respect the notation
	         feature|string                            | Variable : Value,Min,Max,Variation or Volume
	         decode |string                            | type of decoder. default value is utf-8. If it is not working use utf-8-sig
	Outputs:
	        Output | Type                                 | Description
	       ================================================================================= 
	               | pandas.DataFrame (len(args) columns) | close prices of selected equities
	"""
	if type(args[0])==list:
		args=args[0]
	data=pd.DataFrame(columns=args)
	for stock in args:
		value=loadata(stock,start,end,decode)
		data[stock]=value[feature]
	return data


def getIntraday(name,decode="utf-8"):
    """
    Load intraday data
    Inputs: 
        -Name: stock,index 
        -decode: default value is "utf-8", if it is not working use : "utf-8-sig"
    
    """
    if name != "MASI" and name != "MSI20":
        code=get_code(name)
        link="https://medias24.com/content/api?method=getStockIntraday&ISIN="+code+"&format=json"
    elif name == "MASI":
            link="https://medias24.com/content/api?method=getMarketIntraday&format=json"
    else :
            link="https://medias24.com/content/api?method=getIndexIntraday&ISIN=msi20&format=json"
    request_data = requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request_data.text,features="lxml")
    data=intradata(soup,decode)
    return data
