# -*- coding: utf8 -*-
from iternal_game_logic import Dot
from iternal_game_logic import Ship
from iternal_game_logic import Board


class Player:
    def __init__(self):
        self.user_board = Board()
        self.ai_board = Board(True)  # True скрывает корабли ИИ
        self.player_ships_height = [3, 2, 2, 1, 1, 1, 1]
        self.dot = Dot()

    def ask(self, player_board):
        pass

    def move(self, player_board):
        self.ask(player_board)


class User(Player):
    def ask(self, ai_board):
        while True:
            print('Куда выстрелить?')
            hit = ai_board.shot(self.dot.get_dot(ai_board.get_all_shots_list()))
            if not hit:
                break
            elif not ai_board.board_ships_list:
                print('  Доска ИИ')
                ai_board.draw_player_board()
                print('Вы победили!')
                break
            else:
                ai_board.draw_player_board()
                print('Попали!')


class AI(Player):
    def ask(self, user_board):
        while True:
            hit = user_board.shot(self.dot.get_random_dot(user_board.get_all_shots_list()))
            if not hit:
                break
            elif not user_board.board_ships_list:
                print('Доска игрока')
                user_board.draw_player_board()
                print('Победил ИИ!')
                break
            else:
                user_board.draw_player_board()


class Game:
    def __init__(self):
        self.user = User()
        self.ai = AI()

    def random_user_board(self):
        while True:
            for i in range(len(self.user.player_ships_height)):
                player_ship = Ship(self.user.player_ships_height[i])
                player_ship.auto_create_ship(self.user.user_board.get_board_ships_list(),
                                             self.user.user_board.contour_list)
                self.user.user_board.add_ships(player_ship.get_ships())
            if len(self.user.user_board.board_ships_list) != 11:
                self.user.user_board.board_ships_list.clear()
                self.user.user_board.contour_list.clear()
            else:
                break

    def random_ai_board(self):
        while True:
            for i in range(len(self.ai.player_ships_height)):
                player_ship = Ship(self.ai.player_ships_height[i])
                player_ship.auto_create_ship(self.ai.ai_board.get_board_ships_list(),
                                             self.ai.ai_board.contour_list)
                self.ai.ai_board.add_ships(player_ship.get_ships())
            if len(self.ai.ai_board.board_ships_list) != 11:
                self.ai.ai_board.board_ships_list.clear()
                self.ai.ai_board.contour_list.clear()
            else:
                break

    def greet(self):
        print(
            'Добро пожаловать в игру "Морской бой".\n'
            'Вы играете против ИИ на случайно сгенерированной доске.\n'
            'Чтобы сделать выстрел по доске ИИ - последовательно вводите координату.\n'
            'Буквой "X" помечаются подбитые корабли, буквой "T" — промахи.\n'
            'Попадание по кораблю даёт дополнительный выстрел.\n'
            'Побеждает тот, кто быстрее всех разгромит корабли противника.')
        while True:
            ok = input('Чтобы начать игру введите "ок": ').lower()
            if ok == 'ок':
                break

    def loop(self):
        self.random_user_board()
        self.random_ai_board()
        step = 0
        while True:
            if not self.ai.ai_board.board_ships_list:
                break
            elif not self.user.user_board.board_ships_list:
                break

            print('Доска игрока')
            self.user.user_board.draw_player_board()
            print('  Доска ИИ')
            self.ai.ai_board.draw_player_board()
            if step > 0:
                print('Промах')
            self.user.move(self.ai.ai_board)
            self.ai.move(self.user.user_board)
            step += 1

            # print(self.user.user_board.all_shots_list)
            # print(self.ai.ai_board.all_shots_list)

    def start(self):
        self.greet()
        self.loop()


Game().start()
