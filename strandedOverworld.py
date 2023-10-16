import pickle
import keyboard
import curses
import csv
import os
from random import randint
#Imports Needed methods from strandedBattle. 
#Could do with a central location for streamlining as program expands
from strandedBattle import ally, enemy, battle,returnCposits, returnHPstring, waitSpace, loadsprites, clearToLine, printStars, getMenuChoice
from time import sleep
from playsound import playsound
#sets the currently being accessed save file
global FileName
FileName = ""

#Set screen size and initialise the curses window
cmd = 'mode 160,40'
os.system(cmd)
curses.noecho
stdscr = curses.initscr()
#Hard Coded EXP values. Better implementation useful but not currently needed
EXPvals = [0, 20, 35, 50, 70, 100, 140, 200, 280, 400, 600]

#Saves the party data on application exit
def savePlayerData(pLst, mcPositx, mcPosity, map):
    global FileName
    with open((FileName+'/pMember1.pkl'), 'wb') as outp:
        picl1 = pickle.dump(pLst[0], outp, pickle.HIGHEST_PROTOCOL)
    try:
        with open((FileName+'/pMember2.pkl'), 'wb') as outp:
            picl2 = pickle.dump(pLst[1], outp, pickle.HIGHEST_PROTOCOL)
    except:
        pass
    try:
        with open((FileName+'/pMember3.pkl'), 'wb') as outp:
            picl3 = pickle.dump(pLst[2], outp, pickle.HIGHEST_PROTOCOL)
    except:
        pass
    try:
        with open((FileName+'/pMember4.pkl'), 'wb') as outp:
            picl4 = pickle.dump(pLst[3], outp, pickle.HIGHEST_PROTOCOL)
    except:
        pass
    with open((FileName+'/locatData.txt'), 'wt') as outp:
        outp.write(str(mcPositx) + "\n")
        outp.write(str(mcPosity)+ "\n")
        outp.write(str(map)+ "\n")



    



#makes sound a global variable, imports the user's local "options" file, then sets sound based on that
def importSound():
    f = open("options.txt")
    if f.readline == "Sound: On":
        f.close()
        return True
    else:
        f.close()
        return False
    

#this method only plays sound if the sound variable is True
def soundMade(path):
    global sound
    if sound == True:
        playsound(path)

##the equipment class lets me group methods and data to do with the game's equipment
class equipment():
    def __init__(self, Name, cost=0):
        ##import all the item data to the object with only the Name field
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
        self.cost = cost

    #showStats is used in a few places to display the equipment's stats. The eWpn passed in is the currently equipped weapon
    #to allow the player to compare the two pieces of gear 
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

#groups methods and data to do with inventory items. for streamlining purposes, could have a shared parent of item and equipment
class item():
    def __init__(self, Name, count, cost=0):
        #imports all the data based on the Name field
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
        self.cost = cost
    #Item is exceedingly simple, this just changes how many you have.
    #Could possibly be changed to a list/dictionary
    def changeQuant(self, num):
        self.count += num
        

