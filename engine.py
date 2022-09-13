import random
import time
import sys 

class Entity():
    
    def __init__(self, name, x, y, width, height, symbol):
        self.name = name
        self.symbol = symbol
        self.x = []
        self.y = []         
        
        for pos in range(x, x + width):
            self.x.append(pos)
            
        for pos in range(y, y + height):
            self.y.append(pos)
            
class Creature(Entity):

    def __init__(self, name, x, y, symbol):
        super(Creature, self).__init__(name, x, y, 1, 1, symbol)
        self.alive = True
        
    def move(self, direction):
        
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
            
            if ( isinstance(objective, Creature) and objective.alive == True ) or ( isinstance(objective, Weapon) and objective.found == False ):
                
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
        return(obj_x, obj_y)
        
class Hero(Creature):

    def __init__(self, name, x, y, symbol):
        super(Hero, self).__init__(name, x, y, symbol)
        self.armed = False
        
class Weapon(Entity):
    
    def __init__(self, name, x, y, symbol):
        super(Weapon, self).__init__(name, x, y, 1, 1, symbol)
        self.found = False

class Engine():

    def __init__(self):
        self.size = 10        
        self.map = []
        self.structures = []
        self.heroes = []
        self.enemies = []
        self.weapons = []
        self.start_map()
        
    def start_map(self):
        
        # Inicializa o mapa do jogo
        for y in range(self.size):
            line = []
            for x in range(self.size):
              line.append(' ')
            self.map.append(line)
            
    def find_empty_space(self, width, height):
        
        found = False
        
        while found == False:
            
            found = True
            
            # Gera uma posição aleatório, respeitando o tamanho da entidade.
            x = random.randint(0, self.size - width)
            y = random.randint(0, self.size - height)
            
            # Valida espaços vazios.
            for pos_y in range(y, y + height):
                for pos_x in range(x, x + width):
                    if self.map[pos_y][pos_x] != ' ':
                        found = False
                        break
                if found == False:
                    break
                
        return(x, y)        
            
    def add_entity_map(self, entity):
        
        # Adiciona a entidade ao mapa
        for y in entity.y:
            for x in entity.x:
                self.map[y][x] = entity.symbol
                
    def remove_entity_map(self, entity):
        
        # Remove a entidade do mapa
        for y in entity.y:
            for x in entity.x:
                self.map[y][x] = ' '  
                
    def add_structure(self, name, width, height, symbol):
        
        # Procura por uma posição inicial vazia
        (x, y) = self.find_empty_space(width, height)
        
        # Cria a estrutura
        self.structures.append(Entity(name, x, y, width, height, symbol))   
        
        # Adiciona ao mapa
        self.add_entity_map(self.structures[len(self.structures) - 1])
        
    def add_enemy(self, name, symbol):
        
        # Procura por uma posição inicial vazia
        (x, y) = self.find_empty_space(1, 1)        
        
        # Cria um enemigo
        self.enemies.append(Creature(name, x, y, symbol))           
        
        # Adiciona ao mapa
        self.add_entity_map(self.enemies[len(self.enemies) - 1])        
        
    def add_hero(self, name, symbol):
        
        # Procura por uma posição inicial vazia
        (x, y) = self.find_empty_space(1, 1)        
        
        # Cria um herói
        self.heroes.append(Hero(name, x, y, symbol))    
        
        # Adiciona ao mapa
        self.add_entity_map(self.heroes[len(self.heroes) - 1])   
        
    def add_weapon(self, name, symbol):
        
        # Procura por uma posição inicial vazia
        (x, y) = self.find_empty_space(1, 1)        
        
        # Cria uma arma
        self.weapons.append(Weapon(name, x, y, symbol))           
        
        # Adiciona ao mapa
        self.add_entity_map(self.weapons[len(self.weapons) - 1])
        
    def check_collisions(self):
        
        for hero in self.heroes:
            
            if hero.alive == True:
                
                for weapon in self.weapons:
                    if weapon.found == False and hero.x[0] == weapon.x[0] and hero.y[0] == weapon.y[0]:
                        hero.armed = True
                        weapon.found = True
                        self.event(hero.name + ' found ' + weapon.name)
                            
                for enemy in self.enemies:
                    if enemy.alive == True and hero.x[0] == enemy.x[0] and hero.y[0] == enemy.y[0]:
                        if hero.armed == True:
                            enemy.alive = False
                            self.event(hero.name + ' killed ' + enemy.name)
                        else:
                            hero.alive = False
                            self.event(enemy.name + ' killed ' + hero.name)           
                            
    def check_victory(self):
        
        enemies_alive = False
        heroes_alive = False
        
        for enemy in self.enemies:
            if enemy.alive == True:
                enemies_alive = True
        
        for hero in self.heroes:
            if hero.alive == True:
                heroes_alive = True
                
        if enemies_alive == True and heroes_alive == False:
            self.event('Enemies killed all heroes')
            self.end_game()
            
        if heroes_alive == True and enemies_alive == False:
            self.event('Heroes vanquised all enemies')
            self.end_game()          

    def end_game(self):
        sys.exit()
        
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
                    direction = direction.replace('E','')
                if pos_x < entity.x[0]:                
                    direction = direction.replace('W','')
                if pos_y > entity.y[0]:                  
                    direction = direction.replace('S','')
                if pos_y < entity.y[0]:                  
                    direction = direction.replace('N','')
    
        return(direction)

    def check_path(self, x, y, direction):

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

        return( blocked )

    def move_heroes(self, direction):

        for hero in self.heroes:
            blocked = self.check_path(hero.x[0], hero.y[0], direction)
            if blocked:
                self.event("Path blocked")
            else:
                hero.move(direction)
        
    def move_enemies(self):
        
        for enemy in self.enemies:
            (x, y) = enemy.find(self.heroes)
            direction = self.path(enemy, x, y)
            if direction != '':
                enemy.move(direction)
               
    def update_map(self):
        
        self.map = []
        
        self.start_map()
        
        for structure in self.structures:
            self.add_entity_map(structure)
            
        for weapon in self.weapons:
            if weapon.found == False:
                self.add_entity_map(weapon)     
        
        for hero in self.heroes:
            if hero.alive == True:
                self.add_entity_map(hero)
                
        for enemy in self.enemies:
            if enemy.alive == True:
                self.add_entity_map(enemy)
        
    def event(self, text):
        print(text)        
                    
    def screen(self):
        print('------------------------------')
        
        for y in range(self.size):
            for x in range(self.size):
                print('[%s]' % self.map[y][x], end='')
            print('')            
            
        print('------------------------------')