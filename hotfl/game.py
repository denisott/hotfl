import random
from entity import Entity, Creature, Hero, Weapon
from map import Map

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
        self.structures = []
        self.heroes = []
        self.enemies = []
        self.weapons = []
        self.map = Map(size)

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
            x = random.randint(0, self.map.size - width)
            y = random.randint(0, self.map.size - height)

            # Check if space is empty, respecting entity size.
            for pos_y in range(y, y + height):
                for pos_x in range(x, x + width):
                    if self.map.map[pos_y][pos_x] != ' ':
                        found = False
                        break
                if found == False:
                    break

        return (x, y)

    def create_structure(self, name, width, height, symbol):
        """Creates a new structure in the map."""
        (x, y) = self.find_starting_position(width, height)
        self.structures.append(Entity(name, x, y, width, height, symbol))
        self.map.add_entity(self.structures[-1])

    def create_enemy(self, name, symbol):
        """Creates a new Enemy."""
        (x, y) = self.find_starting_position()
        self.enemies.append(Creature(name, x, y, symbol))
        self.map.add_entity(self.enemies[-1])

    def create_hero(self, name, symbol):
        """Creates a new Hero."""
        (x, y) = self.find_starting_position()
        self.heroes.append(Hero(name, x, y, symbol))
        self.map.add_entity(self.heroes[-1])

    def create_weapon(self, name, symbol):
        """Creates a new Wepon."""
        (x, y) = self.find_starting_position()
        self.weapons.append(Weapon(name, x, y, symbol))
        self.map.add_entity(self.weapons[-1])

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
        """Checks which direction to move."""
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
        self.map.initialize()

        for structure in self.structures:
            self.map.add_entity(structure)

        for weapon in self.weapons:
            if weapon.found == False:
                self.map.add_entity(weapon)

        for hero in self.heroes:
            if hero.alive == True:
                self.map.add_entity(hero)

        for enemy in self.enemies:
            if enemy.alive == True:
                self.map.add_entity(enemy)

    def event(self, text):
        """Print the game event."""
        print(text)

    def screen(self):
        """Displays the game screen."""
        for y in range(self.map.size):
            for x in range(self.map.size):
                print('[%s]' % self.map.map[y][x], end='')
            print('')
