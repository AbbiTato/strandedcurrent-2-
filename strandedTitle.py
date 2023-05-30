import curses
import os
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


print("   _____ _______ _____            _   _ _____  ______ _____")  
print("  / ____|__   __|  __ \     /\   | \ | |  __ \|  ____|  __ \\") 
print(" | (___    | |  | |__) |   /  \  |  \| | |  | | |__  | |  | |")
print("  \___ \   | |  |  _  /   / /\ \ | . ` | |  | |  __| | |  | |")
print("  ____) |  | |  | | \ \  / ____ \| |\  | |__| | |____| |__| |")
print(" |_____/   |_|  |_|  \_\/_/    \_\_| \_|_____/|______|_____/")                                                                                                                   