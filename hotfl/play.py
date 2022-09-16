from game import Game

game = Game(10)

# Creating scructures and entities in random places
game.create_structure('Pillar1', 2, 2, '#')
game.create_structure('Pillar2', 2, 2, '#')
game.create_structure('Wall', 1, 4, '#')
game.create_weapon('Sword', '¬')
game.create_weapon('Warhammer', 'T')
game.create_enemy('Spider', '8')
game.create_enemy('Snake', 'S')
game.create_enemy('Blob', 'O')
game.create_hero('Allucard', '@')
game.start_game()
