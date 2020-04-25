import snake_game
from keras.models import model_from_json
import importlib
import numpy as np


def run_game_with_ML(model):
    max_score = 0
    avg_score = 0
    test_games = 100
    game = 0

    for _ in range(test_games):
        game += 1
        print("GAME:", game)
        flag = True
        action, snake_position, apple_position, score, snake_List, game_over = snake_game.play_game(1)

        while flag is True:

            if game_over > 0:
                avg_score += score
                flag = False
                importlib.reload(snake_game)
            if game_over == 0:
                left, front, right = snake_game.is_direction_blocked_data(action, snake_List)

                angle = snake_game.get_angle(snake_position, snake_game.last_snake_position(snake_position, action),
                                             apple_position)

                predicted_direction_n = np.array(model.predict(np.array([left, front, right, angle]).reshape(-1, 4)))

                predicted_direction = np.around(predicted_direction_n[0][0])

                if predicted_direction == -1:
                    if action == 0:
                        new_action = 3
                    if action == 1:
                        new_action = 2
                    if action == 2:
                        new_action = 0
                    if action == 3:
                        new_action = 1

                if predicted_direction == 1:
                    if action == 0:
                        new_action = 2
                    if action == 1:
                        new_action = 3
                    if action == 2:
                        new_action = 1
                    if action == 3:
                        new_action = 0

                if predicted_direction == 0:
                    new_action = action

                if score > max_score:
                    max_score = score

                action, snake_position, apple_position, score, snake_List, game_over = snake_game.play_game(new_action)

    return max_score, (avg_score / test_games)


json_file = open('model.json', 'r')
loaded_json_model = json_file.read()
model = model_from_json(loaded_json_model)
model.load_weights('model.h5')

max_score, avg_score = run_game_with_ML(model)
print("Maximum score achieved is:  ", max_score)
print("Average score achieved is:  ", avg_score)
