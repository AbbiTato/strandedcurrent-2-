import keyboard
import curses
import random
from random import randint, shuffle
import csv 
import os
import sqlite3
from time import sleep
from playsound import playsound

#initialises the screen and curses data
cmd = 'mode 160,40'
os.system(cmd)
stdscr = curses.initscr()

#makes a sound if the player has sounds turned on
def soundMade(path):
    global sound
    try:    
        if sound == True:
            playsound(path)
    except:
        pass

#print stitches together all the kwargs, and turns them into strings to get rid of type errors
def print(*strings):
    strString = ""
    for string in strings:
        strString += str(string)
    #this try/except format is needed for curses to correctly add. I have no clue why
    try:
        stdscr.addstr(strString)
        stdscr.addstr("\n")
        stdscr.refresh()
    except curses.error:
        pass

#a very handy method that checks for the player's input on a 1d menu each time it's run. Saves a lot of repeat code
def getMenuChoice(cOption, optionsCount):
    event = keyboard.read_event()
    #the two directions simply return cOption +-1, and loop around if above/below limits
    if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
        soundMade("sfx/menuMove.wav")
        cOption += 1
        if cOption > optionsCount -1:
            cOption = 0
        return cOption
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
        soundMade("sfx/menuMove.wav")
        cOption -= 1
        if cOption <0:
                cOption = optionsCount -1
        return cOption
    #-1 and -2 are used for back and forward. Used to use True and False but since 1 and 0 are Truthy and Falsey it caused errors
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'x':
        soundMade("sfx/menuMove.wav")
        return -1
    elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
        soundMade("sfx/menuMove.wav")
        return -2
    #since the function is run continually as part of a loop, it needs to sometimes just return the given value
    else:
        return cOption

#one of the largest classes. Contains data on everything relevant to the battle
class combattant:
    def __init__(self, sprID, Name, HP, cHP, MP, cMP, ATK, DEF, mATK, HIT, DODGE, CRIT):
        self._sprID = sprID
        self._Name = Name
        self._HP = HP
        self._MP = MP 
        self._ATK = ATK
        self._DEF = DEF
        self._mATK = mATK
        self._HIT = HIT
        self._DODGE = DODGE
        self._CRIT = CRIT
        self._cHP = cHP
        self._cMP = cMP
    
    def boundStats(self):
        if self._ATK < 1:
            self._ATK = 1 
        if self._DEF < 1:
            self._ATK = 1 
        if self._mATK < 1:
            self._ATK = 1 

    def getName(self):
        return self._Name

    def getHP(self):
        return self._HP
    
    def getcHP(self):
        return self._cHP
    
    def changecHP(self, damage):
        self._cHP += damage
        if self._cHP > self._HP:
            self._cHP = self._HP
    
    def getcMP(self):
        return self._cMP
    
    def getMP(self):
        return self._MP

    def getATK(self):
        return self._ATK
    
    def getDEF(self):
        return self._DEF
    
    def getmATK(self):
        return self._mATK
    
    def getDODGE(self):
        return self._DODGE
    
    def multATK(self, pcent):
        change = int(self._ATK * pcent)
        if change < 1:
            change = 1
        self._ATK += change
        return (change)

    def multDEF(self, pcent):
        change = int(self._DEF * pcent)
        if change < 1:
            change = 1
        self._DEF += change
        return (change)
    
    def multmATK(self, pcent):
        change = int(self._mATK * pcent)
        if change < 1:
            change = 1
        self._mATK += change
        return (change)
    
    def multDEX(self, pcent):
        change = int(self._HIT * pcent)
        if change < 1:
            change = 1
        self._HIT += change
        change = int(self._DODGE * pcent)
        if change < 1:
            change = 1
        self._DODGE += change
        change = int(self._CRIT * pcent)
        if change < 1:
            change = 1
        self._CRIT += change
        return "some"
    
    def getcHP(self):
        return self._cHP
    
    def setcHP(self, value):
        self.cHP = value
    
    def getcMP(self):
        return self._cMP

    def losecMP(self, value):
        self._cMP -= value
        
    

    

    #takeDamage only needs the attack of the attacker and whether it was a crit, then everything else relevant is already here
    def takeDamage(self, eATK, crit):
        #damage is minimum 1 so we use a max function to ensure
        dtotal = int(max((eATK - (self._DEF/2), 1)))
        if crit == True:
            soundMade("sfx/crit.wav")
            dtotal = max((eATK * 2), 2)
        else:
            soundMade("sfx/attack.wav")
        print(self._Name+ " took "+  str(dtotal)+ " points of damage!")
        waitSpace()
        self._cHP -= (dtotal)
        #if the character dies, it is printed
        if(self._cHP <= 0):
            print(self._Name + " has died!")
        waitSpace()

    #returns the sprite. Used several times
    def returnspr(self, lst):
        isnum = False
        sprArray = []
        for i in range(len(lst)):
            if(lst[i] == str(self._sprID+1)+"\n"):
                break   
            if(isnum == True):
                sprArray.append(lst[i])
            if(lst[i] == str(self._sprID)+"\n"):
                isnum = True  
        return sprArray

    #crit is a simple roll below the player's crit stat 
    def critCheck(self, type):
        lCRIT = self._CRIT
        #spells have halved crit chance due to their higher base damage
        if type == "SPELL":
            lCRIT = int((lCRIT / 2))
        if (randint(1,20) < self._CRIT):
            print("Critical Hit!")
            return True
        else:
            return False
    
    #the character's basic attack. deals with hit%, enemy dodge% and crit%
    def attack(self, target):
        print(self._Name +" attacked!")
        hitChance = self._HIT - target.getDODGE()
        if (hitChance > randint(1, 20)):
            target.takeDamage((self._ATK - target.getDEF()), self.critCheck("Melee"))
        else:
            print("But ", target.getName(), " dodged the attack!")
        waitSpace()
    
    def isDed(self):
        if self._cHP <=0:
            return True
        else:
            return False

