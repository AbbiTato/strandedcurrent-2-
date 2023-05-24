
import keyboard
import curses
import csv
import os
from random import randint
from strandedBattle import ally, enemy, returnCposits, returnHPstring, waitSpace, loadsprites,  battle, clearToLine

cmd = 'mode 160,40'
os.system(cmd)
curses.noecho
stdscr = curses.initscr()
EXPvals = [0, 20, 35, 50, 70, 100, 140, 200, 280, 400, 600]

class equipment():
    def __init__(self, Name):
        f = open("equipmentData.csv")
        g = csv.DictReader(f)
        for row in g:
            if (row["Name"] == Name):
                self.Name = row["Name"]
                self.aBonus = int(row["aBonus"])
                self.dBonus = int(row["dBonus"])
                self.mBonus = int(row["mBonus"])
                self.HIT = int(row["HIT"])
                self.eBonus = int(row["eBonus"])
                self.cBonus = int(row["cBonus"])
                self.slot = row["slot"]
                self.eType = row["eType"]
                self.desc = row["desc"]
        f.close()

    def showStats(self, eWpn):
        statString = ""
        if self.aBonus != 0:
            statString+= "ATK + " + str(self.aBonus) + "(" + returnPlus(self.aBonus-eWpn.aBonus) + ") "
        if self.dBonus != 0:
            statString += "DEF + " + str(self.dBonus) + "(" + returnPlus(self.dBonus-eWpn.dBonus) + ") "
        if self.dBonus != 0:
            statString += "DEF + " + str(self.dBonus) + "(" + returnPlus(self.dBonus-eWpn.dBonus) + ") "
        if self.mBonus != 0:
            statString+= "mATK + " + str(self.mBonus) + "(" + returnPlus(self.dBonus-eWpn.dBonus) + ") "
        if self.slot == "Weapon":
            statString += "HIT: " + str(self.HIT * 5)+"%" + "(" + returnPlus((self.HIT*5)-(eWpn.HIT*5)) + "%) "
        else:
            statString += "HIT + " + str(self.HIT * 5)+"%" + "(" + returnPlus((self.HIT*5)-(eWpn.HIT*5)) + "%) "
            
        if self.eBonus !=0:
            statString += "DODGE + " + str(self.eBonus * 5) + "%" + "(" + returnPlus((self.eBonus *5)-(eWpn.eBonus * 5)) + "%) " 
        if self.cBonus !=0:
            statString += "CRIT + "  + str(self.cBonus * 5) + "%" + "(" + returnPlus((self.cBonus *5)-(eWpn.cBonus * 5)) + "%) "
        return statString

class item():
    def __init__(self, Name, count):
        f = open("itemData.csv")
        g = csv.DictReader(f)
        self.count = count
        for row in g:
            if (row["Name"] == Name):
                self.Name = row["Name"]
                self.eType = row["eType"]
                self.power = int(row["power"])
                self.usable = bool(int(row["usable"]))
                self.tossable = bool(int(row["tossable"]))
                self.sellable = bool(int(row["sellable"]))
                self.price = int(row["price"])
                self.description = row["description"]
        f.close()
    def changeQuant(self, num):
        self.count += num
        


