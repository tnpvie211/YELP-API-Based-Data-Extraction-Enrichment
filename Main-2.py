#!/usr/bin/env python
# coding: utf-8

# # Import File

# In[1]:


import pandas as pd
import numpy as np


# In[ ]:


business_df = pd.read_csv('yelp_academic_dataset_business.csv',low_memory=False)


# In[3]:


business_df.sort_index(axis=1, inplace=True)
business_df.info()


# In[4]:


business_df.count()


# In[5]:


business_df.head()


# # Replace Unclear Value In Columns

# In[6]:


def replace_value(dataframe, column, new_values):
    values= dataframe[column].unique()
    for i in range(len(values)):
        dataframe[column].replace({values[i]: new_values[i]}, inplace=True)


# In[7]:


business_df['attributes.AgesAllowed'].unique()


# In[8]:


replace_value(business_df, 'attributes.AgesAllowed',[np.nan, 21, 0, 18, 19, 0])
business_df['attributes.AgesAllowed'].unique()


# In[9]:


business_df['attributes.Alcohol'].unique()


# In[10]:


replace_value(business_df, 'attributes.Alcohol', ['beer and wine', 'beer and wine', np.nan, 'none', 'none', 'full bar', 'full bar', 'none'])
business_df['attributes.Alcohol'].unique()


# In[11]:


business_df['attributes.BikeParking'].unique()


# In[12]:


replace_value(business_df, 'attributes.BikeParking', ['True', 'False', np.nan, 'False'])
business_df['attributes.BikeParking'].unique()


# In[13]:


business_df['attributes.NoiseLevel'].unique()


# In[14]:


replace_value(business_df, 'attributes.NoiseLevel', ['average', np.nan , 'average', 'quiet', 'very loud', 'quiet', 'loud', 'loud', 'very loud', np.nan])
business_df['attributes.NoiseLevel'].unique()


# In[15]:


business_df['attributes.OutdoorSeating'].unique()


# In[16]:


replace_value(business_df, 'attributes.OutdoorSeating', ['True', 'False', np.nan, 'False'])
business_df['attributes.OutdoorSeating'].unique()


# In[17]:


business_df['attributes.RestaurantsAttire'].unique()


# In[18]:


replace_value(business_df, 'attributes.RestaurantsAttire', ['casual', 'casual', np.nan, 'dressy', 'formal', 'dressy', 'none', 'formal'])
business_df['attributes.RestaurantsAttire'].unique()


# In[19]:


business_df['attributes.RestaurantsDelivery'].unique()


# In[20]:


replace_value(business_df, 'attributes.RestaurantsDelivery', ['False', 'False', np.nan, 'True'])
business_df['attributes.RestaurantsDelivery'].unique()


# In[21]:


business_df['attributes.RestaurantsGoodForGroups'].unique()


# In[22]:


replace_value(business_df, 'attributes.RestaurantsGoodForGroups', ['True', 'False', np.nan, 'False'])
business_df['attributes.RestaurantsGoodForGroups'].unique()


# In[23]:


business_df['attributes.RestaurantsPriceRange2'].unique()


# In[24]:


replace_value(business_df, 'attributes.RestaurantsPriceRange2', [2, 1, np.nan, 3, 4, np.nan])
business_df['attributes.RestaurantsPriceRange2'].unique()


# In[25]:


business_df['attributes.RestaurantsReservations'].unique()


# In[26]:


replace_value(business_df, 'attributes.RestaurantsReservations', ['False', np.nan, 'True', np.nan])
business_df['attributes.RestaurantsReservations'].unique()


# In[27]:


business_df['attributes.RestaurantsTableService'].unique()


# In[28]:


replace_value(business_df, 'attributes.RestaurantsTableService', ['True', np.nan, 'False', 'False'])
business_df['attributes.RestaurantsTableService'].unique()


# In[29]:


business_df['attributes.RestaurantsTakeOut'].unique()


# In[30]:


replace_value(business_df, 'attributes.RestaurantsTakeOut', ['True', np.nan, 'False', 'False'])
business_df['attributes.RestaurantsTakeOut'].unique()


