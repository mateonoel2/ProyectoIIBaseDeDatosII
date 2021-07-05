import numpy
import nltk
import operator
import json
import math
import sys
import os
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

TOP_K = 5

index = {}
file_name = "tweets_2021-06-28.json"
index_name = "index/"
name = ""
stemmer = SnowballStemmer("spanish")
N = 0
Lenght = {}
for i in file_name:
    if i != '.':
        index_name += i
    else:
        break
name = index_name+".txt"

with open('stop_words_spanish.txt') as file:
    stop_words = [line.lower().strip() for line in file]
stop_words += ['.', '@', '!', '?', ',', ':', '%', '\'', "\'\'", "\"\" " , '|', "``", "https"]

def Score(q, d):
    score = 0
    sum_1 = 0
    sum_2 = 0
    sum_3 = 0

    for i in q.keys():
        sum_1 += (float(q[i]) * float(d[i]))
        sum_2 += float(q[i]**2)
        sum_3 += float(d[i]**2)
    
    if sum_2 * sum_3 == 0:
        return 0


    score = sum_1 / (math.sqrt(sum_2) * math.sqrt(sum_3))

    return score

def indexar_1(stemmer, name, query, filename):
    file_name = "tweets_2021-06-28.json"
    if(filename == ""):
        print()
    elif os.path.isfile(filename):
        file_name = filename
    else:
        print("No existe")
    tweets = json.load(open(file_name))
    N = len(tweets)
    counter = 0
#CREACION INDICE INVERTIDO
    for  i in tweets:
        tweet_id = i["id"]
        if i["retweeted"]:
            palabra = nltk.word_tokenize(i["RT_text"].lower())
            Lenght[tweet_id] = len(i["RT_text"])
        #print(palabra)
        else:
            palabra = nltk.word_tokenize(i["text"].lower())
            Lenght[tweet_id] = (len(i["text"]))
        #print(palabra)
#filtramos stop words
        clean = palabra[:]
        for token in palabra:
            if token in stop_words:
                clean.remove(token)
#Stemmer
        stemmed = []
        for word in clean:
            word = stemmer.stem(word)
            stemmed.append(word)
#OpenIndex
    #name = index_name+".txt"
        flag = False
        indice = open(name, "w")
        indice.close()
        for final_term in stemmed:
            if final_term in index.keys():
                    if index not in index[final_term]:
                        index[final_term].append(tweet_id)
            else:
                index[final_term] = []
                index[final_term].append(tweet_id)
    
            out_file = open("index/temp.txt", "w")
            for j in index.keys():
                out_file.write(j)
                out_file.write(" ")
                out_file.write(str(len(index[j])))
                for k in index[j]:
                    out_file.write(" ")
                    out_file.write(str(k))
                out_file.write("\n")
            out_file.close()
            os.remove(name)
            os.rename("index/temp.txt", name) 
    Scores = {}
    #query = "En mi pueblo me encontré una libertad para el país"
    palabrita = nltk.word_tokenize(query.lower())
    palabrita_query = []
    for i in palabrita:
        palabrita_query.append(stemmer.stem(i))
#Tenemos los términos de la Query
    tweets_2 = json.load(open(file_name))
    Query_tf_idf = {}
#Iteramos en cada "Documento"
    counter_2 = 0;
    query_lenght = len(palabrita)
    TERMS = {}
    index_file_2 = open(name)
    for i in index_file_2.readlines():
        temporal_list = i.split()
        if temporal_list[0] in palabrita_query:
            TERMS[temporal_list[0]] = []
            for x in temporal_list:
                TERMS[temporal_list[0]].append(x.strip()) 
        else:
            continue
    index_file_2.close()
#Ya tenemos en TERMS los términos con los que compararemos
    for i in palabrita_query:
        if i in TERMS.keys():
            Query_tf_idf[i] = palabrita_query.count(i) * math.log10(N / int(TERMS[i][1]))

    tweets_2 = json.load(open(file_name))
    Docs_tf_idf = {}
    for i in tweets_2:
        Docs_tf_idf[i["id"]] = {}
        if i["retweeted"]:
            palabra = nltk.word_tokenize(i["RT_text"].lower())
        else:
            palabra = nltk.word_tokenize(i["text"].lower())
#filtramos stop words
        clean = palabra[:]
        for token in palabra:
            if token in stop_words:
                clean.remove(token)
#Stemmer
        stemmer = SnowballStemmer("spanish")
        stemmed = []
        for word in clean:
            word = stemmer.stem(word)
            stemmed.append(word)
        lista_temp = TERMS.keys()
        for j in lista_temp:
            if str(i["id"]) in TERMS[j]:
                Docs_tf_idf[i["id"]][j]  = stemmed.count(j) * math.log10(N / int(TERMS[j][1]))
            else:
                Docs_tf_idf[i["id"]][j] = 0
    counter_final = 0
    for i in Docs_tf_idf.keys():
        Scores[i] = Score(Query_tf_idf, Docs_tf_idf[i]) / Lenght[i]
    FINAL_TOP = sorted(Scores.items(), key=operator.itemgetter(1), reverse = True)
#Print Answers:
    ANSWERS = []
    ANS_SCORES = []
    for i in range(5):
        ANSWERS += FINAL_TOP[i*2]
        ANS_SCORES += FINAL_TOP[i+1]
    tweets_final = json.load(open(file_name))

    FINAL_ANSWER = []

    for i in ANSWERS:
        for k in tweets_final:
            if k["id"] == i:
                if k["retweeted"]:
                    flag = False
                    FINAL_ANSWER.append(k["RT_text"])
                else:
                    flag = True
                    FINAL_ANSWER.append(k["text"])
    
    return FINAL_ANSWER



class ejemplo_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)
        self.buttonBuscar.clicked.connect(self.buscar)


    def insert(self):
        i = 0
        self.listWidget.insertItem(i, "string")

    def buscar(self):
        #self.buttonBuscar.setEnabled(False)
        filename = self.lineJSON.text()
        query = self.lineQuerie.text()
        
        answer = indexar_1(stemmer, name, query, filename)
        self.listWidget.clear()
        for i in answer:
            self.listWidget.insertItem(1, i)
        


    

    
        

if __name__=='__main__':
    app = QApplication(sys.argv)
    GUI = ejemplo_GUI()
    GUI.show()
    sys.exit(app.exec())



#tokenizar
