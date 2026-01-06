#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import defaultdict
import json
import math
import numpy as np
import pandas as pd
import requests


# # Create a new json file 

# In[2]:


business_df = pd.read_json("yelp_academic_dataset_businessNEW.json", lines=True)
business_df.head()


# In[3]:


business_df.info()


# In[5]:


covid_df = pd.read_csv('yelp_academic_dataset_covid_features.csv',low_memory=False)
covid_df.head()


# In[6]:


covid_df.info()


# In[7]:


#Drop the duplicated business
covid_df_dropped = covid_df.drop_duplicates(subset=['business_id'], keep='first')
covid_df_dropped.info()


# In[8]:


#Join the covid & business dataframes into 1 dataframe
joined = business_df.merge(covid_df_dropped, on='business_id', how= 'inner')


# In[9]:


joined.info()


# In[10]:


joined.head()


# # Clean data 
# <br> 1/ Choose places in America only
# <br> 1/ Missing values in categories -> pulled from Yelp, google API 
# <br> 2/ Select restaurants only
# <br> 3/ missing values in hours -> pulled from google api for more info
# <br> 5/ restaurants closed before pandemic vs closed after pandemic
# <br> 6/ convert to json & get more columns
# <br> 7/ Get price level missing from google API
# <br> 8/ Get missing data from yelp API

# In[11]:


# Filter out all the locations outside of US
import us

#Get a list of all states in dataframe and list of all states in the US
location_list = joined['state'].unique().tolist()
state_list = [state.abbr for state in us.states.STATES_AND_TERRITORIES]
len(location_list)

#Get the states that are not in US
outside_us_list = list(set(location_list) - set(state_list))

#Delete rows with states outside of US
joined = joined[~joined['state'].isin(outside_us_list)]


# In[12]:


joined.info()


# In[13]:


# Find business_id with missing values for a column
def get_missing_df(df, col):
    df_missing = df[df[col].isnull()]
    return df_missing


# In[15]:


#Fill in missing values in a column from Yelp API
import requests
import json

def yelp_api_null(df, main_df, col, yelp_keyword):
    api_key = 't8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'
    headers = {'Authorization': 'Bearer t8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'}
   
    for business in df.business_id:
        business_id = business
        try:
            response = requests.get(url= 'https://api.yelp.com/v3/businesses/%s' % business_id, headers= headers)
            business_data= response.json()
            if business_data[yelp_keyword]:
                if yelp_keyword == 'categories':
                    main_df.loc[main_df.business_id == business_id, col] = business_data[col][0].get('title')
                else:
                    main_df.loc[main_df.business_id == business_id, col] = business_data[col][0]
                df.drop(index=df[df['business_id'] == business_id].index, inplace=True)
        except:
            pass


# In[169]:


# api_key = 't8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'
# headers = {'Authorization': 'Bearer t8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'}

# business_id_emp = 'uQIja_TjoaY38Idi61nc1w'
# business_id = 'uQIja_TjoaY38Idi61nc1w'
# try:
#     response = requests.get(url= 'https://api.yelp.com/v3/businesses/%s' % business_id, headers= headers)
#     business_data= response.json()
#     if business_data['categories']:
#         print(business_data['categories'][0].get('title'))
#         categories_missing_value_df.loc[categories_missing_value_df.business_id == business_id, 'categories'] = business_data['categories'][0].get('title')
#         #categories_missing_value_df.drop(index=categories_missing_value_df[categories_missing_value_df['business_id'] == business_id].index, inplace=True)
# except:
#     pass


# In[16]:


#Fill in missing values in a column from Google API

import googlemaps
def google_api_null(df, main_df, col, google_keyword):
    api_key = 'AIzaSyBLN7YzY9l23RSrWm24vn4imJn4XJkh9vI'

    gmaps = googlemaps.Client(key = api_key)
    
    for business in df.business_id:
        business_id = business
        
        try:
            name = df.loc[df.business_id == business_id, 'name'].iloc[0]

            address = df.loc[df.business_id == business_id, 'address'].iloc[0]

            city = df.loc[df.business_id == business_id, 'city'].iloc[0]

            state = df.loc[df.business_id == business_id, 'state'].iloc[0]
            
            postal_code = df.loc[df.business_id == business_id, 'postal_code'].iloc[0]

            #full_address = address + ', ' + city + ', ' + state + ', ' + postal_code

            search_key = name + ' ' + city + ', ' + state + ', ' + postal_code
            
            results = gmaps.find_place(input= search_key, input_type="textquery",fields=['name', 'place_id','formatted_address', 'opening_hours', 'price_level', 'business_status', 'types'])

            #Get the correct result that matches with the business in dataframe
            if results['candidates']: #if the results list is not empty
                for candidate in results['candidates']:
                    #print('business id: ', business_id)
                    #print('results: ', results['candidates'])
                    if candidate['name'] == name or candidate['formatted_address'] == full_address:
                        #print('got in -> ')
                        #print(results['candidates'])
                        #get the column that is needed from google api
                        input_value = [i.replace('_', ' ') for i in candidate[google_keyword]]
                        main_df.loc[main_df.business_id == business_id, col] = ', '.join(input_value) 
                        df.drop(index=df[df['business_id'] == business_id].index, inplace=True)
        except:
            pass