#enemy gets all it's data from the enemyData.csv file
class enemy(combattant):
    def __init__(self, enemID):
        con = sqlite3.connect("strandedData.db")
        cur = con.cursor()
        enemData = cur.execute("SELECT sprID, entID, entName, HP, MP, STR, RES, ITL, CHA, DEX FROM entData WHERE entID ="+str(enemID)).fetchall()[0]
        self._sprID = enemData[0]
        self._entID = enemData[1]
        self._Name = enemData[2]
        self._HP = enemData[3]
        self._cHP = enemData[3]
        self._MP = enemData[4]
        self._cMP = enemData[4]
        self._ATK = enemData[5]
        self._DEF = enemData[6]
        self._mATK = enemData[7]
        self._CHA = enemData[8]
        self._HIT = 70 + 2*int(enemData[9]/5)
        self._DODGE = 2*int(enemData[9]/5)
        self._CRIT = 2*int(enemData[9]/5)
        self._EXPYield = int((self._MP+self._mATK+self._ATK+enemData[9]) / 4)
        self._bYield = int((self._HP + self._DEF + self._CHA) / 2)
        self._demand = self._CHA
        if self._ATK >= self._mATK:
            self._convType = "Carnivore"
        elif self._ATK < self._mATK:
            self._convType = "Herbivore"
        spellData = cur.execute("SELECT spellData.spellID FROM spellData INNER JOIN entSpells ON spellData.spellID = entSpells.spellID WHERE entSpells.entID ="+str(self._entID)+" AND entSpells.spellRank=1 ORDER BY entSpells.spellRank").fetchall()
        self._teachSpell = spellData[0][0]
        idLst = []
        for i in range(5):
            idLst.append(spellData[randint(0, (len(spellData)-1))][0])
        if len(spellData) == 0:
            self._aLst = []
            for i in range(8):
                self._aLst.append("Attack")
        elif self._ATK >= self._mATK:
            self._aLst = ["Attack", "Attack", "Attack", "Attack", "Attack"]
            for i in range(3):
                self._aLst.append(idLst[i])
        elif self._ATK <= self._mATK:
            self._aLst = ["Attack", "Attack", "Attack"]
            for i in range(5):
                self._aLst.append(idLst[i])
        cur.close()
    
    def getentID(self):
        return self._entID

    def getCHA(self):
        return self._CHA
    
    def getEXPYield(self):
        return self._EXPYield
    
    def getbYield(self):
        return self._bYield
    
    def getdemand(self):
        return self._demand
    
    def setdemand(self, value):
        self._demand = value

    def getteachSpell(self):
        return self._teachSpell
    

    #selectAction chooses the enemy's action from their list of 8 possible actions       
    def selectAction(self, playerLst, enemLst):   
        ppresentLst = []  
        epresentLst = []
        #first a list of the alive players and alive enemies is made             
        for i in range(len(playerLst)):
            if playerLst[i].isDed() == False:     
                ppresentLst.append(playerLst[i])
        for i in range(len(enemLst)):
            if enemLst[i].isDed() == False:            
                epresentLst.append(enemLst[i])
        #act is decided on randomly as is the target of the move         
        act = self._aLst[randint(0, 7)]
        etarg = epresentLst[randint(0, len(epresentLst)-1)]      
        ptarg = ppresentLst[randint(0, len(ppresentLst)-1)]                              

        if act == "Attack":                     
            self.attack(ptarg)
        else:
            #if the action is a spell, it is cast              
            a = getSpellProperties(act)
            self._cMP-=a[1]
            if a[6] == "enemOne":
                cast(a, self, ptarg)                  
            elif a[6] == "enemAll":
                for i in range(len(ppresentLst)):
                    cast(a, self, ppresentLst[i])
            elif a[6] == "partyOne":
                cast(a, self, etarg)
            elif a[6] == "partyAll":
                for i in range(len(epresentLst)):
                    cast(a, self, epresentLst[i])
    
    #each enemy has a unique conversation loaded from the file talkData
    def loadConvo(self):
        string = "talkData\\"+self._Name+".csv"
        finalLst = []
        f = open(string)
        g = csv.DictReader(f)
        for line in g:
            finalLst.append(line)
        f.close()
        return finalLst




#allies inherit their properties from combattant and use a constructor to be made so they can be transferred from the Overworld
class ally(combattant):
    def __init__(self, _sprID, _Name, _HP, _cHP, _MP, _cMP, _ATK, _DEF, _mATK, _HIT, _DODGE, _CRIT, _Level, _CHA, _spellList = [], _bCount = -1, _sCount = -1):
        super().__init__(_sprID, _Name, _HP, _cHP, _MP, _cMP, _ATK, _DEF, _mATK, _HIT, _DODGE, _CRIT)
        self._spellList = _spellList
        self._Level = int(_Level)
        self._CHA = _CHA
        if _bCount!=-1:
            self._bCount = _bCount
            self._sCount = _sCount
    #this function is only needed for the player. lets the player forget a spell if they already know 8 
    def learnSpell(self, spell):
        if (spell in self.spellList):
            print("You already know that spell...")
            waitSpace()
        else:
            if len(self.spellList) <8:
                self.spellList.append(spell)
                print("You learned ", spell)
            else:
                print("You can't learn any more spells! Which spell would you like to forget?")
                running = True
                cOption = 0
                cPosits = returnCposits()
                nineLst = self.spellList
                nineLst.append(spell)
                while(running):
                    clearToLine(cPosits)
                    for i in range(len(nineLst)):
                        cString = " "
                        if i == cOption:
                            cString = ">"
                        cString+=nineLst[i]
                        print(cString)
                    choice = getMenuChoice(cOption, len(nineLst))
                    if choice == -2:
                        nineLst.pop(cOption)
                        self.spellList = nineLst
                    else:
                        cOption = choice
    def getCHA(self):
        return self._CHA
    def getLevel(self):
        return self._Level
    def getspellList(self):
        return self._spellList
    def getsCount(self):
        return self._sCount
    def getbCount(self):
        return self._bCount
    def changesCount(self, value):
        self._sCount +=value
    def changebCount(self, value):
        self._bCount += value
        




#cuts down on a line of code in certain places when making submenus
def returnCposits():
    print("")
    return stdscr.getyx()     
    
#returns a HP bar with the HP as a number if it's an ally   
def returnHPstring(ent, ally = True):
    a = ent.getcHP()/ent.getHP() * 10
    a = round(a)
    if ally == True:
        hpstring = "HP: "+str(ent.getcHP())+ "/"+str(ent.getHP())+ ":  ["
    else:
        hpstring="HP:        ["
    for i in range(10):
        if (a>0):
            hpstring+="I"
            a-=1
        else:
            hpstring+=" "
    hpstring+= "]       "
    return hpstring

#runs the previous method multiple times to put all of a team's data on a line
def HPstringonline(entLst, ally):
    online  = ""
    spaces = 30
    for i in range(len(entLst)):
        if(entLst[i].isDed() == False):
            online += returnHPstring(entLst[i], ally)
        else:
            online+=" " * spaces
    return online

#writes a team's name on a line
def namesonline(entLst):
    online  = ""
    spaces = 30
    for i in range(len(entLst)):
        if(entLst[i].isDed() == False):
            online += entLst[i].getName() + (" " * (spaces - len(entLst[i].getName())))
        else:
            online+=" " * spaces
    return online