#pmember is one of the more important to be a class classes
class pMember:
    def __init__(self, Name, startAcc = "None" ):
        #imports certain characteristics based on the charStats file
        f = open("charStats.csv")
        g = csv.DictReader(f)
        for row in g:
            if (row["Name"] == Name):
                self.sprID = int(row["sprID"])
                self.Name = Name
                #All characters atm start at level 1 with 0 exp. May need an override
                self.Level = 1
                self.EXP = 0
                #Every star has both bases and growths. Bases=LVL1 stats, growths=%chance to gain stat on LVL+
                self.HP = int(row["HPBase"])
                self.cHP = self.HP
                self.MP = int(row["MPBase"])
                self.cMP = self.MP
                self.STR = int(row["STRBase"])
                self.INT = int(row["INTBase"])
                self.RES = int(row["RESBase"])                
                self.CHA = int(row["CHABase"])
                #the equipment slots are filled with equipment objects
                self.eWpn = equipment(row["startWPN"])
                self.eAmr = equipment(row["startAMR"])
                self.eAcc = equipment(startAcc)
                #changes what can be equipped
                self.eType = row["eType"]
                #the hero carries the party's cash and items. If not the hero, bCount is set to -1 to simplify debugging
                if self.eType == "Hero":
                    self.bCount = 0
                    self.sCount = 0
                else:
                    self.bCount = -1
                    self.sCount = -1
                self.itemList = []
                self.equipList = []
                #startspells gets split or not depending on if the character has any
                if row["startSpells"] == "None":
                    self.spellList = []
                else:
                    self.spellList = row["startSpells"].split(",")
                #growths are assembled into a list of staircasey summed numbers going up to 20. EG: [2, 4, 4, 4, 2, 4] becomes [2, 6, 10, 14, 16, 20]
                HPGrow = int(row["HPGrow"])
                MPGrow = int(row["MPGrow"]) + HPGrow
                STRGrow = int(row["STRGrow"]) + MPGrow
                INTGrow = int(row["INTGrow"]) + STRGrow
                RESGrow = int(row["RESGrow"]) + INTGrow
                CHAGrow = int(row["CHAGrow"]) + RESGrow
                self.growths = [HPGrow, MPGrow, STRGrow, INTGrow, RESGrow, CHAGrow]
                #extra data related to levelling up is imported
                self.growCount = int(row["growCount"])
                self.EXPRate = int(row["EXPRate"])
                self.LVLCap = int(row["LVLCap"])
                #composite stats. HIT, DODGE and CRIT must be at least 1, and while they can be above 20, this doesn't help the player
                self.ATK = self.STR + self.eWpn.aBonus + self.eAmr.aBonus + self.eAcc.aBonus
                self.DEF = self.eWpn.dBonus + self.eAmr.dBonus + self.eAcc.dBonus
                self.mATK = self.INT + self.eWpn.mBonus + self.eAmr.mBonus + self.eAcc.mBonus
                self.HIT = 1+self.eWpn.HIT
                self.DODGE = 1+self.eWpn.eBonus + self.eAmr.eBonus + self.eAcc.eBonus
                self.CRIT = 1+self.eWpn.cBonus + self.eAmr.cBonus + self.eAcc.cBonus
            
    #applies a level up
    def levelUp(self):
        self.Level +=1
        #the bonuses array is just to make the stat printing at the end less messy
        bonuses = [0, 0, 0, 0, 0, 0]
        print(self.Name, " levelled up!")
        #the for loop happens as many times as growcount, and decides based on the %s from earlier 6 stats to increase
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
        #print a well laid out set of level up data
        print("HP+", bonuses[0], " (", self.HP,")")
        print("MP+", bonuses[1], " (", self.MP,")")
        print("STR+", bonuses[2], " (", self.STR,")")
        print("INT+", bonuses[3], " (", self.INT,")")
        print("RES+", bonuses[4], " (", self.RES,")")
        print("CHA+", bonuses[5], " (", self.CHA,")")
        #stat change must be run here to fix the composite stats
        self.statChange()
        waitSpace()

    #the only reason gainEXP needs to be a function is so that if the player gains more EXP than would be required to level up
    #the new EXP gets added to their total, and due to the function being recursive, can level up the player a second time        
    def gainEXP(self, gEXP):
        if self.Level != self.LVLCap and gEXP!= 0:
            self.EXP += gEXP
            if self.EXP >= EXPvals[self.Level]:
                self.levelUp()
                oEXP = self.EXP
                self.EXP = 0
                self.gainEXP(oEXP - EXPvals[self.Level])


    #fixes the composite stats if the player's equipment changes
    def statChange(self):
        self.ATK = self.STR + self.eWpn.aBonus + self.eAmr.aBonus + self.eAcc.aBonus
        self.DEF = self.RES + self.eWpn.dBonus + self.eAmr.dBonus + self.eAcc.dBonus
        self.mATK = self.INT + self.eWpn.mBonus + self.eAmr.mBonus + self.eAcc.mBonus
        self.HIT = 1+self.eWpn.HIT
        self.DODGE = 1+self.eWpn.eBonus + self.eAmr.eBonus + self.eAcc.eBonus
        self.CRIT = 1+self.eWpn.cBonus + self.eAmr.cBonus + self.eAcc.cBonus
    
    #a clone of the sprite printing method from strandedBattle, but due to being methodbound doesn't need a passed in sprID
    def returnspr(self, lst):
        isnum = False
        sprList = []
        for i in range(len(lst)):
            if(lst[i] == str(self.sprID+1)+"\n"):
                break   
            if(isnum == True):
                sprList.append(lst[i])
            if(lst[i] == str(self.sprID)+"\n"):
                isnum = True  
        return sprList
    
    #could possibly be cut, heals the player
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
    
    #returns the % chances of dodging, critting and hitting. Used on several display screens
    def returnPcentchances(self):
        eChance = 5 * self.DODGE
        cChance = 5 * self.CRIT
        hChance = 5 * self.HIT
        return hChance, eChance, cChance

    #was surprised how simple this function turned out to be. Sets a new piece of equipment
    def equip(self, pEquip):
        if pEquip.eType == "Weapon":
            self.eWpn = pEquip
        elif pEquip.eType == "Armour":
            self.eAmr = pEquip
        elif pEquip.eType == "Accessory":
            self.eAcc = pEquip
        self.statChange()
    
    #a longass function which to summarise prints all the player's data to the screen
    def printStats(self):
        print(self.Name, "  LVL:", self.Level)
        print("EXP:", self.EXP, " To Next: ", (EXPvals[self.Level] - self.EXP))
        if self.sCount != -1:
            print("Sticks and Stones: ", self.sCount)
            print("Blood and Bones: ", self.bCount)
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
        for spell in self.spellList:
            print(spell)
    
    #when the battle starts, an Ally object is made using the pMember's data
    def makeCombattant(self):
        return ally(self.sprID,self.Name, self.HP, self.cHP, self.MP, self.cMP, self.ATK, self.DEF, self.mATK, self.HIT, self.DODGE, self.CRIT,  self.Level, self.CHA, self.spellList, self.bCount, self.sCount)