# In[31]:


business_df['attributes.Smoking'].unique()


# In[32]:


replace_value(business_df, 'attributes.Smoking', [np.nan, 'no', 'outdoor', 'yes', 'no', 'outdoor', 'yes', 'no'])
business_df['attributes.Smoking'].unique()


# In[33]:


business_df['attributes.WheelchairAccessible'].unique()


# In[34]:


replace_value(business_df, 'attributes.WheelchairAccessible', ['True', np.nan, 'False', 'False'])
business_df['attributes.WheelchairAccessible'].unique()


# In[35]:


business_df['attributes.WiFi'].unique()


# In[36]:


replace_value(business_df, 'attributes.WiFi', ['free', np.nan, 'no', 'free', 'no', 'paid', 'paid', 'no'])
business_df['attributes.WiFi'].unique()


# In[2]:


business_df['attributes.DriveThru'].unique()


# In[38]:


replace_value(business_df, 'attributes.DriveThru', [np.nan, 'True', 'False', 'False'])
business_df['attributes.DriveThru'].unique()


# # Filter Out Restaurants/Food & Drink Service

# In[39]:


business_df = business_df[business_df.categories.notnull()]
business_df.info()


# In[40]:


categories = list(business_df['categories'].unique())
categories


# In[41]:


filter_list = ['Restaurants','Bars','Food','Desserts','Bakery', 'Coffee', 'Tea'] 
pat = '|'.join(r"\b{}\b".format(x) for x in filter_list)
restaurant_df = business_df[business_df['categories'].str.contains(pat)]
restaurant_df


# In[42]:


restaurant_df.dropna(axis=0, how='all', inplace=True)
restaurant_df


# In[43]:


# Drop row with places accept insurance
restaurant_df = restaurant_df.loc[restaurant_df['attributes.AcceptsInsurance']!='True']
restaurant_df['attributes.AcceptsInsurance'].unique()


# In[44]:


restaurant_df.loc[restaurant_df['attributes.HairSpecializesIn'].notnull()].categories


# In[45]:


# Drop row with places have hair specializes in
restaurant_df = restaurant_df.loc[restaurant_df['attributes.HairSpecializesIn'].isnull()]
restaurant_df['attributes.HairSpecializesIn'].unique()


# In[46]:


restaurant_df.loc[restaurant_df['attributes.ByAppointmentOnly'].notnull()].categories


# In[47]:


# Delete Unecessary Columns
del restaurant_df['attributes.AcceptsInsurance']
del restaurant_df['attributes.HairSpecializesIn']
del restaurant_df['attributes']
del restaurant_df['attributes.BYOB']
del restaurant_df['attributes.BYOBCorkage']
del restaurant_df['attributes.Corkage']
del restaurant_df['attributes.BestNights']
del restaurant_df['attributes.BusinessAcceptsBitcoin']
del restaurant_df['attributes.CoatCheck']
del restaurant_df['attributes.Music']
del restaurant_df['attributes.HasTV']


# In[48]:


restaurant_df.info()


# # Get The New Columns From The List in Attributes

# In[49]:


import ast
def attributes_list(column):
    restaurant_df[column].replace({np.nan:'None'}, inplace=True)
    column = restaurant_df[column].unique()
    for each in column:
        if each != 'None':
            dictionary = ast.literal_eval(each)
            break
    return set(dictionary.keys())


# In[50]:


def label_attribute(column):
    restaurant_df[column].replace({np.nan:'None'}, inplace=True)
    for i, row in restaurant_df.iterrows():
        column_list = row[column]
        if column_list != 'None':
            dictionary = ast.literal_eval(column_list)
            for k, v in dictionary.items():
                restaurant_df.loc[i, k] = v


# In[51]:


label_attribute('attributes.Ambience')


# In[52]:


label_attribute('attributes.BusinessParking')


# In[53]:


label_attribute('attributes.GoodForMeal')


# In[54]:


restaurant_df


# # List Out Categories in Restaurant

# In[55]:


# Transform into a list
categories_list = restaurant_df['categories'].unique()
categories_list


# In[56]:


import re
categories_list_rep = []
for i in range(len(categories_list)):
    try:
        temp = re.sub('[&/\(),]', ' ', categories_list[i])
        categories_list_rep.append(temp)
    except:
        print(i,categories_list[i])
        pass


# In[57]:


categories_list_rep


# In[58]:


import nltk
nltk.download('punkt')


# In[59]:


from nltk.tokenize import word_tokenize 


# In[60]:


tokenized_category = [word_tokenize(word) for word in categories_list_rep]
tokenized_category


# In[61]:


import itertools
tokenized_category_list = list(itertools.chain.from_iterable(tokenized_category))
tokenized_category_list


# In[62]:


len(tokenized_category_list)


# In[63]:


from nltk import FreqDist
from nltk.probability import ConditionalFreqDist
freq_list = FreqDist(tokenized_category_list)
freq_df = pd.DataFrame.from_dict(freq_list, orient='index').reset_index()
freq_df.head(10)


# In[64]:


freq_df.head(20)


# In[65]:


del restaurant_df['attributes.Ambience']
del restaurant_df['attributes.BusinessParking']
del restaurant_df['attributes.GoodForMeal']
#del restaurant_df['hours']


# In[66]:


restaurant_df


# In[67]:


col_name = restaurant_df.columns
col_name


# In[68]:


def rename_col(col_name):
    for each in col_name:
        if 'attributes' in each:
            new_name = each.split('.')
            restaurant_df.rename(columns={each:new_name[1]}, inplace=True)


# In[69]:


rename_col(col_name)
restaurant_df


# In[70]:


restaurant_df.info()


# In[72]:


restaurant_open_df = restaurant_df[restaurant_df['is_open']==1]
restaurant_open_df.info()


# In[73]:


#Delete restaurants with big chains (more than 4 locations)
def get_non_chains(restaurants):
    num_locations_dict = restaurant_df['name'].value_counts().to_dict()
    valid_locations = set([name for name in num_locations_dict.keys() if num_locations_dict[name] < 4])
    return restaurant_df[restaurant_df['name'].isin(valid_locations)]


# In[76]:


non_chains = get_non_chains(restaurant_df)


# In[78]:


non_chains.info()


# In[83]:


#restaurant_df.to_csv('restaurant_yelp.csv')


# In[79]:


covid_df = pd.read_csv('yelp_academic_dataset_covid_features.csv',low_memory=False)
covid_df.head()


# In[80]:


covid_df.info()


# In[83]:


covid_restaurants = covid_df[covid_df['business_id'].isin(set(restaurant_open_df['business_id']))]
covid_restaurants = covid_restaurants[(covid_restaurants['highlights'] != 'FALSE') | (covid_restaurants['Covid Banner'] != 'FALSE') | (covid_restaurants['Temporary Closed Until'] != 'FALSE')]


# In[84]:


covid_restaurants


# In[86]:


response_json_by_id = dict()


# In[89]:


def decorate_with_yelp_rest_api(df, response_json_by_id):
    headers = {
    'Authorization': 't8HOmsPXHzP-YxYvGoTaGBgqQSjiQ-PJc6XeXOXLjmPGzTlT5ndbvJefQ_pMVxP_5iYwjxVkb7aiqefs3aHb0NN_WHlRD1FB0WZVPcuvgEGrBZr70qXIW2jbEcU7YXYx'
    }
    
    for business_id in restaurant_open_df['business_id'].tolist():
        if business_id in response_json_by_id:
            continue
        print(business_id)
        url = 'https://api.yelp.com/v3/businesses/%s' % business_id
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
            if response.status_code == 200:
                response_json_by_id[business_id] = response.json()
            else:
                print("invalid request for %s" % business_id)
        except Exception as e:
            print("invalid request for %s" % business_id)        
    
    return response_json_by_id


# In[91]:


import requests
response_json_by_id = decorate_with_yelp_rest_api(restaurant_open_df, response_json_by_id)
responseDF = pd.DataFrame.from_dict(response_json_by_id, orient='index')


# In[93]:


response_json_by_id


# In[ ]:




