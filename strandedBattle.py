
import keyboard
import curses
import random
from random import randint, shuffle
import csv 
import os


cmd = 'mode 160,50'
os.system(cmd)
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
def getMenuChoice(cOption, optionsCount):
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
        cOption += 1
        if cOption > optionsCount -1:
            cOption = 0
        return cOption
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
        cOption -= 1
        if cOption <0:
                cOption = optionsCount -1
        return cOption
    elif event.event_type == keyboard.KEY_DOWN and event.name == 'x':
        return -1
    elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
        return -2
    else:
        return cOption


class combattant:
    def __init__(self, sprID, Name, HP, cHP, MP, cMP, ATK, DEF, mATK, HIT, DODGE, CRIT):
        self.sprID = sprID
        self.Name = Name
        self.HP = HP
        self.MP = MP 
        self.ATK = ATK
        self.DEF = DEF
        self.mATK = mATK
        self.HIT = HIT
        self.DODGE = DODGE
        self.CRIT = CRIT
        self.cHP = cHP
        self.cMP = cMP
        self.oATK = self.ATK
        self.oDEF = self.DEF
        self.omATK = mATK

    def takeDamage(self, eATK, crit):
        dtotal = max((eATK - self.DEF), 1)
        if crit == True:
            dtotal = max((eATK * 2), 2)
        print(self.Name+ " took "+  str(dtotal)+ " points of damage!")
        waitSpace()
        self.cHP -= (dtotal)
        if(self.cHP <= 0):
            print(self.Name + " has died!")
        waitSpace()

    def returnspr(self, array):
        isnum = False
        sprArray = []
        for i in range(len(array)):
            if(array[i] == str(self.sprID+1)+"\n"):
                break   
            if(isnum == True):
                sprArray.append(array[i])
            if(array[i] == str(self.sprID)+"\n"):
                isnum = True  
        return sprArray
    
    def critCheck(self, type):
        lCRIT = self.CRIT
        if type == "SPELL":
            lCRIT = int((lCRIT / 2))
        if (randint(1,20) < self.CRIT):
            print("Critical Hit!")
            return True
        else:
            return False
    
    def attack(self, target):
        print(self.Name +" attacked!")
        hitChance = self.HIT - target.DODGE
        if (hitChance > randint(1, 20)):
            target.takeDamage((self.ATK - target.DEF), self.critCheck("Melee"))
        else:
            print("But ", target.Name, " dodged the attack!")
        waitSpace()
    
    def isDed(self):
        if self.cHP <=0:
            return True
        else:
            return False


class enemy(combattant):
    def __init__(self, Name):
        f = open("enemyData.csv")
        g = csv.DictReader(f)
        for row in g:
            if(row["Name"] == Name):
                self.Name = row["Name"]
                self.sprID = int(row["sprID"])
                self.HP = int(row["HP"])
                self.cHP = self.HP
                self.MP = int(row["MP"])
                self.cMP = self.MP
                self.ATK = int(row["ATK"])
                self.DEF = int(row["DEF"])
                self.mATK = int(row["mATK"])
                self.HIT = int(row["HIT"])
                self.DODGE = int(row["DODGE"])
                self.CRIT = int(row["CRIT"])
                self.aLst = [row["Mov1"], row["Mov2"], row["Mov3"], row["Mov4"], row["Mov5"], row["Mov6"], row["Mov7"], row["Mov8"]]
                self.expYield = int(row["expYield"])
                self.bYield = int(row["bYield"])
                self.oATK = self.ATK
                self.oDEF = self.DEF
                self.omATK = self.mATK
                self.convType = row["convType"]
                self.demand = int(row["demand"])
                self.teachSpell = row["teachSpell"]
        f.close()
            
    def selectAction(self, playerLst, enemLst, dict):     
        epresentLst = []
        ppresentLst = []             
        for i in range(len(playerLst)):
            if playerLst[i] != False:     
                ppresentLst.append(playerLst[i])
            if enemLst[i] != False:            
                epresentLst.append(enemLst[i])         
        act = self.aLst[randint(0, 7)]
        etarg = epresentLst[randint(0, len(epresentLst)-1)]      
        ptarg = ppresentLst[randint(0, len(ppresentLst)-1)]                                 

        if act == "Attack":                     
            self.attack(ptarg)
        else:                    
            a = getSpellProperties(act, dict)
            self.cMP-=a[1]
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
    
    def loadConvo(self):
        string = "talkData\\"+self.Name+".csv"
        finalLst = []
        f = open(string)
        g = csv.DictReader(f)
        for line in g:
            finalLst.append(line)
        f.close()
        return finalLst





class ally(combattant):
    def __init__(self, sprID, Name, HP, cHP, MP, cMP, ATK, DEF, mATK, HIT, DODGE, CRIT, Level, CHA, spellList = [], bCount = -1, sCount = -1):
        super().__init__(sprID, Name, HP, cHP, MP, cMP, ATK, DEF, mATK, HIT, DODGE, CRIT)
        self.spellList = spellList
        self.oATK = self.ATK
        self.oDEF = self.DEF
        self.Level = Level
        self.CHA = CHA
        if bCount!=-1:
            self.bCount = bCount
            self.sCount = sCount
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
        





def returnCposits():
    return stdscr.getyx()[0], stdscr.getyx()[1]     

            


        
def makeOptionsMenu(optionsLst):
    cOption = 0
    isGoing = True 
    cposits = returnCposits()
    while(isGoing):
        clearToLine(cposits)
        for i in range(len(optionsLst)):
            cString = " "
            if cOption == i:
                cString = ">"
            cString+=optionsLst[i]
            print(cString)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            cOption += 1
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            cOption -= 1
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'x':
             return False
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'z':
            return optionsLst[cOption]
        if(cOption <0):
            cOption = len(optionsLst)
        if(cOption >=len(optionsLst)):
            cOption = 0 
        




def returnHPstring(ent, ally = True):
    a = ent.cHP/ent.HP * 10
    a = round(a)
    if ally == True:
        hpstring = "HP: "+str(ent.cHP)+ "/"+str(ent.HP)+ ":  ["
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

def HPstringonline(entLst, ally):
    online  = ""
    spaces = 30
    for i in range(len(entLst)):
        if(entLst[i].isDed() == False):
            online += returnHPstring(entLst[i], ally)
        else:
            online+=" " * spaces
    return online

def namesonline(entLst):
    online  = ""
    spaces = 30
    for i in range(len(entLst)):
        if(entLst[i].isDed() == False):
            online += entLst[i].Name + (" " * (spaces - len(entLst[i].Name)))
        else:
            online+=" " * spaces

    return online


def targetMenu(entLst):
    goBack = False
    targsLst = []
    for i in range(len(entLst)):
        if (entLst[i].isDed() == False):
            targsLst.append(entLst[i])
    cOption = 0
    cposits = returnCposits()
    while(goBack == False):
        clearToLine(cposits)
        for i in range(len(targsLst)):      
             if(i == cOption):                        
                print(">"+targsLst[i].Name)
             else:
                print(" "+targsLst[i].Name)       
        choice = getMenuChoice(cOption, len(entLst))
        if choice == -1:
             return False
        elif choice == -2:
            return targsLst[cOption]        
        else:
            cOption = choice          
        

def printOnLine(entLst, array):
    LstLine = ""
    maxsent = 0
    gap = 30
    sprsLst = []
    for i in range(len(entLst)):
        if (entLst[i].isDed() == False):
            a = entLst[i].returnspr(array)
            sprsLst.append(a)
            maxsent = max(maxsent, len(a))
    
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
        LstLine = ""        


def printbattletopscreen(playerLst, enemLst, a):
        print(namesonline(enemLst))
        printOnLine(enemLst, a)
        print(HPstringonline(enemLst, False))
        print("")
        print(namesonline(playerLst))
        printOnLine(playerLst, a)
        print(HPstringonline(playerLst, True))

def waitSpace():
    x = True
    while (x == True):
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'z':
            x = False
        
def buffHandler(stat, ostat, spell, target, debuff = False):
    if stat == "ATK":
        x = target.ATK
    elif stat == "DEF":
        x = target.DEF
    elif stat == "mATK":
        x = target.mATK
    x = int(x*spell[3])
    if (x < 1):
        x = 1
    word = " increased "
    word2 = " lower "
    num = 3
    if debuff == True:
        word = " decreased "
        num = 0.3
    print(target.Name+"'s " + str(stat)+word+ "by "+ str(x)+ " points!")
    waitSpace()
    if stat=="ATK" and target.ATK>(max((ostat*num), num)):
            print("But "+target.Name+"'s ATK can't go any"+ word2+"! (Stat"+ word2+"to cap)")
            waitSpace()
            target.ATK = int(target.oATK *num)
    elif stat=="DEF" and target.DEF>(max((ostat*num), num)):
            print("But "+target.Name+"'s DEF can't go any"+ word2+"! (Stat"+ word2+"to cap)")
            waitSpace()
            target.DEF = target.oDEF *num
            if target.DEF % 1 !=0:
                target.DEF = -1
    elif stat=="mATK" and target.mATK>(max((ostat*num), num)):
            print("But "+target.Name+"'s mATK can't go any"+ word2+"! (Stat"+ word2+"to cap)")
            waitSpace()
            target.mATK = int(target.omATK *num)


    
        
def cast(spell, caster, target):
    print(caster.Name+ " cast "+ spell[0]+ "!")
    damage = int((spell[2] +caster.mATK)* spell[3])
    if(spell[4] == "Heal"):
        target.cHP += damage
        print(target.Name+ " was healed by "+ str(damage)+ " points")
        waitSpace()
        if (caster.cHP >= caster.HP):
            caster.cHP = caster.HP
    elif spell[4] == "ATK+":
        buffHandler("ATK", target.oATK, spell, target)
    elif spell[4] == "DEF+":
        buffHandler("DEF", target.oDEF, spell, target)
    elif spell[4] == "mATK+":
        buffHandler("mATK", target.omATK, spell, target)
    elif spell[4] == "ATK-":
        buffHandler("ATK", target.oATK, spell, target, True)
    elif spell[4] == "DEF-":
        buffHandler("DEF", target.oDEF, spell, target, True)
    elif spell[4] == "mATK-":
        buffHandler("mATK", target.omATK, spell, target,True)
    else:
        target.takeDamage(damage, caster.critCheck("Spell"))
        waitSpace()

def spellsMenu(caster, partyLst, enemLst, dict):
    if len(caster.spellList) == 0:
        print(caster.Name+ " doesn't know any spells!")
        waitSpace()    
        return False
    spellplist = []
    goBack = False
    cOption = 0
    cposits = returnCposits()
    for i in range(len(caster.spellList)):
        spellplist.append(getSpellProperties(caster.spellList[i], dict))
    while(goBack == False):
        t = True
        clearToLine(cposits)
        for i in range(len(spellplist)):
             if(i == cOption):
                print(">"+str(spellplist[i][0])+ "["+ str(spellplist[i][1])+ "]") 
             else:
                 print(str(spellplist[i][0])+ "["+ str(spellplist[i][1])+ "]") 
        print("MP: "+str(caster.cMP)+"/"+str(caster.MP))
        choice = getMenuChoice(cOption, len(caster.spellList))
        if choice==-1:
             return False
        elif choice == -2:
            if (caster.cMP < spellplist[cOption][1]):
                print("Not enough MP")
                waitSpace()
            else:
                
                if spellplist[cOption][6] == "enemOne":
                    t = targetMenu(enemLst)
                    if t!=False:
                        caster.cMP -= spellplist[cOption][1]
                        cast(spellplist[cOption], caster, t) 
                elif spellplist[cOption][6] == "enemAll":
                    caster.cMP -= spellplist[cOption][1]
                    for i in range(len(enemLst)):
                        if enemLst[i].isDed() ==False:
                            cast(spellplist[cOption], caster, enemLst[i])
                elif spellplist[cOption][6] == "partyOne":
                    t = targetMenu(partyLst)
                    if t!=False:
                        caster.cMP -= spellplist[cOption][1]
                        cast(spellplist[cOption], caster, t)                               
                elif spellplist[cOption][6] == "partyAll":
                    caster.cMP -= spellplist[cOption][1]
                    for i in range(len(partyLst)):
                        if partyLst[i].isDed() ==False:
                                cast(spellplist[cOption], caster, partyLst[i])
                if t!=False:     
                    goBack = True         
                    return True    
        else:
            cOption = choice
    return True

                   
    
    
def allDed(entLst):
    for i in range(len(entLst)):
        if entLst[i].isDed() == False:
            return False
    return True

def clearToLine(posits):
    stdscr.move(posits[0], posits[1])
    stdscr.clrtobot()

def getRealCurrentPlayerName(playerLst, turn):
    for i in range(len(playerLst)):
        if i == turn:
            if playerLst[i].isDed() == False:
                return playerLst[i].Name
            else:
                turn +=1
    return "Error"


     