#targetMenu chooses the target of spells, physical attacks and healing spells. entLst is generic so can be allies or enemies depending on spell type
def targetMenu(entLst):
    goBack = False
    targsLst = []
    #makes a list of all living members
    for i in range(len(entLst)):
        if (entLst[i].isDed() == False):
            targsLst.append(entLst[i])
    cOption = 0
    cposits = returnCposits()
    while(goBack == False):
        clearToLine(cposits)
        #prints the list of targets with the current selection >'d
        for i in range(len(targsLst)):      
             if(i == cOption):                        
                print(">"+targsLst[i].getName())
             else:
                print(" "+targsLst[i].getName())
        #returns the current selection if z pressed
        choice = getMenuChoice(cOption, len(entLst))
        if choice == -1:
             return False
        elif choice == -2:
            return targsLst[cOption]        
        else:
            cOption = choice          
        
#prints the player's sprites on a line, which since each is several lines ended up being complicated
def printOnLine(entLst, array, doPrint = False):
    LstLine = ""
    maxsent = 0
    gap = 30
    sprsLst = []
    #gets the sprites of every alive member and puts them in a list
    for i in range(len(entLst)):
        if (entLst[i].isDed() == False):
            a = entLst[i].returnspr(array)
            sprsLst.append(a)
            maxsent = max(maxsent, len(a))
    
    #prints the first line of every alive member's sprite
    for i in range(maxsent):
        accLocat = 0
        for j in range(len(entLst)):
            if(entLst[j].isDed()==False):
                if (i<len(sprsLst[accLocat])):
                    LstLine+=sprsLst[accLocat][i].strip("\n")
                    LstLine+= " " * (gap-len(sprsLst[accLocat][i]))
                else:
                    LstLine+= " " * (gap -1)
                accLocat+=1
            else:
                LstLine+=" " * (gap -1) 
        print(LstLine)
        printStars(doPrint)
        LstLine = ""        

#prints stars on the screen for various transitions
def printStars(doPrint):
    if doPrint == True:
        cPosity = returnCposits()[0]
        print("**********************************************************************")
        sleep(0.02)
        stdscr.move((cPosity-1), 0)


#does all of the battle print methods
def printbattletopscreen(playerLst, enemLst, a, doPrint = False):
        print(namesonline(enemLst))
        printStars(doPrint)
        printOnLine(enemLst, a, doPrint)
        print(HPstringonline(enemLst, False))
        printStars(doPrint)
        print("")
        printStars(doPrint)
        print(namesonline(playerLst))
        printStars(doPrint)
        printOnLine(playerLst, a, doPrint)
        print(HPstringonline(playerLst, True))
        printStars(doPrint)

#makes the player press the confirm button to advance dialogue
def waitSpace():
    x = True
    while (x == True):
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'z':
            x = False


#buffHandler increases or decreases target's stats        
def buffHandler(spell, target):
    if spell[4] == "cATK":
        sBonus = target.multATK(spell[3])
        sWord = "ATK"
    elif spell[4] == "cDEF":
        sBonus = target.multDEF(spell[3])
        sWord = "DEF"
    elif spell[4] == "cmATK":
        sBonus = target.multmATK(spell[3])
        sWord = "mATK"
    elif spell[4] == "cDEX":
        sBonus = target.multDEX(spell[3])
        sWord = "DEX"
    if sBonus > 0:
        word = "rose"
    else:
        word = "fell"
    sBonus = abs(sBonus)
    print(target.getName(), " 's ", sWord, " ", word, " by ", sBonus, "point(s)!")
    waitSpace()
    
#casts spells. MP has already been deducted, so all that remains is to cast the spell       
def cast(spell, caster, target):
    soundMade("sfx/spell.wav")
    #spell is cast, damage is calculated
    print(caster.getName()+ " cast "+ spell[0]+ "!")
    waitSpace()
    damage = int((spell[2] +caster.getmATK())* spell[3] - target.getCHA())
    #the spell's element determines some properties
    if(spell[4] == "HEAL"):
        target.changecHP(damage)
        print(target.getName()+ " was healed by "+ str(damage)+ " points")
        waitSpace()
    #could maybe be simplified but works
    elif spell[4] == "cATK" or spell[4] == "cDEF" or spell[4] == "cmATK" or spell[4] == "cDEX":
        buffHandler(spell, target)
    else:
        target.takeDamage(damage, caster.critCheck("Spell"))
        waitSpace()

#makes a menu of the caster's spells
def spellsMenu(caster, partyLst, enemLst):
    #exits if the casters knows 0 spells
    if len(caster.getspellList()) == 0:
        print(caster.getName()+ " doesn't know any spells!")
        waitSpace()    
        return False
    #a list of the spells' properties is made by looking them up from the dict
    spellplist = []
    goBack = False
    cOption = 0
    cposits = returnCposits()
    for i in range(len(caster.spellList)):
        spellplist.append(getSpellProperties(caster.spellList[i]))
    while(goBack == False):
        t = True
        clearToLine(cposits)
        #the spells are printed with the relevant MP cost data on the side
        for i in range(len(spellplist)):
             if(i == cOption):
                print(">"+str(spellplist[i][0])+ "["+ str(spellplist[i][1])+ "]") 
             else:
                 print(str(spellplist[i][0])+ "["+ str(spellplist[i][1])+ "]") 
        print("MP: "+str(caster.getcMP())+"/"+str(caster.getMP()))
        choice = getMenuChoice(cOption, len(caster.spellList))
        if choice==-1:
             return False
        elif choice == -2:
            #if the caster has insufficient MP, the spell is not cast and the loop continues
            if (caster.getcMP() < spellplist[cOption][1]):
                print("Not enough MP")
                waitSpace()
            #chooses the target based on the spell's proprties, then invokes cast with the relevant info passed in
            else:
                if spellplist[cOption][6] == "enemOne":
                    t = targetMenu(enemLst)
                    if t!=False:
                        caster.losecMP(spellplist[cOption][1])
                        cast(spellplist[cOption], caster, t) 
                elif spellplist[cOption][6] == "enemAll":
                    caster.losecMP(spellplist[cOption][1])
                    for i in range(len(enemLst)):
                        if enemLst[i].isDed() ==False:
                            cast(spellplist[cOption], caster, enemLst[i])
                elif spellplist[cOption][6] == "partyOne":
                    t = targetMenu(partyLst)
                    if t!=False:
                        caster.losecMP(spellplist[cOption][1])
                        cast(spellplist[cOption], caster, t)                               
                elif spellplist[cOption][6] == "partyAll":
                    caster.losecMP(spellplist[cOption][1])
                    for i in range(len(partyLst)):
                        if partyLst[i].isDed() ==False:
                                cast(spellplist[cOption], caster, partyLst[i])
                if t!=False:     
                    goBack = True         
                    return True    
        else:
            cOption = choice
    return True

                   
    
#checks if an entire side is dead or not    
def allDed(entLst):
    for i in range(len(entLst)):
        if entLst[i].isDed() == False:
            return False
    return True

#clears to a certain line, allows for submenus
def clearToLine(posits):
    stdscr.move(posits[0], posits[1])
    stdscr.clrtobot()

#to prevent the players list from desyncing when characters die, this method is used to keep parity
def getRealCurrentPlayerName(playerLst, turn):
    for i in range(len(playerLst)):
        if i == turn:
            if playerLst[i].isDed() == False:
                return playerLst[i].getName()
            else:
                turn +=1
    return "Error"


