from engine import *

game = Engine(10) #rounds

game.add_structure('Pillar1', 2, 2, '#') #name, width, height, symbol
game.add_structure('Pillar2', 2, 2, '#') #name, width, height, symbol                   
game.add_structure('Wall', 1, 4, '#') #name, width, height, symbol                 
game.add_weapon('Sword', '¬')
game.add_weapon('Warhammer', 'T')
game.add_enemy('Spider', '8')
game.add_enemy('Snake', 'S')
game.add_enemy('Blob', 'O')
game.add_hero('Allucard', '@')
 
game.run()