def battle(playerLst, enemLst):
    battleContinue = True
    spritesDict = loadsprites()
    spellsDict = loadspells()
    cOption = 1
    turn = 1
    runPower = 20
    totalEXP = 0
    totalB = 0
    while(battleContinue):
        stdscr.clear() 
        spellsDict = loadspells()
        printbattletopscreen(playerLst, enemLst, spritesDict)
        print("Current Turn: "+ str(getRealCurrentPlayerName(playerLst, (turn-1))))
        print(turn)
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
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            cOption += 2
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            cOption -= 2
        elif event.event_type == keyboard.KEY_DOWN and event.name == "right":
            cOption +=1
        elif event.event_type == keyboard.KEY_DOWN and event.name == "left":
            cOption -=1
        elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
            if(cOption == 1):
                t = targetMenu(enemLst)
                if t!=False:
                    playerLst[turn-1].attack(t)
                    turn+=1
                    while(turn<(len(playerLst) + 1)):
                        if playerLst[turn-1].isDed == True:
                            turn+=1
                        else:
                            break                       
            elif(cOption == 2):
                 if (spellsMenu(playerLst[turn-1], playerLst, enemLst,  spellsDict) == True):     
                     turn+=1
                     while(turn<(len(playerLst) +1)):
                        if playerLst[turn-1].isDed == True:
                            turn+=1
                        else:
                            break
        
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
            elif(cOption == 4):
                a = targetMenu(enemLst)
                if a!=False:
                    if a.demand / ((playerLst[0].CHA+1) / 5) > 10:
                        print("You don't think you know how to talk to this enemy yet...")
                    else:
                        x = convoMenu(a, playerLst[0])
                        playerLst[0] = x[0]
                        if x[1] == True:
                            if len(playerLst) > 3:
                                print("Your party is full...")
                                print(a.Name, " wandered off...")
                                a.cHP = 0
                                waitSpace()
                            else:
                                for i in range(len(enemLst)):
                                    totalEXP+=enemLst[i].expYield
                                print("Victory! You recieved ",  totalEXP," EXP")    
                                waitSpace()                            
                                return playerLst, totalEXP, totalB, a.Name
                        turn = len(playerLst) + 1
            if(allDed(enemLst) == True):
                    for enem in enemLst:
                        totalEXP+=enem.expYield
                        totalB+=enem.bYield
                    print("Victory! You recieved ",  totalEXP," EXP and ", totalB, " Blood and Bones!")
                    waitSpace()
                    battleContinue = False
                    break   
            if(turn == (len(playerLst)+1)):
                for i in range(len(enemLst)):
                    if enemLst[i].isDed() == False:
                        enemLst[i].selectAction(playerLst, enemLst, spellsDict)                                     
                if(allDed(playerLst) == True):
                    print("The party was defeated! Game over")                               
                    waitSpace()
                    exit("Battle Lost")
                turn = 1
              
        if (cOption >= 5):                      
             cOption -= 4
        elif (cOption <= 0):
            cOption +=  4
    return playerLst, totalEXP, totalB, False

def chooseDemand():
    cOption = 0
    isDone = False
    optionsLst = ["Join me", "Teach me a spell", "Give me something cool"]
    cposits = returnCposits()
    while(isDone==False):
        clearToLine(cposits)
        x = getMenuChoice(cOption, 3)
        if x == -1:
            return False
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

def makeDemandMeter(demandPosit):
    totalStr = "["
    for i in range(10):
        if i >= demandPosit:
            totalStr+"I"
        else:
            totalStr+=" "
    totalStr +="]"
    return totalStr





def convoMenu(target, mc):
    stdscr.clear()
    convoData = target.loadConvo()
    lenience = -(10-target.demand)
    dChoice = chooseDemand()
    demandPosit = 1
    if dChoice == False:
        return False
    isDone = False
    
    cposits = returnCposits()
    while(isDone == False):
        clearToLine(cposits)
        print(makeDemandMeter(demandPosit))
        if demandPosit >= target.demand:
            if target.convType == "Carnivore":
                dString = " Blood and Bones"
            if dChoice == "Give me something cool":
                print("The monster acquiesces to your demands!")
                payout = target.demand * mc.CHA
                print("You get ", payout, " sticks and stones!")
                mc.sCount += payout
                waitSpace()
                return mc, False
            else:
                dCost = max(((target.demand * mc.Level) - mc.CHA), 1)
                print("The monster acquiesces to your demands, in exchange for ", dCost," ", dString, ". Accept? (Z to accept, X to refuse")
                notDone = True
                while(notDone):
                    event = keyboard.read_event()
                    if event.event_type == keyboard.KEY_DOWN and event.name == 'z':
                        if target.convType == "Carnivore" and (target.demand * mc.Level) > mc.bCount:
                            print("But you didn't have enough...")
                            waitSpace()
                            notDone = False
                        else:
                            mc.bCount - (target.demand * mc.Level)
                            
                            if dChoice == "Teach me a spell":
                                print(target.Name + "will teach you ", target.teachSpell, "!")
                                waitSpace()
                                mc.learnSpell(target.teachSpell)
                                return mc, False
                            else:
                                print(target.Name + " will join you!!")
                                waitSpace()
                                return mc, True
                    elif event.event_type == keyboard.KEY_DOWN and event.name == 'x':
                        notDone = False
                payout = target.demand * mc.CHA
                print("The monster gives you something else instead... You get ", payout, " sticks and stones!")
                mc.sCount += payout
                waitSpace()
                return mc, False
        elif demandPosit < lenience:
            print("Negotiations Broke Down...")
            waitSpace()
            return mc, False

        a = askQuestion(mc, convoData, demandPosit)
        demandPosit = a[1]
        mc = a[0]