#the main loop for the battle     
def battle(playerLst, enemLst, soundState):
    global sound
    sound=soundState
    battleContinue = True
    #loads all the relevant data to this battle
    spritesDict = loadsprites()
    cOption = 1
    turn = 1
    runPower = 20
    totalEXP = 0
    totalB = 0
    printbattletopscreen(playerLst, enemLst, spritesDict, True)
    while(battleContinue):
        stdscr.clear() 
        printbattletopscreen(playerLst, enemLst, spritesDict)
        print("Current Turn: "+ str(getRealCurrentPlayerName(playerLst, (turn-1))))
        #the current options is printed. a better implementation is needed for when the options expand
        if (cOption ==1):
            print(">FIGHT   SPELL")
            print(" RUN     TALK")
        if (cOption ==2):     
            print(" FIGHT  >SPELL")
            print(" RUN     TALK")
        if (cOption ==3):
            print(" FIGHT   SPELL")
            print(">RUN     TALK")
        if (cOption ==4):
            print(" FIGHT   SPELL")
            print(" RUN    >TALK")
        #player moves between options
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            soundMade("sfx/menuMove.wav")
            cOption += 2
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            soundMade("sfx/menuMove.wav")
            cOption -= 2
        elif event.event_type == keyboard.KEY_DOWN and event.name == "right":
            soundMade("sfx/menuMove.wav")
            cOption +=1
        elif event.event_type == keyboard.KEY_DOWN and event.name == "left":
            soundMade("sfx/menuMove.wav")
            cOption -=1
        #when an options is selected, the relevant functions are ran
        elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
            if(cOption == 1):
                #if t is false targetMenu was cancelled so turn is not increased
                t = targetMenu(enemLst)
                if t!=False:
                    playerLst[turn-1].attack(t)
                    turn+=1
                    #if the player's party has dead members, turn is moved up
                    while(turn<(len(playerLst) + 1)):
                        if playerLst[turn-1].isDed == True:
                            turn+=1
                        else:
                            break   
            #spellsMenu is opened if the player selected SPELL                    
            elif(cOption == 2):
                 if (spellsMenu(playerLst[turn-1], playerLst, enemLst) == True):     
                     turn+=1
                     while(turn<(len(playerLst) +1)):
                        if playerLst[turn-1].isDed == True:
                            turn+=1
                        else:
                            break
            
            #run away is attempted. run gets more likely the more times it fails
            elif(cOption == 3):       
                x = randint(1, runPower)
                if x<10:
                    print("Escaped Successfully")
                    waitSpace()
                    battleContinue = False
                    break
                else:
                    print("Run Failed!")
                    waitSpace()
                    turn = (len(playerLst)+1)
                    runPower-=3
            #starts a conversation
            elif(cOption == 4):
                a = targetMenu(enemLst)
                if a!=False:
                    #if the player can't finish talking to the enemy in the 10 questions they have due to low CHA, they can't start a conversation
                    if a.getdemand() / ((playerLst[0].getCHA()+1) / 5) > 10:
                        print("You don't think you know how to talk to this enemy yet...")
                    elif a.getdemand() == 99999999:
                        print("You already spoke to that enemy...")
                    else:
                        #opens convoMenu, if it is cancelled turn is not increased
                        x = convoMenu(a, playerLst[0])
                        if x != False:
                            if x[1] == True:
                                playerLst[0] = x[0]
                                #if the player party is full, the monster wanders off
                                if len(playerLst) > 3:
                                    print("Your party is full...")
                                    print(a.getName(), " wandered off...")
                                    a.setcHP(0)
                                    waitSpace()
                                else:
                                    #if a party member is added, the battle ends with EXP gain but no blood gain
                                    for i in range(len(enemLst)):
                                        totalEXP+=enemLst[i].getEXPYield()
                                    print("Victory! You recieved ",  totalEXP," EXP")    
                                    waitSpace()                            
                                    return playerLst, totalEXP, totalB, a.getentID()
                            #ends all the player's turns
                            turn = len(playerLst) + 1
                            a.setdemand(99999999)
            #if all the enemies are dead, end the battle with a victory
            if(allDed(enemLst) == True):
                    for enem in enemLst:
                        totalEXP+=enem.getEXPYield()
                        totalB+=enem.getbYield()
                    print("Victory! You recieved ",  totalEXP," EXP and ", totalB, " Blood and Bones!")
                    waitSpace()
                    battleContinue = False
                    break 
            #if enemies remain alive, select their actions  
            if(turn == (len(playerLst)+1)):
                for i in range(len(enemLst)):
                    if enemLst[i].isDed() == False:
                        enemLst[i].selectAction(playerLst, enemLst) 
                #once this occurs, if the player has died the application exits                                    
                if(allDed(playerLst) == True):
                    print("The party was defeated!")   
                    print("You black out and lose half your blood, bones, sticks and stones...")                            
                    waitSpace()
                    return playerLst, totalEXP, totalB, "Lost"
                turn = 1
        #lets the menu loop around     
        if (cOption >= 5):                      
             cOption -= 4
        elif (cOption <= 0):
            cOption +=  4
    return playerLst, totalEXP, totalB, False

#the player chooses what they want from the enemy via negotiation
def chooseDemand():
    cOption = 0
    isDone = False
    optionsLst = ["Join me", "Teach me a spell", "Give me something cool"]
    cposits = returnCposits()
    while(isDone==False):
        clearToLine(cposits)
        x = getMenuChoice(cOption, 3)
        if x == -1:
            return -1
        elif x ==-2:
            return optionsLst[cOption]
        else:
            cOption = x
        for i in range(3):
            choice = " "
            if i==cOption:
                choice = ">"
            choice+=optionsLst[i]
            print(choice)

#the demand meter shows how the player's negotiation is going
def makeDemandMeter(demandPosit, lenience, demand):
    totalStr = "Progress: ["
    for i in range(lenience, demand):
        if i == (demandPosit):
            totalStr+="I"
        else:
            totalStr+=" "
    totalStr +="]"
    if demandPosit > demand:
        return "[NEGOTIATION SUCCESS!!]"
    else:
        return totalStr

#convoMenu is where the negotiation takes place
def convoMenu(target, mc):
    stdscr.clear()
    convoData = target.loadConvo()
    #higher demand = lower lenience
    lenience = (min(-(10-target.getdemand()), -1))
    waitSpace()
    dChoice = chooseDemand()
    demandPosit = 1
    if dChoice == -1:
        return False
    isDone = False
    cposits = returnCposits()
    truDemand = max(target.getdemand(), 3)
    while(isDone == False):
        clearToLine(cposits)
        print(makeDemandMeter(demandPosit, lenience, truDemand))
        #if the monster is happy you've answered their questions
        if demandPosit > truDemand:
            #carnivores want blood and bones, while herbivores want Sticks and Stones
            if target.getconvType() == "Carnivore":
                dString = " Blood and Bones"
            else:
                dString = " Sticks and Stones"
            #if the player asked for sticks and stones, they are given it without cost
            if dChoice == "Give me something cool":
                print("The monster acquiesces to your demands!")
                payout = truDemand * (max(mc.getCHA(), 1))
                print("You get ", payout, " sticks and stones!")
                mc.changesCount(payout)
                waitSpace()
                return mc, False
            #otherwise, the player is given a cost for their request to be granted, reduced by CHA
            else:
                dCost = max(((truDemand * mc.getLevel()) - (int(mc.getCHA())-1), 1))
                print("The monster acquiesces to your demands, in exchange for ", dCost," ", dString, ". Accept? (Z to accept, X to refuse")
                notDone = True
                while(notDone):
                    event = keyboard.read_event()
                    #if the player doesn't have enough, or they say no, they get sticks and stones instead
                    if event.event_type == keyboard.KEY_DOWN and event.name == 'z':
                        if (target.getconvType() == "Carnivore" and (truDemand * mc.getLevel()) > mc.getbCount()) or (target.getconvType() == "Herbivore" and (truDemand * mc.getLevel()) > mc.getsCount()):
                            print("But you didn't have enough...")
                            waitSpace()
                            notDone = False
                        else:
                            #appropriate cost is deducted
                            if target.getconvType() == "Carnivore":
                                mc.changebCount(-(truDemand * mc.getLevel()))
                            else:
                                mc.changesCount(-(truDemand * mc.getLevel()))
                            #a spell is taught if the player requested it, invoking their class method
                            if dChoice == "Teach me a spell":
                                print(target.getName() + "will teach you ", target.getteachSpell(), "!")
                                waitSpace()
                                mc.learnSpell(target.getteachSpell())
                                return mc, False
                            #target joins the player, True is returned
                            else:
                                print(target.getName() + " will join you!!")
                                waitSpace()
                                return mc, True
                    elif event.event_type == keyboard.KEY_DOWN and event.name == 'x':
                        soundMade("sfx/menuMove.wav")
                        notDone = False
                #when the loop is exited, if not already returned the player gets the second prize, and the loop exits
                payout = truDemand * mc.getCHA()
                print("The monster gives you something else instead... You get ", payout, " sticks and stones!")
                mc.changesCount(payout)
                waitSpace()
                return mc, False
        #if there's no more questions to ask, or the player annoyed the enemy, the conversation ends
        elif (demandPosit < lenience) or (len(convoData) == 0):
            print("Negotiations Broke Down...")
            waitSpace()
            return mc, False
        #a question is asked, and the MC is updated depending on the question's consequences
        a = askQuestion(mc, convoData, demandPosit)
        demandPosit = a[1]
        mc = a[0]