# In[19]:


#Filter out all the other categories, just keep the restaurants/food/bar
def restaurants_only(df):
    category_list = df['categories'].tolist()
    restaurant_list = list()
    for i in range(len(category_list)):
        if category_list[i] is None:
            continue
        category_string = category_list[i].lower()
        if category_string.contains('restaurants') or category_string.contains('bars'):
            restaurant_list.append(i)
    return df.ix[restaurant_list]


# In[20]:


#Fill in the null values in categories column by catching api from yelp
categories_missing_value_df = get_missing_df(joined, 'categories')
categories_missing_value_df.info()


# In[21]:


# Get API from Yelp for missing Categories
yelp_api_null(categories_missing_value_df, joined, 'categories', 'categories')


# In[22]:


categories_missing_value_df.info()


# In[23]:


#Get APT from Google for missing Categories
google_api_null(categories_missing_value_df, joined, 'categories', 'types')


# In[47]:


# business_id = 'iQ05W_hGmTfMlWXisJsHrQ'
# api_key = 'AIzaSyBLN7YzY9l23RSrWm24vn4imJn4XJkh9vI'
# gmaps = googlemaps.Client(key = api_key)
    
# try:
#     name = categories_missing_value_df.loc[categories_missing_value_df.business_id == business_id, 'name'].iloc[0]

#     address = categories_missing_value_df.loc[categories_missing_value_df.business_id == business_id, 'address'].iloc[0]

#     city = categories_missing_value_df.loc[categories_missing_value_df.business_id == business_id, 'city'].iloc[0]

#     state = categories_missing_value_df.loc[categories_missing_value_df.business_id == business_id, 'state'].iloc[0]
            
#     postal_code = categories_missing_value_df.loc[categories_missing_value_df.business_id == business_id, 'postal_code'].iloc[0]

#     full_address = address + ', ' + city + ', ' + state + ', ' + postal_code
    
#     print('address: ', full_address)
#     print('name: ', name)
#     search_key = name + ' ' + city + ', ' + state + ', ' + postal_code
#     print(search_key)
#     results = gmaps.find_place(input= search_key, input_type="textquery",fields=['name', 'place_id','formatted_address', 'opening_hours', 'price_level', 'business_status', 'types'])
#     print('result: ', results)
    
#     #Get the correct result that matches with the business in dataframe
#     if results['candidates']: #if the results list is not empty
#         for candidate in results['candidates']:
#             print('first loop')
#             if candidate['name'] == name or candidate['formatted_address'] == full_address:
#                 print('got in -> ')
#                 print(results['candidates'])
# except:
#     pass


# In[49]:


#google_api_null(categories_missing_value_df, joined, 'categories', 'types')


# In[24]:


categories_missing_value_df.info()


# In[26]:


joined.info()


# In[29]:


#Delete rows with null value in categories
joined = joined[~joined['categories'].isnull()]
joined.info()


# In[81]:


joined2 = joined
joined2.info()


# In[82]:


#Get the restaurants, food places only
filter_list = ['restaurants','bars','food','desserts','bakery', 'coffee', 'tea']
joined2['categories']=joined2['categories'].str.lower()
# joined2['categories'].apply(lambda x: any([key in x for key in filter_list]))
joined2 = joined2[joined2['categories'].apply(lambda x: any([key in x for key in filter_list]))]
joined2.info()


# In[85]:


#joined2.info()


# In[88]:


#Find the dataframe of all missing values for hour column
hours_missing_value_df = get_missing_df(joined2, 'hours')
hours_missing_value_df.info()


# In[92]:


#Get the missing values for hour column from Google API
google_api_null(hours_missing_value_df, joined2, 'hours', 'hours')
joined2.info()


# In[93]:


joined2.info()


# In[110]:


def yelp_api_null2(df, main_df, col1, yelp_keyword1, col2= None, yelp_keyword2 = None):
    api_key = 't8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'
    headers = {'Authorization': 'Bearer t8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'}
    
    for business in df.business_id:
        business_id = business
        try:
            response = requests.get(url= 'https://api.yelp.com/v3/businesses/%s' % business_id, headers= headers)
            business_data= response.json()
            if business_data[yelp_keyword1]:
                if yelp_keyword1 == 'categories':
                    main_df.loc[main_df.business_id == business_id, 'categories'] = business_data['categories'][0].get('title')
                else:
                    main_df.loc[main_df.business_id == business_id, col1] = business_data[col1][0]
                df.drop(index=df[df['business_id'] == business_id].index, inplace=True)
            if (yelp_keyword2 != None) and (business_data[yelp_keyword2]):
                main_df.loc[main_df.business_id == business_id, col2] = business_data[col2][0]
                df.drop(index=df[df['business_id'] == business_id].index, inplace=True)
        except:
            pass


# In[ ]:


# Get API from Yelp for missing Categories
yelp_api_null(hours_missing_value_df, joined2, 'hours', 'opening_hours/periods')


# In[124]:


# business_id = 'iQ05W_hGmTfMlWXisJsHrQ'
# name = 'Roselli Realty'
# full_address = ''
# if results['candidates']: #if the results list is not empty
#     for candidate in results['candidates']:
#         if candidate['name'] == name or candidate['formatted_address'] == full_address:
#             #get the column that is needed from google api
            
#             #print(candidate['types'])
#             input_value = [i.replace('_', ' ') for i in candidate['types']]
#             #print(input_value)
#             categories_missing_value_df.loc[categories_missing_value_df.business_id == business_id, 'categories'] = ', '.join(input_value) 
#             df.drop(index=df[df['business_id'] == business_id].index, inplace=True)


# In[61]:


# import requests
# import json
# def get_api_null_2(df, col, yelp_keyword):
#     api_key = 't8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'
#     headers = {'Authorization': 'Bearer t8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'}
    
#     fill = []
#     business_id = 'pG8D1gthGbMMOj9y1MxOeA'
#     #business_id = '2W1tLg8ybRUEKMPoAPHTsQ'
#     try:
#         response = requests.get(url= 'https://api.yelp.com/v3/businesses/%s' % business_id, headers= headers)
#         business_data= response.json()
#         print(business_data[yelp_keyword])
#         if len(business_data[yelp_keyword]) != 0:
#             print('not empty')
#             df.loc[df.business_id == business_id, col] = response[yelp_keyword]
#         #fill.append([business_id, business_data[yelp_keyword]])
#         #df.loc[df.business_id == business_id, col] = response[yelp_keyword]
#     except:
#         fill.append([business_id, np.nan])
        
          
# #convert the json string into a dictionary object
# # business_data= response.json()
# # print(business_data['hours'])


# # Save new json file

# In[130]:


joined2.info()


# In[112]:


joined2.to_json('business_df2.json', orient= 'records')


# # Load new json file

# In[20]:


new_df = pd.read_csv('business_df2NEW.csv', low_memory= False)


# In[21]:


new_df.head()


# In[22]:


new_df.sort_index(axis=1, inplace=True)


# In[23]:


new_df.info()


# # Clean data 2
# <br> 1/ Delete uneceassary columns
# <br> 2/ Replace unclear value in some columns
# <br> 3/ Get The New Columns From The List in Attributes (Ambience, BusinessParking, GoodForMeals)
# <br> 4/ change name of columns
# <br> 5/ List Out Categories in Restaurant

# In[24]:


# Delete Unecessary Columns or columns with small amout of non-null values
del new_df['attributes.AcceptsInsurance']
del new_df['attributes.HairSpecializesIn']
del new_df['attributes.BYOB']
del new_df['attributes.BYOBCorkage']
del new_df['attributes.Corkage']
del new_df['attributes.BestNights']
del new_df['attributes.BusinessAcceptsBitcoin']
del new_df['attributes.CoatCheck']
del new_df['attributes.Music']
del new_df['attributes.HasTV']
del new_df['attributes.AgesAllowed']
del new_df['attributes.Open24Hours']
del new_df['attributes.DietaryRestrictions']
del new_df['attributes.Smoking']
del new_df['attributes.RestaurantsCounterService']
del new_df['attributes.DogsAllowed']
del new_df['attributes.DriveThru']
del new_df['attributes.GoodForDancing']
del new_df['attributes.HappyHour']
del new_df['attributes.RestaurantsTableService']
del new_df['attributes.WheelchairAccessible']
del new_df['attributes.ByAppointmentOnly']