#just returns the number as a string, but if positive it has a + in front of it
def returnPlus(num):
    if num >0:
        string = "+"
    else:
        string = "-"
    string+=str(abs(num))
    return string

#gets pretty UI data from a file
def importUIData():
    totalLst = []
    f = open("UIdata.txt")
    for line in f:
        totalLst.append(line.strip("\n"))
    f.close()
    return totalLst

#checks over all the inventory items, and if their Quant is 0 they are removed
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


    



#displays the player's basic items in a list
def itemLoop(itemInventory, pLst):
    goBack = False
    cOption = 0
    #checks the player actually has items to look at
    if (len(itemInventory) == 0):
        print("You have no items!")
        waitSpace()
        return itemInventory, pLst
    else:
        #goBack is semi-obselete since I leave the loop with return statements, but it makes the code cleaner
        while (goBack == False):
            #since items are being used further down the loop, it is worthwhile to check they still >0
            a = checkEmptyItems(itemInventory)
            itemInventory = a[0]
            if a[1] == True: 
                cOption = 0
            #for main menus, we clear the entire screen
            stdscr.clear()
            #prints all the items, with the current item being preceeded by a ">" if i matches cOption
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
            #opens the itemUseInventory subMenu of the item the player selected if they press Z, otherwise returns to the main menu
            if choice == -2:
                a = itemUseInventory(itemInventory[cOption], pLst)
                itemInventory[cOption] = a[0]
                pLst = a[1]
            elif choice == -1:
                return itemInventory, pLst
            else:
                cOption = choice
    
#the submenu for using an item
def itemUseInventory(item, pLst):
    print("")
    cOption = 0
    goBack = False
    oList = []
    #prints the item's name and description
    print(item.Name, ":")
    print(item.description)
    #adds options to the list depending on if the item is usable/tossable
    if item.usable == True:
        oList.append("Use")
    if item.tossable == True:
        oList.append("Toss")
    oList.append("Back")
    #sets the point to clear the menu to, to avoid reprinting the above data
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
            #if the item is used, use partyChoice to check who the item is used on
            if oList[cOption] == "Use": 
                return partyChoice(item, pLst)
            #one last check before item is actually tossed. entire stack is tossed
            elif oList[cOption] == "Toss":
                print("Really Toss? (Yes: Z) (No: X)")
                miniGoBack = False
                while(miniGoBack == False):
                    event2 = keyboard.read_event()
                    if event2.event_type == keyboard.KEY_DOWN and event2.name == "z":
                        soundMade("sfx/menuMove.wav")
                        item.count = 0
                        return item, pLst
                    elif event2.event_type == keyboard.KEY_DOWN and event2.name == "x":
                        soundMade("sfx/menuMove.wav")
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
        #displays the HP and MP stats of your party with nice clean bars
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
        #recover stats based on item type
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



