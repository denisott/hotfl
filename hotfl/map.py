class Map:
    """Class that encapsulates all map stuff."""

    def __init__(self, size):
        """Creates a new map instance."""
        self.size = size
        self.map = []
        self.initialize()

    def initialize(self):
        """Initializes all map positions."""
        self.map = []
        for y in range(self.size):
            line = []
            for x in range(self.size):
                line.append(' ')
            self.map.append(line)

    def add_entity(self, entity):
        """Puts the Entity symbol in the map."""
        for pos_y in entity.y:
            for pos_x in entity.x:
                self.map[pos_y][pos_x] = entity.symbol

    def remove_entity(self, entity):
        """Removes entity symbol from the map."""
        for pos_y in entity.y:
            for pos_x in entity.x:
                self.map[pos_y][pos_x] = ' '