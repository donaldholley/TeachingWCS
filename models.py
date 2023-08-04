class CraneWork:
    """An object comprised of 1 or more crane commands.
    """
    def __init__(self):
        # TODO a cranework should be comprised of multiple crane
        # commands.  A crane work's purpose is to use the crane
        # to move a load from 1 location to another.
        pass
        
class CraneCommand:
    """A single crane command, can be a pickup, deposit, or position."""
    def __init__(self, command_type, bay, level):
        self.command_type = command_type
        self.bay = bay
        self.level = level
        # TODO a crane command represents a single movement or action that
        # is part of a bigger task.  It can be just movement, just a
        # pickup/dropoff, or both.  How much a crane command does is up
        # to the developers.
        
    def send(self, crane):
        """send a command to a crane"""
        # TODO look at the crane class and piece together
        # how you can set crane values to make the cranes move.