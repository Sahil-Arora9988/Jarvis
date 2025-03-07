from time import strftime

import speech_recognition as sr
import os
import win32com.client
import pyttsx3
import webbrowser
from openai import OpenAI
from pyexpat.errors import messages

from config import apikey
import datetime

chatStr = []
def chat(query):
    global chatStr
    # print(chatStr)

    client = OpenAI(api_key=apikey)

    # Append user message correctly
    chatStr.append({"role": "user", "content": f"Sahil: {query}"})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract AI response
    ai_response = response.choices[0].message.content

    # Append AI response correctly
    chatStr.append({"role": "assistant", "content": ai_response})

    say(ai_response)
    return ai_response

def ai(prompt):
    client = OpenAI(api_key=apikey)
    text = f"OpenAI response for prompt: {''.join(prompt.split('intelligence')[1:]).strip() } \n *****************\n\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
        {"role": "user", "content": prompt}
    ],
        response_format={
            "type": "text"
        },
        temperature=1,
        max_completion_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


    # print(response.choices[0].message.content)
    text += response.choices[0].message.content

    if not os.path.exists("OpenAI"):
        os.mkdir("OpenAI")

    with open (f"OpenAI/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio,language="en-in" )
            print(f"User Said: {query}")
            return query
        except Exception as e:
            return "Some error occurred. Sorry From Jarvis"

if __name__ == '__main__':
    print('PyCharm')
    say("Hey I am Jarvis")
    while True:
        print("Listening....")
        query = takeCommand()
        sites = [["youtube","https://www.youtube.com/"],["wikipedia","https://www.wikipedia.com/"],["instagram","https://www.instagram.com/"],["google","https://www.google.com/"]]
        for site in sites:
            if  f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath ="c:/Users/Device/Downloads/Afsos - Anuv Jain.mp3"
            os.startfile(musicPath)

        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H,%M,%S")
            say(f"The Time is {strfTime}")

        elif "Using Artificial intelligence".lower() in query.lower():
            ai(prompt=query)


        elif "Jarvis Quit".lower() in query.lower():
            exit()

        else:
            print("Chatting....")
            chat(query)

        #say(query)
