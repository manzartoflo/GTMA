#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 00:30:14 2019

@author: manzars
"""

import time
import pandas
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.gtma.co.uk/resources/supplier-directory/'

req = webdriver.Firefox()
req.get(url)

html = req.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, 'lxml')
div = soup.findAll('div', {'class': 'direcotry-item'})

file = open('assignment.csv', 'w')
header = 'Company Name, Telephone, Email\n'
file.write(header)

count = 0
inner_count = 0

for element in div:
    link = element.a.attrs['href']
    link = urljoin(url, link)
    #print(link)
    req.get(link)
    html1 = req.execute_script('return document.documentElement.outerHTML')
    soup1 = BeautifulSoup(html1, 'lxml')
    div1 = soup1.findAll('div', {'class': 'direcotry-item'})
    time.sleep(0.5)
    for element1 in div1:
        link1 = element1.a.attrs['href']
        link1 = urljoin(url, link1)
        count += 1
        #print(link1)
        req.get(link1)
        html2 = req.execute_script('return document.documentElement.outerHTML')
        soup2 = BeautifulSoup(html2, 'lxml')
        div2 = soup2.findAll('div', {'class': 'tax_holder'})
        time.sleep(0.5)
        for element2 in div2:
            inner_count =+ 1
            name = element2.h2.a.text
            para = element2.contents[1::2]
            email = para[3].strong.text
            telephone = para[2].strong.text
            file.write(name.replace(',', '') + ',' + telephone.replace(',', '') + ',' + email.replace(',', '') + '\n')
            print(name.replace(',', '') + ',' + telephone.replace(',', '') + ',' + email.replace(',', '') + '\n')
            
file.close()

file = pandas.read_csv('assignment.csv')
