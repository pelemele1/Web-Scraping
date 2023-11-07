import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import smtplib 
from email.mime.multipart import MIMEMultipart 

#Get data from website
result = requests.get('https://firstbridgedata.com/deepdive/index/GVIP')
request_text = result.text

#Create the soup
soup = BeautifulSoup(request_text, 'html.parser')

#Get the table that contains our wished information
table = soup.find(string=re.compile("Top 10 Holdings")).find_parents("table")[0]



#Get the date

date_str = table.find('td').text
date_str = re.findall('\(.*\)',date_str)[0][1:-1]
date_object = datetime.strptime(date_str,
                                "%d %B %Y")
date_as_string = date_object.strftime('%Y-%m-%d')

#Get the top ten stocks
stocks = []
rows = table.find_all('tr')[2:]
for row in rows:
    stock = row.find_all('td')[0].text
    stocks.append(stock)

#Write to .csv-file
path = './stocks.csv'
with open(path,'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                        quotechar='|',
                        quoting=csv.QUOTE_MINIMAL)
    if os.path.getsize(path) == 0:
        columns_list = ['Date'] + list(range(1,10+1))
        filewriter.writerow(columns_list)
    
    row = [date_as_string] + stocks
    filewriter.writerow(row)

#Create Dataframe and check, whether last any change occured
df = pd.read_csv('stocks.csv')
if df.iloc[-1:].duplicated().size != 0:
    print('send mail')

msg = """Subject: Rasperry pi: stock-notification
"""
msg += 'Top 10 Stocks of Goldman Sachs VIP ETF has changed'

gmail_user = 'deichselfelix17@gmail.com'
gmail_passwort = '03.April1988'
sent_from = gmail_user
to = 'deichselfelix@gmx.de'



try:   
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
    server.ehlo() 
    server.login(gmail_user, '03.April1988') 
    server.sendmail(sent_from, to, msg) 
    server.close() 
 
    print ('Email sent!') 
except:   
    print ('Something went wrong...')  