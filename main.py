import speech_recognition as sr
import numpy as n
import os
import webbrowser
import datetime
import pyttsx3
import pyaudio
import wikipedia
import pyjokes
import requests
import json
import openai
import random


apikey = "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"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 

def speak_text(audio):
    engine.say(audio)
    engine.runAndWait()
    
    

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"boss: {query}\n EDDY: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
  
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
   
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('AI')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')

def takecommand():
    r = sr.Recognizer()
    while True:
     with sr.Microphone() as source:
          r.pause_threshold = 0.6
          audio = r.listen(source)
          try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query
          except Exception as e:
            print(f"Error: {e}")
            print("Say that again, please...")
            return "Some Error Occurred. Sorry from EDDY"
        
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
     speak_text("Good Morning!")

    elif hour>=12 and hour<18:
        speak_text("Good Afternoon!")   

    else:
        speak_text("Good Evening!")  

    speak_text("I am EDDY. how may I help you")  

if __name__ == '__main__':
    print('Welcome')
    wishMe()
    while True:
        print("Listening...")
        query = takecommand()
        sites = [["youtube", "https://www.youtube.com"], 
                 ["wikipedia", "https://www.wikipedia.com"], 
                 ["google", "https://www.google.com"],
                 ["Meet","https://meet.google.com"],
                 ["Instagram","https://www.instagram.com"]
                 ]
        for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                 speak_text(f"Opening {site[0]} sir...")
                 webbrowser.open(site[1])
       
        if 'play music' in query:                      # command for music...
            music_dir = 'D:\\songs\\new music'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            speak_text(f"Sir time is {hour} hours {min} minutes")
       
        elif 'news' in query:                        # command for today's news...
            speak_text("news...")
            url= "https://newsapi.org/v2/top-headlines?country=in&apiKey=255b9b624edd43aa847bdc63095d4892"
            news=requests.get(url).text
            news_arti=json.loads(news)
            arts=news_arti['articles']                         
            for article in arts:
                speak_text(article['title'])
                speak_text("moving to next news...")
            speak_text("That's all Thank You..")
        
        # elif "open pass" in query:
        #     os.system(f"open /Applications/Passky.app")

        elif "Using AI" in query.lower():
            ai(prompt=query)

        elif 'joke' in query:                        # command for jokes...
            speak_text(pyjokes.get_joke()) 
        
        elif 'love' in query:
            speak_text("Sorry, I have a Boyfriend.") 
        
        elif "reset chat"in query:
                chatStr = ""   
            
        elif "stop" in query:
            speak_text("bye bye ,BOSS.")
            print("THANK YOU...") 
            exit()
    
        elif "sleep" in query:
            speak_text("BYE BYE ,BOSS.")
            print("THANK YOU...") 
            exit()
            
    