class pMember:
    def __init__(self, Name, startAcc = "None" ):
        f = open("charStats.csv")
        g = csv.DictReader(f)
        for row in g:
            if (row["Name"] == Name):
                self.sprID = int(row["sprID"])
                self.Name = Name
                self.Level = 1
                self.EXP = 0
                self.HP = int(row["HPBase"])
                self.cHP = self.HP
                self.MP = int(row["MPBase"])
                self.cMP = self.MP
                self.STR = int(row["STRBase"])
                self.INT = int(row["INTBase"])
                self.RES = int(row["RESBase"])                
                self.CHA = int(row["CHABase"])
                self.eWpn = equipment(row["startWPN"])
                self.eAmr = equipment(row["startAMR"])
                self.eAcc = equipment(startAcc)
                self.eType = row["eType"]
                if self.eType == "Hero":
                    self.bCount = 20
                    self.sCount = 20
                if row["startSpells"] == "None":
                    self.spellList = []
                else:
                    self.spellList = row["startSpells"].split(",")
                HPGrow = int(row["HPGrow"])
                MPGrow = int(row["MPGrow"]) + HPGrow
                STRGrow = int(row["STRGrow"]) + MPGrow
                INTGrow = int(row["INTGrow"]) + STRGrow
                RESGrow = int(row["RESGrow"]) + INTGrow
                CHAGrow = int(row["CHAGrow"]) + RESGrow
                self.growths = [HPGrow, MPGrow, STRGrow, INTGrow, RESGrow, CHAGrow]
                self.growCount = int(row["growCount"])
                self.EXPRate = int(row["EXPRate"])
                self.LVLCap = int(row["LVLCap"])
                self.ATK = self.STR + self.eWpn.aBonus + self.eAmr.aBonus + self.eAcc.aBonus
                self.DEF = self.eWpn.dBonus + self.eAmr.dBonus + self.eAcc.dBonus
                self.mATK = self.INT + self.eWpn.mBonus + self.eAmr.mBonus + self.eAcc.mBonus
                self.HIT = 1+self.eWpn.HIT
                self.DODGE = 1+self.eWpn.eBonus + self.eAmr.eBonus + self.eAcc.eBonus
                self.CRIT = 1+self.eWpn.cBonus + self.eAmr.cBonus + self.eAcc.cBonus
            

    def levelUp(self):
        self.Level +=1
        bonuses = [0, 0, 0, 0, 0, 0]
        print(self.Name, " levelled up!")
        for i in range(self.growCount):
            a = randint(1, 20)
            if a <= self.growths[0]:
                self.HP+=3
                bonuses[0] +=3
                self.cHP = self.HP
            elif a <= self.growths[1]:
                self.MP+=2
                bonuses[1] +=2
                self.cMP = self.MP
            elif a<= self.growths[2]:
                self.STR += 1
                bonuses[2] +=1
            elif a<= self.growths[3]:
                self.INT += 1
                bonuses[3] +=1
            elif a<= self.growths[4]:
                self.RES += 1
                bonuses[4] +=1
            elif a <= self.growths[5]:
                self.CHA += 1
                bonuses[5] +=1
            else:
                print("Error")
        print("HP+", bonuses[0], " (", self.HP,")")
        print("MP+", bonuses[1], " (", self.MP,")")
        print("STR+", bonuses[2], " (", self.STR,")")
        print("INT+", bonuses[3], " (", self.INT,")")
        print("RES+", bonuses[4], " (", self.RES,")")
        print("CHA+", bonuses[5], " (", self.CHA,")")
        self.statChange()
        waitSpace()
            
    def gainEXP(self, gEXP):
        if self.Level != self.LVLCap and gEXP!= 0:
            self.EXP += gEXP
            if self.EXP >= EXPvals[self.Level]:
                self.levelUp()
                oEXP = self.EXP
                self.EXP = 0
                self.gainEXP(oEXP - EXPvals[self.Level])


    
    def statChange(self):
        self.ATK = self.STR + self.eWpn.aBonus + self.eAmr.aBonus + self.eAcc.aBonus
        self.DEF = self.RES + self.eWpn.dBonus + self.eAmr.dBonus + self.eAcc.dBonus
        self.mATK = self.INT + self.eWpn.mBonus + self.eAmr.mBonus + self.eAcc.mBonus
        self.HIT = 1+self.eWpn.HIT
        self.DODGE = 1+self.eWpn.eBonus + self.eAmr.eBonus + self.eAcc.eBonus
        self.CRIT = 1+self.eWpn.cBonus + self.eAmr.cBonus + self.eAcc.cBonus
    
    def returnspr(self, lst):
        isnum = False
        sprArray = []
        for i in range(len(lst)):
            if(lst[i] == str(self.sprID+1)+"\n"):
                break   
            if(isnum == True):
                sprArray.append(lst[i])
            if(lst[i] == str(self.sprID)+"\n"):
                isnum = True  
        return sprArray
    
    def heal(self, power, hpmp):
        if hpmp == "hp":
            if (self.HP - self.cHP < power):
                print(self.Name, " was fully healed!")
                self.cHP = self.HP
            else:
                print(self.Name, "was healed by ", str(power), " points!")
                self.cHP+=power
        elif hpmp == "mp":
            if (self.MP - self.cMP < power):
                print(self.Name, "'s MP is fully recovered")
                self.cMP = self.MP
            else:
                print(self.Name, "'s MP is recovered by ", str(power), " points!")
                self.cMP+=power
    
    def returnPcentchances(self):
        eChance = 5 * self.DODGE
        cChance = 5 * self.CRIT
        hChance = 5 * self.HIT
        return hChance, eChance, cChance

    def equip(self, pEquip):
        if pEquip.eType == "Weapon":
            self.eWpn = pEquip
        elif pEquip.eType == "Armour":
            self.eAmr = pEquip
        elif pEquip.eType == "Accessory":
            self.eAcc = pEquip
        self.statChange()
    
    def printStats(self):
        print(self.Name, "  LVL:", self.Level)
        print("EXP:", self.EXP, " To Next: ", (EXPvals[self.Level] - self.EXP))
        print(returnHPstring(self, True))
        print("MP: ", self.cMP, "/", self.MP)
        print("STR: ", self.STR)
        print("INT: ", self.INT)
        print("ATK: ", self.ATK)
        print("DEF: ", self.DEF)
        print("mATK: ", self.mATK)
        a = self.returnPcentchances()
        print("HIT: ", a[0], "%")
        print("DODGE: ", a[1],"%")
        print("CRIT: ", a[2],"%")
        print("[[[SPELLS:]]]")
        for i in range(len(self.spellList)):
            print(self.spellList[i])
    
    def makeCombattant(self):
        return ally(self.sprID,self.Name, self.HP, self.cHP, self.MP, self.cMP, self.ATK, self.DEF, self.mATK, self.HIT, self.DODGE, self.CRIT,  self.Level, self.spellList, self.bCount, self.sCount)



