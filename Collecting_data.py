# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 00:49:00 2022

@author: hm21396
"""

from twarc import Twarc2
import datetime
import json
import os
import random

# Initiate the twarc client
client = Twarc2(bearer_token="AAAAAAAAAAAAAAAAAAAAADpveQEAAAAAwzzGLkLC7iByKHGlJ092AjDwAQY%3DlUYxpMOS9ZIZQQcMPv3tyNmVK705kDjml9QXmJERzgM0476waO")

import pandas as pd


#Reading the list of companies

df_comp = pd.read_csv("constituents_modified.csv")
print(df_comp)

#Reading the total number of tweets
df_total = pd.read_csv("Tweet_Counts/Total_Count_Tweet.csv")
print(df_total)

#Setting the number of tweets per company
total =sum(df_total['total_tweet_count'])
df_total['Number']=df_total['total_tweet_count']*9000000/total
df_total['Number'] = df_total['Number'].astype('int')
print(df_total['Number'])

#Setting the search based on the information provided 
def get_tweets(target, sample):

    #Writing the querry
    query ='"' +target[1] + ' OR ' + target[0]+ ' --lang:en' +'"'
    #Setting the start time
    start_time =sample[2][:-5]
    #The random aspect of the starting time 
    h2 = random.randint(0,9)
    m1 = random.randint(0,5)
    m2 = random.randint(0,9)

    start_time = sample[2][:-12]+ str(h2)+':'+str(m1)+str(m2)+':00'
    #Setteing the end time
    end_time =sample[1][:-5]
    #Setting the limit
    limit = str(sample[4])
    #Setting the path for the json file
    path_json = 'Json_files/'+target[1]+'_json_files'+'/'+ sample[2][:-14] +'_'+target[1]+'.jsonl'
    path_json = path_json.replace(' ', '_')
    #Setting the path for the csv file
    path_csv =  'Csv_files/'+target[1]+'_csv_files'+'/'+ sample[2][:-14] +'_'+target[1]+'.csv'
    path_csv = path_csv.replace(' ', '_')
    #Create and writing the command
    command_search = 'twarc2 search --archive --start-time "'+start_time+'" --end-time "'+end_time+'"  --limit '+limit+' '+query+ ' '+ path_json
    with open('search_tweet.txt', 'a') as f:
        f.write(command_search)
        f.write('\n')
    #Create and writing the command for the csv
    command_save = 'twarc2 csv '+ path_json+ ' '+ path_csv
    with open('transform_tweet.txt', 'a') as f:
        f.write(command_save)
        f.write('\n')
    #twarc2 search --archive --start-time "2022-03-16T00:00:00" --end-time "2022-03-17T00:00:00"  --limit 500 Bitcoin Bitcoin.jsonl

#Setting the number of tweets per day per company
for i in range(0,10):
    df = pd.read_csv(os.path.join("Tweet_Counts/{}.csv".format(df_comp.iloc[i,][1])))
    s=sum(df['tweet_count'])
    df['Sample']=df['tweet_count']*df_total.at[i, 'Number']/s
    df['Sample']=df['Sample'].astype('int')
    for j in df.index:
        get_tweets(df_comp.iloc[i,], df.iloc[j,])
    
    


    