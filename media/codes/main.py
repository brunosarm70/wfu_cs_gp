from bussiness_logic.classes import *
from bussiness_logic.game_controllers import *

countries = []
universities = []
games = []
players = []
players_jd = 0
tournaments_id = 0
games_id = 0


countries = [Country('United States','USA'), Country('Costa Rica','CRC')]
universities = [University('Tecnologico de Costa Rica','CRC','TEC'), University('Wake Forest University','USA','WFU')]
players = [Player('Bruno', 'Sarmiento','TEC','CRC'), Player('Jose Andres', 'Garcia', 'TEC','CRC'), Player('Kenneth', 'Meza', 'TEC','CRC')]
controllers = [controller_game0000]
# QUESTION: HIS O HER O THEIR O NONE?

games = [Game('Dice game', [], 'This is a simple dice game where each player has a turn to roll the dices how many times they want,\nhowever if the player roll doubles will have to stop rolling the dices and will lose the points earned during the current turn.\nIf the player decides to stop rolling dices, the sum of all rolls will be added to his total.\nThe game ends when a player reach to a target score and the winner will be the player with the highest score at the end of the round.','game0000',2,99)]
games[0].add_parameters([Parameter('dices','integer','it shows the number of dices to roll in each turn'), Parameter('player index','integer','it shows the position of the player in the list of scores'), Parameter('scores','list of integer','it shows the current score for each player'), Parameter("player's current roll",'integer','it shows how many rolls the player has done'), Parameter('objetive score','integer','it contains the amount of points necessary to win the game'), Parameter("previous player's dice roll",'integer',"the sum of points of the previous player's roll (zero if it's the first roll)")])

print(games[0].to_string())

test_match = Match(['player0000','player0001','player0002'],'game0000')



controller_game0000(test_match)


print(test_match.scores)




t = Tournament("First Dice Tournament", "game0000",['player0000','player0001','player0002','player0003'])
t.create_bracket_tournament(2)
t.run_tournament()
print(t.to_string())
print(t.winner)


import random

def test():
    i = 0
    results = []
    turns = []
    while(i < 1000):
        turn = 0
        rolls = 0
        while(True):

            d1 = random.randint(1,6)
            d2 = random.randint(1,6)
            if d1 == d2:
                break
            rolls += 1
            turn += d1+ d2
        results.append(turn)
        turns.append(rolls)
        i+=1

    total = 0
    total_rolls = 0
    for i in results:
        total += i
    for i in turns:
        total_rolls += i
    avg = total / len(results)
    avg_rolls = total_rolls / len(turns)
    print(avg)
    print(avg_rolls)