#equipment menu
def equipLoop(pLst, equipInventory):
    goBack = False
    cOption = 0
    while(goBack == False):
        stdscr.clear()
        #displays the names of the entire party, with the current option >'d
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
        #shows the equipment of the highlighted party member         
        if choice == -2:
            a = equipView(pLst[cOption], equipInventory)
            pLst[cOption] = a[0]
            equipInventory = a[1]
        else:
            cOption = choice
    return pLst, equipInventory

#shows the equipment of the highlighted party member
def equipView(pMember, equipInventory):
    cposits = returnCposits()
    cOption = 0
    goBack = False
    while(goBack == False):
        clearToLine(cposits)
        print("-----------------")
        #makes a list of the member's equipment laid out in proper syntax
        dLst = [("Weapon: " + pMember.eWpn.Name), ("Armour: " + pMember.eAmr.Name), ("Accessory: " + pMember.eAcc.Name)]
        for i in range(3):
            cString = " "
            if cOption == i:
                cString=">"
            cString+= dLst[i]
            print(cString)
        print("-----------------")
        #lets me reprint the member's stats so they can change as your equipment changes
        cpositx2 = stdscr.getyx()[1]
        cposity2 = stdscr.getyx()[0]
        pMember.printStats()
        choice = getMenuChoice(cOption, 3)
        if choice == -1:
            goBack = True
        elif choice == -2:
            #one final sub-menu for selecting the piece of equipment to change to
            x = equipChangeMenu(pMember, equipInventory, cOption, cpositx2, cposity2)
            pMember = x[0]
            equipInventory = x[1]
            clearToLine(cposits)
        else:
            cOption = choice
    clearToLine(cposits)
    return pMember, equipInventory

#one final sub-menu for selecting the piece of equipment to change to
def equipChangeMenu(pMember, equipInventory, eChoice, cpositx, cposity):
    #the equpment slot being changed is important as it changes which pieces will be displayed
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
        clearToLine([cpositx, cposity])
        pMember.printStats()
        print("")
        print("-----------------")
        pMember.equip(e)
        cLst = []
        #prints a list of all the equipment, with the currently equipped being preceeded with an E
        for i in range(len(equipInventory)):
            if (equipInventory[i].slot == eChoice and (equipInventory[i].eType == pMember.eType or equipInventory[i].eType == "All")):
                cLst.append(equipInventory[i])
        if cOption == 0:
            print(">E ", e.Name)
        else:
            print(" E ", e.Name)
        #adds useful extra info to the ends of the equipment basd on if it's an improvement
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
        #this code is semi-unnecessary but does fix a small bug
        if cOption == 0:
            print(e.showStats(e))
            print(e.desc)
        else:
            print(cLst[cOption-1].showStats(e))
            print(cLst[cOption-1].desc)
        choice = getMenuChoice(cOption, (len(cLst)+1))
        #swaps out the equipment chosen, and fixes all the necessary menus
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
                    e = pMember.eAcc
                equipInventory.remove(cLst[cOption-1])
        else:
            cOption = choice
    return pMember, equipInventory

#status is very simple and just shows the currently selected member's info. the methods in pMember help with this
#in future, I will need to add the ability to use healing spells from this menu
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

#options lets the player turn sound on or off, and maybe other things later
def optionsLoop():
    stdscr.clear()
    f = open("options.txt")
    oLine = f.readline()
    f.close
    global sound
    if oLine == "Sound: On": 
        cOption = 1
    elif oLine == "Sound: Off":
        cOption = 0
    while True:
        stdscr.clear()
        print(oLine)
        choice = getMenuChoice(cOption, 2)
        if choice == -1:
            soundMade("sfx/menuMove.wav")
            return oLine
        elif choice == 0: 
            soundMade("sfx/menuMove.wav")
            oLine = "Sound: Off"
            sound = False
        elif cOption == 1:
            soundMade("sfx/menuMove.wav")
            oLine = "Sound: On"
            sound = True
        cOption = choice
    




