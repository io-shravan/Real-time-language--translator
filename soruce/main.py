import os
import time
import pygame
from gtts import gTTS
import streamlit as st
st.markdown(
    """
    <style>
        .stApp {
            background: url("https://plus.unsplash.com/premium_photo-1661963515041-661b417c0b45?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center fixed;
            background-size: cover;
        }
    </style>
    """,
    unsafe_allow_html=True
)


import speech_recognition as sr
from googletrans import LANGUAGES, Translator

isTranslateOn = False

translator = Translator() # Initialize the translator module.
pygame.mixer.init()  # Initialize the mixer module.

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src='{}'.format(from_language), dest='{}'.format(to_language))

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang='{}'.format(to_language), slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")  # Load a sound.
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    
    global isTranslateOn
    
    while isTranslateOn:

        rec = sr.Recognizer()
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
        try:
            output_placeholder.markdown(
    """
    <div style="text-align: center;">
        <p>Processing...</p>
        <div class="loader"></div>
    </div>
    <style>
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

            spoken_text = rec.recognize_google(audio, language='{}'.format(from_language))
            
            output_placeholder.text("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)

            text_to_voice(translated_text.text, to_language)
    
        except Exception as e:
            print(e)

# UI layout
st.title("Language Translator")


# Dropdowns for selecting languages
from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Button to trigger translation
start_button = st.button("🎤 Speak Now")

stop_button = st.button("Stop")

# Check if "Start" button is clicked
if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        output_placeholder = st.empty()
        main_process(output_placeholder, from_language, to_language)

# Check if "Stop" button is clicked
if stop_button:
    isTranslateOn = False
st.markdown(
    """
     <style>
        .footer {
            position: fixed;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 15px;
            font-family: 'Arial', sans-serif;
            color: #BBBBBB;
            opacity: 0.7;
            text-align: center;
        }
    </style>
    <div class="footer">
        Project by Shravan and Sanjay  
    </div>
    """,
    unsafe_allow_html=True
)
