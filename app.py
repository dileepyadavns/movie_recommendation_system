
from unittest import result
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests

# load the nlp model and tfidf vectorizer from disk
# filename = 'nlp_model.pkl'
# clf = pickle.load(open(filename, 'rb'))
# vectorizer = pickle.load(open('tranform.pkl','rb'))

# def create_similarity():
#     data = pd.read_csv('main_data.csv')
#     data=data.iloc[:100,:]
#     # creating a count matrix
#     cv = CountVectorizer()
#     count_matrix = cv.fit_transform(data['comb'])
#     # creating a similarity score matrix
#     similarity = cosine_similarity(count_matrix)
#     return data,similarity

# def rcmd(m):
#     m = m.lower()
#     try:
#         data.head()
#         similarity.shape
#     except:
#         data, similarity = create_similarity()
#     # if m not in data['movie_title'].unique():
#     #     return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    
#     if m in data['genres'].unique():
#         i=data.loc[data['geres']==m].index[0]
#         lst = list(enumerate(similarity[i]))
#         lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
#         lst = lst[1:11] # excluding first item since it is the requested movie itself
#         l = []
#         for i in range(len(lst)):
#             a = lst[i][0]
#             l.append(data['movie_title'][a])
#         return l

        


#     else:
#         i = data.loc[data['movie_title']==m].index[0]
#         lst = list(enumerate(similarity[i]))
#         lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
#         lst = lst[1:11] # excluding first item since it is the requested movie itself
#         l = []
#         for i in range(len(lst)):
#             a = lst[i][0]
#             l.append(data['movie_title'][a])
#         return l
    
# # converting list of string to list (eg. "["abc","def"]" to ["abc","def"])
# def convert_to_list(my_list):
#     my_list = my_list.split('","')
#     my_list[0] = my_list[0].replace('["','')
#     my_list[-1] = my_list[-1].replace('"]','')
#     return my_list

# def get_suggestions():
#     data = pd.read_csv('main_data.csv')
#     return list(data['movie_title'].str.capitalize())

app = Flask(__name__)


@app.route("/similarity",methods=["GET","POST"])
def similarity():
    data = pd.read_csv('main_data.csv')
    data=data.iloc[:10000][:]
    m_str=list(data['movie_title'].str.capitalize())
    return m_str



# def recommend():
#     data = pd.read_csv('main_data.csv')
#     data=data.iloc[:500,:]

#     m_str=list(data['movie_title'].str.capitalize())
    
#     return render_template('recommend.html',movies=m_str)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home", methods=['POST','GET'])
def home():


    data = pd.read_csv('main_data.csv')
    data=data.iloc[:500,:]
   
    token= '5492165c61b1a21c06eb3a3b578a6339'
    
    
    arr= list(data['movie_title'].str.capitalize())
    ppath=[]

    for i in arr:
        response = requests.get("https://api.themoviedb.org/3/search/movie?api_key="+token+"&query="+i).json()
        try:
           path= 'https://image.tmdb.org/t/p/original'+str(response['results'][0]['poster_path'])
           new=[i,path]
           ppath.append(new)
        except IndexError:
            pass   
    
    print(ppath)

    return render_template('recommend.html',ppath=ppath)

if __name__ == '__main__':
    app.run(debug=True)

