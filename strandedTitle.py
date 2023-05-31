import pickle
import curses
import os
import keyboard
from strandedBattle import clearToLine, returnCposits, waitSpace
from strandedOverworld import overWorldLoop
import shutil

cmd = 'mode 160,40'
os.system(cmd)
stdscr = curses.initscr()
curses.echo()
curses.nocbreak()
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
def loadPlayerData(FileName):
    pLst = []
    with open((FileName+'/pMember1.pkl'), 'rb') as inp:
        pLst.append(pickle.load(inp))
    try:
        with open((FileName+'/pMember2.pkl'), 'rb') as inp:
            pLst.append(pickle.load(inp))
    except:
        pass
    try:
        with open((FileName+'/pMember3.pkl'), 'rb') as inp:
            pLst.append(pickle.load(inp))
    except:
        pass
    try:
        with open((FileName+'/pMember4.pkl'), 'rb') as inp:
            pLst.append(pickle.load(inp))
    except:
        pass
    with open((FileName+'/locatData.txt'), 'rt') as inp:
        mcpositx = int(inp.readline().strip("\n"))
        mcposity = int(inp.readline().strip("\n"))
        mapName = inp.readline().strip("\n")
    return pLst, mcpositx, mcposity, mapName

        
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
    print("Welcome to Stranded! Would you like to make a new save file or open an old one?(n: New, l: Load)") 
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'n':
        print("What would you like to name your new save?")
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
    elif event.event_type == keyboard.KEY_DOWN and event.name == "l":
        print("What is the name of your file?")
        ipt = stdscr.getstr().decode(encoding="utf-8")
        if os.path.exists(ipt) == True:
            pData = loadPlayerData(ipt)
            overWorldLoop(ipt, pData[0], pData[1], pData[2], pData[3], False)
            waitSpace()
        else:
            print("Something went wrong... This file may not exist")
            waitSpace()
startGame(ipt)




        
                                                                                                                  