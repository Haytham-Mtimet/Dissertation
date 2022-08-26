# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 20:37:21 2022

@author: hm21396
"""

import pandas as pd
#Reading the list of companies
df_comp = pd.read_csv('constituents_modified.csv') 
print(df_comp)

from twarc import Twarc2
import datetime
import json
import os

# Initiate the twarc client
client = Twarc2(bearer_token="********")


def main():
    def count_tweets(target):
        
        # Specify the start time in UTC for the time period you want Tweets from
        start_time = datetime.datetime(2022, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

        # Specify the end time in UTC for the time period you want Tweets from
        end_time = datetime.datetime(2022, 6, 30, 0, 0, 0, 0, datetime.timezone.utc)

        # This is where we specify our query as discussed in module 5
        query = target[1] + ' OR ' + target[0]+ ' --lang:en'

        # The counts_all method call the full-archive Tweet counts endpoint to get Tweet volume based on the query, start and end times
        count_results = client.counts_all(query=query, start_time=start_time, end_time=end_time, granularity='day')
        
        #Create data frame 
        df_count =pd.DataFrame(columns=['end', 'start', 'tweet_count'])
        # Twarc returns all Tweet counts for the criteria set above, so we page through the results
        for page in count_results:
            df_test = pd.DataFrame.from_dict(page['data'])
            #print(df_test['tweet_count'])
            df_count =df_count.append(df_test, ignore_index=True)
            df_test =pd.DataFrame(columns=['end', 'start', 'tweet_count'])
        df_count.to_csv(os.path.join("Tweet_Counts/{}.csv".format(target[1])))
        return sum(df_count['tweet_count'])
    df_total = pd.DataFrame(columns=['Stock', 'total_tweet_count'])
    for i in range(0,10):
        count_tweets(df_comp.iloc[i,])
        total = count_tweets(df_comp.iloc[i,])
        df_total = df_total.append({'Stock': df_comp.iloc[i,][1], 'total_tweet_count': total},ignore_index=True)
    df_total.to_csv("Tweet_Counts/Total_Count_Tweet.csv")
        

if __name__ == "__main__":
    main()