def returnPlus(num):
    if num >0:
        string = "+"
    else:
        string = "-"
    string+=str(abs(num))
    return string



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

def printCol(string, color):
    try:
        stdscr.addstr(string, color)
        stdscr.addstr("\n")
        stdscr.refresh()
    except curses.error:
        pass

def importUIData():
    totalLst = []
    f = open("UIdata.txt")
    for line in f:
        totalLst.append(line.strip("\n"))
    f.close()
    return totalLst

def checkEmptyItems(itemLst):
    removYes = False
    for i in range(len(itemLst)):
        try:
            if itemLst[i].count <= 0:
                itemLst.pop(i)
                removYes = True
                if (len(itemLst))!=1:
                    i -=1
        except:
            pass
    return itemLst, removYes

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
    




def itemLoop(itemInventory, pLst):
    goBack = False
    cOption = 0
    while (goBack == False):
        a = checkEmptyItems(itemInventory)
        itemInventory = a[0]
        if a[1] == True: cOption = 0

        stdscr.clear()
        for i in range(len(itemInventory)):
            cString = ""
            if i == cOption:
                cString+=">"
            else:
                cString+=" "
            cString+=itemInventory[i].Name
            cString+=" x "
            cString+=str(itemInventory[i].count)
            print(cString)
        choice = getMenuChoice(cOption, len(itemInventory))
        if choice == -2:
            a = itemUseInventory(itemInventory[cOption], pLst)
            itemInventory[cOption] = a[0]
            pLst = a[1]
        elif choice == -1:
            return itemInventory, pLst
        else:
            cOption = choice
    

