# -*- coding: utf-8 -*-
"""
@author: Kamal Singh
"""
import pandas as pd
df = pd.read_csv('Glassdoor_Scrapped_jobs.csv')

#list of columnns i m going to clean
#salary
#company name - text only
#state field
#age of company instead found year
#clean job discription
df1 = df[df['Salary Estimate']!='-1']
df1['Salary Estimate'] = df1['Salary Estimate'].apply(lambda x:x.split('(')[0])
df1['Salary Estimate'] = df1['Salary Estimate'].apply(lambda x : 1 if '/hr' in x.lower() else x)
df2 = df1[df1['Salary Estimate']!=1]
#Now we have our data set having salary in doller and per year
#lets remove $ sign and /yr from our salary coluumn
df2['Salary Estimate'] = df2['Salary Estimate'].apply(lambda x:x.replace('$','').replace('/yr',''))
df2['Salary Estimate'] = df2['Salary Estimate'].apply(lambda x:x.replace(',',''))
df2['Salary Estimate'] = df2['Salary Estimate'].apply(lambda x:int(x))
#Now we succesfully cleaned our salary column with int values in it

#Next is to remove rating from company name column
df2['Company Name'] = df2.apply(lambda x:x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis=1)

#Next is to Remove state names from location column
df3 = df2[df2['Location'].apply(lambda x:str(x))]
df3 = df3[df3['Location']!=None]

df4 = df3['Location'].apply(lambda x:x[:-4] if ',' in x else x)




