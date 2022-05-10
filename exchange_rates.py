# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 14:25:19 2020

@author: kbhattacharjee
"""
import pandas
from pandas import ExcelWriter
import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.rrule import rrule, DAILY
import pyodbc


def ReadUrl(URL):      
    response = requests.get(URL)
    return BeautifulSoup(response.text,"html.parser") 

writer = ExcelWriter("Ex Rates.xlsx")
#Variables
Country = "USD" #Options like CAD instead for USD
StartDate = datetime.date(2020,10,27) #YYYY-MM-DD change to your requirement
CurrentDate = datetime.datetime.now()

datamatrix = []
for datetime in rrule(DAILY, dtstart=StartDate, until=CurrentDate):
    while(True):
        url = "https://www.xe.com/currencytables/?from="+ Country +"&date="+ str(datetime)[:10]
        soup = ReadUrl(url)
        Table = soup.find("table")
        if Table is not None:
            break
    for row in Table.findAll('tr'):
        columns = row.findAll('td')
        if len(columns) > 2:
            Currency_name  = columns[0].text
            Currency_rate1 = columns[1].text
            Currency_rate2 = columns[2].text
            row_data = [datetime,Currency_rate1,Currency_rate2]
            if Currency_name == 'Canadian Dollar':
                print(row_data)
                datamatrix.append(row_data)
                break
            
dataframe = pandas.DataFrame.from_records(datamatrix, columns = ["Date","CAD_per_USD", "USD_per_CAD"])
dataframe.to_excel(writer, sheet_name='Ex rates', index=False)
writer.save()

''' insert to sandbox
conn_sandbox = pyodbc.connect('Driver={SQL Server};Server=GMSSQL16DW01\DATAWAREHOUSE;Database=Sandbox;Trusted_Connection=True;')
c = conn_sandbox.cursor()
dataframe.insert(3, '_75', 0.75)

for index, row in dataframe.iterrows():
    c.execute("INSERT INTO dbo.[EXRates] (Date,CAD_Per_USD,USD_Per_CAD,_75) values(?,?,?,?)",
row.Date,row.CAD_per_USD,row.USD_per_CAD, row._75)
conn_sandbox.commit()
print("All new data have been inserted into database!")
print("Please check SQL server to make sure that all data has been inserted")
'''