def askQuestion(mc, convoData, demandPosit):
    quesNum = randint(0, (len(convoData)-1))
    questData = convoData[quesNum]
    convoData.pop(quesNum)
    if questData["question"][-1] == "!":
        questData["question"] = questData["question"][:-1]
        mc.takeDamage(int(questData["question"][-1]), False)
        if mc.cHP <=0:
            print("You held on for the rest of this conversation...")
            mc.cHP = 1
        waitSpace()
        questData["question"] = questData["question"][:-1]
    cposits = returnCposits()
    running = True
    iptedLst = [qInterpret(questData["ansCorrect"], mc.Level, mc.CHA, "Correct"), qInterpret(questData["ansNeutral"], mc.Level, mc.CHA, "Neutral"), qInterpret(questData["ansIncorrect"], mc.Level, mc.CHA, "Incorrect")]
    shuffle(iptedLst)
    cOption = 0
    while(running):
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
            if (iptedLst[1] == "£" and mc.sCount < max((iptedLst[2]*mc.Level - mc.CHA), 1)) or (iptedLst[1] == "$" and mc.sCount < max((iptedLst[2]*mc.Level - mc.CHA), 1)):
                print("But you didn't have enough...")
            else:
                if iptedLst[cOption][3] == "Correct":
                    demandPosit+=1
                    print("They seemed to like that")
                elif iptedLst[cOption][3] == "Incorrect":
                    demandPosit-=1
                    print("They didn't seem to like that...")
                else:
                    print("They seemed to have no strong feelings about that")
                waitSpace()
                if iptedLst[1] == "!":
                    mc.takeDamage(iptedLst[2], False)
                    if mc.cHP <=0:
                        print("You held on for the rest of this conversation...")
                        mc.cHP = 1
                    waitSpace()
                elif iptedLst[1] == "£":
                    mc.sCount -= max((iptedLst[2]*mc.Level - mc.CHA), 1)
                    print("You used some sticks and stones")
                elif iptedLst[1] == "$":
                    mc.bCount -= max((iptedLst[2]*mc.Level - mc.CHA), 1)
                    print("You used some blood and bones")
                elif iptedLst[1] == "%":
                    mc.ATK = min(int(mc.oATK * 0.3), int(mc.ATK * 0.7))
                    print("You lost some attack power")
                return [mc, demandPosit]
        else:
            cOption = choice

    

def qInterpret(q, pLVL, pCHA, correctNess):
    if q[-1] == "!" or q[-1] =="%" or q[-1] =="$" or q[-1] =="£":
        efType = q[-1]
        q = q[:-1]
        amt = int(q[-1])
        q = q[:-1]
        if efType == "!":
            q+=("(Take " + str(max((amt*pLVL - pCHA), 1)) + "points of damage)")
        elif efType == "%":
            q+=("(Lose " + str(amt * 10) + "%% of your attack power)") 
        elif efType == "£":
            q+=("(Lose " + str(max((amt*pLVL - pCHA), 1)) + " of your sticks and stones)")
        elif efType == "$":
            q+=("(Lose " + str(max((amt*pLVL - pCHA), 1)) + " of your blood and bones)")
        return q, efType, amt, correctNess
    else:
        return q, "", "", correctNess
        


                






            

def loadsprites():        
    f = open("monsters.txt")
    sprarray = []
    for line in f:      
        sprarray.append(line)  
    f.close()
    return sprarray

def loadenemydata():
    f = open("enemydata.csv")
    g = csv.DictReader(f)
    f.close()
    return g


def loadspells():
    f = open("spells.csv")
    g = csv.DictReader(f)
    totalLst = []
    for line in g:
        totalLst.append(line)
    f.close()
    return totalLst
    
def getSpellProperties(name, dict):
    spellArray = []
    for row in dict :
        if(row["Name"] == name):
            spellArray.append(row["Name"])
            spellArray.append(int(row["MP Cost"]))
            spellArray.append(int(row["Base Power"]))
            spellArray.append(round(float(row["Multiplier"]), 1))
            spellArray.append(row["Element"])
            spellArray.append(bool(row["silenceStop?"]))
            spellArray.append(row["Target"])    
            return spellArray                                                 