# In[25]:


new_df.info()


# In[26]:


# Replace unclear value in some columns
def replace_value(df, col, new_values):
    values= df[col].unique()
    for i in range(len(values)):
        df[col].replace({values[i]: new_values[i]}, inplace=True)


# In[27]:


# Get The New Columns From The List in Attributes (Ambience, BusinessParking, GoodForMeals)
import ast
def label_attribute(df, col):
    df[col].replace({np.nan:'None'}, inplace=True)
    for i, row in df.iterrows():
        column_list = row[col]
        if column_list != 'None':
            dictionary = ast.literal_eval(column_list)
            for k, v in dictionary.items():
                df.loc[i, k] = v


# In[28]:


new_df['attributes.BikeParking'].unique()


# In[29]:


replace_value(new_df, 'attributes.BikeParking', ['False', 'True', np.nan, np.nan])
new_df['attributes.BikeParking'].unique()


# In[30]:


new_df['attributes.NoiseLevel'].unique()


# In[31]:


replace_value(new_df, 'attributes.NoiseLevel', ['quiet', np.nan , 'average', 'loud', 'very loud', 'average', 'quiet', 'loud', 'very loud', np.nan])
new_df['attributes.NoiseLevel'].unique()


# In[32]:


new_df['attributes.OutdoorSeating'].unique()


# In[33]:


replace_value(new_df, 'attributes.OutdoorSeating', ['False', np.nan, 'True', np.nan])
new_df['attributes.OutdoorSeating'].unique()


# In[34]:


new_df['attributes.RestaurantsAttire'].unique()


# In[35]:


replace_value(new_df, 'attributes.RestaurantsAttire', ['casual', np.nan, 'casual', 'formal', 'dressy', 'dressy', np.nan, 'formal'])
new_df['attributes.RestaurantsAttire'].unique()


# In[36]:


new_df['attributes.RestaurantsDelivery'].unique()


# In[37]:


replace_value(new_df, 'attributes.RestaurantsDelivery', ['True', np.nan, 'False', np.nan])
new_df['attributes.RestaurantsDelivery'].unique()


# In[38]:


new_df['attributes.RestaurantsGoodForGroups'].unique()


# In[39]:


replace_value(new_df, 'attributes.RestaurantsGoodForGroups', ['False', np.nan, 'True', np.nan])
new_df['attributes.RestaurantsGoodForGroups'].unique()


# In[40]:


new_df['attributes.RestaurantsPriceRange2'].unique()


# In[41]:


replace_value(new_df, 'attributes.RestaurantsPriceRange2', [1, np.nan, 2, 4, 3, np.nan])
new_df['attributes.RestaurantsPriceRange2'].unique()


# In[42]:


new_df['attributes.RestaurantsReservations'].unique()


# In[43]:


replace_value(new_df, 'attributes.RestaurantsReservations', ['False', np.nan, 'True', np.nan])
new_df['attributes.RestaurantsReservations'].unique()


# In[44]:


new_df['attributes.RestaurantsTakeOut'].unique()


# In[45]:


replace_value(new_df, 'attributes.RestaurantsTakeOut', ['True', np.nan, 'False', np.nan])
new_df['attributes.RestaurantsTakeOut'].unique()


# In[46]:


new_df['attributes.WiFi'].unique()


# In[47]:


replace_value(new_df, 'attributes.WiFi', [np.nan, 'no wifi', 'no wifi', 'free wifi', 'free wifi', 'paid wifi', 'paid wifi', np.nan])
new_df['attributes.WiFi'].unique()


# In[48]:


new_df['attributes.BusinessAcceptsCreditCards'].unique()


# In[49]:


replace_value(new_df, 'attributes.BusinessAcceptsCreditCards', ['True', 'False', np.nan, np.nan])
new_df['attributes.BusinessAcceptsCreditCards'].unique()


# In[50]:


new_df['attributes.Caters'].unique()


# In[51]:


replace_value(new_df, 'attributes.Caters', [np.nan, 'True', 'False', np.nan])
new_df['attributes.Caters'].unique()


# In[52]:


new_df.info()


# In[53]:


# Get The New Columns From The List in Attributes
label_attribute(new_df, 'attributes.Ambience')
label_attribute(new_df, 'attributes.BusinessParking')
label_attribute(new_df, 'attributes.GoodForMeal')