#the main menu, allowing access to items, equipment, status and options menus
#UI data is a pretty menu loaded from a file
def menuLoop(UIdata, itemInventory, equipInventory, pLst):
    loopDone = False
    cOption = 3
    while(loopDone == False):
        stdscr.clear()
        event = keyboard.read_event()
        #increases are in sets of 8 to line up with the pretty menu icons
        #better implementation via curses possible
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            soundMade("sfx/menuMove.wav")
            cOption += 8
            if cOption>27:
                cOption = 3
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            soundMade("sfx/menuMove.wav")
            cOption -= 8
            if cOption <3:
                cOption = 27
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'x'  :
            soundMade("sfx/menuMove.wav")
            return itemInventory, pLst
        elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
            soundMade("sfx/menuMove.wav")
            #depending on selection, open the relevant menu
            if cOption == 3:
                a = itemLoop(pLst[0].itemList, pLst)
                pLst[0].itemList = a[0]
                pLst = a[1]
            elif cOption == 11:
                equipLoop(pLst, equipInventory)
            elif cOption == 19:
                statusLoop(pLst)
            elif cOption == 27:
                #to prevent un-necessary read/write, options menu only writes after completion
                x = optionsLoop()
                f = open("options.txt", "w")
                f.write(x)
                f.close()
        
        for i in range(len(UIdata)):
            string = UIdata[i]
            if (i==cOption):
                string+=" <--"
            print(string)

#imports the set of encounters from the relevant map file
def importMapEncounters(mapName = "Test"):
    global FileName
    string = FileName+"/maps/"+ mapName + "/mapencounter.csv"
    f = open(string)
    g = csv.DictReader(f)
    dictLst = []
    #it's important to move the csv.DictReader file to a list of dictionaries
    #as this allows me to close f
    for line in g:
        dictLst.append(line)
    f.close()
    return dictLst

#chooses the random encounter the player will fight
def chooseEncounter(dict, partyLst):
    chanceCounts = []
    #makes a list of the chances of every individual encounter (should sum to 20 if encounter file correctly written)
    for line in dict:
        chanceCounts.append(int(line["EncNum"]))
    chanceTracker = 0
    for i in range(len(chanceCounts)):
        chanceCounts[i] = chanceCounts[i] + chanceTracker
        chanceTracker = chanceCounts[i]
    a = randint(1, 20)
    finalID = 0
    #chooses a finalID based on the list position of the chosen encounter
    for i in range(len(chanceCounts)):
        if a<=chanceCounts[i]:
            finalID = i
            break
    #starts the battle, and begins the return chain to bring back the relevant info
    for line in dict:
        if int(line["EncID"]) == finalID:
            return startEncounter([line["MemA"], line["MemB"], line["MemC"], line["MemD"]], partyLst)


#starts the battle with the chosen random encounter
def startEncounter(memLst, partyLst):
    enemLst = []
    #only makes an enemy if an actual enemy is in the slot rather than None
    for i in range(4):
        if memLst[i] != "None":
            enemLst.append(enemy(memLst[i]))
    pLst = []
    for i in range(len(partyLst)):
        pLst.append(partyLst[i].makeCombattant())
    transitionStart()
    global sound
    #updates is set to the return of the battle method, so that the pMember can be updated
    updates = battle(pLst, enemLst, sound)
    stdscr.move(0,0)
    transitionStart(True)
    stdscr.move(0,0)
    return updatedParty(partyLst, updates)

#used several times. Makes a smoother screen transition by filling the screen with stars
def transitionStart(direction = False):
    if direction == True:
        for i in range(13):
            print("**********************************************************************")
            sleep(0.02)
    else:
        cPosity = 14
        while(cPosity > 0):
            print("**********************************************************************")
            sleep(0.02)
            cPosity -=1
            stdscr.move(cPosity, 0)

#updates all the attributes that can change after a battle
def updatedParty(partyLst, updates):
    for i in range(len(partyLst)):
        partyLst[i].cHP = updates[0][i].cHP
        partyLst[i].HP = updates[0][i].HP
        partyLst[i].cMP = updates[0][i].cMP
        partyLst[i].MP = updates[0][i].MP
        #gainEXP is used here instead of just adding EXP so that it can automatically use the levelUp method
        partyLst[i].gainEXP(updates[1])
        partyLst[i].spellList = updates[0][i].spellList
    partyLst[0].bCount = updates[0][0].bCount + updates[2]
    partyLst[0].sCount = updates[0][0].sCount
    #if a new party member was gained during the battle, it's added to the party
    if updates[3] != False:
        partyLst.append(pMember(updates[3]))
    return partyLst
    

#the maplayout is just kept in a text file
#it gets made into an array of arrays
def importMapLayout(mapName = "Test"):
    totalLst = []
    global FileName
    string =  FileName+"/maps/" + mapName + "/maplayout.txt"
    f = open(string)
    for line in f:
        localLst = []
        for i in range(len(line)):
            localLst.append(line[i].strip("\n"))
        totalLst.append(localLst)
    f.close()
    return totalLst

#the mapData is a list of all the events, such as chests, NPCs and area transitions
def importMapData(mapName = "Test"):
    global FileName
    string = FileName+"/maps/" + mapName + "/mapdata.csv"
    f = open(string)
    g = csv.DictReader(f)
    totalLst = []
    for row in g:
        totalLst.append(row)
    f.close()
    return totalLst

#if the position being checked matches the event's position, it gets returned, otherwise -1,-1,-1 is returned
def getMapEventPosit(data, x, y):
    for i in range(len(data)):
        if int(data[i]["eventx"]) == x and int(data[i]["eventy"]) == y:
            return [data[i]["eventName"], data[i]["eventContents"], i]
    return[-1, -1, -1]



#changes the overworld sprite dependant on the mcDir value
def getMcDir(mcDir):
    if mcDir == 0:
        return "^"
    elif mcDir == 1:
        return ">"
    elif mcDir == 2:
        return "V"
    elif mcDir == 3:
        return "<"

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

#printMap would in theory be simple, but it should only print the local area around the player in a 20*12 square
def printMap(mdata, mcPositx, mcPosity, mcDir, doStars = False):
    stdscr.move(0,0)
    stdscr.clrtobot()
    cRangex = 20
    cRangey = 12
    #sets the bounds on the screen. max is used to prevent the bounds from going out of list 
    lowrangx = max((mcPositx-cRangex), -1)
    highrangx = min((mcPositx+cRangex), (len(mdata[mcPosity])))
    lowrangy = max((mcPosity-cRangey), -1)
    highrangy = min((mcPosity+cRangey), (len(mdata)))
    #linestr is constructed then printed
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
            #the doStars method means stars will only be printed if the map is being transitioned
            printStars(doStars)              
    stdscr.refresh()



def maxLineLen(data):
    sentlen = 0
    for line in data:
        sentlen = max(sentlen, len(line))
    return sentlen

