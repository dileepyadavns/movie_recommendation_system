#!/usr/bin/env python
# coding: utf-8

# In[12]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
    


# In[13]:


import numpy as np
import pandas as pd


# In[14]:


new=pd.read_csv("main_data.csv")


# In[15]:


new


# In[16]:


vector = cv.fit_transform(new['comb']).toarray()


# In[ ]:


vector.shape
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)


# In[ ]:





# In[1]:


similarity
new[new['movie_title'] == 'toy story'].index[0]


# In[ ]:


def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].movie_title)
        
    
recommend('toy story')


# In[ ]:




