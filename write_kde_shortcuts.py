#!/usr/bin/env python3
import sys, getopt, os, argparse, random, subprocess, re

# Given a line determine what type it is.  If there is an "=" then it is
# something we want to check against our dictionary. Make a key from
# the line of text and search the dictionary for a value.

def write_line_out(input_line):
    output_line =''
    key  = re.search('(.+?)=', input_line)

    if key:
        from_dictionary = line_dict.get(key.group(0))
        if from_dictionary:
            output_line = from_dictionary + '\n'
            print(output_line)
        else:
            output_line = input_line
    else:
        output_line = input_line
    customized_file.write(output_line)   
    return

def is_line_blank(line):
    
    # If a line is blank, return True.

    if re.search('^\s*$', line):
        blank = True
    else:
        blank = False

    return blank

def write_block(line):

    written = False
    key = re.search("\[.*?\]", line)
    print (key)
    if key:
        from_dictionary = block_dict.get(key.group(0))
        print (key.group(0))
        if from_dictionary:
            print ("We have a match!\n")
            print (from_dictionary + "\n")
            customized_file.write(from_dictionary)
            for item in block_list:
                if key.group(0) == item[0]:
                        print ("List item is " + item[0] + "\n")
                        item[1] = True
                        print (item)
            written = True 
            
    return written



# Key, value pairs. Value will be written to config file in place of
# existing line in that file.
line_dict = {
        'Switch to Desktop 1=':'Switch to Desktop 1=Meta+1,,Switch to Desktop 1',
        'Switch to Desktop 2=':'Switch to Desktop 2=Meta+2,,Switch to Desktop 2',
        'Switch to Desktop 3=':'Switch to Desktop 3=Meta+3,,Switch to Desktop 3',
        'Switch to Desktop 4=':'Switch to Desktop 4=Meta+4,,Switch to Desktop 4',
        'Switch to Desktop 5=':'Switch to Desktop 5=Meta+5,,Switch to Desktop 5',
        'Switch to Desktop 6=':'Switch to Desktop 6=Meta+6,,Switch to Desktop 6',
        'Switch to Screen 0=':'Switch to Screen 0=Meta+Ctrl+2,,Switch to Screen 0',
        'Switch to Screen 1=':'Switch to Screen 1=Meta+Ctrl+1,,Switch to Screen 1',
        'Switch to Screen 2=':'Switch to Screen 2=Meta+Ctrl+3,,Switch to Screen 2',
        'Window to Desktop 1=':'Window to Desktop 1=Meta+!,,Window to Desktop 1',
        'Window to Desktop 2=':'Window to Desktop 2=Meta+@,,Window to Desktop 2',
        'Window to Desktop 3=':'Window to Desktop 3=Meta+#,,Window to Desktop 3',
        'Window to Desktop 4=':'Window to Desktop 4=Meta+$,,Window to Desktop 4',
        'Window to Desktop 5=':'Window to Desktop 5=Meta+%,,Window to Desktop 5',
        'Window to Desktop 6=':'Window to Desktop 6=Meta+^,,Window to Desktop 6',
        'Overview=':'Overview=Meta+O,,Toggle Overview',


}



dolphin_entry = """
[org.kde.dolphin.desktop]
_k_friendly_name=Dolphin
_launch=Meta+F\tMeta+E,Meta+E,Dolphin
"""
dolphin_data = ["[org.kde.dolphin.desktop]",False, 3, dolphin_entry]

terminal_entry = """
[org.kde.konsole.desktop]
NewTab=none,none,Open a New Tab
NewWindow=none,none,Open a New Window
_k_friendly_name=Konsole
_launch=Ctrl+Alt+T\tMeta+Return,none,Konsole
"""
terminal_data = ["[org.kde.konsole.desktop]", False, 5, terminal_entry]

keepassxc_entry = """
[org.keepassxc.KeePassXC.desktop]
_k_friendly_name=KeePassXC
_launch=Meta+K,none,KeePassXC
"""
keepassxc_data = ["[org.keepassxc.KeePassXC.desktop]", False, 3, keepassxc_entry]


email_entry = """
[thunderbird.desktop]
ComposeMessage=none,none,Write new message
OpenAddressBook=none,none,Open address book
_k_friendly_name=Thunderbird
_launch=Meta+M,none,Thunderbird
"""
email_data = ["[thunderbird.desktop]", False, 5, email_entry]


browser_entry = """
[firedragon.desktop]
_k_friendly_name=FireDragon
_launch=Meta+W,none,FireDragon
new-private-window=none,none,New Private Window
new-window=none,none,New Window
"""
browser_data = ["[firedragon.desktop]", False, 5, browser_entry]


block_dict = {
        
        '[org.kde.dolphin.desktop]':dolphin_entry,
        '[org.kde.konsole.desktop]':terminal_entry,
        '[org.keepassxc.KeePassXC.desktop]':keepassxc_entry,
        '[thunderbird.desktop]':email_entry,
        '[firedragon.desktop]':browser_entry
}

block_list = (dolphin_data, terminal_data, email_data, keepassxc_data, browser_data)



################################################################
#
#              Execution Starts Here
#
################################################################



# Check for existance of "new_kglobalshortcutsrc" and delete it
# if it exists
filePath = "new_kglobalshortcutsrc"
if os.path.exists(filePath):
    os.remove(filePath)
    # print("Removed old copy of new_kglobalshortcutsrce")

original_file = open("kglobalshortcutsrc", "rt")
customized_file = open("new_kglobalshortcutsrc", "w")

# Read config file in a line at a time, make changes if needed
# and write out to new file.

# Handle blocks, like .desktop entries by knowing when we are 
# replacing one and if so, throw away the old one by not writing 
# the lines out to the new customized file.  When we start replacing
# a block, just throw away all the lines in the original file until
# we get to a blank line.  Most of the time this replacemt won't happen since
# the purpose of this program is to take a new install of KDE and 
# add shortcuts.  The .desktop shortcuts won't be there and will 
# usually be added by the code that goes through the block_list and 
# checks to see if that block has been written or not.  Usually 
# it hasn't been and that code will then write it at the end of the
# modified file.
skip_to_block_end = False

for line in original_file:
    if (is_line_blank(line)):
        skip_to_block_end = False

    if not (skip_to_block_end):
        # write_block() will test line to see if its the start of a block
        # we are interested in replacing.  If so, it will write that block
        # to the new file.
        if (write_block(line)):
            skip_to_block_end = True 
        else:
            # either write an unmodified line, or if a change is
            # needed, write out a modified line
            write_line_out(line) 

# Go through list of blocks to be modified and modify them
# now if they weren't replaced.  On a fresh file, the entries
# won't exist, so they will not be replaced so they need to be added.

for entry in block_list:
    if not entry[1]:
        print ("dictionary block to write: " + block_dict.get(entry[0] ))
        customized_file.write(block_dict.get(entry[0]))



original_file.close()
customized_file.close()