#a question is asked, the list of questions is reduced in number so the same question isn't asked more than once
def askQuestion(mc, convoData, demandPosit):
    quesNum = randint(0, (len(convoData)-1))
    questData = convoData[quesNum]
    convoData.pop(quesNum)
    #certain parts have codes at the end that deal damage to the player
    if questData["question"][-1] == "!":
        questData["question"] = questData["question"][:-1]
        mc.takeDamage(int(questData["question"][-1]), False)
        #the player cannot die as part of a conversation
        if mc.getcHP() <=0:
            print("You held on for the rest of this conversation...")
            mc.setcHP(1)
        waitSpace()
        questData["question"] = questData["question"][:-1]
    cposits = returnCposits()
    running = True
    #a list of the questions is made, then shuffled so they're in a different order each time
    iptedLst = [qInterpret(questData["ansCorrect"], mc.getLevel(), mc.getCHA(), "Correct"), qInterpret(questData["ansNeutral"], mc.getLevel(), mc.getCHA(), "Neutral"), qInterpret(questData["ansIncorrect"], mc.getLevel(), mc.getCHA(), "Incorrect")]
    shuffle(iptedLst)
    cOption = 0
    while(running):
        #shows the different responses
        clearToLine(cposits)
        print(questData["question"])
        for i in range(3):
            cString = " "
            if cOption == i:
                cString = ">"
            cString+=iptedLst[i][0]
            print(cString)
        choice = getMenuChoice(cOption, 3)
        if choice == -2:
            #certain options take away stuff when selected. if the player doesn't have enough, they can't select it
            if (iptedLst[cOption][1] == "*" and mc.getsCount() < max((iptedLst[cOption][2]*mc.getLevel() - mc.getCHA()), 1)) or (iptedLst[cOption][1] == "$" and mc.getbCount() < max((iptedLst[cOption][2]*mc.getLevel() - mc.getCHA()), 1)):
                print("But you didn't have enough...", max((iptedLst[cOption][2]*mc.getLevel() - mc.getCHA()), 1) )
                waitSpace()
            else:
                #print the result and change demandPosit
                if iptedLst[cOption][3] == "Correct":
                    demandPosit+= 1
                    print("They seemed to like that")
                elif iptedLst[cOption][3] == "Incorrect":
                    demandPosit-=1
                    print("They didn't seem to like that...")
                else:
                    print("They seemed to have no strong feelings about that")
                waitSpace()
                #player takes damage if they selected a ! option
                if iptedLst[cOption][1] == "!":
                    mc.takeDamage(iptedLst[cOption][2], False)
                    if mc.getcHP() <=0:
                        print("You held on for the rest of this conversation...")
                        mc.getcHP(1)
                    waitSpace()
                #player spends sticks and stones if they selected a * option
                elif iptedLst[cOption][1] == "*":
                    mc.changesCount(-max((iptedLst[1][2]*mc.getLevel() - mc.getCHA()), 1))
                    print("You used some sticks and stones")
                #player spends blood and bones if they selected a $ option
                elif iptedLst[cOption][1] == "$":
                    mc.setbCount(-max((iptedLst[1][2]*mc.getLevel() - mc.getCHA()), 1))
                    print("You used some blood and bones")
                #player loses stats if they selected a % option
                elif iptedLst[cOption][1] == "%":
                    mc.multATK(0.3)
                    print("You lost some attack power")
                return [mc, demandPosit]
        else:
            cOption = choice

    
#qinterpret makes the question text human readable
def qInterpret(q, pLVL, pCHA, correctNess):
    if q[-1] == "!" or q[-1] =="%" or q[-1] =="$" or q[-1] =="*":
        efType = q[-1]
        q = q[:-1]
        amt = int(q[-1])
        q = q[:-1]
        if efType == "!":
            q+=("(Take " + str(max((amt*pLVL - pCHA), 1)) + " points of damage)")
        elif efType == "%":
            q+=("(Lose " + str(amt * 10) + "%"+ "of your attack power)") 
        elif efType == "*":
            q+=("(Lose " + str(max((amt*pLVL - pCHA), 1)) + " of your sticks and stones)")
        elif efType == "$":
            q+=("(Lose " + str(max((amt*pLVL - pCHA), 1)) + " of your blood and bones)")
        return q, efType, amt, correctNess
    else:
        return q, "", "", correctNess

#loads the sprites from the spritesheet txt file        
def loadsprites():        
    f = open("monsters.txt")
    sprarray = []
    for line in f:      
        sprarray.append(line)  
    f.close()
    return sprarray

#loads the enemy data from the csv file
def loadenemydata():
    f = open("enemydata.csv")
    g = csv.DictReader(f)
    f.close()
    return g

#loads a specific spell's properties from the relevant dict    
def getSpellProperties(spellID):
    con = sqlite3.connect("strandedData.db")
    cur = con.cursor()
    spellProperties= cur.execute("SELECT spellName, mpCost, basePower, multiPl, type, descP, target FROM spellData WHERE spellID="+str(spellID)).fetchall()[0]
    cur.close()
    return spellProperties                                               