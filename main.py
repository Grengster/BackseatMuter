from pynput.keyboard import Listener
from pycaw.pycaw import AudioUtilities
import time
import os    

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
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "RiotClientServices.exe":
            global toggleMute
            volume.SetMute(toggleMute, None)
            toggleMute = not toggleMute

def changeSettings():
    global listener, keybind, inSettings
    inSettings = True
    os.system('clear')
    print("SETTINGS MENU")
    while inSettings:
        tempval = input("To change the keybind, press 1\nTo return, press 2\n:")
        if tempval == "1":
            keybind = input("Enter your value: ").upper()
            print(keybind)
        if tempval == "2":
            os.system('clear')
            print("Listening for input..")
            inSettings = False

# def manualStart():
#     global listener
#     with Listener(on_press=listenMuteButton) as listener:
#         listener.join()

# Collecting events until stopped
def main():
    print("Thank you for using my backseat muter!")
    time.sleep(0.5)
    print("The program is starting any second..")
    time.sleep(1)
    print("Successfully started!")
    print("\nListening for input..")
    global listener
    with Listener(on_press=listenMuteButton) as listener:
        listener.join()

main()

# 'with' will automatically close the listener. When we stop the program the memory allocated
# to this listener won't be released. 'with' makes sure whatever happens, when an error is there
# or the program stops the memory is released. It's just a good coding principle to follow