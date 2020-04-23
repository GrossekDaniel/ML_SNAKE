import snake_game
import numpy as np
import importlib
import math


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def training_data_angle():
    max_score = 0
    avg_score = 0
    trainingData = []
    actions = []
    training_games = 2000
    for i in range(training_games):
        flag = True
        print("#Game:", i+1)
        action, snake_position, apple_position, score, snake_List, game_over = snake_game.play_game(1)

        while flag is True:
            angle = snake_game.get_angle(snake_position, snake_game.last_snake_position(snake_position, action),
                                         apple_position)

            new_action_angle = snake_game.generate_next_direction(angle, action)

            '''

            -1  => LEFT
            0   => AHEAD
            1   => RIGHT

            '''

            left, front, right = snake_game.is_direction_blocked_data(action, snake_List)

            if angle > 0:
                if right == 0:
                    action_ml = 1
                if right == 1:
                    if front == 0 and left == 1:
                        action_ml = 0
                    if front == 1 and left == 0:
                        action_ml = -1
                    if front == 0 and left == 0:
                        action_ml = -1
                    if front == 1 and left == 1:
                        action_ml = 0

            if angle < 0:
                if left == 0:
                    action_ml = -1
                if left == 1:
                    if right == 0 and front == 1:
                        action_ml = 1
                    if right == 1 and front == 0:
                        action_ml = 0
                    if right == 0 and front == 0:
                        action_ml = 1
                    if right == 1 and front == 1:
                        action_ml = 0

            if angle == 0:
                if front == 0:
                    action_ml = 0
                if front == 1:
                    if right == 0 and left == 1:
                        action_ml = 1
                    if right == 1 and left == 0:
                        action_ml = -1
                    if right == 0 and left == 0:
                        action_ml = -1
                    if right == 1 and left == 1:
                        action_ml = 0

            if score > max_score:
                max_score = score

            if game_over == 0:
                data = [left, front, right, angle]

                actions.append(action_ml)

                trainingData.append(data)

                #print('DATA:', data)
                #print('PREDICTED:', action_ml)

                action, snake_position, apple_position, score, snake_List, game_over = snake_game.play_game(
                    new_action_angle)

            if game_over > 0:
                avg_score += score
                flag = False
                importlib.reload(snake_game)

    print("Maximum score achieved is:  ", max_score)
    print("Average score achieved is:  ", avg_score/training_games)

    return np.array(trainingData), np.array(actions)
