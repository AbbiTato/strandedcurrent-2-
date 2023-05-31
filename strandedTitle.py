import pickle
import curses
import os
import keyboard
from strandedBattle import clearToLine, returnCposits, waitSpace
from strandedOverworld import overWorldLoop
import shutil

cmd = 'mode 160,40'
os.system(cmd)
curses.noecho
stdscr = curses.initscr()

def print(*strings):
    strString = ""
    for string in strings:
        strString += str(string)
    try:
        stdscr.addstr(strString)
        stdscr.addstr("\n")
        stdscr.refresh()
    except curses.error:
        pass

#gives the opening text crawl, and starts the game
def startGame(ipt):
    stdscr.clear()
    print("For years, you've been doing hard mining labor under the cruel Warden Damocles")
    waitSpace()
    print("Jailed for a crime you can't quite remember, forced to suffer countless beatings. ")
    waitSpace()
    print("But as one of your few friends is dragged away, you feel a flame of rebellion burn within you")
    waitSpace()
    print("You grab a pipe and bash your supervisor in the face, and sprint towards the mines' great sinkhole")
    waitSpace()
    print("Tossing yourself into the pit, you wonder what will happen next...")
    overWorldLoop(ipt)

#prints the title screen
print("   _____ _______ _____            _   _ _____  ______ _____")  
print("  / ____|__   __|  __ \     /\   | \ | |  __ \|  ____|  __ \\") 
print(" | (___    | |  | |__) |   /  \  |  \| | |  | | |__  | |  | |")
print("  \___ \   | |  |  _  /   / /\ \ | . ` | |  | |  __| | |  | |")
print("  ____) |  | |  | | \ \  / ____ \| |\  | |__| | |____| |__| |")
print(" |_____/   |_|  |_|  \_\/_/    \_\_| \_|_____/|______|_____/")
print("")
posits = returnCposits()
running = True
while(running):
    clearToLine(posits)
    #checks if an old or new save is being loaded
    print("Welcome to Stranded! Would you like to make a new save file or open an old one?(N: New, L: Load)") 
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'N':
        print("What would you like to name your new save?")
        print("")
        curses.echo
        ipt = stdscr.getstr().decode(encoding="utf-8")
        #a new file is made with the maps and charStats
        try:
            os.mkdir(ipt)
            shutil.copytree("maps", (str(ipt)+"\\maps"))
            print("File created!")
            running = False
        except:
            print("Something went wrong... This file may already exist")
            waitSpace()
    ##will wait til a save file has been created adequately to add loading
    elif event.event_type == keyboard.KEY_DOWN and event.name == "L":
        pass
startGame(ipt)


        
                                                                                                                  