# In[54]:


# Delete the columns with nested value
del new_df['attributes.Ambience']
del new_df['attributes.BusinessParking']
del new_df['attributes.GoodForMeal']
del new_df['attributes']


# In[55]:


# Modify the columns' name
def rename_col(df):
    col_name = df.columns
    for each in col_name:
        if 'attributes' in each:
            new_name = each.split('.')
            df.rename(columns={each:new_name[1]}, inplace=True)


# In[56]:


rename_col(new_df)


# In[57]:


new_df.info()


# In[59]:


# Get all the current open restaurants
open_df = new_df[new_df['is_open'] == 1]
open_df.info()


# In[60]:


open_df[open_df['Temporary Closed Until'] == 'FALSE']


# In[61]:


# Get all the closed restaurants
closed_df = new_df[new_df['is_open'] == 0]
closed_df.info()


# In[62]:


#Restaurants closed
closed_df.info()


# In[63]:


#Restaurants temporary closed
open_df[open_df['Temporary Closed Until'] != 'FALSE'].info()


# In[64]:


#Restaurants open after covid
open_df[open_df['Temporary Closed Until'] == 'FALSE'].info()


# # Export File For Analysis
# <br> 1/ closed, temporary closed, open

# In[65]:


# Restaurants open until now
open_covid_df = open_df[open_df['Temporary Closed Until'] != 'FALSE']


# In[66]:


# Restaurants temporary closed
closed_temp_df = open_df[open_df['Temporary Closed Until'] == 'FALSE']


# In[67]:


# Restaurants closed permanently
closed_df


# In[79]:


# new_df['Store Status'] = 'abc'
# new_df[new_df['Store Status'].where((new_df['is_open']== 1) & (new_df['Temporary Closed Until'] != 'FALSE') & (new_df['Store Status'] == 'abc'), 'Temporarily Closed')]


# In[90]:


mask1 = (new_df['is_open'] == 1) & (new_df['Temporary Closed Until'] != 'FALSE')
new_df['Store Status'][mask1] = 'Temporarily Closed'


# In[91]:


#Update store status column's values for open restaurants
mask2 = (new_df['is_open'] == 1) & (new_df['Temporary Closed Until'] == 'FALSE')
new_df['Store Status'][mask2] = 'Currently Open'


# In[93]:


#Update store status column's values for permanently closed restaurants
mask3 = (new_df['is_open'] == 0)
new_df['Store Status'][mask3] = 'Permanently Closed'


# In[94]:


new_df['Store Status'].unique()


# In[95]:


new_df.info()


# In[96]:


#Export official dataframe 
new_df.to_csv('restaurants_all.csv')
open_covid_df.to_csv('restaurants_open.csv')
closed_temp_df.to_csv('restaurants_temp_closed.csv')
closed_df.to_csv('restaurants_perm_closed.csv')


# In[97]:


import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize 
import itertools
from nltk import FreqDist
from nltk.probability import ConditionalFreqDist

def get_frequency_categories(df):
    # Transform into a list
    categories_list = df['categories'].unique()

    # Create list of each rows' categories
    categories_list_rep = []
    for i in range(len(categories_list)):
        try:
            temp = re.sub('[&/\(),]', ' ', categories_list[i])
            categories_list_rep.append(temp)
        except:
            #print(i,categories_list[i])
            pass
    # Tokenize inside the list to get each category
    tokenized_category = [word_tokenize(word) for word in categories_list_rep]
    
    # Combine together into 1 list of categories
    tokenized_category_list = list(itertools.chain.from_iterable(tokenized_category))
    
    # Find the frequency of each category in a dataframe
    freq_list = FreqDist(tokenized_category_list)
    freq_df = pd.DataFrame.from_dict(freq_list, orient='index').reset_index()
    return freq_df


# In[98]:


#Frequence categories of open restaurants
freq_open = get_frequency_categories(open_covid_df)
freq_open.sort_values(by=0, ascending=False).head(20)


# In[99]:


#Frequency categories of temporary closed restaurants
freq_temp_close = get_frequency_categories(closed_temp_df)
freq_temp_close.sort_values(by=0, ascending=False).head(20)


# In[100]:


#Frequence categories of permanently closed restaurants
freq_permn_closed = get_frequency_categories(closed_df)
freq_permn_closed.sort_values(by=0, ascending=False).head(20)


# In[101]:


new_df.head(5)


# In[102]:


new_df['stars']


# In[103]:


closed_df.to_csv('restaurants_perm_closed.csv')


# In[ ]:




