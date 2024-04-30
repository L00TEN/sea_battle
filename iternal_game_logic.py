from random import randrange
from random import choice


class Exceptions:
    def check_isrange(self, ship, player_board_ships_list, contour_list):
        for i in range(len(ship)):
            num = ship[i]
            if num in player_board_ships_list:
                ship = [-1]
                break
            elif num in contour_list:
                ship = [-1]
                break
            elif num < 1 or num > 36:
                ship = [-1]
                break
            elif len(ship) > 1 and num in [7, 13, 19, 25, 31]:
                ship = [-1]
                break
        return ship

    def check_ship(self, nose, direction, height, player_board_ships_list, contour_list):
        ship = []
        if direction == 'г':
            for i in range(height):
                ship.append(int(nose) + i)
                ship = self.check_isrange(ship, player_board_ships_list, contour_list)
        elif direction == 'в':
            for i in range(height):
                ship.append(int(nose) + (i * 6))
                ship = self.check_isrange(ship, player_board_ships_list, contour_list)
        return ship

    def check_coordinate(self, name):
        while True:
            try:
                coordinate = int(input(f'Введите координату {name}: '))
                if int(coordinate) > 6 or int(coordinate) < 1:
                    print('Неправильный ввод')
                else:
                    break
            except:
                print('Неправильный ввод')
        return coordinate


class Dot(Exceptions):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dot = 0

    def get_dot(self, all_shots_list):
        while True:
            self.x = self.check_coordinate('X')
            self.y = str(self.check_coordinate('Y'))
            if self.y == '1':
                self.dot = self.x
            elif self.y == '2':
                self.dot = self.x + 6
            elif self.y == '3':
                self.dot = self.x + 12
            elif self.y == '4':
                self.dot = self.x + 18
            elif self.y == '5':
                self.dot = self.x + 24
            elif self.y == '6':
                self.dot = self.x + 30

            if self.dot in all_shots_list:
                print('Вы уже стреляли по этим координатам')

            else:
                break
        return self.dot

    def get_random_dot(self, all_shots_list):
        while True:
            self.dot = randrange(1, 36)
            if self.dot in all_shots_list:
                return
            else:
                break
        return self.dot


class Ship(Exceptions):
    def __init__(self, height):
        self.height = height
        self.nose = 0
        self.direction = ['г', 'в']
        self.ship = []

    def get_height(self):
        return self.height

    def get_nose(self):
        return self.nose

    def get_direction(self):
        return self.direction

    def auto_create_ship(self, board_ships_list, contour_list):
        ship = [-1]
        count = 0
        while ship[0] == -1:
            count += 1
            # print('count', count)
            if count == 1000:
                return

            self.nose = randrange(36)
            # print(self.nose, ': нос корабля')
            self.direction = choice(self.direction)
            # print(self.direction, ': направление корабля')
            ship = self.check_ship(self.nose, self.direction, self.height, board_ships_list, contour_list)
        self.ship.extend(ship)
        # print(self.ship, ': список координат подходящего корабля')

    def get_ships(self):
        return self.ship


class Board(Exceptions):
    def __init__(self, hid=False):
        self.board_list = [[1, 2, 3, 4, 5, 6],
                           [7, 8, 9, 10, 11, 12],
                           [13, 14, 15, 16, 17, 18],
                           [19, 20, 21, 22, 23, 24],
                           [25, 26, 27, 28, 29, 30],
                           [31, 32, 33, 34, 35, 36]]
        self.board_ships_list = []
        self.hid = hid
        self.player_hits_list = []
        self.player_miss_list = []
        self.all_shots_list = []
        self.contour_list = []

    def get_board_list(self):
        return self.board_list

    def get_board_ships_list(self):
        return self.board_ships_list

    def get_all_shots_list(self):
        return self.all_shots_list

    def add_ships(self, get_ship):
        self.board_ships_list.extend(get_ship)
        self.contour(get_ship)
        # print('добавляем корабль и его контур\n')

    def contour(self, get_ship):
        for i in get_ship:
            # print('i =', i)
            if i in [6, 12, 18, 24, 30, 36]:
                self.contour_list.append(i + 5)
                self.contour_list.append(i + 6)
                self.contour_list.append(i - 1)
                self.contour_list.append(i - 6)
                self.contour_list.append(i - 7)
            elif i in [1, 7, 13, 19, 25, 31]:
                self.contour_list.append(i + 1)
                self.contour_list.append(i + 6)
                self.contour_list.append(i + 7)
                self.contour_list.append(i - 5)
                self.contour_list.append(i - 6)
            else:
                self.contour_list.append(i + 1)
                self.contour_list.append(i + 5)
                self.contour_list.append(i + 6)
                self.contour_list.append(i + 7)
                self.contour_list.append(i - 1)
                self.contour_list.append(i - 5)
                self.contour_list.append(i - 6)
                self.contour_list.append(i - 7)
        for i in self.contour_list:
            if i < 0 or i > 36:
                self.contour_list.remove(i)

        # print('Cписок контура:\n', self.contour_list)

    def shot(self, get_dot):
        if get_dot in self.board_ships_list:
            self.all_shots_list.append(get_dot)
            self.player_hits_list.append(get_dot)
            self.board_ships_list.remove(get_dot)
            return True
            # print('Удаляем из списка кораблей ячейку: ', get_dot)
        else:
            self.all_shots_list.append(get_dot)
            # print('список всех выстрелов :', self.all_shots_list)
            self.player_miss_list.append(get_dot)
            return False
        # print(self.player_hits_list, ': список попаданий')

    def draw_player_board(self):
        print('1 2 3 4 5 6')
        count = 1
        for i in self.board_list:
            for j in i:
                if j in self.player_hits_list:
                    j = 'X'
                elif j in self.contour_list and j in self.board_ships_list and not self.hid:
                    j = '■'
                # elif j in self.contour_list:
                # j = '$'
                elif j in self.board_ships_list and not self.hid:
                    j = '■'
                elif j in self.player_miss_list:
                    j = 'T'
                else:
                    j = 'O'
                print(j, end=' ')
            print(count)
            count += 1
        print()
