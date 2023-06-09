#MODEL 2-USING KNN TO PREDICT CLOSEST MOVIES(SIMILAR)

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.corpus import stopwords
from scipy import spatial


def get_results(user_text):
    credits = pd.read_csv("tmdb_5000_credits.csv")
    movies = pd.read_csv("modified_movies_final.csv")
    
    # changing the genres column from json to string
    movies['genres'] = movies['genres'].apply(json.loads)
    for index,i in zip(movies.index,movies['genres']):
    
        list1 = []
        for j in range(len(i)):
            list1.append((i[j]['name'])) # the key 'name' contains the name of the genre
        movies.loc[index,'genres'] = str(list1)
        
    # changing the keywords column from json to string
    movies['keywords'] = movies['keywords'].apply(json.loads)
    for index,i in zip(movies.index,movies['keywords']):
        list1 = []
        for j in range(len(i)):
            list1.append((i[j]['name']))
        movies.loc[index,'keywords'] = str(list1)
        
    # changing the production_companies column from json to string
    movies['production_companies'] = movies['production_companies'].apply(json.loads)
    for index,i in zip(movies.index,movies['production_companies']):
        list1 = []
        for j in range(len(i)):
            list1.append((i[j]['name']))
        movies.loc[index,'production_companies'] = str(list1)
        
    # changing the cast column from json to string
    credits['cast'] = credits['cast'].apply(json.loads)
    for index,i in zip(credits.index,credits['cast']):
        list1 = []
        for j in range(len(i)):
            list1.append((i[j]['name']))
        credits.loc[index,'cast'] = str(list1)
        
    # changing the crew column from json to string    
    credits['crew'] = credits['crew'].apply(json.loads)
    def director(x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
    credits['crew'] = credits['crew'].apply(director)
    credits.rename(columns={'crew':'director'},inplace=True)


    movies = movies.merge(credits,left_on='id',right_on='movie_id',how='left')
    movies = movies[['id','original_title','genres','cast','vote_average','director','keywords']]

    movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
    movies['genres'] = movies['genres'].str.split(',')


    for i,j in zip(movies['genres'],movies.index):
        list2=[]
        list2=i
        list2.sort()
        movies.loc[j,'genres']=str(list2)
    movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
    movies['genres'] = movies['genres'].str.split(',')
    
    
    genreList = []
    for index, row in movies.iterrows():
        genres = row["genres"]
        
        for genre in genres:
            if genre not in genreList:
                genreList.append(genre)
                
    #genreList[:10] 
    #now we have a list with unique genres   

    def binary(genre_list):
        binaryList = []
        
        for genre in genreList:
            if genre in genre_list:
                binaryList.append(1)
            else:
                binaryList.append(0)
        
        return binaryList


    movies['genres_bin'] = movies['genres'].apply(lambda x: binary(x))
    #movies['genres_bin'].head()

    movies['cast'] = movies['cast'].str.strip('[]').str.replace(' ','').str.replace("'",'').str.replace('"','')
    movies['cast'] = movies['cast'].str.split(',')


    for i,j in zip(movies['cast'],movies.index):
        list2 = []
        list2 = i[:4]
        movies.loc[j,'cast'] = str(list2)
    movies['cast'] = movies['cast'].str.strip('[]').str.replace(' ','').str.replace("'",'')
    movies['cast'] = movies['cast'].str.split(',')
    for i,j in zip(movies['cast'],movies.index):
        list2 = []
        list2 = i
        list2.sort()
        movies.loc[j,'cast'] = str(list2)
    movies['cast']=movies['cast'].str.strip('[]').str.replace(' ','').str.replace("'",'')

    castList = []
    for index, row in movies.iterrows():
        cast = row["cast"]
        
        for i in cast:
            if i not in castList:
                castList.append(i)
                              
    def binary(cast_list):
        binaryList = []
        
        for genre in castList:
            if genre in cast_list:
                binaryList.append(1)
            else:
                binaryList.append(0)
        
        return binaryList

    movies['cast_bin'] = movies['cast'].apply(lambda x: binary(x))
    #movies['cast_bin'].head()

    def xstr(s):
        if s is None:
            return ''
        return str(s)
    movies['director'] = movies['director'].apply(xstr)

    directorList=[]
    for i in movies['director']:
        if i not in directorList:
            directorList.append(i)
            
    def binary(director_list):
        binaryList = []  
        for direct in directorList:
            if direct in director_list:
                binaryList.append(1)
            else:
                binaryList.append(0)
        return binaryList

    movies['director_bin'] = movies['director'].apply(lambda x: binary(x))

    movies['keywords'] = movies['keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'').str.replace('"','')
    movies['keywords'] = movies['keywords'].str.split(',')
    for i,j in zip(movies['keywords'],movies.index):
        list2 = []
        list2 = i
        movies.loc[j,'keywords'] = str(list2)
    movies['keywords'] = movies['keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'')
    movies['keywords'] = movies['keywords'].str.split(',')
    for i,j in zip(movies['keywords'],movies.index):
        list2 = []
        list2 = i
        list2.sort()
        movies.loc[j,'keywords'] = str(list2)
    movies['keywords'] = movies['keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'')
    movies['keywords'] = movies['keywords'].str.split(',')


    words_list = []
    for index, row in movies.iterrows():
        genres = row["keywords"]
        
        for genre in genres:
            if genre not in words_list:
                words_list.append(genre)
                
                
    def binary(words):
        binaryList = []
        for genre in words_list:
            if genre in words:
                binaryList.append(1)
            else:
                binaryList.append(0)
        return binaryList


    movies['words_bin'] = movies['keywords'].apply(lambda x: binary(x))
    movies = movies[(movies['vote_average']!=0)] #removing the movies with 0 score and without director names 
    movies = movies[movies['director']!='']

    def Similarity(movieId1, movieId2):
        a = movies.iloc[movieId1]
        b = movies.iloc[movieId2]
        
        genresA = a['genres_bin']
        genresB = b['genres_bin']
        
        genreDistance = spatial.distance.cosine(genresA, genresB)
        
        scoreA = a['cast_bin']
        scoreB = b['cast_bin']
        scoreDistance = spatial.distance.cosine(scoreA, scoreB)
        directA = a['director_bin']
        directB = b['director_bin']
        directDistance = spatial.distance.cosine(directA, directB)
        wordsA = a['words_bin']
        wordsB = b['words_bin']
        wordsDistance = spatial.distance.cosine(directA, directB)
        return genreDistance + directDistance + scoreDistance + wordsDistance

    #Similarity(3,160) #checking similarity between any 2 random movies

    new_id = list(range(0,movies.shape[0]))
    movies['new_id']=new_id
    movies=movies[['original_title','genres','vote_average','genres_bin','cast_bin','new_id','director','director_bin','words_bin']]
    #movies.head()

    import operator

    def predict_score(name):
        #name = input('Enter a movie title: ')
        new_movie = movies[movies['original_title'].str.contains(name)].iloc[0].to_frame().T
        #print('Selected Movie: ',new_movie.original_title.values[0])
        def getNeighbors(baseMovie, K):
            distances = []
        
            for index, movie in movies.iterrows():
                if movie['new_id'] != baseMovie['new_id'].values[0]:
                    dist = Similarity(baseMovie['new_id'].values[0], movie['new_id'])
                    distances.append((movie['new_id'], dist))
        
            distances.sort(key=operator.itemgetter(1))
            neighbors = []
            for x in range(K):
                neighbors.append(distances[x])
            return neighbors
        K = 10
        avgRating = 0
        neighbors = getNeighbors(new_movie, K)
        
        movies_list=[]
        genres_list=[]
        ratings_list=[]
        #print('\nRecommended Movies: \n')
        for neighbor in neighbors:
            avgRating = avgRating+movies.iloc[neighbor[0]][2]  
            
            movies_list.append(movies.iloc[neighbor[0]][0])
            genres_list.append(str(movies.iloc[neighbor[0]][1]).strip('[]').replace(' ',''))
            ratings_list.append(str(movies.iloc[neighbor[0]][2]))
            
        
        data = {'Movies': movies_list,'Genres': genres_list,'Rating': ratings_list}

        results_dataframe = pd.DataFrame(data)
        #print(results_dataframe)
        
            #print( movies.iloc[neighbor[0]][0])
            #print("Genres: "+str(movies.iloc[neighbor[0]][1]).strip('[]').replace(' ',''))
            #print("Rating: "+str(movies.iloc[neighbor[0]][2]))
        #print('\n')
        avgRating = avgRating/K
        return results_dataframe,len(results_dataframe.index)
    
    result_df,length = predict_score(user_text)
    return result_df,length