def itemUseInventory(item, pLst):
    print("")
    cOption = 0
    goBack = False
    oList = []
    print(item.Name, ":")
    print(item.description)
    if item.usable == True:
        oList.append("Use")
    if item.tossable == True:
        oList.append("Toss")
    oList.append("Back")
    cposits = returnCposits()
    while (goBack == False):
        clearToLine(cposits)
        for i in range(len(oList)):
            cPrint = " "
            if i==cOption:
                cPrint = ">"
            cPrint+= oList[i]
            print(cPrint)
        choice = getMenuChoice(cOption, len(oList))
        if choice == -1:
            return item, pLst
        elif choice == -2:
            if oList[cOption] == "Use": 
                return partyChoice(item, pLst)
            elif oList[cOption] == "Toss":
                print("Really Toss? (Yes: Z) (No: X)")
                miniGoBack = False
                while(miniGoBack == False):
                    event2 = keyboard.read_event()
                    if event2.event_type == keyboard.KEY_DOWN and event2.name == "z":
                        item.count = 0
                        return item, pLst
                    elif event2.event_type == keyboard.KEY_DOWN and event2.name == "x":
                        miniGoBack = True        
            elif oList[cOption] == "Back":
                return item, pLst
        else:
            cOption = choice

def partyChoice(item, pLst):
    cposits = returnCposits()
    cOption = 0
    goBack = False
    while(goBack == False):
        clearToLine(cposits)
        for i in range(len(pLst)):
            cString = " "
            if i == cOption:
                cString = ">"
            cString+=pLst[i].Name + " "
            cString+=returnHPstring(pLst[i]) + " "
            cString+="MP: " + str(pLst[i].cMP) + "/" + str(pLst[i].MP)
            print(cString)
        choice = getMenuChoice(cOption, len(pLst))
        if choice == -1:
            return item, pLst
        elif choice == -2:
            if item.eType == "HP+":
                pLst[cOption].heal(item.power, "hp")
            elif item.eType == "MP+":
                pLst[cOption].heal(item.power, "mp")
            elif item.eType == "HPMP+":
                pLst[cOption].heal(item.power, "hp")          
                pLst[cOption].heal(item.power, "mp")
            waitSpace()
            item.count -=1
            return item, pLst
        else:
            cOption = choice

def equipLoop(pLst, equipInventory):
    goBack = False
    cOption = 0
    while(goBack == False):
        stdscr.clear()
        print("Party:")
        print("")
        for i in range(len(pLst)):
            cString = " "
            if i == cOption:
                cString = ">"
            cString+=pLst[i].Name
            print(cString)
        choice = getMenuChoice(cOption, len(pLst))
        if choice == -1:
            goBack = True            
        if choice == -2:
            a = equipView(pLst[cOption], equipInventory)
            pLst[cOption] = a[0]
            equipInventory = a[1]
        else:
            cOption = choice
        if cOption > len(pLst):
            cOption = 0
        elif cOption < 0:
            cOption = len(pLst)
    return pLst, equipInventory

def equipView(pMember, equipInventory):
    cposits = returnCposits()
    cOption = 0
    goBack = False
    while(goBack == False):
        clearToLine(cposits)
        print("-----------------")
        dLst = [("Weapon: " + pMember.eWpn.Name), ("Armour: " + pMember.eAmr.Name), ("Accessory: " + pMember.eAcc.Name)]
        for i in range(3):
            cString = " "
            if cOption == i:
                cString=">"
            cString+= dLst[i]
            print(cString)
        print("-----------------")
        cpositx2 = stdscr.getyx()[1]
        cposity2 = stdscr.getyx()[0]
        pMember.printStats()
        choice = getMenuChoice(cOption, 3)
        if choice == -1:
            goBack = True
        elif choice == -2:
            x = equipChangeMenu(pMember, equipInventory, cOption, cpositx2, cposity2)
            pMember = x[0]
            equipInventory = x[1]
            clearToLine(cposits)
        else:
            cOption = choice
    clearToLine(cposits)
    return pMember, equipInventory

