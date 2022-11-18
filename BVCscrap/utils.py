from bs4 import BeautifulSoup
import requests 
import pandas as pd
import json
import datetime
from .Notation import *


def get_code(name):
    nottation_code=notation_code()
    for action in nottation_code :
        if action["name"]==name :
            code=action['ISIN']
            return code
def get_valeur(name):
    if name=="MASI":
        print("MASI can't be an argument for this function")
    name_value=notation_value()
    return name_value[name]

def get_data(soup,decode):
    table= json.loads(soup.text.encode().decode(decode))
    row_data=pd.DataFrame(table["result"])
    row_data.columns=["Date","Value","Min","Max","Variation","Volume"]
    date=row_data['Date']
    row_data.drop(['Date'],axis=1,inplace=True)
    row_data.index=date
    return row_data

def intradata(soup,decode):
    table= json.loads(soup.text.encode().decode(decode))
    row_data=pd.DataFrame(table["result"][0])
    index=row_data['labels'].values
    row_data.drop(['labels'],axis=1,inplace=True)
    row_data.index=index
    row_data.columns=["Value"]
    return row_data


def get_index(soup,decode):
    table= json.loads(soup.text.encode().decode(decode))
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

def getTables(soup):
    tabs=['table1',"table6","table7","table4"]
    result=dict()
    for tab in tabs :
        t=soup.find(id=tab).find_all("span")
        t=[ x.get_text() for x in t]
        if tab=='table1':
            a=getTable1(t)
            result["Données_Seance"]=a
        elif tab=="table6":
            a=getTable6(t)
            result["Meilleur_limit"]=a
        elif tab=='table7':
            a=getTable7(t)
            result['Dernieres_Tansaction']=a
        else:
            a=getTable4(t)
            result["Seance_prec"]=a
    return result
def cleanText(text):
    return text.replace(",",".").replace("%","").replace("\xa0","").replace("Â","")
def getTable1(t):
    cols=['Cours','Variation','Ouverture','Plus haut','Plus bas','Cours de cloture veille',
          'Volume','Volume en titres','Capitalisation','Nombre de titres','Devise de cotation']
    t=list(map(cleanText,t))
    a=dict(zip(cols,t))
    return a
def getTable6(t):
    if len(t)>4:
        t=t[1:]
    cols=['Prix achat', 'Quantite_achat', 'Prix de vente', 'Quantite_vente']
    t=list(map(cleanText,t))
    a=dict(zip(cols,t))
    return a
def getTable7(t):
    a=dict()
    i=0
    heure=[]
    prix=[]
    qte=[]
    while i<len(t):
        heure.append(t[i])
        prix.append(t[i+1])
        qte.append(t[i+2].replace("\xa0","").replace("Â",""))
        i+=3
    a["Heure"]=heure
    a["Prix"]=prix
    a["Quantite"]=qte
    return a
def getTable4(t):
    a=dict()
    i=0
    Date = []
    Variation = []
    Cloture = []
    Volume = []
    Ouverture =[]
    Plus_haut = []
    Plus_bas=[]
    while i<len(t):
        Date.append(t[i])
        Variation.append(t[i+1])
        Cloture.append(t[i+2])
        Volume.append(t[i+3])
        Ouverture.append(t[i+4])
        Plus_haut.append(t[i+5])
        Plus_bas.append(t[i+6])
        i+=7    
    a["Date"]=list(map(cleanText,Date))
    a["Variation"]=list(map(cleanText,Variation)) 
    a["Cloture"]=list(map(cleanText,Cloture))
    a["Volume"]=list(map(cleanText,Volume))
    a["Ouverture"]=list(map(cleanText,Ouverture))
    a["Plus_haut"]=list(map(cleanText,Plus_haut))
    a["Plus_bas"]=list(map(cleanText,Plus_bas))
    return a

