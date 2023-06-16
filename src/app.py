import eel
import os
from queue import Queue
from threading import Thread
import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller 


class ChatBot:

    today = date.today()
    r = sr.Recognizer()
    keyboard = Controller()
    engine = pyttsx3.init('sapi5')
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # ----------------Variables------------------------
    file_exp_status = False
    files =[]
    path = ''
    is_awake = True  #Bot status


    started = False
    userinputQueue = Queue()

    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    def popUserInput():
        return ChatBot.userinputQueue.get()
        print(len(userinputQueue))

    def close_callback(route, websockets):
        # if not websockets:
        #     print('Bye!')
        exit()

    @eel.expose
    def getUserInput(msg):
        ChatBot.userinputQueue.put(msg)
        print("added to queue", msg)
    
    def close():
        ChatBot.started = False
    
    def addUserMsg(msg):
        userinputQueue.put(msg)
        eel.addUserMsg(msg+"from app")
    
    def addAppMsg(msg):
        eel.addAppMsg(msg)

    # ------------------Functions----------------------
    def reply(audio):
        app.ChatBot.addAppMsg(audio)
        print(audio)
        engine.say(audio)
        engine.runAndWait()


    def wish():
        hour = int(datetime.datetime.now().hour)

        if hour>=0 and hour<12:
            reply("Good Morning!")
        elif hour>=12 and hour<18:
            reply("Good Afternoon!")   
        else:
            reply("Good Evening!")  
            
        reply("I am Jarvis, how may I help you?")


    # Set Microphone parameters
    with sr.Microphone() as source:
            r.energy_threshold = 300 
            r.dynamic_energy_threshold = False

    # Audio to String
    def record_audio():
        with sr.Microphone() as source:
            r.pause_threshold = 0.8
            voice_data = ''
            audio = r.listen(source, phrase_time_limit=5)

            try:
                voice_data = r.recognize_google(audio)
            except sr.RequestError:
                reply('Sorry my Service is down. Plz check your Internet connection')
            except sr.UnknownValueError:
                print('cant recognize')
                pass
            return voice_data.lower()


    def respond(voice_data):
        global file_exp_status, files, is_awake, path
        print(voice_data)
        voice_data.replace('jarvis','')
        app.ChatBot.addAppMsg(audio)

        if is_awake==False:
            if 'wake up' in voice_data:
                is_awake = True
                wish()

        # STATIC CONTROLS
        elif 'hello' in voice_data:
            wish()


        elif 'start voice assistant' in voice_data:
            reply("Voice Assistant Started")

        elif 'stop voice assistant' in voice_data:
            reply("Voice Assistant Stopped")

        elif 'what is your name' in voice_data:
            reply('My name is Jarvis!')

        elif 'date' in voice_data:
            reply(today.strftime("%B %d, %Y"))

        elif 'time' in voice_data:
            reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

        elif 'search' in voice_data:
            reply('Searching for ' + voice_data.split('search')[1])
            url = 'https://google.com/search?q=' + voice_data.split('search')[1]
            try:
                webbrowser.get().open(url)
                reply('This is what I found Sir')
            except:
                reply('Please check your Internet')

        elif 'location' in voice_data:
            reply('Which place are you looking for ?')
            temp_audio = record_audio()
            app.eel.addUserMsg(temp_audio)
            reply('Locating...')
            url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
            try:
                webbrowser.get().open(url)
                reply('This is what I found Sir')
            except:
                reply('Please check your Internet')

        elif ('bye' in voice_data) or ('by' in voice_data):
            reply("Good bye Sir! Have a nice day.")
            is_awake = False

        elif ('exit' in voice_data) or ('terminate' in voice_data):
            if Gesture_Controller.GestureController.gc_mode:
                Gesture_Controller.GestureController.gc_mode = 0
            app.ChatBot.close()
            #sys.exit() always raises SystemExit, Handle it in main loop
            sys.exit()
            
        
        # DYNAMIC CONTROLS
        elif 'launch gesture recognition' in voice_data:
            if Gesture_Controller.GestureController.gc_mode:
                reply('Gesture recognition is already active')
            else:
                gc = Gesture_Controller.GestureController()
                t = Thread(target = gc.start)
                t.start()
                reply('Launched Successfully')

        elif ('stop gesture recognition' in voice_data) or ('top gesture recognition' in voice_data):
            if Gesture_Controller.GestureController.gc_mode:
                Gesture_Controller.GestureController.gc_mode = 0
                reply('Gesture recognition stopped')
            else:
                reply('Gesture recognition is already inactive')
            
        elif 'copy' in voice_data:
            with keyboard.pressed(Key.ctrl):
                keyboard.press('c')
                keyboard.release('c')
            reply('Copied')
            
        elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
            with keyboard.pressed(Key.ctrl):
                keyboard.press('v')
                keyboard.release('v')
            reply('Pasted')
            
        # File Navigation (Default Folder set to C://)
        elif 'list' in voice_data:
            counter = 0
            path = 'C://'
            files = listdir(path)
            filestr = ""
            for f in files:
                counter+=1
                print(str(counter) + ':  ' + f)
                filestr += str(counter) + ':  ' + f + '<br>'
            file_exp_status = True
            reply('These are the files in your root directory')
            app.ChatBot.addAppMsg(audio)

            
        elif file_exp_status == True:
            counter = 0   
            if 'open' in voice_data:
                if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                    os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                    file_exp_status = False
                else:
                    try:
                        path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                        files = listdir(path)
                        filestr = ""
                        for f in files:
                            counter+=1
                            filestr += str(counter) + ':  ' + f + '<br>'
                            print(str(counter) + ':  ' + f)
                        reply('Opened Successfully')
                        app.ChatBot.addAppMsg(audio)
                        
                    except:
                        reply('You do not have permission to access this folder')
                                        
            if 'back' in voice_data:
                filestr = ""
                if path == 'C://':
                    reply('Sorry, this is the root directory')
                else:
                    a = path.split('//')[:-2]
                    path = '//'.join(a)
                    path += '//'
                    files = listdir(path)
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('ok')
                    app.ChatBot.addAppMsg(audio)       
        else: 
            reply('I am not functioned to do this !')


    # ------------------Driver Code--------------------
    # t1=Thread(target = app.ChatBot.start)
    # t1.start()



    def voice_assistant():

        # window.mainloop()
        # reply("hello")
        # reply("Listening")
        voice_data = None
        while True:        
            voice_data = record_audio()
            if "jarvis" in voice_data:
                try:
                    #Handle sys.exit()
                    print("calling function with", voice_data)
                    respond(voice_data)
                except SystemExit:
                    reply("Exit Successfull")
                    break
                except:
                    #some other exception got raised
                    print("EXCEPTION raised while closing.") 
                    break
            print(voice_data)
        

    
            


    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        eel.init(path + r'\web', allowed_extensions=['.js', '.html'])
        try:
            eel.start('index.html', mode='chrome',
                                    host='localhost',
                                    port=27005,
                                    block=False,
                                    size=(1920, 1080),
                                    position=(10,100),
                                    disable_cache=True,
                                    close_callback=ChatBot.close_callback,
                                    cmdline_args=['--kiosk'])
            ChatBot.started = True
            while ChatBot.started:
                try:
                    eel.sleep(5.0)
                except:
                    #main thread exited
                    break
        
        except:
            pass





# app = ChatBot()

# t1 = Thread(target = app.start)
# t1.start()