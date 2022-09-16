import random
import sys


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
        super(Creature, self).__init__(name, x, y, 1, 1, symbol)
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
        super(Hero, self).__init__(name, x, y, symbol)
        self.armed = False


class Weapon(Entity):
    """Class for weapons, used by heroes."""

    def __init__(self, name, x, y, symbol):
        """Creates a new weapons, with a found attribute."""
        super(Weapon, self).__init__(name, x, y, 1, 1, symbol)
        self.found = False


class Game:
    """Class that has all the logic to run the game."""

    valid_commands = (
        'QUIT',
        'HELP',
        'N',
        'S',
        'E',
        'W',
        'NE',
        'NW',
        'SE',
        'SW',
    )

    def __init__(self, size):
        """Creates a new game instance."""
        self.size = size
        self.map = []
        self.structures = []
        self.heroes = []
        self.enemies = []
        self.weapons = []
        self.initialize_map()

    def initialize_map(self):
        """Initializes all map positions."""
        for y in range(self.size):
            line = []
            for x in range(self.size):
                line.append(' ')
            self.map.append(line)

    def start_game(self):
        """Starts the game."""
        self.event('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        self.event('     Hero of the Forgotten Land       ')
        self.event('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        self.event('  Find weapons and kill all enemies!  ')
        self.event('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        self.game_loop()

    def game_loop(self):
        """Game loop."""
        self.screen()
        user_command = self.get_command()

        if user_command == 'QUIT':
            self.end_game()
            return

        self.move_heroes(user_command)
        self.move_enemies()
        self.check_collisions()
        self.update_map()
        if self.check_victory():
            self.screen()
            self.end_game()
            return

        self.game_loop()

    def end_game(self):
        """Ends the game."""
        self.event('Thank you for playing!')

    def get_command(self):
        """Gets the user command."""
        user_command = input('Wich direction do you want to move?\n').upper()

        if user_command not in self.valid_commands:
            self.event('Invalid Command')
            self.get_command()
        else:
            return user_command

    def find_starting_position(self, width=1, height=1):
        """
        Finds a starting position for the Entity in the map.
        The surrounding area must comport the Entity size.
        """
        found = False

        while found == False:

            found = True

            # Generate random position that could fit the entity, remove map border.
            x = random.randint(0, self.size - width)
            y = random.randint(0, self.size - height)

            # Check if space is empty, respecting entity size.
            for pos_y in range(y, y + height):
                for pos_x in range(x, x + width):
                    if self.map[pos_y][pos_x] != ' ':
                        found = False
                        break
                if found == False:
                    break

        return (x, y)

    def add_entity_to_map(self, entity):
        """Puts the Entity symbol in the map."""
        for pos_y in entity.y:
            for pos_x in entity.x:
                self.map[pos_y][pos_x] = entity.symbol

    def remove_entity_from_map(self, entity):
        """Removes entity symbol from the map."""
        for pos_y in entity.y:
            for pos_x in entity.x:
                self.map[pos_y][pos_x] = ' '

    def create_structure(self, name, width, height, symbol):
        """Creates a new structure in the map."""
        (x, y) = self.find_starting_position(width, height)
        self.structures.append(Entity(name, x, y, width, height, symbol))
        self.add_entity_to_map(self.structures[-1])

    def create_enemy(self, name, symbol):
        """Creates a new Enemy."""
        (x, y) = self.find_starting_position()
        self.enemies.append(Creature(name, x, y, symbol))
        self.add_entity_to_map(self.enemies[-1])

    def create_hero(self, name, symbol):
        """Creates a new Hero."""
        (x, y) = self.find_starting_position()
        self.heroes.append(Hero(name, x, y, symbol))
        self.add_entity_to_map(self.heroes[-1])

    def create_weapon(self, name, symbol):
        """Creates a new Wepon."""
        (x, y) = self.find_starting_position()
        self.weapons.append(Weapon(name, x, y, symbol))
        self.add_entity_to_map(self.weapons[-1])

    def check_collisions(self):
        """
        Checks if 2 or more entities are in the same position.
        Heroes move first, and can pick up weapons before enemies reach.
        """
        for hero in self.heroes:

            if hero.alive == True:

                for weapon in self.weapons:
                    if (
                        weapon.found == False
                        and hero.x[0] == weapon.x[0]
                        and hero.y[0] == weapon.y[0]
                    ):
                        hero.armed = True
                        weapon.found = True
                        self.event(hero.name + ' found ' + weapon.name)

                for enemy in self.enemies:
                    if (
                        enemy.alive == True
                        and hero.x[0] == enemy.x[0]
                        and hero.y[0] == enemy.y[0]
                    ):
                        if hero.armed == True:
                            enemy.alive = False
                            self.event(hero.name + ' killed ' + enemy.name)
                        else:
                            hero.alive = False
                            self.event(enemy.name + ' killed ' + hero.name)

    def check_victory(self):
        """Checks if all enemies or the hero is dead."""
        enemies_alive = False
        heroes_alive = False

        for enemy in self.enemies:
            if enemy.alive == True:
                enemies_alive = True

        for hero in self.heroes:
            if hero.alive == True:
                heroes_alive = True

        if enemies_alive == True and heroes_alive == False:
            self.event('Enemies killed all heroes!')
            return True

        if heroes_alive == True and enemies_alive == False:
            self.event('Heroes vanquised all enemies!')
            return True

    def path(self, entity, x, y):

        # Define a direção do movimento para o mais próximo
        dist_y = y - entity.y[0]
        dist_x = x - entity.x[0]

        direction = ''

        if dist_y > 0:
            direction = 'S'
        elif dist_y < 0:
            direction = 'N'

        if dist_x > 0:
            direction = direction + 'E'
        elif dist_x < 0:
            direction = direction + 'W'

        # Checa pra ver se existe alguma estrutra na direção definida.
        pos_x = entity.x[0]
        pos_y = entity.y[0]

        if direction.__contains__('N'):
            pos_y -= 1
        if direction.__contains__('S'):
            pos_y += 1
        if direction.__contains__('E'):
            pos_x += 1
        if direction.__contains__('W'):
            pos_x -= 1

        for structure in self.structures:
            bloq = False

            for y in structure.y:
                for x in structure.x:
                    if y == pos_y and x == pos_x:
                        bloq = True

            if bloq == True:
                if pos_x > entity.x[0]:
                    direction = direction.replace('E', '')
                if pos_x < entity.x[0]:
                    direction = direction.replace('W', '')
                if pos_y > entity.y[0]:
                    direction = direction.replace('S', '')
                if pos_y < entity.y[0]:
                    direction = direction.replace('N', '')

        return direction

    def check_path(self, x, y, direction):
        """Check if direction of movement is not blocked by a structure."""
        blocked = False
        pos_x = x
        pos_y = y

        if direction.__contains__('N'):
            pos_y -= 1
        if direction.__contains__('S'):
            pos_y += 1
        if direction.__contains__('E'):
            pos_x += 1
        if direction.__contains__('W'):
            pos_x -= 1

        for structure in self.structures:

            if y == structure.y or x == structure.x:
                blocked = True

        return blocked

    def move_heroes(self, direction):
        """Moves the hero in desired direction, checking if path is blocked."""
        for hero in self.heroes:
            blocked = self.check_path(hero.x[0], hero.y[0], direction)
            if blocked:
                self.event('Path blocked')
            else:
                hero.move(direction)

    def move_enemies(self):
        """Moves the enemies in the hero direction."""
        for enemy in self.enemies:
            (x, y) = enemy.find(self.heroes)
            direction = self.path(enemy, x, y)
            if direction != '':
                enemy.move(direction)

    def update_map(self):
        """Update maps after movements and collisions check."""
        self.map = []
        self.initialize_map()

        for structure in self.structures:
            self.add_entity_to_map(structure)

        for weapon in self.weapons:
            if weapon.found == False:
                self.add_entity_to_map(weapon)

        for hero in self.heroes:
            if hero.alive == True:
                self.add_entity_to_map(hero)

        for enemy in self.enemies:
            if enemy.alive == True:
                self.add_entity_to_map(enemy)

    def event(self, text):
        """Print the game event."""
        print(text)

    def screen(self):
        """Displays the game screen."""
        for y in range(self.size):
            for x in range(self.size):
                print('[%s]' % self.map[y][x], end='')
            print('')
