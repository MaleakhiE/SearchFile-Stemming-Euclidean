import string
import nltk
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from pdfminer.high_level import extract_text
import streamlit as st
import pandas as pd
import docx2txt
import os
import numpy as np
from math import *
import math
import numbers
from sklearn.feature_extraction.text import *

factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
factory = StemmerFactory()
stemmer = factory.create_stemmer()
datauji = [[]]
hasilstem =[[]]
hasilstem2=[]
hasilstemsemua=[]
hasilstemuser=''
inputuser=''
jumlahdata=[]
hasilhitung=[]
jarak=[]
path=''
query=''
jumlahuser=[]
hasiltfidf=[]
global file

st.set_page_config(
    page_title="Information Retrieval",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

def uploadfiles():
    uploaded_file = st.text_input(label = "Please enter the path to the file")
    try :
        global inputuser,path,query
        path = uploaded_file
        os.chdir(uploaded_file)
        files = os.listdir()
        st.write(files)
        inputuser = st.text_input(label="Input Query")
        query = inputuser
        for file_name in files:
            if uploaded_file is not None:
                global datauji
                try:
                    text = extract_text(file_name)
                    text = re.sub("[^a-zA-Z]", " ", text)
                except:
                    text = docx2txt.process(file_name)
                    text = re.sub("[^a-zA-Z]", " ", text)
                datauji.append(text)
        del datauji[0]
        st.write("**Hasil Ekstraksi Data Uji**")
        st.write((datauji))
    except :
        st.text('')

def steeming2(datauji):
    for i in datauji :
        text = "".join(i)
        text = text.lower()
        # Menghilangkan komponen selain angka dan huruf
        text = re.sub("[^a-zA-Z]", " ", text)
        text = text.translate(str.maketrans("","",string.punctuation))
        text = text.strip()
        text = re.sub('\s+',' ',text)

        # Tokenizing dan lemmatizing
        text = nltk.word_tokenize(text)
        # proses unarray data
        text = " ".join(text)

        # Proses Stemming Nazief dan Adriani
        text = stemmer.stem(text)

        # Melakukan filltering (menghapus stopword)
        text = stopword.remove(text)
        text = nltk.tokenize.word_tokenize(text)
        text = " ".join(text)

        global hasilstem2
        # output data
        hasilstem2.append(text)

#proses steeming text
def steeming(datauji):
    for i in datauji:
        text = "".join(i)
        text = text.lower()
        # Menghilangkan komponen selain angka dan huruf
        text = re.sub("[^a-zA-Z]", " ", text)
        text = text.translate(str.maketrans("","",string.punctuation))
        text = text.strip()
        text = re.sub('\s+',' ',text)

        # Tokenizing dan lemmatizing
        text = nltk.word_tokenize(text)
        # proses unarray data
        text = " ".join(text)

        # Proses Stemming Nazief dan Adriani
        text = stemmer.stem(text)

        # Melakukan filltering (menghapus stopword)
        text = stopword.remove(text)
        text = nltk.tokenize.word_tokenize(text)

        global hasilstem
        global hasilstemsemua
        # output data
        hasilstemsemua = hasilstemsemua+text
        hasilstem.append(text)
    del hasilstem[0]
    st.write("**Hasil Stemming (Nazief dan Adriani) Semua File**")
    st.write((hasilstem))

def steeminguser(inputuser):
    text = inputuser.lower()
    # Menghilangkan komponen selain angka dan huruf
    text = re.sub("[^a-zA-Z]", " ", text)
    text = text.translate(str.maketrans("","",string.punctuation))
    text = text.strip()
    text = re.sub('\s+',' ',text)

    # Tokenizing dan lemmatizing
    text = nltk.word_tokenize(text)
    # proses unarray data
    text = " ".join(text)

    # Proses Stemming Nazief dan Adriani
    text = stemmer.stem(text)

    # Melakukan filltering (menghapus stopword)
    text = stopword.remove(text)
    text = nltk.tokenize.word_tokenize(text)

    global hasilstemuser
    hasilstemuser = text
    st.write("**Hasil Stemming Input User**")
    st.text(str(hasilstemuser))

#proses menghitung jumlah kata
def countstring(hasilstem,path):
    datasama = {}
    kata = []
    jumlah=[]
    global hasilhitung
    try :
        os.chdir(path)
        files = os.listdir()
        b = -1
        for a in hasilstem :
            b = b+1
            for i in set(a):
                datasama[i] = a.count(i)
                kata.append(i)
                jumlah.append(datasama[i])

                hasil_data = {
                    'Jumlah': jumlah,
                    'Kata': kata
                }
            write = pd.DataFrame(hasil_data)
            kata.clear()
            jumlah.clear()
            datasama.clear()
            tab1, tab2 = st.tabs(["Data", "Grafik"])
            with tab1:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1 :
                    st.write('')
                with col2 :
                    st.write('')
                with col3 :
                    st.write('Hasil Stemming File  - **' + files[b] + '**')
                    st.write(write)
                with col4 :
                    st.write('')
                with col5 :
                    st.write('')
            with tab2:
                st.bar_chart(write,x="Kata",y="Jumlah")
    except :
        st.text('')

def countstringuser(hasilstemuser):
    datasama = {}
    kata = []
    jumlah=[]
    for i in set(hasilstemuser) :
        datasama[i] = hasilstemuser.count(i)
        kata.append(i)
        jumlah.append(datasama[i])

    global jumlahuser
    jumlahuser = jumlah

def hitungsama(hasilstem,hasilstemuser):
    datasama = {}
    kata = []
    jumlah=[]
    global hasilhitung
    for a in hasilstem :
        for i in set(a):
            datasama[i] = a.count(i)
            kata.append(i)
            jumlah.append(datasama[i])

            hasil_data = {
                'Jumlah': jumlah,
                'Kata': kata
            }
            write = pd.DataFrame(hasil_data)
        for c in hasilstemuser :
            global jumlahdata
            df = write[write['Kata'] == c].values
            if len(df) == 0 :
                jumlahdata.append(0)
            else :
                symbols = "!\"#$%&*+-/:;<=>?@[\]^_`{|}~[]\n"
                for i in symbols:
                    # print(sentence)
                    df = np.char.replace(str(df), i, '')
                df = re.findall(r'\d+', str(df))
                df = list(map(int, df))
                jumlahdata = jumlahdata + df
        kata.clear()
        jumlah.clear()
        datasama.clear()

def tfidf(hasilstem2,hasilstemuser,jumlahuser):
    global hasiltfidf
    dump=[]
    try :
        tfidfvectorizer = TfidfVectorizer()
        tfidf_wm = tfidfvectorizer.fit_transform(hasilstem2)
        tfidf_tokens = tfidfvectorizer.get_feature_names_out()
        df_tfidfvect = pd.DataFrame(data=tfidf_wm.toarray(), columns=tfidf_tokens)
        tfidf_user = tfidfvectorizer.fit_transform(hasilstemuser)
        tfidf_tokens_user = tfidfvectorizer.get_feature_names_out()
        df_user = pd.DataFrame(data=tfidf_user.toarray(), columns=tfidf_tokens_user)
        col1,col2 = st.columns(2)
        with col1 :
            st.write('Pembobotan TF - IDF (Keseluruhan)')
            st.write(df_tfidfvect)
        with col2 :
            st.write('Pembobotan TF - IDF (User)')
            st.write(df_user)
        try :
            for a in range(len(df_tfidfvect.index)):
                for i in hasilstemuser :
                    dump.append(df_tfidfvect.iloc[a][i])
            for i in range(0, len(dump), len(jumlahuser)):
                hasiltfidf.append(dump[i:i + len(jumlahuser)])
        except :
            hasiltfidf = []
    except:
        hasiltfidf = []

def euclidean(hasiltfidf,jumlahuser,path):
    st.write('Nilai Pembobotan TF - IDF')
    st.text(hasiltfidf)
    try :
        count = 0
        for i in os.listdir(path):
            # check if current path is a file
            if os.path.isfile(os.path.join(path, i)):
                count += 1
        global jarak
        try :
            for i in hasiltfidf :
                hasil = math.dist(jumlahuser,i)
                jarak.append(hasil)
        except :
                st.text('')
                jarak = []
    except :
        st.text('')

def cekfile(jarak,path,query):
    try :
        count = 0
        for i in os.listdir(path):
            # check if current path is a file
            if os.path.isfile(os.path.join(path, i)):
                count += 1
        if not jarak :
            with st.expander("**Rujukan File Dari Hasil Euclidean Distance**"):
                st.write("**Tidak Ada File Yang Menyerupai Query **")
        else :
            terkecil = jarak.index(min(jarak))
            os.chdir(path)
            files = os.listdir()
            with st.expander("**Rujukan File Dari Hasil Euclidean Distance**") :
                st.write("Mungkin dengan query yang dimasukkan "
                         "adalah **"+str(query)+"** , File yang dimaksud "
                         "adalah **"+str(files[terkecil])+"**" + " Dengan Jumlah Euclidean Distance : **"+str(min(jarak))+"**")
                st.write("**(Total Perhitungan Euclidean Distance Lainnya : "
                         + str(jarak) + ")**")
    except :
        st.text('')

#proses utama program
def default_page():
    uploadfiles()
    with st.expander("**Stemming Text**"):
            steeming(datauji)
            steeming2(datauji)
    steeminguser(inputuser)
    st.markdown("""---""")
    with st.expander("**Jumlah Kemunculan Setiap Kata**"):
        countstring(hasilstem,path)
    countstringuser(hasilstemuser)
    hitungsama(hasilstem, hasilstemuser)
    tfidf(hasilstem2, hasilstemuser, jumlahuser)
    euclidean(hasiltfidf,jumlahuser,path)
    st.text('')
    st.markdown("""---""")
    cekfile(jarak,path,query)

st.markdown("<h1 style='text-align: center; color: black;'>Sistem Information Retrieval</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Maleakhi E - Nicolaus B - Agni P</h2>", unsafe_allow_html=True)
st.markdown("""---""")
st.header('')
default_page()