def equipChangeMenu(pMember, equipInventory, eChoice, cpositx, cposity):
    if eChoice == 0:
        eChoice = "Weapon"
        e = pMember.eWpn
    elif eChoice == 1:
        eChoice = "Armour"
        e = pMember.eAmr
    elif eChoice == 2:
        eChoice = "Accessory"
        e = pMember.eAcc
    goBack = False
    cOption = 0
    while(goBack == False):
        clearToLine(cposity, cpositx)
        pMember.printStats()
        print("")
        print("-----------------")
        pMember.equip(e)
        cLst = []
        for i in range(len(equipInventory)):
            if (equipInventory[i].slot == eChoice and (equipInventory[i].eType == pMember.eType or equipInventory[i].eType == "All")):
                cLst.append(equipInventory[i])
        if cOption == 0:
            print(">E ", e.Name)
        else:
            print(" E ", e.Name)
        for i in range(len(cLst)):
            cString = " "
            if (i+1) == cOption:
                cString = ">"
            cString+=cLst[i].Name
            if eChoice == "Weapon":
                if(cLst[i].aBonus < e.aBonus):
                    bText = "(-)"
                elif(cLst[i].aBonus > e.aBonus):
                    bText = "(+)"
                else:
                    bText = "(=)"
                cString+=bText
            elif eChoice == "Armour":
                if(cLst[i].dBonus < e.dBonus):
                    bText = "(-)"
                elif(cLst[i].dBonus > e.dBonus):
                    bText = "(+)"
                else:
                    bText = "(=)"
                cString+=bText
            print(cString)
        if cOption == 0:
            print(e.showStats(e))
            print(e.desc)
        else:
            print(cLst[cOption-1].showStats(e))
            print(cLst[cOption-1].desc)
        choice = getMenuChoice(cOption, (len(cLst)+1))
        if choice == -1:
            goBack = True            
        elif choice == -2:
            if cOption!=0:
                if eChoice == "Weapon":
                    equipInventory.append(pMember.eWpn)
                    pMember.eWpn = cLst[cOption-1]
                    e = pMember.eWpn
                if eChoice == "Armour":
                    equipInventory.append(pMember.eAmr)
                    pMember.eAmr = cLst[cOption-1]
                    e = pMember.eAmr
                if eChoice == "Accessory":
                    equipInventory.append(pMember.eAcc)
                    pMember.eAcc = cLst[cOption-1]
                equipInventory.remove(cLst[cOption-1])
        else:
            cOption = choice
    return pMember, equipInventory

def statusLoop(pLst):
    a = loadsprites()
    cOption = 0
    goBack = False
    while(goBack == False):
        stdscr.clear()
        sprLst = pLst[cOption].returnspr(a)
        for i in range(len(sprLst)):
            print(sprLst[i].strip("\n"))
        pLst[cOption].printStats()
        choice = getMenuChoice(cOption, len(pLst))
        if choice == -1:
            goBack = True
        elif choice == -2:
            pass
        else:
            cOption = choice


def optionsLoop():
    stdscr.clear()
    print("No Options Currently, more will be added once I've implemented difficulty and sound")
    waitSpace()


def menuLoop(UIdata, itemInventory, equipInventory, pLst):
    loopDone = False
    cOption = 3
    while(loopDone == False):
        stdscr.clear()
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            cOption += 8
            if cOption>27:
                cOption = 3
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            cOption -= 8
            if cOption <3:
                cOption = 27
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'x'  :
            return itemInventory, pLst
        elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
            if cOption == 3:
                a = itemLoop(itemInventory, pLst)
                itemInventory = a[0]
                pLst = a[1]
            elif cOption == 11:
                equipLoop(pLst, equipInventory)
            elif cOption == 19:
                statusLoop(pLst)
            elif cOption == 27:
                optionsLoop()
        
        for i in range(len(UIdata)):
            string = UIdata[i]
            if (i==cOption):
                string+=" <--"
            print(string)

