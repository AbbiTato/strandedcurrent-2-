from strandedBattle import ally, enemy, battle

h  = ally(0, "Hero", 15, 15, 20, 20, 5, 3, 0, 18, 2, 4, ["Blaze", "Icestorm", "Cure", "PowerUP", "Mass Fortify"])
f = ally(1, "Florp", 8, 8, 0, 0, 5, 0, 0, 18, 2, 4)
f2 = ally(2, "Eyesoar", 12, 12, 4, 4, 7, 2, 0, 18, 2, 4,  ["Blaze"])
f3 = ally(3, "Mousile", 18, 18,  0, 0, 15, 0, 0, 18, 2, 4)
y = enemy("Florp")
y2 = enemy("Eyesoar")
y3 = enemy("Florp") 
y4 = enemy("Florp")                                      
battle(h, f, f2, f3, y, y2, y3, y4)                                                                                                                                                 