from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
#region CustomImports

import re
import nltk
import numpy as np
import pandas as pd
from wordcloud import WordCloud
nltk.download("stopwords")
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
nltk.download('punkt')
import os
from pdfminer.high_level import extract_text
import docx2txt
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

#endregion


#region All Action Methods

def index(request):
    return render(request,'PersonalityPredictor.html')

def PredictPersonality(request):
    responseDataDict = dict()

    userJD = request.GET["userJD"]
    resumePath = 'D:/Mohsin-Naqvi/Practice Projects/Python/Personality Predictor/Project/Static/Resume/Resume.csv'
    ttPath = 'D:/Mohsin-Naqvi/Practice Projects/Python/Personality Predictor/Project/Static/top10similarity'
    dataPath="D:/Mohsin-Naqvi/Practice Projects/Python/Personality Predictor/Project/Static/data/data"
    oceanKeywordsPath = 'D:/Mohsin-Naqvi/Practice Projects/Python/Personality Predictor/Project/Static/oceankeywords.csv'
    print("in the action")
    df = pd.read_csv(resumePath)
    df.head()
    df['Cleaned Resume'] = df['Resume_str'].apply(lambda w: __preprocess(w))
    cr= df['Cleaned Resume']
    cs = []

    for r in cr:    
        clean_jd = __clean_job_decsription(userJD) ## Get a Keywords Cloud 
        text1 = r 
        #text1 = df["Cleaned Resume"][2]
        text = [text1, userJD] 
        score = __get_resume_score(text)
        
        # print(score)
        cs.append(score)

    df['Cosine_similarity']= cs
    df.sort_values(['Cosine_similarity'], ascending=False)
    df.nlargest(n=10, columns=['Cosine_similarity'])
    
    tt = df.nlargest(n=10, columns=['Cosine_similarity'])
    tt.to_csv(ttPath)
    
    resumeScores = dict()

    for i in tt.index: # read csv column having file names(ids)
        id= tt['ID'][i]
    #print(id)
    #ids = tt.ID.tolist()
        for r,d, f in os.walk(dataPath): 
            for file in f:
                fp=os.path.join(r, file)
                #print(fp)
                if file.endswith(".pdf"):
                    fn=os.path.basename(file)
                    fname=fn.split('.')[0]
                    #print(fname, id)
                    if str(tt['ID'][i]) == fname:
                    #print(fname,id)
                    #text = extract_text(file)
                        with open(fp,'rb') as t:
                            text = extract_text(t)
                            text = str(text)
                            text = text.replace("\\n", "")
                            text = text.lower()

                            eachResumeScore = __phrase_match(text,oceanKeywordsPath)
                            resumeScores["r"+str(len(resumeScores)+1)] = eachResumeScore
        
    responseDataDict["Result"] = resumeScores
    return JsonResponse(responseDataDict)

#endregion

#region process methods

def __clean_job_decsription(jd):
     ''' a function to create a word cloud based on the input text parameter'''
     ## Clean the Text
     # Lower
     clean_jd = jd.lower()
     # remove punctuation
     clean_jd = re.sub(r'[^\w\s]', '', clean_jd)
     # remove trailing spaces
     clean_jd = clean_jd.strip()
     # remove numbers
     clean_jd = re.sub('[0-9]+', '', clean_jd)
     # tokenize 
     clean_jd = word_tokenize(clean_jd)
     # remove stop words
     stop = stopwords.words('english')
     clean_jd = [w for w in clean_jd if not w in stop] 
     return(clean_jd)

def __get_resume_score(text):
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(text)
    #Print the similarity scores
    print("\nSimilarity Scores:")
     
    #get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2) # round to two decimal
     
    print("Your resume matches about "+ str(matchPercentage)+ "% of the job description.")
    return matchPercentage


def __preprocess(txt):
    print("preprocess method start")
    # convert all characters in the string to lower case
    txt = txt.lower()
    # remove non-english characters, punctuation and numbers
    txt = re.sub('[^a-zA-Z]', ' ', txt)
    txt = re.sub('http\S+\s*', ' ', txt)  # remove URLs
    txt = re.sub('RT|cc', ' ', txt)  # remove RT and cc
    txt = re.sub('#\S+', '', txt)  # remove hashtags
    txt = re.sub('@\S+', '  ', txt)  # remove mentions
    txt = re.sub('\s+', ' ', txt)  # remove extra whitespace
    # tokenize word
    txt = nltk.tokenize.word_tokenize(txt)
    # remove stop words
    txt = [w for w in txt if not w in nltk.corpus.stopwords.words('english')]
    return ' '.join(txt)


def __phrase_match(text,path):    
    keyword_df = pd.read_csv(path)
    Openness_words  = keyword_df['Openness']
    Conscientiousness_words = keyword_df['Conscientiousness']
    Extraversion_words = keyword_df['Extraversion']
    Agreeableness_words = keyword_df['Agreeableness']
    Neuroticism_words = keyword_df['Neuroticism']

    opennessCount = 0
    conscientiousnessCount = 0
    ExtraversionCount = 0
    AgreeablenessCount = 0
    NeuroticismCount = 0

    for opennessWord in Openness_words:
        if re.search(r"\b{}\b".format(opennessWord.lower()), text, re.IGNORECASE) is not None:
            opennessCount += 1

    for conscientiousnessWord in Conscientiousness_words:
        if re.search(r"\b{}\b".format(conscientiousnessWord.lower()), text, re.IGNORECASE) is not None:
            conscientiousnessCount += 1

    for extraversionWord in Extraversion_words:
        if re.search(r"\b{}\b".format(extraversionWord.lower()), text, re.IGNORECASE) is not None:
            ExtraversionCount += 1

    for agreeablenessWord in Agreeableness_words:
        if re.search(r"\b{}\b".format(agreeablenessWord.lower()), text, re.IGNORECASE) is not None:
            AgreeablenessCount += 1

    for neuroticismWord in Neuroticism_words:
        if re.search(r"\b{}\b".format(neuroticismWord.lower()), text, re.IGNORECASE) is not None:
            NeuroticismCount += 1
    
    return dict(opennessCount = opennessCount, 
                conscientiousnessCount = conscientiousnessCount, 
                ExtraversionCount = ExtraversionCount,
                AgreeablenessCount = AgreeablenessCount,
                NeuroticismCount = NeuroticismCount
                )

    
def __read_pdf_resume(pdf_doc):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_doc, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True,check_extractable=True):           
            page_interpreter.process_page(page)     
        text = fake_file_handle.getvalue() 
    # close open handles      
    converter.close() 
    fake_file_handle.close() 
    if text:     
        return text

def __read_word_resume(word_doc):
     resume = docx2txt.process(word_doc)
     resume = str(resume)
     #print(resume)
     text =  ''.join(resume)
     text = text.replace("\n", "")
     if text:
         return text

#endregion