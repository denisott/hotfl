class Entity:
    """Class that describes a Entity in the map."""

    def __init__(self, name, x, y, width, height, symbol):
        """
        Creates a new Entity, with name, symbol for the map
        Entity size and starting position
        """
        self.name = name
        self.symbol = symbol
        self.x = []
        self.y = []

        for position in range(x, x + width):
            self.x.append(position)

        for position in range(y, y + height):
            self.y.append(position)


class Creature(Entity):
    """Class for living creatures."""

    def __init__(self, name, x, y, symbol):
        """
        Creates a creture, with alive as default.
        All creatures occupy only on position in the map.
        """
        super().__init__(name, x, y, 1, 1, symbol)
        self.alive = True

    def move(self, direction):
        """
        Moves the creature in desired direction.
        Diagonal movement is accepted.
        """
        if direction.__contains__('N'):
            self.y[0] -= 1
        if direction.__contains__('S'):
            self.y[0] += 1
        if direction.__contains__('E'):
            self.x[0] += 1
        if direction.__contains__('W'):
            self.x[0] -= 1

    def find(self, objectives):

        max_distance = 999

        # Define qual a entidade mais próxima
        for objective in objectives:

            dist_x = 0
            dist_y = 0

            if (
                isinstance(objective, Creature) and objective.alive == True
            ) or (isinstance(objective, Weapon) and objective.found == False):

                dist_x = abs(objective.x[0] - self.x[0])
                dist_y = abs(objective.y[0] - self.y[0])

                # Define a distância diagonal
                if dist_x > dist_y:
                    diag = dist_y
                elif dist_y > dist_x:
                    diag = dist_x
                else:
                    diag = 0

                # calcula a distancia
                distance = dist_x + dist_y - diag

                if distance < max_distance:
                    max_distance = distance
                    obj_x = objective.x[0]
                    obj_y = objective.y[0]

        # Retorna a posição do objetivo
        return (obj_x, obj_y)


class Hero(Creature):
    """Class that describes a hero."""

    def __init__(self, name, x, y, symbol):
        """Creates a new hero, that can wield weapons."""
        super().__init__(name, x, y, symbol)
        self.armed = False


class Weapon(Entity):
    """Class for weapons, used by heroes."""

    def __init__(self, name, x, y, symbol):
        """Creates a new weapons, with a found attribute."""
        super().__init__(name, x, y, 1, 1, symbol)
        self.found = False