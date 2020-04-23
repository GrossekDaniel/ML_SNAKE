import pygame as pg
import random
import math
import numpy as np

training_data = []


def our_snake(snake_list, window): #Wydrukowanie snake
    for z in snake_list:
        pg.draw.rect(window, (0, 255, 0), [z[0], z[1], 40, 40])
    pg.draw.circle(window, (0, 0, 0), (z[0] + 10, z[1] + 10), 4)
    pg.draw.circle(window, (0, 0, 0), (z[0] + 30, z[1] + 10), 4)


def get_angle(snake_position, last_snake_position, apple_position):

    apple_direction_vector = np.array(apple_position) - np.array(snake_position)
    snake_direction_vector = np.array(snake_position) - np.array(last_snake_position)

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)

    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = 40
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 40

    apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
    snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
    angle = math.atan2(apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] -
                       apple_direction_vector_normalized[0] * snake_direction_vector_normalized[1],
                       apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] +
                       apple_direction_vector_normalized[0] * snake_direction_vector_normalized[0]) / math.pi

    return angle


def snake_eat_itself(snake_List, snake_Head):
    for snake in snake_List[:-1]:
        if snake == snake_Head:
            return 0
    return 1


def generate_next_direction(angle, akcja):
    if angle > 0:  # prawo
        if akcja == 0:
            return 2
        if akcja == 1:
            return 3
        if akcja == 2:
            return 1
        if akcja == 3:
            return 0

    if angle < 0:  # lewo
        if akcja == 0:
            return 3
        if akcja == 1:
            return 2
        if akcja == 2:
            return 0
        if akcja == 3:
            return 1
    return akcja


def is_direction_blocked_data(akcja, snake_list):
    przeszkoda_wprost = 0
    przeszkoda_prawo = 0
    przeszkoda_lewo = 0

    snake_head = snake_list[-1]
    a = int(snake_head[0])
    b = int(snake_head[1])

    for snake in snake_List:
        if akcja == 0:
            if a - 40 < 0 or ([a - 40, b] == snake):
                przeszkoda_wprost = 1
            if b + 40 > 440 or ([a, b + 40] == snake):
                przeszkoda_lewo = 1
            if b - 40 < 0 or ([a, b - 40] == snake):
                przeszkoda_prawo = 1

        if akcja == 1:
            if a + 40 > 440 or ([a + 40, b] == snake):
                przeszkoda_wprost = 1
            if b - 40 < 0 or ([a, b - 40] == snake):
                przeszkoda_lewo = 1
            if b + 40 > 440 or ([a, b + 40] == snake):
                przeszkoda_prawo = 1

        if akcja == 2:
            if b - 40 < 0 or ([a, b - 40] == snake):
                przeszkoda_wprost = 1
            if a - 40 < 0 or ([a - 40, b] == snake):
                przeszkoda_lewo = 1
            if a + 40 > 440 or ([a + 40, b] == snake):
                przeszkoda_prawo = 1

        if akcja == 3:
            if b + 40 > 440 or ([a, b + 40] == snake):
                przeszkoda_wprost = 1
            if a - 40 < 0 or ([a - 40, b] == snake):
                przeszkoda_prawo = 1
            if a + 40 > 440 or ([a + 40, b] == snake):
                przeszkoda_lewo = 1

    return przeszkoda_lewo, przeszkoda_wprost, przeszkoda_prawo


def new_direction(snake_position, action):

    new_x = snake_position[0]
    new_y = snake_position[1]

    new_snake_position = []

    if action == 0:
        new_snake_position = [new_x - 40, new_y]

    if action == 1:
        new_snake_position = [new_x + 40, new_y]

    if action == 2:
        new_snake_position = [new_x, new_y - 40]

    if action == 3:
        new_snake_position = [new_x, new_y + 40]

    return new_snake_position, action


def last_snake_position(snake_position, action):
    last_x = snake_position[0]
    last_y = snake_position[1]

    if action == 0:
        return [last_x + 40, last_y]

    if action == 1:
        return [last_x - 40, last_y]

    if action == 2:
        return [last_x, last_y + 40]

    if action == 3:
        return [last_x, last_y - 40]


# Ustawienie początkowej długości snake
snake_length = 1
# Utworzenie obiektu clock aby śledzić czas
clock = pg.time.Clock()
# Stworzenie pustej tablicy celem zapisywania koordynatów
snake_List = []
# Inicjalizacja biblioteki PyGame
pg.init()
# Wyświetlenie tytułu aplikacji
pg.display.set_caption("Snake for ML")
# Ustawienie początkowej akcji na poruszanie się w prawo

loop = True

# Położenie startowe snake
x = 240
y = 240

# Położenie startowe jabłka
x_snack = random.randint(0, 11) * 40
y_snack = random.randint(0, 11) * 40
snake_position = (x, y)


def play_game(action):

    global loop
    global snake_length
    global x, y, x_snack, y_snack, snake_position, clock, snake_List

    while loop is True:
        snake_position, _ = new_direction(snake_position, action)

        apple_position = (x_snack, y_snack)

        # Wyświetlenie ekranu
        window = pg.display.set_mode((480, 480))

        game_over = 0

        if snake_position[0] == x_snack and snake_position[1] == y_snack:
            x_snack = random.randint(0, 11) * 40
            y_snack = random.randint(0, 11) * 40
            apple_position = (x_snack, y_snack)
            snake_length += 1

        # Prędkość gry
        clock.tick(150)
        # Pokolorowanie okna
        window.fill((255, 255, 255))

        # Umiejscowienie jabłka
        pg.draw.rect(window, (255, 0, 0), (x_snack, y_snack, 40, 40), 0)

        # Tablica pomocnicza aktualnej pozycji początku snake
        snake_Head = []
        # Dodawanie koordynatów do tablicy pomocniczej
        snake_Head.append(snake_position[0])
        snake_Head.append(snake_position[1])
        # Dodanie do tablicy kolejnego bloku
        snake_List.append(snake_Head)


        #sprawdzanie czy jablko jest w tej samej pozycji co aktulne ciało snake
        for s in range(len(snake_List)):
            if [x_snack, y_snack] == snake_List[s]:
                x_snack = random.randint(0, 11) * 40
                y_snack = random.randint(0, 11) * 40

        # Usuwanie rysowania bloków jeżeli snake jest krótszy niż długość listy
        if len(snake_List) > snake_length:
            del snake_List[0]

        # Sprawdzenie czy nie zjedliśmy samego siebie
        if snake_eat_itself(snake_List, snake_Head) == 0:
            game_over = 1
            loop = False

        # Sprawdzenie czy nie wyjechaliśmy poza mapę
        if (snake_position[0] > 440) or (snake_position[0] < 0) or (snake_position[1] > 440) or (snake_position[1] < 0):
            game_over = 1
            loop = False

        our_snake(snake_List, window)
        pg.display.update()

        return action, snake_position, apple_position, snake_length, snake_List, game_over