def importMapEncounters(mapName = "Test"):
    string = "maps/"+ mapName + "/mapencounter.csv"
    f = open(string)
    g = csv.DictReader(f)
    dictLst = []
    for line in g:
        dictLst.append(line)
    f.close()
    return dictLst

def chooseEncounter(dict, partyLst):
    chanceCounts = []
    for line in dict:
        chanceCounts.append(int(line["EncNum"]))
    chanceTracker = 0
    for i in range(len(chanceCounts)):
        chanceCounts[i] = chanceCounts[i] + chanceTracker
        chanceTracker = chanceCounts[i]
    a = randint(1, 20)
    finalID = 0
    for i in range(len(chanceCounts)):
        if a<=chanceCounts[i]:
            finalID = i
            break
    for line in dict:
        if int(line["EncID"]) == finalID:
            return startEncounter([line["MemA"], line["MemB"], line["MemC"], line["MemD"]], partyLst)



def startEncounter(memLst, partyLst):
    enemLst = []
    for i in range(4):
        if memLst[i] != "None":
            enemLst.append(enemy(memLst[i]))
    pLst = []
    for i in range(len(partyLst)):
        pLst.append(partyLst[i].makeCombattant())
    updates = battle(pLst, enemLst)
    return updatedParty(partyLst, updates)


def updatedParty(partyLst, updates):
    for i in range(len(partyLst)):
        partyLst[i].cHP = updates[0][i].cHP
        partyLst[i].HP = updates[0][i].HP
        partyLst[i].cMP = updates[0][i].cMP
        partyLst[i].MP = updates[0][i].MP
        partyLst[i].gainEXP(updates[1])
    partyLst[0].bCount = updates[0][0].bCount
    partyLst[0].bCount = updates[0][0].sCount
    return partyLst
    


def importMapLayout(mapName = "Test"):
    totalLst = []
    string =  "maps\\" + mapName + "\maplayout.txt"
    f = open(string)
    for line in f:
        localLst = []
        for i in range(len(line)):
            localLst.append(line[i].strip("\n"))
        totalLst.append(localLst)
    f.close()
    return totalLst

def importMapData(mapName = "Test"):
    string = "maps\\" + mapName + "\mapdata.csv"
    f = open(string)
    g = csv.DictReader(f)
    totalLst = []
    for row in g:
        totalLst.append(row)
    f.close()
    return totalLst

def getMapEventPosit(data, x, y):
    for i in range(len(data)):
        if int(data[i]["eventx"]) == x and int(data[i]["eventy"]) == y:
            return [data[i]["eventName"], data[i]["eventContents"], data[i]["iD"]]
    return[-1, -1, -1]




def getMcDir(mcDir):
    if mcDir == 0:
        return "^"
    elif mcDir == 1:
        return ">"
    elif mcDir == 2:
        return "V"
    elif mcDir == 3:
        return "<"

def printMap(mdata, mcPositx, mcPosity, mcDir):
    cRangex = 20
    cRangey = 12
    lowrangx = max(mcPositx-cRangex, -1)
    highrangx = max(mcPositx+cRangex, len(mdata[0]))
    lowrangy = max(mcPosity-cRangey, -1)
    highrangy = min(mcPosity+cRangey, len(mdata))
    ##print(lowrangx," ",highrangx," ",lowrangy," ",highrangy)
    for y in range(len(mdata)):
        linestr = "          "
        if (lowrangy<y<highrangy):
            for x in range(len(mdata[y])):
                if (lowrangx<x<highrangx):
                    if y ==mcPosity and x == mcPositx:
                        linestr+=getMcDir(mcDir)
                    else:
                        linestr+=mdata[y][x]
            print(linestr)
    stdscr.refresh()






