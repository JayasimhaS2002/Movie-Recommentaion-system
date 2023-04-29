#MODEL 2-USING CONTENT BASED FILTERING
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import ast

def get_results_2(user_text):
    
    credits = pd.read_csv("tmdb_5000_credits.csv")
    movies = pd.read_csv("modified_movies_final.csv")
    credits_column_renamed = credits.rename(index=str, columns={"movie_id": "id"})
    movies_merge = movies.merge(credits_column_renamed, on='id')
    movies_cleaned = movies_merge.drop(columns=[ 'title_x', 'title_y', 'status','production_countries'])
    
    a=movies_cleaned['genres']
    #a.head(10)
    for j in range(len(a)):
        ele=ast.literal_eval(a[j])
        s=''
        for i in ele:
            s+=i["name"]+" "
        a[j]=s
        
    k=movies_cleaned["genres"]+movies_cleaned["overview"]
    movies_cleaned["statement"]=k
    
    tfv = TfidfVectorizer(min_df=3,  max_features=None,
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english') 
      
    x = tfv.fit_transform(movies_cleaned['statement'].apply(lambda x: np.str_(x)))
    #Tf-idf-weighted document-term matrix i stored in x.
    
    tfv_matrix = x
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    
    #computes similiarity scores between every two terms thus diagnol values are 1 and returns the similarity matrix.
    
    indices = pd.Series(movies_cleaned.index, index=movies_cleaned['original_title']).drop_duplicates()
    #indices of all the movie titles inclined with the similarity matrix.

    
    def give_recomendations(title, sig=sig):
        #receives the sig value which is the similarity matrix along with user input.
        
        # Get the index for the user input.
        idx = indices[title]

        # Get the pairwsie similarity scores for this title with the all other titles.
        sig_scores = list(enumerate(sig[idx]))

        # Sort the movies using this score.
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # Scores of the 10 most similar movies
        sig_scores = sig_scores[1:11]

        # Movie indices
        movie_indices_list = [i[0] for i in sig_scores]
        movies_list_2=[]
        #data = {'Movies': movies_list}

        #results_dataframe = pd.DataFrame(data)
        # Top 10 most similar movies
        #print(movie_indices_list)
        for i in movie_indices_list:
            movies_list_2.append(movies_cleaned['original_title'].iloc[i])
    
        data = {'Ids': movie_indices_list,'Movies':movies_list_2}

        results_dataframe_2 = pd.DataFrame(data)
        return results_dataframe_2,len(results_dataframe_2.index)
    
    result_df_2,length_2 = give_recomendations(user_text)

    return result_df_2,length_2
    