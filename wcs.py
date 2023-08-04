import time
from ascii_art.render import render
from devices import Crane, Conveyor, LoadCreator, Locations
import plc_client

class SystemState:
    """Overall state of the warehouse system.
    Keeps track of locations, cranes, loads, and conveyors"""
    cranes = [Crane(1), Crane(2)]
    locations = Locations.locations
    conveyors = [Conveyor(1,1), Conveyor(1,2), Conveyor(1,3,True),
                 Conveyor(2,1), Conveyor(2,2), Conveyor(2,3,False,True)]
    
    @classmethod
    def checkstate(cls):
        """check for fault such as collisions"""
        if cls.cranes[0].bay <= cls.cranes[1].bay - 2:
            # too close
            pass
        

def main_loop():
    # main wcs loop.  This sets up everything to run together.  The
    # ascii art is rendered, the devices are processed, and the plc_client
    # logic is processed.
    
    load_creator = LoadCreator()
    
    while(True):
        time.sleep(1)
        
        # the code below is simulating the real world
        # 'render' will display the current state of things on your terminal
        # the two loops will simulation what the real world devices would do
        render(SystemState)
        load_creator.create_load()
        for crane in SystemState.cranes:
            crane.run()
        for conveyor in SystemState.conveyors:
            conveyor.run()
            
        # now your plc_client main loop is called
        # this should run all of your decision making logic
        # to tell the cranes what to do.
        plc_client.process(SystemState)
        
if __name__ == '__main__':
    main_loop()
        