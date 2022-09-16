from random import randint


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

    def find_starting_position(self, width=1, height=1):
        """
        Finds a starting position for the Entity in the map.
        The surrounding area must comport the Entity size.
        """
        found = False

        while found == False:

            found = True

            # Generate random position that could fit the entity, remove map border.
            x = randint(0, self.size - width)
            y = randint(0, self.size - height)

            # Check if space is empty, respecting entity size.
            for pos_y in range(y, y + height):
                for pos_x in range(x, x + width):
                    if self.map[pos_y][pos_x] != ' ':
                        found = False
                        break
                if found == False:
                    break

        return (x, y)

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
