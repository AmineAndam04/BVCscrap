import requests 
from bs4 import BeautifulSoup
from .utils import *

def getCours(name):
    """
         load : Session data, latest transaction, best limit and  data of the last 5 sessions

         Input  | Type              |Description
         ===============================================================================
         name   | String            |Name of the company.You must respect the notation.
                |                   |To g:et the notation : BVCscrap.notation()

         Output |Type               |Description
         =====================================================
                |Dictionary         | 
    """
    code=get_valeur(name) 
    data={"__EVENTTARGET": "SocieteCotee1$LBIndicCle"}
    headers =   {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    link="https://www.casablanca-bourse.com/bourseweb/Societe-Cote.aspx?codeValeur="+code+"&cat=7"
    res = requests.post(link,data=data,headers=headers).content
    soup = BeautifulSoup(res,'html.parser')
    result= getTables(soup)
    return result

def getKeyIndicators(name,decode='utf-8'):
    """
         load : get key indicators

         Input  | Type              |Description
         ===============================================================================
         name   | String            |Name of the company.You must respect the notation.
                |                   |To get the notation : BVCscrap.notation()

         Output |Type               |Description
         =====================================================
                |Dictionary         | 
    """
    code=get_valeur(name)
    data={"__EVENTTARGET": "SocieteCotee1$LBFicheTech"}
    headers =   {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    link="https://www.casablanca-bourse.com/bourseweb/Societe-Cote.aspx?codeValeur="+code+"&cat=7"
    res = requests.post(link,data=data,headers=headers).content.decode(decode)
    soup = BeautifulSoup(res,'html.parser')
    result=getTablesFich(soup)
    return result

def getDividend(name,decode='utf-8'):
    """
         load :get dividends

         Input  | Type              |Description
         ===============================================================================
         name   | String            |Name of the company.You must respect the notation.
                |                   |To get the notation : BVCscrap.notation()

         Output |Type               |Description
         =====================================================
                |Dictionary         | 
    """
    code=get_valeur(name)
    data={"__EVENTTARGET": "SocieteCotee1$LBDividende"}
    headers =   {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    link="https://www.casablanca-bourse.com/bourseweb/Societe-Cote.aspx?codeValeur="+code+"&cat=7"
    res = requests.post(link,data=data,headers=headers).content.decode(decode)
    soup = BeautifulSoup(res,'html.parser')
    result=getDivi(soup)
    return result

def getIndex():
    """
         load : indexes summary

         Input  | Type              |Description
         ===============================================================================
                |                   |

         Output |Type               |Description
         =====================================================
                |Dictionary         | 
    """
    link="https://www.casablanca-bourse.com/bourseweb/Activite-marche.aspx?Cat=22&IdLink=297"
    request= requests.Session()
    code_soup= request.get(link,headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(code_soup.content,features="lxml")
    result=getAllIndex(soup)
    return result

def getPond():
    """
         load : weights(Pondération)

         Input  | Type              |Description
         ===============================================================================
                |                   |

         Output |Type               |Description
         =====================================================
                |Dictionary         | 
    """
    link="https://www.casablanca-bourse.com/bourseweb/indice-ponderation.aspx?Cat=22&IdLink=298"
    request= requests.Session()
    code_soup= request.get(link,headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(code_soup.content,'html.parser')
    return getPondval(soup)

def getIndexRecap():
    """
         load : session recap

         Input  | Type              |Description
         ===============================================================================
                |                   |

         Output |Type               |Description
         =====================================================
                |Dictionary         | 
    """
    data={"TopControl1$ScriptManager1": "FrontTabContainer1$ctl00$UpdatePanel1|FrontTabContainer1$ctl00$ImageButton1"}
    link="https://www.casablanca-bourse.com/bourseweb/index.aspx"
    headers =   {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    res = requests.post(link,data=data,headers=headers).content.decode('utf8')
    soup = BeautifulSoup(res,'html.parser')
    return getIndiceRecapScrap(soup)