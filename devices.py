"""

devices.py

This script contains classes that represent real world devices.

"""

class Crane:
    """The crane class represents a single crane that
    can pickup and dropoff loads.
    """
    def __init__(self, crane_nbr):
        """Constructor for the crane.  Set initial
        variables."""
        self.crane_nbr = crane_nbr
        if crane_nbr == 1:
            # start crane 1 at bay 1
            self.bay = 1
            self.target_bay = 1
        else:
            # start crane 2 at bay 20
            self.bay = 20
            self.target_bay = 20
        self.level = 1
        self.target_level = 1
        self.picking = False
        self.depositing = False
        self.load = Load(load_id='1234')
        self.active_command = False
        
    def run(self):
        """This method is called every cycle and simulates
        movement and other actions"""
        at_target_bay = self.target_bay == self.bay
        at_target_level = self.target_level == self.level
        at_target_position = at_target_bay and at_target_level
        
        # move crane if not at target position
        if not at_target_bay:
            if self.target_bay < self.bay:
                self.bay -= 1
            elif self.target_bay > self.bay:
                self.bay += 1
                
        if not at_target_level:
            if self.target_level < self.level:
                self.level -= 1
            elif self.target_level > self.level:
                self.level += 1
                
        if at_target_position and self.picking:
            load = Locations.locations[self.bay][self.level]
            self.load = load
            Locations.locations[self.bay][self.level] = None
            self.picking = False
        
        if at_target_position and self.depositing:
            load = Locations.locations[self.bay][self.level]
            self.load = load
            Locations.locations[self.bay][self.level] = None
            self.picking = False
        
class Conveyor:
    """Represents a single conveyor section"""
    shipped_loads = 0
    def __init__(self, side, zone, is_rack_entry=False, is_system_exit=False):
        self.running = False
        self.side = side
        self.zone = zone
        self.is_rack_entry = is_rack_entry
        self.is_system_exit = is_system_exit
        
    def run(self):
        """This method is called every cycle and simulates
        movement and other actions"""
        if not self.is_rack_entry:
            if self.is_system_exit:
                if not self.running and Locations.locations[self.side - 1][self.zone - 1]:
                    self.running = True
                else:
                    self.running = False
                    if Locations.locations[self.side - 1][self.zone - 1]:
                        Locations.locations[self.side - 1][self.zone - 1] = None
                        # load has been shipped!
                        Conveyor.shipped_loads += 1
                    
            else:
                load = Locations.locations[self.side - 1][self.zone - 1]
                next_zone_load = Locations.locations[self.side - 1][self.zone]
                if self.running:
                        if load and not next_zone_load:
                            Locations.locations[self.side - 1][self.zone] = load
                            Locations.locations[self.side - 1][self.zone - 1] = None
                            self.running = False
                elif load and not next_zone_load:
                    self.running = True

    
class Load:
    """Represents a single load with an id"""
    def __init__(self, load_id):
        self.load_id = load_id
        
class LoadCreator:
    """The load creator class adds loads to the system"""
    def __init__(self):
        self.load_id = 1
        
    def create_load(self):
        if not Locations.locations[0][0]:
            Locations.locations[0][0] = Load(str(self.load_id).zfill(4))
            self.load_id += 1
        
        
class Locations:
    """20x5 rack. 3 conveyor sections each side.
    """
    locations = [
        [None, None, None], # conveyors
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None], 
        [None, None, None, None, None], 
        [None, None, None, None, None],
        [None, None, None, None, None], 
        [None, None, None, None, None], 
        [None, None, None, None, None], 
        [None, None, None, None, None],
        [None, None, None, None, None], 
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None], # conveyors
    ]