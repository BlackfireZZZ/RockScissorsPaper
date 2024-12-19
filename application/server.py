import random
from collections import deque


loses = {
    'scissors': 'rock',
    'paper': 'scissors',
    'rock': 'paper'
}


class Moves:
    def __init__(self, max_length=30):
        """Инициализация с использованием deque с фиксированной длиной."""
        self.moves_list = deque(maxlen=max_length)

    def add_move(self, user_move: str, computer_move: str):
        """Добавляет ход пары [computer_move, user_move] в список.
        Если длина больше max_length, автоматически удаляется первый элемент.
        """
        self.moves_list.append([user_move, computer_move])

    def get_all_moves(self):
        """Возвращает все ходы в виде списка пар."""
        return list(self.moves_list)

    def get_last_move(self):
        """Возвращает последний ход."""
        return self.moves_list[-1]

    def __repr__(self):
        return " <-> ".join(str(data) for data in self.moves_list)


class Server:
    def __init__(self):
        self.moves = Moves()
        self.rounds = []    # 0 - победа пользователя, 1 - победа компьютера, 2 - ничья
        self.computer_move = None   # последний ход компьютера
        self.result = [0, 0, 0]    # [пользователь, компьютер, ничьи]
        self.count_moves = {
            'rock': 0,
            'paper': 0,
            'scissors': 0
        }

    def start(self):
        print("Starting server...")
        print("Possible commands are: 'rock', 'paper', 'scissors', 'stop', 'stats'")
        print("")
        while True:
            user_move = self.get_user_move()
            if user_move == "stop":
                break
            if user_move == "stats":
                continue
            self.make_turn(user_move)
            self.get_result()

    def get_less_common_user_move(self) -> str:
        """
        Возвращает ход, который реже всего сделал пользователь.
        """
        moves = self.moves.get_all_moves()
        if len(moves) == 0:
            return random.choice(["rock", "paper", "scissors"])
        else:
            count = {"rock": 0, "paper": 0, "scissors": 0}
            for move in moves:
                count[move[1]] += 1
            return min(count, key=count.get)

    def make_turn(self, user_move: str):
        possible_moves = ["rock", "paper", "scissors"]
        if len(self.rounds) == 0:
            computer_move = random.choice(possible_moves)
            self.moves.add_move(user_move, computer_move)
            return
        last_move = self.moves.get_last_move()
        if self.rounds[-1] == 0:  # в случай победы пользователя в последний ход
            random_number = random.randint(1, 10)
            generated_move = self.get_win_of(last_move[0])  # с шансом 40 % ходим так, чтобы победить последний
            # ход пользователя
            if random_number < 5:
                self.moves.add_move(user_move, generated_move)
            if random_number == 5:  # с шансом 10  предполагаем, что пользователь сходит так, как ходил реже всего
                possible_user_move = self.get_less_common_user_move()
                computer_move = self.get_win_of(possible_user_move)
                self.moves.add_move(user_move, computer_move)
            else:   # с шансом 50 % ходим случайно из двух других значений
                other_moves = possible_moves
                other_moves.remove(generated_move)
                computer_move = random.choice(other_moves)
                self.moves.add_move(user_move, computer_move)
        elif self.rounds[-1] == 1:   # в случай победы компьютера в последний ход
            random_number = random.randint(1, 10)
            generated_move = self.get_win_of(self.get_win_of(last_move[0]))
            if random_number < 5:  # предполагаем, что в случае проигрыша пользователь будет использовать жест,
                # который побеждает его предыдущий
                self.moves.add_move(user_move, generated_move)
            elif random_number == 5:  # с шансом 10  предполагаем, что пользователь сходит так, как ходил реже всего
                possible_user_move = self.get_less_common_user_move()
                computer_move = self.get_win_of(possible_user_move)
                self.moves.add_move(user_move, computer_move)
            else:   # с шансом 50 % ходим случайно из двух других значений
                other_moves = possible_moves
                other_moves.remove(generated_move)
                computer_move = random.choice(other_moves)
                self.moves.add_move(user_move, computer_move)
        elif self.rounds[-1] == 2:  # в случай ничьи
            random_number = random.randint(1, 10)
            if random_number <= 5:  # с шансом 50% делаем случайный ход
                computer_move = random.choice(possible_moves)
                self.moves.add_move(user_move, computer_move)
            else:   # с шансом 50% предполагаем, что пользователь сходит так, как ходил реже всего
                possible_user_move = self.get_less_common_user_move()
                computer_move = self.get_win_of(possible_user_move)
                self.moves.add_move(user_move, computer_move)

    def get_result(self):
        last_move = self.moves.get_last_move()
        self.count_moves[last_move[0]] += 1
        self.count_moves[last_move[1]] += 1
        print(f'Computer move is {last_move[1]}')
        if last_move[0] == last_move[1]:
            self.rounds.append(2)
            self.result[2] += 1
            print("Draw")
        elif last_move[1] == loses[last_move[0]]:
            self.result[1] += 1
            self.rounds.append(1)
            print("Computer won!")
        else:
            self.result[0] += 1
            self.rounds.append(0)
            print("You won!")
        print("")

    def get_user_move(self) -> str:
        move = input("Enter your move: ")
        move = move.lower()
        while move not in ["rock", "paper", "scissors", "stop", "stats"]:
            print("Wrong move. Try again.")
            move = input("Enter your move: ")
        if move == "stop":
            print("")
            print("Thank you for the game! Bye!")
        elif move == "stats":
            print(f"User: {self.result[0]} Computer: {self.result[1]} Draws: {self.result[2]}")
            print(f"Counted moves are.. Rock: {self.count_moves['rock']} Paper: {self.count_moves['paper']} "
                  f"Scissors: {self.count_moves['scissors']}")
            print("")
        return move

    @staticmethod
    def get_win_of(move: str) -> str:
        """
        Получаем ход, побеждающий заданный
        """
        return loses[move]

