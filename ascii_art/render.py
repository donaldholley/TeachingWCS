"""

render.py

This script is responsible for rendering ascii art based on the
current state of the crane, conveyors, and loads

"""

from os import system, name
from devices import Conveyor

class RenderObject:
    """an object containing a 2d list of characters to be
    rendered in the terminal"""
    def __init__(self, filename, buffer_x=0, buffer_y=0):
        art_file = open(filename, 'r')
        self.characters = []
        lines = art_file.read().splitlines() 
        ascii_size = len(lines[0]) + buffer_x * 2
        for _ in range (buffer_y):
            self.characters.append([' ' for _ in range(ascii_size)])
        for line in lines:
            buff_x = [' ' for _ in range(buffer_x)]
            self.characters.append(buff_x + [character for character in line] + buff_x)
            line = art_file.readline()
        for _ in range (buffer_y):
            self.characters.append([' ' for _ in range(ascii_size)])
        art_file.close()
        
    def insert_characters(self, character_list, row_offset, col_offset):
        """insert list of characters, the coordinates represent the bottom left of the 2d list"""
        for row in range(len(character_list)):
            for col in range(len(character_list[row])):
                self.characters[row_offset+row][col_offset+col] = character_list[row][col]
        
        

def render(system_state):
    """One rendering of the current state of the system""" 
    
    # first clear the terminal
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
    crane1_ascii = RenderObject('ascii_art/cranes/cranelvl' + str(system_state.cranes[0].level) + '.txt')
    crane2_ascii = RenderObject('ascii_art/cranes/cranelvl' + str(system_state.cranes[1].level) + '.txt')
    conv_asciis = [RenderObject('ascii_art/conveyor.txt'),RenderObject('ascii_art/conveyor.txt'),RenderObject('ascii_art/conveyor.txt'),
                   RenderObject('ascii_art/conveyor.txt'),RenderObject('ascii_art/conveyor.txt'),RenderObject('ascii_art/conveyor.txt')]
    rack = RenderObject('ascii_art/rack.txt', 30, 5)
    floor = [['-' for _ in range(180)]]
    for i in range(len(conv_asciis)):
        conv = system_state.conveyors[i]
        rack.insert_characters(conv_asciis[i].characters, 9,
                               6 + conv.zone * 6 + 138 * (conv.side - 1))
        
    for bay in range(len(system_state.locations)):
        for level in range(len(system_state.locations[bay])):
            if system_state.locations[bay][level]:
                load = system_state.locations[bay][level]
                id_list = [num for num in load.load_id]
                on_conveyor = bay in [0, 21]
                if on_conveyor:
                    load_level = 9
                    load_bay = (13 + 6 * level if bay == 0 else 180 + 6 * level) 
                else:
                    load_level = 9 - level
                    load_bay =  bay * 6 + 25
                rack.insert_characters([id_list,], load_level, load_bay)
    
    rack.insert_characters(crane1_ascii.characters, 4,
                           system_state.cranes[0].bay * 6 + 22)
    rack.insert_characters(crane2_ascii.characters, 4,
                           system_state.cranes[1].bay * 6 + 22)
    
    if system_state.cranes[0].load:
        rack.insert_characters([[c for c in system_state.cranes[0].load.load_id]],
                               10 - system_state.cranes[0].level,
                               system_state.cranes[0].bay * 6 + 25)
    if system_state.cranes[1].load:
        rack.insert_characters([[c for c in system_state.cranes[1].load.load_id]],
                               10 - system_state.cranes[1].level,
                               system_state.cranes[1].bay * 6 + 25)
    
    rack.insert_characters(floor, 11, 0)
    rack.insert_characters([['S','H','I','P','P','E','D',' ','L','O','A','D','S',':',' '] + [c for c in str(Conveyor.shipped_loads)]], 1, 75)
    
    # print to terminal
    for row in rack.characters:
        print(''.join(row))
        
