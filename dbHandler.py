import sqlite3

def makedbntbls1():
    con = sqlite3.connect("strandedData.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE spellData(spellID INT(3) NOT NULL PRIMARY KEY, spellName VARCHAR(20) NOT NULL,
     mpCost INT(2) NOT NULL, basePower INT(3) NOT NULL, multiPl DECIMAL(5,3) NOT NULL,
                type VARCHAR(10) NOT NULL, target VARCHAR(10) NOT NULL, descP VARCHAR(100))""") 
    cur.execute("""
                CREATE TABLE entData(sprID INT(3), entID INT(3) NOT NULL PRIMARY KEY, entName VARCHAR(20), HP INT(3),
                 MP INT(3), STR INT(2), RES INT(2), ITL INT(2), CHA INT(2), DEX INT(2), 
                physGrow INT(2), magGrow INT(2), finGrow INT(2), descP VARCHAR(100))
                """)
    cur.execute("""CREATE TABLE entSpells(entID INT(3) NOT NULL, spellID INT(3) NOT NULL, spellRank INT(2),
                FOREIGN KEY(entID) REFERENCES entData(entID), FOREIGN KEY(entID) REFERENCES entData(entID))
                """)
    cur.execute("CREATE TABLE itemData(itemID INT(3) NOT NULL PRIMARY KEY, name VARCHAR(30), canEquip BOOLEAN NOT NULL, usable BOOLEAN, price INT(4), descP VARCHAR(100), power INT(3), rtype VARCHAR(4))")
    cur.execute("CREATE TABLE equipData(itemID INT(3) NOT NULL, eSlot VARCHAR(10), aBonus INT(3), dBonus INT(3), mBonus INT(3), hitDodge INT(4), cBonus INT(4), FOREIGN KEY(itemID) REFERENCES itemData(itemID))")
    cur.execute("CREATE TABLE shopData(shopID INT(3) NOT NULL PRIMARY KEY, entryText VARCHAR(100), currencTyp CHAR(1))")
    cur.execute("CREATE TABLE shopItem(itemID INT(3) NOT NULL, shopID INT(3) NOT NULL, FOREIGN KEY(itemID) REFERENCES itemData(itemID), FOREIGN KEY(shopID) REFERENCES shopData(shopID))")
    cur.execute("""
                INSERT INTO spellData(spellID, spellName, mpCost, basePower, multiPl, type, target, descP) VALUES
                (1, 'Bal', 2, 5, 1.0, 'DMG', 'enemOne', 'Attack one enemy with a small bolt of energy'),
                (2, 'Oscyll', 5, 10, 0.8, 'DMG', 'enemAll', 'Attack a group of enemies with painful vibrations'),
                (3, 'Suuth', 3, 10, 0.8, 'HEAL', 'partyOne', 'Close one party members wounds'),
                (4, 'Wysuuthma', 14, 30, 1.0, 'HEAL', 'partyAll', 'Soothe the pain of your entire group'),
                (5, 'Chae', 8, 0, 0.5, 'cATK', 'partyOne', 'Raise a party members ATK with a rallying cry'),
                (6, 'Wydyssul', 12, 0, -0.2, 'cDEF', 'enemOne', 'Dissolve the DEF of all enemies with acid'),
                (7, 'Wyemus', 12, 0, 0.3, 'cMATK', 'partyAll', 'Amass psychic energy for your entire group, raising their mATK'),
                (8, 'Roaf', 8, 0, -0.3, 'cDEX', 'enemOne', 'Roughen one enemy, lowering their DEX')
                """)
    
    cur.execute("""
                INSERT INTO entData(sprID, entID, entName, HP, MP, STR, RES, ITL, CHA, DEX, physGrow, magGrow, finGrow, descP) VALUES
                (1, 1, 'Florp', 15, 6, 4, 0, 2, 1, 4, 2, 5, 3, 'A small, squishy bird-like creature preyed upon by most of the planets inhabitants'),
                (2, 2, 'Eyesoar', 19, 8, 3, 0, 0, 4, 5, 1, 7, 2, 'Hundreds of floating eyes. They regard most creatures coldly while floating out on unknowable errands'),
                (0, 3, 'Strandee', 12, 0, 5, 0, 5, 0, 5, 3, 3, 3, 'Stranded after their escape from the dastardly damocles, their desire for revenge burns bright')
                """)
    cur.execute("""
                INSERT INTO entSpells(entID, spellID, spellRank) VALUES
                (1, 3, 1),
                (1, 1, 2),
                (1, 5, 3),
                (2, 5, 1),
                (2, 2, 2),
                (2, 6, 3)
                """)
    cur.execute("""INSERT INTO itemData(itemID, name, canEquip, usable, price, descP, power, rtype) VALUES
                (1, 'Healing Herb', 0, 1, 10, 'This simple herb is a fixture of the planets simple but effective herbal remedies', 30, 'hp'),
                (2, 'Lead Pipe', 1, 0, 20, 'A heavy and inaccurate leaden pipe. A symbol of your furious rebellion', 0, ''),
                (3, 'Spiked Branch', 1, 0, 50, 'Watch it with the spikes! An accurate and strong weapon', 0, ''),
                (4, 'Dirty Rags', 1, 0 , 20, 'The rags that covered your body as you worked under damocles. Dont offer much protection', 0, ''),
                (5, 'Leather Jerkin', 1, 0, 60, 'Simple defensive armour made from florp leather', 0, ''),
                (6, 'Iron Gauntlets', 1, 0, 40, 'These iron gloves deflect certain blows', 0, ''),
                (7, 'Main-Gauche', 1, 0, 80, 'An offhand knife that raises attack power', 0, ''),
                (8, 'Magic charm', 1, 0, 100, 'This handmade charm raises magical strength', 0, ''),
                (9, 'Beastial Power', 1, 0, 0, 'Every monster, from the lowliest florp to the mightiest beast has its own way to defend itself', 0, ''),
                (10, 'Beastial Guard', 1, 0, 0, 'Every monster, from the lowliest florp to the mightiest beast has some kind of armour', 0, ''),
                (11, 'None', 1, 0, 0, 'Nothing equipped', 0, '')
                """)
    cur.execute("""INSERT INTO equipData(itemID, eSlot, aBonus, dBonus, mBonus, hitDodge, cBonus) VALUES
                (2, 'Weapon', 5, 0, 0, 14, 4),
                (3, 'Weapon', 8, 0, 0, 17, 0),
                (4, 'Armour', 0, 0, 0, 2, 0),
                (5, 'Armour', 3, 0, 0, 4, 0),
                (6, 'Accessory', 0, 5, 0, 0, 0), 
                (7, 'Accessory', 5, 0, 0, 0, 3),
                (8, 'Accessory', 0, 0, 5, 0, 0),
                (9, 'Weapon', 5, 0, 0, 17, 1),
                (10, 'Armour', 2, 0, 0, 2, 0),
                (11, 'Accessory', 0, 0, 0, 0, 0)
                """)
    cur.execute("""INSERT INTO shopData(shopID, entryText, currencTyp) VALUES
                (0, 'Welcome to my shop! We trade in blood and bones', 'b'),
                (1, 'Welcome to my shop! We trade in sticks and stones', 's')
                """)
    cur.execute("""INSERT INTO shopItem(itemID, shopID) VALUES
                (5, 0),
                (6, 0),
                (7, 1),
                (8, 1)
                """)
    print(cur.execute("""SELECT * FROM itemData""").fetchall())
    print(cur.execute("""SELECT * FROM equipData""").fetchall())
    print(cur.execute("SELECT equipData.itemID, itemData.name, itemData.price, itemData.descP, eSlot, aBonus, dBonus, mBonus, hitDodge, cBonus FROM equipData INNER JOIN itemData ON equipData.itemID = itemData.itemID WHERE equipData.itemID =11").fetchall()[0])
    print(cur.execute("""SELECT * FROM shopData""").fetchall())
    print(cur.execute("""SELECT * FROM shopItem""").fetchall())
    con.commit()
    print(cur.execute("SELECT spellID, spellName, basePower FROM spellData").fetchall())
    print(cur.execute("SELECT entID, entName, MP FROM entData").fetchall())
    print(cur.execute("SELECT spellID, entID, spellRank FROM entSpells").fetchall()[0][2])
    cur.close()

    
def reversedbtbls():
    con = sqlite3.connect("strandedData.db")
    cur = con.cursor()
    try:
        cur.execute("DROP TABLE spellData")
    except:
        pass
    try:
        cur.execute("DROP TABLE entSpells")
    except:
        pass
    try:
        cur.execute("DROP TABLE entData")
    except:
        pass
    try:
        cur.execute("DROP TABLE itemData")
    except:
        pass
    try:
        cur.execute("DROP TABLE equipData")
    except:
        pass
    try:
        cur.execute("DROP TABLE shopData")
    except:
        pass
    try:
        cur.execute("DROP TABLE shopItem")
    except:
        pass


    
reversedbtbls()
makedbntbls1()