def overWorldLoop():
    pLst = [pMember("Troubador", "Wooden Charm"), pMember("Florp")]
    itemInventory = [item("HealingHerb", 3), item("SoulDrop", 5), item("Rock", 19), item("MegaHerb", 1)]
    equipInventory = [equipment("Spiked Branch"), equipment("Iron Band"), equipment("Leather Pelt")]
    mapName= "Test"
    mLayout = importMapLayout(mapName)
    mData = importMapData(mapName)
    encData = importMapEncounters(mapName)
    UIData = importUIData()
    mcPositx = 15
    mcPosity = 5
    ##0: North, 1: East, 2: South, 3: West
    mcDir = 2
    leaveMap = False
    stepcount = randint(1, 1)
    while(leaveMap == False):
        stdscr.clear()
        if stepcount <=0:
            pLst = chooseEncounter(encData, pLst)
            stepcount = randint(20, 30)
        printMap(mLayout, mcPositx, mcPosity, mcDir)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            mcDir = 2
            if mLayout[mcPosity+1][mcPositx] == "." :
                mcPosity +=1
                stepcount -=1
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            mcDir = 0
            if mLayout[mcPosity-1][mcPositx] == "." :
                mcPosity -=1
                stepcount -=1
        elif event.event_type == keyboard.KEY_DOWN and event.name == "right":
            mcDir = 1
            if mLayout[mcPosity][mcPositx+1] == "." :
                mcPositx +=1
                stepcount -=1
        elif event.event_type == keyboard.KEY_DOWN and event.name == "left":
            mcDir = 3
            if mLayout[mcPosity][mcPositx-1] == "." :
                mcPositx -=1
                stepcount -=1
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'c'  :
            a = menuLoop(UIData, itemInventory, equipInventory, pLst)
            itemInventory = a[0]
            pLst = a[1]
        elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
            coord = getCheckCoord(mcPositx, mcPosity, mcDir)
            eventPosit = getMapEventPosit(mData, coord[0], coord[1])
            if (eventPosit!=([-1, -1, -1])):
                invData = eventHandler(eventPosit, itemInventory, equipInventory)
                itemInventory = invData[0]
                equipInventory = invData[1]
                if (eventPosit[0] == "chestItem" or eventPosit[0] =="chestEquip"):
                    mLayout[coord[1]][coord[0]] = "."
                for i in range(len(mData)-1):
                    if mData[i]["iD"] == eventPosit[2]:
                        mData.pop(int(eventPosit[2]))


def eventHandler(data, Iinventory, Einventory):
    if data[0] == "chestItem":
        quant = int(data[1][-1])
        dataName = data[1][:-1]
        Iinventory.append(item(dataName, quant))
        print("You found ", quant, " ", dataName, "(s) in the chest!")
        Iinventory = combineStacks(Iinventory)
        waitSpace()
    elif data[0] == "chestEquip":
        dataName = data[1]
        Einventory.append(equipment(dataName))
        print("You found ", dataName)
        waitSpace()
    elif data[0] == "npc":
        print(data[1])
        waitSpace()
    return Iinventory, Einventory

def combineStacks(itemLst):
    sentLst = []
    i = 0
    while i < len(itemLst):
        x = itemLst[i]
        j = i+1
        while j<len(itemLst):
            if itemLst[j].Name == x.Name:
                x.count+=itemLst[j].count
                itemLst.pop(j)
            j+=1
        sentLst.append(x)
        i+=1
    return sentLst


        


def getCheckCoord(mcPositx, mcPosity, mcDir):
    if mcDir == 0:
        return (mcPositx, (max((mcPosity-1), 0)))
    elif mcDir == 1:
        return (max((mcPositx+1), 0), mcPosity)
    elif mcDir == 2:
        return (mcPositx, (max((mcPosity+1), 0)))
    elif mcDir == 3:
        return (max((mcPositx-1), 0), mcPosity)




overWorldLoop()






