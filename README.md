# BVCscrap
BVCscrap is a Python library to retrieve data from [LeBoursier.ma](https://www.leboursier.ma/), which provides data retrieval from up to 74 stocks. BVCscrap allows the user to download historical data from all the shares traded at Casablanca Stock Exchange. 

## Requirements 
In order to use BVCscrap you should download the following packages: requests, beautifulsoup4, lxml, json, and datetime.

The outputs of this library are DataFrames, so Pandas should be installed 

## Installation
Download the source code of the library [BVCscrap](https://github.com/AmineAndam04/BVCscrap/tree/main/BVCscrap) and put it in your working directory or  use
```python
import os
path="C:/Users/pc/Desktop/..."  # the location of the downloaded code 
os.chdir(path)
```
Then import the libray : 
```python
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
```python
import BVCscrap  as load
data=load.loadata('Wafa Assur')
data.tail()
```
```{r, engine='python', count_lines}
              close     high     low    open    vol
2020-10-27	3355	3355	3355	3355	10
2020-11-02	3355	3355	3355	3355	3
2020-11-03	3360	3360	3357	3357	307
2020-11-09	3427	3427	3427	3427	1
2020-11-10	3450	3450	3428	3428	9
```
### Data of many stocks
```python
import BVCscrap  as load
data=load.loadmany('BoA','BCP','BMCI')
data.tail()
```
```{r, engine='python', count_lines}
	         BoA	 BCP	BMCI
2020-11-09	140.5	241.90	609.0
2020-11-10	143.0	244.00	608.9
2020-11-11	143.7	241.50	NaN
2020-11-12	143.0	243.80	NaN
2020-11-13	143.7	242.45	610.0
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