def getTablesFich(soup):
    tabs=['table4',"table3","table6"]
    result=dict()
    for tab in tabs :
        if tab=='table4':
            t=soup.find(id=tab).find_all("span")
            t=[ x.get_text() for x in t]
            a=getTable4Fich(t)
            result["Info_Societe"]=a
        elif tab=="table3":
            t=soup.find(id="table3").find_all('span')
            t=[x.get_text() for x in t]
            a=getTable3Fich(t)
            result["Actionnaires"]=a
        elif tab=='table6':
            t=soup.find(id="table6").find_all("span")
            t1=soup.find(id="table6").find_all(class_="desc")
            t=[x.get_text().replace("\xa0","").replace("-","") for x in t if x not in t1]
            a=getTable6Fich(t)
            result['Chiffres_cles']=a[0]
            result["Ratio"]=a[1]
    return result

def getTable4Fich(t):
    cols=["Raison_sociale" ,"ISIN","Ticker","Siege_social" ,"Secteur_activité" ,"Commissaire_aux_comptes",
          "Date_de_constitution","Date_introduction","Durée_Exercice_Social","Objet_social"]
    t=t[:4]+t[5:11]
    a=dict(zip(cols,t))
    return a
def getTable3Fich(t):
    a=dict()
    i=0
    while i<len(t):
        a[t[i]]=t[i+1].replace(",",".")
        i+=2
    return a
def getTable6Fich(t):
    a=dict()
    cols_chifr=["Annee","Comptes_consolide","Capital_social","Capitaux_propres","Nombre_titres",
         "Chiffre_Affaires","Resultat_exploitation","Resultat_net"]
    cols_ratio=["Annee","BPA","ROE","Payout","Dividend_yield","PER","PBR"]
    if "Chiffre d'Affaires" in t:
        t.remove("Chiffre d'Affaires")
    if "Résultat d'exploitation" in t:
        t.remove("Résultat d'exploitation")
    annee=[]
    anne=[]
    Comptes_consolide=[]
    Capital_social=[]
    Capitaux_propres=[]
    Nombre_titres=[]
    Chiffre_Affaires=[]
    Resultat_exploitation=[]
    Resultat_net=[]
    BPA=[]
    ROE=[]
    Payout=[]
    Dividend_yield=[]
    PER=[]
    PBR=[]
    chifr=[annee,Comptes_consolide,Capital_social,Capitaux_propres,Nombre_titres,Chiffre_Affaires,
          Resultat_exploitation,Resultat_net]
    ratio=[anne,BPA,ROE,Payout,Dividend_yield,PER,PBR]
    i,j,u=0,0,0
    while i <len(t) and j<len(chifr):
        if i>5 and t[i].replace(",","").isdigit()==False:
            cols_chifr[j]=t[i]
            i+=1
        chifr[j].append(t[i])
        chifr[j].append(t[i+1])
        chifr[j].append(t[i+2])
        i+=3
        j+=1
    while i<len(t) and u<len(ratio):
        ratio[u].append(t[i].replace("\xa0",""))
        ratio[u].append(t[i+1].replace("\xa0",""))
        ratio[u].append(t[i+2].replace("\xa0",""))
        i+=3
        u+=1
    a=dict(zip(cols_chifr,chifr))
    b=dict(zip(cols_ratio,ratio))
    return [a,b]

def getDivi(soup):
    t=soup.find_all(class_="txt_table")[1]
    t=t.find_all("span")
    t=[x.get_text() for x in t ]
    cols=["Annee","Montant_Dividende","Type_Dividende","Date_detachement","Date_paiement"]
    anne=[]
    md=[]
    td=[]
    dd=[]
    dp=[]
    i=0
    while i<len(t) :
        anne.append(t[i])
        md.append(t[i+1])
        td.append(t[i+2])
        dd.append(t[i+3])
        dp.append(t[i+4])
        i+=5
    vals=[anne,md,td,dd,dp]
    return dict(zip(cols,vals))


def getAllIndex(soup):
    indexSumry=getIndexSumry(soup)
    indiceRent=getIndiceRentab(soup)
    indiceDevis=getIndiceDevise(soup)
    indiceDevisF=getIndiceDeviseF(soup)
    indiceSect=getIndiceSect(soup)
    return {"Resume indice":indexSumry,"Indice rentabilite":indiceRent,"Indices en devises":indiceDevis,
           "Indice FTSE":indiceDevisF,"Indices sectoriels":indiceSect}

