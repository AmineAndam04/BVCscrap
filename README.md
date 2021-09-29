# BVCscrap
BVCscrap is a Python library to retrieve data from [LeBoursier.ma](https://www.leboursier.ma/), which provides data retrieval from up to 74 stocks. BVCscrap allows the user to download historical and intraday data from all the shares traded at Casablanca Stock Exchange. 

## Requirements 
In order to use BVCscrap you should download the following packages: requests, beautifulsoup4, lxml, json, and datetime.

The outputs of this library are DataFrames, so Pandas should be installed 

## Installation

```python
pip install BVCscrap
import BVCscrap as load
```
## Usage
To use this libary there is a notation to respect: names of stocks.
### Get the notation
```python 
import BVCscrap  as load
load.notation()
```
```{r, engine='python', count_lines}
['Addoha',
 'AFMA',
 'Afric Indus',
 'Afriquia Gaz',
 'Agma',
 'Alliances',
 'Aluminium Maroc',
 'ATLANTASANAD',
 'Attijariwafa',

```

### Data of one single stock
To get data from date 0 (The data is provided from Septembre 2016)
```python
import BVCscrap  as load
data=load.loadata('BCP')
data.tail()
```
```{r, engine='python', count_lines}
             Value	  Low	   High	  Variation(%)	Volume
   date                                  
22/09/2021	271.00	 269.60	  271.00	0.00		52908
23/09/2021	272.60	 271.00	  273.00	0.59		37230
24/09/2021	276.00	 271.00	  278.00	1.25		162109
27/09/2021	275.00	 272.05	  276.95   -0.36		51533
28/09/2021	276.05	 272.70	  276.05	0.38		17676
```
You can get data between two periods :
```python
data=load.loadata('CIH',start='2018-01-01',end='2019-01-01')
data
```
```{r, engine='python', count_lines}
	       Value	Low	 High   Variation (%)	Volume
date					
02/01/2018	278.0	278.00	279.5	-2.80	  	312
03/01/2018	278.0	278.00	279.5	0.00		312
...	...	...	...	...	...
28/12/2018	294.0	294.00	301.0	-2.00		211865
31/12/2018	300.0	300.00	300.0	2.04		12
```
### Data of many stocks
```python
import BVCscrap  as load
load.loadmany('BCP','CIH')
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
load.loadmany('BCP','CIH',start='2018-01-01',end='2019-01-01')
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
## Intraday data
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
