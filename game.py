from engine import *

game = Engine()
game.add_structure('Pillar1', 2, 2, '#') #name, width, height, symbol
game.add_structure('Pillar2', 2, 2, '#') #name, width, height, symbol                   
game.add_structure('Wall', 1, 4, '#') #name, width, height, symbol                 
game.add_weapon('Sword', '¬')
game.add_weapon('Warhammer', 'T')
game.add_enemy('Spider', '8')
game.add_enemy('Snake', 'S')
game.add_enemy('Blob', 'O')
game.add_hero('Allucard', '@')

game.event('Welcome to Hero of the Forgotten Land')
game.screen()     

user_input = ""

while user_input != 'Q':
    user_input = input("Wich direction do you want to move?")
    user_input = user_input.upper()

    game.move_heroes(user_input)
    game.move_enemies()
    game.check_collisions()   
    game.update_map()
    game.screen()                        
    game.check_victory()

game.event('Thank you for playing!')