def getIndexSumry(soup):
    title=soup.find_all(class_='arial11turquoibold')
    values=soup.find_all(class_='arial11noir')
    tabs=["Morocco Stock Index 20","MASI","Casablanca ESG 10","FTSE CSE Morocco 15 Index","FTSE CSE Morocco All-Liquid"]
    result=dict()
    for i in range(len(tabs)):
        cols=[x.get_text().replace("\r","").replace("\n","").replace("  ","") for x in title[i].find_all("td")]
        val=[x.get_text().replace("\xa0","").replace("\n","").replace("Â","") for x in values[i].find_all('td')]
        result[tabs[i]]=dict(zip(cols,val))
    return result

def getIndiceRentab(soup):
    t=soup.find_all(id="Table3")[-1].find_all("span")
    t=[x.get_text().replace("Â","").replace("\xa0","") for x in t]
    cols=["Valeur","Var %","Var % 31/12"]
    return {"MASI-Rentabilite Brut":dict(zip(cols,t[:3])),"MASI-Rentabilite Net":dict(zip(cols,t[3:]))}

def getIndiceDevise(soup):
    t=soup.find(id="Table4").find_all("span")
    t=[x.get_text().replace("Â","").replace("\xa0","") for x in t]
    cols=["Valeur","Var %","Var % 31/12"]
    return {"MASI Dollar":dict(zip(cols,t[:3])),"MASI Euro":dict(zip(cols,t[3:]))}

def getIndiceDeviseF(soup):
    result=dict()
    t=soup.find_all(id="Table2")[-1].find_all("span")
    t=[x.get_text().replace("Â","").replace("\xa0","") for x in t]
    cols=["Valeur","Var %","Var % 31/12"]
    cl=["FTSE Dollar","FTSE Euro","FTSE TR","FTSE All-liquid Dollar","FTSE All-liquid Euro","FTSE All-liquid TR"]
    j=0
    for i in range(len(cl)):
        result[cl[i]]=dict(zip(cols,t[i+j:i+j+3]))
        j+=2
    return result

def getIndiceSect(soup):
    t=soup.find_all(id='arial11bleu')[-1].find_all('span')
    t=[x.get_text().replace("\xa0","").replace("Â","") for x in t]
    i=0
    secteur=[]
    valeur=[]
    var=[]
    var1=[]
    i=0
    while i<len(t):
        secteur.append(t[i])
        valeur.append(t[i+1])
        var.append(t[i+2])
        var1.append(t[i+3])
        i+=4
    vals=[{"Valeur":valeur[i],"Var%":var[i],"Var% 31/12":var1[i]} for i in range(len(secteur))]
    return dict(zip(secteur,vals))

def getPondval(soup):
    t=soup.find_all(class_="arial11gris")
    isin=[]
    inst=[]
    nbrtr=[]
    cours=[]
    flot=[]
    plaf=[]
    capflo=[]
    poid=[]
    vl=[isin,inst,nbrtr,cours,flot,plaf,capflo,poid]
    cl=["Code Isin","Instrument","Nombre de titres","Cours","Facteur flottant","Facteur plafonnement","Capitalisation flottante","Poids"]
    for i in range(1,len(t)):
        vals=[x.get_text().replace("\xa0","").replace("Â","") for x in t[i].find_all('span')]
        for j in range(len(vl)):
            vl[j].append(vals[j])
    return dict(zip(cl,vl))

def getIndiceRecapScrap(soup):
    t=soup.find_all(class_="arial11bleu")
    t=[x.get_text().replace("\n","").replace("\xa0","").replace("\r","").replace("  ","") for x in t][1:]
    b=t[1:6]+t[7:15]+t[16:17]+t[18:21]+[t[22]]+t[24:]
    cl=["Indice","Volume Global","Plus forte hausse","Plus forte baisse"]
    indc=dict()
    hausse=[]
    baisse=[]
    i=0
    while i<len(b) and i<12 :
        indc[b[i]]={"Cours":b[i+1],"Var%":b[i+2],"Var31/12":b[i+3]}
        i+=4
    cols=["Instrument","Cours","Difference","Difference en %"]
    hausse=dict(zip(cols,b[i:i+4]))
    baisse=dict(zip(cols,b[i+4:]))
    volum=soup.find(class_='arial18vertfluo').get_text().replace('\n','').replace("\xa0","")
    result=dict(zip(cl,[indc,volum,hausse,baisse]))
    return result