#main overworld loop
def overWorldLoop(fileName, pLst=[], mcPositx = 15, mcPosity = 5, mapName= "Test", firstStart=True):
    global FileName
    FileName = fileName
    global sound
    sound = importSound()
    somethingHappened = 0
    #make a basic character if the game is just being started
    if (firstStart):
        pLst = [pMember("Troubador", "Wooden Charm")]
    #imports the map layout, data and encounters, as well as the UI for the menu
    mLayout = importMapLayout(mapName)
    mData = importMapData(mapName)
    encData = importMapEncounters(mapName)
    UIData = importUIData()
    #0: North, 1: East, 2: South, 3: West
    mcDir = 2
    leaveMap = False
    #stepcount is used to count the number of steps before the next encounter. it's random in a range
    stepcount = randint(20, 30)
    while(leaveMap == False):
        if somethingHappened == 1:
            mapSave(mapName, mLayout, mData)
            savePlayerData(pLst, mcPositx, mcPosity, mapName)
            somethingHappened = 0
        #loop begins and continues here
        stdscr.clear()
        #when the stepcount runs down, an encounter is started
        if stepcount <=0 and encData[0]["EncNum"] != "-1":
            pLst = chooseEncounter(encData, pLst)
            stepcount = randint(20, 30)
            stdscr.move(0,0)
            #map is printed again with the stars
            printMap(mLayout, mcPositx, mcPosity, mcDir, True)
        else:
            printMap(mLayout, mcPositx, mcPosity, mcDir)
        if firstStart == True:
            print("Your head hurts like hell. You're still clutching the pipe you used for your escape")
            waitSpace()
            print("Well, you'd better look around")
            waitSpace()
            print("CONTROLS: Arrow Keys to move. Z to interact and confirm, X to go back. C opens the menu")
            waitSpace()
            firstStart = False
        event = keyboard.read_event()
        #moves the main character and changes their direction. If the space that would be moved to isn't empty, the move doesn't occur
        if event.event_type == keyboard.KEY_DOWN and event.name == 'down':
            mcDir = 2
            if mLayout[mcPosity+1][mcPositx] == "." :
                mcPosity +=1
                stepcount -=1
            somethingHappened = 1
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'up':
            mcDir = 0
            if mLayout[mcPosity-1][mcPositx] == "." :
                mcPosity -=1
                stepcount -=1
            somethingHappened = 1
        elif event.event_type == keyboard.KEY_DOWN and event.name == "right":
            mcDir = 1
            if mLayout[mcPosity][mcPositx+1] == "." :
                mcPositx +=1
                stepcount -=1
            somethingHappened = 1
        elif event.event_type == keyboard.KEY_DOWN and event.name == "left":
            mcDir = 3
            if mLayout[mcPosity][mcPositx-1] == "." :
                mcPositx -=1
                stepcount -=1
            somethingHappened = 1
        #opens the menu if this key is pressed
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'c'  :
            a = menuLoop(UIData, pLst[0].itemList, pLst[0].equipList, pLst)
            pLst[0].itemList = a[0]
            pLst = a[1]
            somethingHappened = 1
        #checks the tile in front of the player
        elif event.event_type == keyboard.KEY_DOWN and event.name == "z":
            #first, the position they're checking is gotten
            coord = getCheckCoord(mcPositx, mcPosity, mcDir)
            #then, the list of events is checked against the position being checked
            eventPosit = getMapEventPosit(mData, coord[0], coord[1])
            if (eventPosit!=([-1, -1, -1])):
                #eventhandler handles the event, then the relevant fields are updated
                invData = eventHandler(eventPosit, pLst[0].itemList, pLst[0].equipList, pLst[0].bCount, pLst[0].sCount)
                pLst[0].itemList = invData[0]
                pLst[0].equipList = invData[1]
                pLst[0].bCount = invData[3]
                pLst[0].sCount = invData[4]
                if invData[5] == True:
                    printMap(mData, mcPositx, mcPosity, mcDir, True)
                    for member in pLst:
                        member.cHP = member.HP
                        member.cMP = member.MP
                    print("You rested for a while, and recovered your strength")
                    waitSpace()
                
                
                if invData[2] == "None":
                    if (eventPosit[0] == "chestItem" or eventPosit[0] =="chestEquip"):
                        mLayout[coord[1]][coord[0]] = "."
                        mData.pop(eventPosit[2])
                #if the position being checked is an area transition
                else:
                    #saves the current map's data to the file
                    mapSave(mapName, mLayout, mData)
                    #sets the map and player position to the new map
                    mapName = invData[2][0]
                    mcPositx = int(invData[2][1])
                    mcPosity = int(invData[2][2])
                    mLayout = importMapLayout(mapName)
                    mData = importMapData(mapName)
                    encData = importMapEncounters(mapName)
                    printMap(mLayout, mcPositx, mcPosity, mcDir, True)
            somethingHappened = 1

#saves the current map's data to the relevant file
def mapSave(mapName, mLayout, mData):
    try:
        global FileName
        f = open(FileName+"/maps/" + mapName+"/maplayout.txt", "w")
        for line in mLayout:
            f.write("".join(line)+"\n")
        f.close()
        g = open(FileName+"/maps/" + mapName+"/mapdata.csv", "w")
        #lineterminator is used here so that the lines dont' have gaps
        gWriter = csv.writer(g, lineterminator="")
        gWriter.writerow(mData[0].keys())
        gWriter.writerow("\n")
        for line in mData:
            gWriter.writerow(line.values())
            gWriter.writerow("\n")
        g.close()
    except:
        pass
        





