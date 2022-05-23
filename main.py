from pynput.keyboard import Listener
from pycaw.pycaw import AudioUtilities
import time
import os    
import json

sessions = AudioUtilities.GetAllSessions()
listener = Listener
toggleMute = True
inSettings = False
keybind = "5"
letter = ""



def listenMuteButton(key):
        global letter, listener, keybind, tempval
        letter = str(key).replace("'", "").upper()
        # print(letter)
        if not inSettings: #ADD os.system(‘CLS’) AND MAKE DISPLAY IF VALORANT MUTED/ADD CONFIG FOR MUTE TO SAVE VARIABLE
            if letter == keybind:
                muteValorant()
            if letter == "KEY.F10":
                tempval = letter
                changeSettings()
        if inSettings:
            tempval = letter
        if letter == "KEY.ESC":
            print("Escaping program..")
            if not toggleMute:
                muteValorant()
            return False
        
def muteValorant():
    isRunning = False
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "RiotClientServices.exe":
            global toggleMute, keybind
            volume.SetMute(toggleMute, None)
            config = {"keybind": keybind, "isMuted": toggleMute}
            toggleMute = not toggleMute
            isRunning = True
            with open('settings.json', 'w') as f:
                json.dump(config, f)
    if not isRunning:
        print("Valorant not running, please start the game!")

def changeSettings():
    global listener, keybind, inSettings, tempval, toggleMute
    inSettings = True
    os.system('CLS')
    print("SETTINGS MENU")
    while inSettings:
        tempval = input("To change the keybind, press 1\nTo return, press 2\n:")
        if tempval == "1":
            keybind = input("New keybind: ").upper()
            print("Keybind successfully set to " + keybind)
            config = {"keybind": keybind, "isMuted": toggleMute}
            with open('settings.json', 'w') as f:
                json.dump(config, f)
        if tempval == "2":
            os.system('CLS')
            mainText()
            tempval = "";
            inSettings = False

def mainText():
    global keybind
    print("Backseat Muter is currently running in the background.")
    time.sleep(0.5)
    print("\n---------------------------------")
    print("| Escape - Quit | F10 - Settings |")
    print("---------------------------------\n")

    time.sleep(0.5)
    print("Your current bind is: " + keybind)
    time.sleep(0.5)

    print("\nListening for input.. ")




# def manualStart():
#     global listener
#     with Listener(on_press=listenMuteButton) as listener:
#         listener.join()

# Collecting events until stopped
def main():
    global keybind, toggleMute
    with open('settings.json', 'r') as f:
        config = json.load(f)

    #edit the data
    keybind = config['keybind']
    toggleMute = config['isMuted']

    print("-------------------------------------")
    print("Thank you for using my backseat muter!")
    print("-------------------------------------")
    time.sleep(0.5)
    print("The program is starting any second..")
    time.sleep(1)
    print("Successfully started!")
    if toggleMute:
        print("It was detected that the valorant voice chat is already muted!")
    mainText()
    global listener
    with Listener(on_press=listenMuteButton) as listener:
        listener.join()

main()

# 'with' will automatically close the listener. When we stop the program the memory allocated
# to this listener won't be released. 'with' makes sure whatever happens, when an error is there
# or the program stops the memory is released. It's just a good coding principle to follow