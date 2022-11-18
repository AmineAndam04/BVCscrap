# BVCscrap
BVCscrap is a Python library to retrieve data from [LeBoursier.ma](https://www.leboursier.ma/) and [Bourse de Casablanca](https://www.casablanca-bourse.com/bourseweb/index.aspx), which provides data retrieval from up to 78 stocks and indices. BVCscrap allows the user to download historical and intraday data from all the shares traded on Casablanca Stock Exchange. 

BVCscrap stands for "La Bourse des valeurs de Casablanca" scraper.

-	PyPI: https://pypi.org/project/BVCscrap/
## Requirements 
In order to use BVCscrap you should download the following packages: requests, beautifulsoup4, lxml, json, and datetime.

The outputs of this library are DataFrames or dictionaries, so Pandas should be installed 

## Install

```python
pip install BVCscrap
import BVCscrap as bvc
```
## What's new :
For each stock you can get: Session data, latest transactions, best limit and  data of the last 5 sessions:

https://user-images.githubusercontent.com/49843367/159122217-c2bc3225-df3a-40eb-abfd-a890fdfa2f2b.mp4


You can get all the key indicators available at "Bourse de Casablanca"


https://user-images.githubusercontent.com/49843367/159122265-efe58782-02ae-43ff-8fe8-04054c3de5e3.mp4

You can also get indexes summary for each session. Examples and more functions are available at  [this notebook](/BVCscrap_Exemple.ipynb)
![indicateur_02](https://user-images.githubusercontent.com/49843367/159123465-bd556c63-bbbf-4354-aea8-fbd43f900983.png)

## How to use
To use this libary there is a notation to respect: names of stocks.
You can find jupyter notebooks on [Github](https://github.com/AmineAndam04/BVCscrap)
### Get the notation
```python 
import BVCscrap  as bvc
bvc.notation()
```
```{r, engine='python', count_lines}
['Addoha',
 'AFMA',
 'Afric Indus',
 'Afriquia Gaz',
 'Agma',
 .
 .
 'Zellidja',
 'MASI','MSI20']

```

### Data of one single stock
Syntaxe :`loadata(name, start=None,end=None,decode="utf-8")`

To get data from date 0 (The data is provided from Septembre 2016)
```python
import BVCscrap  as bvc
data=bvc.loadata('BCP')
data.tail()
```
```{r, engine='python', count_lines}
             Value	  Min	   Max	    Variation	       Volume
   date                                  
22/09/2021	271.00	 269.60	  271.00	0.00		52908
23/09/2021	272.60	 271.00	  273.00	0.59		37230
24/09/2021	276.00	 271.00	  278.00	1.25		162109
27/09/2021	275.00	 272.05	  276.95       -0.36		51533
28/09/2021	276.05	 272.70	  276.05	0.38		17676
```
You can get data between two periods :
```python
data=bvc.loadata('CIH',start='2018-01-01',end='2019-01-01')
data
```
```{r, engine='python', count_lines}
	       Value	Min	 Max   Variation  	Volume
date					
02/01/2018	278.0	278.00	279.5	-2.80	  	312
03/01/2018	278.0	278.00	279.5	0.00		312
...	...	...	...	...	...
28/12/2018	294.0	294.00	301.0	-2.00		211865
31/12/2018	300.0	300.00	300.0	2.04		12
```
You can get the historical data of MASI and MSI20
```python
data=bvc.loadata('MASI',start='2022-09-01',end='2022-09-5')
data
```
```{r, engine='python', count_lines}
		   Value
labels	
2022-09-01	12127.1717
2022-09-02	12136.2882
2022-09-05	12140.7196
```

```python
data=bvc.loadata('MSI20',start='2022-09-01',end='2022-09-5')
data
```
```{r, engine='python', count_lines}
		   Value
labels	
2022-09-01	980.633689
2022-09-02	981.350658
2022-09-05	982.005686
```
Sometime you may face some encoding\decoding issues, you can change the value of `decode` argument from its default value "utf-8" to another format  (e.g "utf-8-sig" is working )

### Data of many stocks
Syntaxe :`loadmany(*args,start=None,end=None,feature="Value",decode="utf-8")`
```python
data=bvc.loadmany('BCP','CIH')
data.tail()
```
```{r, engine='python', count_lines}
             BCP     CIH
22/09/2021	271.00	301.0
23/09/2021	272.60	305.0
24/09/2021	276.00	313.0
27/09/2021	275.00	310.0
28/09/2021	276.05	305.8
```
You can use start and end arguments :
```python
data=bvc.loadmany('BCP','CIH',start='2018-01-01',end='2019-01-01')
data.tail()
```
```{r, engine='python', count_lines}
	         BCP	CIH
date		
02/01/2018	293.0	278.0
03/01/2018	289.9	278.0
04/01/2018	285.3	280.8
05/01/2018	283.0	280.8
08/01/2018	285.4	280.8
...	...	...
25/12/2018	279.0	294.2
26/12/2018	277.0	296.0
27/12/2018	279.9	300.0
28/12/2018	280.0	294.0
31/12/2018	280.0	300.0
```
In case you want to have data of lots of stocks you can give the function a list of these stocks. Moreover `feature` argument let you choose another variable (Value, Min, Max, Variation, Volume")

```python
data=bvc.loadmany(['BCP','BMCI','BOA','CIH'],start="2021-08-30",end='2021-09-04',feature="Volume")
data
```
```{r, engine='python', count_lines}
		BCP	BMCI	BOA	CIH
  Date				
30/08/2021	702	33	172	53
31/08/2021	69575	2515	5853	1005
01/09/2021	28095	2515	3700	1005
02/09/2021	55744	2353	14	50
03/09/2021	26533	2353	8300	500
```
## Intraday data
Syntaxe : `getIntraday(name,decode="utf-8")`
```python
import BVCscrap  as load
data=load.getIntraday('MASI')
data
```
```{r, engine='python',count_lines}
 	 Value
09:30	12899.66
09:31	12900.10
09:32	12900.60
09:34	12900.45
09:35	12901.24
...	...
15:12	12975.64
15:14	12976.79
15:17	12976.69
15:18	12978.58
15:30	13019.20
```
## Session data
Syntaxe : `getCours(name)`
```python
cours=bvc.getCours("BOA") 
cours.keys()
```
```{r,engine="python",count_lines}
dict_keys(['Données_Seance', 'Meilleur_limit', 'Dernieres_Tansaction', 'Seance_prec'])
```
```python
import pandas as pd
cours["Données_Seance"]
cours['Meilleur_limit']
pd.DataFrame(cours["Seance_prec"])
pd.DataFrame(cours["Dernieres_Tansaction"])
```
## Key Indicators
Syntaxe : `getKeyIndicators(name,decode='utf-8')`
```python
indicateur=bvc.getKeyIndicators('BOA')
indicateur.keys()
```
```{r,engine="python",count_lines}
dict_keys(['Info_Societe', 'Actionnaires', 'Chiffres_cles', 'Ratio'])
```
## Dividend
Syntaxe: `getDividend(name,decode='utf-8')`
```python
dividends=bvc.getDividend("BOA")
pd.DataFrame(dividends)
```
```{r,engine="python",count_lines}
        Annee	Montant_Dividende Type_Dividende  Date_detachement  Date_paiement
0	2020	  5,00	           Ordinaire	   15/07/2021	    29/07/2021
1	2019	  5,00	           Ordinaire	   10/08/2020	    28/09/2020
2	2018	  5,00		   Ordinaire	   03/07/2019	    15/08/2019
3	2017	  5,00		   Ordinaire	   29/06/2018	    10/07/2018
```
## Indexes summary
Syntaxe : `getIndex()`
```python
index=bvc.getIndex()
index.keys()
```
```{r,engine="python",count_lines}
dict_keys(['Resume indice', 'Indice rentabilite', 'Indices en devises', 'Indice FTSE', 'Indices sectoriels'])
```
## Weights
Syntaxe : `getPond()`
```python
pond=bvc.getPond()
pd.DataFrame(pond)
```
```{r,engine="python",count_lines}
	Code Isin	Instrument    Nombre de titres	Cours	Facteur flottant Facteur plafonnement	Capitalisation flottante Poids
0	MA0000012445	ATTIJARIWAFA BANK	215140839 477,95	0,30	  1,00	                    30847969200,02	 0,1834
1	MA0000011488	ITISSALAT AL-MAGHRIB	879095340 130,10	0,20	  1,00			    22874060746,80	 0,1360
2	MA0000012320	LAFARGEHOLCIM MAR	23431240 1919,00	0,30	  1,00			    13489364868,00	 0,0802
```
## Indexes of the current session
Syntaxe: `getIndexRecap()`
```python
recap=bvc.getIndexRecap()
recap.keys()
```
```{r,engine="python",count_lines}
dict_keys(['Indice', 'Volume Global', 'Plus forte hausse', 'Plus forte baisse'])
```


## Getting Help 
If you are working in Jupyter notebook/lab, you can see the docstring of our  functions by using Shift+Tab. An example is shown below
```python
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
	     	                | pandas.DataFrame (4 columns)     | close high low open vol
"""
```


Question? Contact me on Twitter [@AmineAndam](https://twitter.com/AmineAndam)  or on Linkedin [ANDAM AMINE](https://www.linkedin.com/in/amineandam/).