#handles the events. has access to the relevant fields to change
def eventHandler(data, Iinventory, Einventory, bCount, sCount):
    areaChange = "None"
    fullHeal = False
    #adds items in any quantity from 1-9 to the inventory
    if data[0] == "chestItem":
        soundMade("sfx/pickupCoin.wav")
        waitSpace()
        quant = int(data[1][-1])
        dataName = data[1][:-1]
        Iinventory.append(item(dataName, quant))
        print("You found ", quant, " ", dataName, "(s)!")
        Iinventory = combineStacks(Iinventory)
        waitSpace()
    #adds a single piece of equipment to the inventory
    elif data[0] == "chestEquip":
        dataName = data[1]
        Einventory.append(equipment(dataName))
        print("You found a ", dataName)
        waitSpace()
    #displays a single line of dialogue
    elif data[0] == "npc":
        print(data[1])
        waitSpace()
    #transitions the player to a different area
    elif data[0] == "areaTrans":
        areaChange = data[1].split(",")
    elif data[0] == "shop":
        x = shopMenu(data[1], Iinventory, Einventory, bCount, sCount)
        Iinventory = x[0]
        Iinventory = combineStacks(Iinventory)
        Einventory = x[1]
        bCount = x[2]
        sCount = x[3]
    elif data[0] == "campfire":
        fullHeal = True
    return Iinventory, Einventory, areaChange, bCount, sCount, fullHeal

#opens the menu for the item shop
def shopMenu(data, Iinventory, Einventory, bCount, sCount):
    with open("shopdata.csv") as shopdata:
        shops = csv.DictReader(shopdata)
        for row in shops:
            if row["shopID"] == data:
                shopDict = row
    shopInv = list(shopDict["shopInventory"].split(","))
    shopContinuing = True
    print(shopDict["shopText"])
    cposits = returnCposits()
    shopInvLst = []
    for i in range(0,len(shopInv), 2):
        if shopDict["shopType"] == "Item":
            shopInvLst.append(item(shopInv[i], 1, int(shopInv[i+1])))  
        elif shopDict["shopType"] == "Equipment":
            shopInvLst.append(equipment(shopInv[i], int(shopInv[i+1]))) 
    cOption = 0
    while(shopContinuing):
        clearToLine(cposits)
        if shopDict["shopCurrency"] == "Sticks and Stones":
            print("Sticks and Stones: ", sCount)
        elif shopDict["shopCurrency"] == "Blood and Bones":
            print("Blood and Bones: ", bCount)
        for i in range(len(shopInvLst)):
            cString = " "
            if i == cOption:
                cString = ">"
            cString+=shopInvLst[i].Name
            for j in range(15-len(cString)):
                cString+=" "
            cString+="||"
            cString+= str(shopInvLst[i].cost)
            cString+=" "
            cString+=shopDict["shopCurrency"]
            print(cString)
        choice = getMenuChoice(cOption, len(shopInvLst))
        if choice == -1:
            return Iinventory, Einventory, bCount, sCount
        elif choice == -2:
            if shopDict["shopCurrency"] == "Sticks and Stones":
                if shopInvLst[cOption].cost <= sCount:
                    print("You bought", shopInvLst[cOption].Name)
                    waitSpace()
                    if shopDict["shopType"] == "Item":
                        Iinventory.append(shopInvLst[cOption])
                    elif shopDict["shopType"] == "Equipment":
                        Einventory.append(shopInvLst[cOption])
                    sCount -= shopInvLst[cOption].cost
                else:
                    print("You didn't have enough...")
                    waitSpace()
            elif shopDict["shopCurrency"] == "Blood and Bones":
                if shopInvLst[cOption].cost <= bCount:
                    print("You bought", shopInvLst[cOption].Name)
                    if shopDict["shopType"] == "Item":
                        Iinventory.append(shopInvLst[cOption])
                    elif shopDict["shopType"] == "Equipment":
                        Einventory.append(shopInvLst[cOption])
                    bCount -= shopInvLst[cOption].cost
                else:
                    print("You didn't have enough...")
            
        else:
            cOption = choice


#if an item the player already has is added, this makes sure they're stacked together
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


        

#gets the location the player is checking based on where they're facing
def getCheckCoord(mcPositx, mcPosity, mcDir):
    if mcDir == 0:
        return (mcPositx, (max((mcPosity-1), 0)))
    elif mcDir == 1:
        return (max((mcPositx+1), 0), mcPosity)
    elif mcDir == 2:
        return (mcPositx, (max((mcPosity+1), 0)))
    elif mcDir == 3:
        return (max((mcPositx-1), 0), mcPosity)

