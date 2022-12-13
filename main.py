from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import csv

def add(df,row):
    newdata=pd.DataFrame(row,index=[0])
    if df.shape[0]==0:
        return newdata
    else:
        return pd.concat([df, newdata])

web_driver_path="./chrome driver/chromedriver.exe"
web_target_url="https://www.akc.org/dog-breeds/"

driver = webdriver.Chrome(web_driver_path)
driver.get(web_target_url)

######## load more data into the page

while 1:
    try:
        l=driver.find_element(By.ID,'load-more-btn')
        driver.execute_script("arguments[0].click();", l)
    except:
        break
   

    

# ###### get the links of all dogs pages
elems=driver.find_elements(By.CSS_SELECTOR,'.breed-type-card > a')
links=[ elem.get_attribute('href') for elem in elems ]

df=pd.DataFrame()
# ##### get the information from pages
for link in links:
    try:
        driver.get(link)
        driver.find_element(By.ID,'tab__breed-page__traits__all').click()
        t=driver.find_element(By.CSS_SELECTOR,'.page-header__title').text
        dog={'title':t}
        overView=driver.find_elements(By.CSS_SELECTOR,'.breed-page__hero__overview__icon-block')
        for elem in overView:
            key=elem.find_element(By.CSS_SELECTOR,'h3').text
            value=elem.find_element(By.CSS_SELECTOR,'p').text
            dog[key]=value

        dataContainer=driver.find_elements(By.CSS_SELECTOR,'.breed-trait-group__trait-all')
        for elem in dataContainer:
            key=elem.find_element(By.CSS_SELECTOR,'h4').text
            if key =='COAT TYPE' or key=='COAT LENGTH':
                value=""
                Selected=elem.find_elements(By.CSS_SELECTOR,'.breed-trait-score__choice--selected')
                for v in Selected:
                    value+= v.find_element(By.CSS_SELECTOR,'span').text+";"
            else:
                value=len(elem.find_elements(By.CSS_SELECTOR,'.breed-trait-score__score-unit--filled'))
            
            dog[key]=value
    except:
        continue

    df=add(df,dog)
   
df.to_csv('result.csv')
driver.quit()
