from flask import Flask
from flask import render_template,request,session
import warnings


warnings.filterwarnings('ignore')
from Bio import Entrez
import pandas as pd
import json
from pyparsing import anyOpenTag, anyCloseTag
from xml.sax.saxutils import unescape as unescape


from flask import send_file
from flask_session import Session
from datetime import timedelta

import recomm_movies_knn as reco
import recomm_movies_content as recon

import pandas as pd
import pickle


app = Flask(__name__)


@app.route('/')
def search():
    return render_template('search.html')


@app.route('/save',methods=['GET','POST'])
def tag():
    if request.method =='POST':
        file =request.form.to_dict()
      
        user_text= file['user_info']
        result_dataframe,dataframe_length= reco.get_results(user_text)
    else:
        print("not found")
    
    return render_template('save.html',word_passed=True,text=file,tables=[result_dataframe.to_html(classes='data',index=False)], titles=result_dataframe.columns.values,len=dataframe_length)
   
@app.route('/result2',methods=['GET','POST'])
def tag2():
    if request.method =='POST':
        file_2=request.form.to_dict()
        user_text= file_2['user_info_2']
        result_dataframe_2,dataframe_length_2= recon.get_results_2(user_text)
    else:
        print("not found")
    return render_template('result2.html',word_passed=True,text=file_2,tables=[result_dataframe_2.to_html(classes='data',index=False)], titles=result_dataframe_2.columns.values,len2=dataframe_length_2)
       

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    

   app.run(debug=True)