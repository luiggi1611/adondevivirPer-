# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:28:43 2021

@author: luigg
"""

import requests
from bs4 import BeautifulSoup
import os 
URL = 'https://www.adondevivir.com/departamentos-en-venta.html'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
os.chdir(r"C:\Users\luigg\OneDrive\Documentos\adondevivir")

from bs4 import BeautifulSoup
import requests
import urllib.request
from pytesseract import image_to_string
from PIL import Image ##pillow
import pytesseract
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd
import re
import time
url = 'https://www.adondevivir.com/departamentos-en-venta.html'
maxpages=5
pagesurl=[]
pagesurl.append(url)
for i in range(2,maxpages+1):
    pagesurl.append("https://www.adondevivir.com/departamentos-en-venta-pagina-"+str(i)+".html")

def data_perpage(url):
    driver = webdriver.Edge(executable_path="msedgedriver.exe")
    driver.get(url)
    time.sleep(3)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="modalContent"]/div/button').click()
    price=[]
    all_spans = driver.find_elements_by_xpath('//*[@class="firstPriceContainer"]')
    for span in all_spans:
        price.append(span.text)
        
    ubicacion=[]
    all_spans = driver.find_elements_by_xpath('//*[@data-qa="ubicacion"]')
    for span in all_spans:
        ubicacion.append(span.text)
    
    direccion=[]
    all_spans = driver.find_elements_by_xpath('//*[@data-qa="direccion"]')
    for span in all_spans:
        direccion.append(span.text)
        
    features=[]
    all_spans = driver.find_elements_by_xpath('//*[@data-qa="features"]')
    for span in all_spans:
        features.append(span.text)
    
    titulo=[]
    all_spans = driver.find_elements_by_xpath('//*[@data-qa="titulo"]')
    for span in all_spans:
        titulo.append(span.text)
    
    descripcion=[]
    all_spans = driver.find_elements_by_xpath('//*[@data-qa="descripcion"]')
    for span in all_spans:
        descripcion.append(span.text) 

    urls=[]
    all_spans = driver.find_elements_by_xpath('//*[@class="go-to-posting"]')
    for span in all_spans:
        urls.append(span.get_attribute("href"))       
        
    data=pd.DataFrame({'price':price,'ubicacion':ubicacion,'titulo':titulo,'descripcion':descripcion,'features':features,'direccion':direccion,'urls':urls})
    driver.close()
    return data

Base_final=pd.DataFrame(columns=['price', 'ubicacion', 'titulo', 'descripcion', 'features', 'direccion','urls'])
for i in range(len(pagesurl)):
    Base_final=Base_final.append(data_perpage(pagesurl[i]))
Base_final['price']=Base_final['price'].str.replace(',','').str.split("\n", expand=True)[0]
Base_final.to_excel("base.xlsx")
