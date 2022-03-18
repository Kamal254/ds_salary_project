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
#remove na value first
df3 = df2[df2['Location'].notna()]
#create a new column of county
df3['Job_country'] = df3['Job_state'] = df3['Location'].apply(lambda x:x.split(',')[0])
#create a new column of states
df3['Job_state'] = df3['Location'].apply(lambda x:x.split(',')[1] if ',' in x else x)
df3 = df3[df3['Rating']!=-1]
df4 = df3[df3['Founded']!=-1]

#Now Update year founded column into curent year of company

df4['Company_Year'] = df4['Founded'].apply(lambda x:2022-x)

#now Parsing of job Discription(python, etc)
#let's list down skills for data scientist
#python
df4['python_yn'] = df4['Job Description'].apply(lambda x:1 if 'python' in x.lower() else 0)
#visualization
df4['visualization_yn'] = df4['Job Description'].apply(lambda x:1 if 'visualization' in x.lower() else 0)
#Excel
df4['Excel_yn'] = df4['Job Description'].apply(lambda x:1 if 'excel' in x.lower() else 0)
#analysis
df4['analysis_yn'] = df4['Job Description'].apply(lambda x:1 if 'analysis' in x.lower() else 0)
#communication
df4['communication_yn'] = df4['Job Description'].apply(lambda x:1 if 'communication' in x.lower() else 0)
#aws
df4['aws_yn'] = df4['Job Description'].apply(lambda x:1 if 'aws' in x.lower() else 0)

df5 = df4.drop([ 'Location', 'Competitors'], axis = 1)
df5 = df5.reset_index()
#now df5 is our final dataset for EDA save this

df5.to_csv('Salary_cleaned_data.csv', index=False)



