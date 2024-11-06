# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 13:11:53 2022

@author: omer.adiguzel
"""
from selenium import webdriver
from message import Messenger
from login import MainWpPage
import time
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))



nameList=[]  
stateKeeper = {}
df = pd.DataFrame(columns = ['ID',  'IN_MESSAGE' , 'IN_MESSAGE_TIME' ,'OUT_MESSAGE' , 'OUT_MESSAGE_TIME'])

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res



def openWpWeb():
    
    chrom_options = webdriver.ChromeOptions()
    chrom_options.add_argument(
    "user-data-dir=C:\\Users\\INTOME~1.ADI\\AppData\\Local\\Temp\\scoped_dir16956_1688294984\\Default\\Default\\Default")

    driver = webdriver.Chrome(executable_path=r"C:/Users/omer.adiguzel/Desktop/wpBot/chromedriver.exe", options = chrom_options)
    driver.maximize_window()
    
    return driver

        

def mainWpPage(driver):
    
    mainPage = MainWpPage(driver)
    mainPage.load()
    return mainPage

def removizer(raw_opened_chats , raw_contact_list):
    opened_chats = []
    contact_list = []

    for index,data in enumerate(raw_contact_list):
        if data[2] or data[0] in nameList:
            opened_chats.append(raw_opened_chats[index])
            contact_list.append(raw_contact_list[index])
            
    return opened_chats , contact_list


def getChats(mainPage):
    
    raw_contact_list = []
    raw_opened_chats = []
   
    while len(raw_opened_chats)<1:
        time.sleep(5)
        raw_opened_chats = mainPage.openedChats()
        for oc in raw_opened_chats:
        
            name = mainPage.name(oc)  
            last_msg_time = mainPage.last_message_time(oc)
            has_notif = mainPage.has_notifications(oc)  
            count_notif = mainPage.notifications(oc) 
            
            raw_contact_list.append([name,last_msg_time,has_notif,count_notif])
        
        
        opened_chats , contact_list = removizer(raw_opened_chats , raw_contact_list)
        return opened_chats , contact_list  


def chatter(opened_chats,contact_list,mainPage,msg):
        for index,data in enumerate(contact_list):
            if data[2]:    
                mainPage.click(opened_chats[index])
                recievedMsg = msg.read_last_message(who = 'in', count = data[3])
                Tr2Eng = str.maketrans("çğıöşü", "cgiosu")
                recievedMsg = recievedMsg.translate(Tr2Eng)
                print(recievedMsg)
                res = chatbot_response(recievedMsg)        
                msg.send_message(res)



driver = openWpWeb()
mainPage = mainWpPage(driver)
msg = Messenger(driver)    

while True:
    
    opened_chats , contact_list = getChats(mainPage)  
    chatter(opened_chats, contact_list, mainPage, msg)
    time.sleep(1)
    driver.refresh()
    time.sleep(5)


















