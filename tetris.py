import random


class TetrisBoard():
    z_shape = [['.', 'O', 'O'],
               ['O', 'O', '.']]

    L_shape = [['O', '.', '.'],
               ['O', 'O', 'O']]

    i_shape = [['O', 'O', 'O', 'O']]

    square_shape = [['O', 'O'], ['O', 'O']]

    tetris_shapes = [z_shape, L_shape, i_shape, square_shape]

    def __init__(self):
        self.boardWidth = 10
        self.boardHeight = 10
        self.board = [['.'] * self.boardWidth for __ in range(self.boardHeight)]
        self.start_location_y = int(self.boardHeight)
        self.start_location_x = int((self.boardWidth / 2) - 1)
        self.rotations_count = 0
        self.empty_line = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']

    def print_board(self):
        print('\n\n')
        print('\n'.join((''.join('{0:^1s}'.format(x) for x in row)) for row in self.board))

    def generate_shape(self):
        random_int = random.randint(0, len(self.tetris_shapes) - 1)
        random_shape = self.tetris_shapes[random_int]
        return random_shape

    def put_piece_on_board(self, shape):

        # CHECK IF GAME OVER WHILE PUTTIN PIECE
        for i in range(len(shape)):
            for j in range(0, len(shape[i])):
                if self.board[0 + i][self.start_location_x + j] == '.':
                    self.board[0 + i][self.start_location_x + j] = str(shape[i][j])
                else:
                    return False
        return self.board

    def get_move_from_user(self):
        accepted_move = False
        while not accepted_move:
            move = input("Please provide a move (L,R,D,T): ")
            if move not in ['L', 'R', 'D', 'T']:
                print("Error! Not an actual move! Try again!")
                accepted_move = False
            else:
                accepted_move = True

        return move

    def make_the_move(self, shape, move, board):
        new_shape = shape
        if move == 'L':
            result = self.move_left(shape, board)
        elif move == 'R':
            result = self.move_right(shape, board)
        elif move == 'D':
            result = self.move_down(shape, board)
        elif move == 'T':
            result = self.rotate_move(shape, board)

        if result and move != 'D' and move != 'T':
            result = self.move_down(new_shape, result)

        if result:
            self.board = result

        return result

    def check_height_of_shape_in_column(self, shape, column_index):
        height = 0
        for i in range(self.boardHeight):
            if self.board[i][column_index] == 'O':
                height += 1
        return height

    def checkShapeLanded(self):
        # CHECK BOTTOM
        occurrence_of_O_in_line = self.board[self.boardHeight - 1].count('O')
        if occurrence_of_O_in_line:
            return True

        i = self.boardHeight - 2
        while i >= 0:
            occurrence_of_O_in_line = self.board[i].count('O')

            if occurrence_of_O_in_line:
                for j in range(self.boardWidth):
                    if self.board[i][j] == 'O':
                        if self.board[i + 1][j] == 'X':
                            return True
            i -= 1
        return False

    def put_shape_on_boar_permanently(self):
        for i in range(self.boardHeight):
            for j in range(self.boardWidth):
                if self.board[i][j] == 'O':
                    self.board[i][j] = 'X'

    def checkFullLine(self):
        i = self.boardHeight - 1
        while i >= 0:
            occurrence_of_O_in_line = self.board[i].count('X')
            if occurrence_of_O_in_line == self.boardWidth:
                # DELETE LINE
                self.board = self.empty_line + self.board[:i] + self.board[i + 1:]
                i += 1  # CHECK SAME ROW AGAIN
            i -= 1

    def check_game_over(self):
        for i in range(self.boardWidth):
            height = 0
            for j in range(self.boardHeight):
                if self.board[j][i] == 'X' or self.board[j][i] == 'O':
                    height += 1
            if height == self.boardHeight:
                return True
        return False

    def move_down(self, shape, board):

        moment_board = board
        i = self.boardHeight - 2

        while i >= 0:
            occurrence_of_O_in_line = board[i].count('O')

            if occurrence_of_O_in_line:
                for j in range(self.boardWidth):
                    if board[i][j] == 'O':
                        if board[i + 1][j] != 'X':
                            # FIND HIGHT OF SHAPE IN COLUMN
                            height = self.check_height_of_shape_in_column(shape, j)
                            moment_board[i + 1][j] = 'O'
                            if (i - height + 1) >= 0:
                                moment_board[i - height + 1][j] = '.'

                        else:
                            return False
            i -= 1

        return moment_board

    def rotate_move(self, shape, board):
        # SQUARE SHAPE DOESNT NEED TO BE ROTATED
        if shape == self.square_shape:
            return board

        start_position_x, start_position_y = 0, 0
        moment_board = board
        new_shape = self.rotate_shape(self.rotations_count, shape)
        i = 0
        while i < self.boardHeight:
            occurrence_of_O_in_line = moment_board[i].count('O')
            if occurrence_of_O_in_line:
                for j in range(self.boardWidth):
                    if moment_board[i][j] == 'O':
                        start_position_x = j
                        start_position_y = i
                        break
                break
            i += 1

        # REMOVE CURRENT O's
        moment_board = [list("." if element == 'O' else element
                             for element in list(row))
                        for row in moment_board]

        # CHECK IF PIECE CAN BE PUT ON BOARD
        i = 0
        while i < len(new_shape):
            for j in range(0, len(new_shape[0])):
                if new_shape[i][j] == 'O':
                    if moment_board[start_position_y + i][start_position_x + j] != 'X':
                        moment_board[start_position_y + i][start_position_x + j] = 'O'
                    else:
                        return False
            i += 1
        self.rotations_count += 1
        return moment_board

    def rotate_shape(self, nr_rotations, orig_matrix):
        new_matrix = orig_matrix
        moment_matrix = orig_matrix
        for i in range(nr_rotations + 1 % 4):
            new_matrix = [[0] * len(moment_matrix) for __ in range(len(moment_matrix[0]))]
            for i in range(0, len(moment_matrix[0])):
                for j in range(0, len(moment_matrix)):
                    new_matrix[i][j] = moment_matrix[len(moment_matrix) - j - 1][i]
            moment_matrix = new_matrix
        return new_matrix

    def move_left(self, shape, board):
        moment_board = board
        for i in range(self.boardHeight):
            occurrence_of_O_in_line = board[i].count('O')
            for j in range(self.boardWidth):
                if occurrence_of_O_in_line:
                    if board[i][j] == 'O':
                        if j - 1 >= 0:
                            if board[i][j - 1] != 'X':
                                moment_board[i][j - 1] = 'O'
                                moment_board[i][j + occurrence_of_O_in_line - 1] = '.'
                            else:
                                # MOVE CAN NOT BE DONE
                                return False
                        else:
                            # MOVE CAN NOT BE DONE
                            return False

        return moment_board

    def move_right(self, shape, board):
        moment_board = board
        for i in range(self.boardHeight):
            occurrence_of_O_in_line = board[i].count('O')
            if occurrence_of_O_in_line:
                # SHAPE STANDS AT RIGHTMOST
                if board[i][self.boardWidth - 1] == 'O':
                    return False

                j = self.boardWidth - 2
                # Iterate till 1st element and keep on decrementing i
                while j >= 0:
                    if board[i][j] == 'O':
                        if board[i][j + 1] != 'X':
                            moment_board[i][j + 1] = 'O'
                            moment_board[i][j - occurrence_of_O_in_line + 1] = '.'
                            print(moment_board[i])
                        else:
                            # MOVE CAN NOT BE DONE
                            return False
                    j -= 1

        return moment_board

    def start_game(self):

        game_on = True
        # generate piece

        while game_on:
            shape_landed = False
            self.rotations_count = 0
            shape = self.generate_shape()
            box_at_begining = self.put_piece_on_board(shape)
            self.print_board()
            # IF NOT GAME OVER
            if box_at_begining:
                while not shape_landed:
                    # GET A MOVE FROM USER
                    move = self.get_move_from_user()

                    # MAKE THE MOVE
                    result_move = self.make_the_move(shape, move, self.board)
                    if result_move:
                        self.print_board()
                        shape_landed = self.checkShapeLanded()
                        # IF SHAPE LANDED CHECK IF THERE IS ANY FULL LINE
                        if shape_landed:
                            self.put_shape_on_boar_permanently()
                            full_line = self.checkFullLine()
                            break

                    else:
                        # CHECK IF GAME OVER
                        result = self.check_game_over()
                        if result:
                            break
                        print('CAN NOT MAKE THAT MOVE')

            else:
                print("GAME OVER")
                game_on = False


TetrisBoard().start_game()