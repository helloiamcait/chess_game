# Author: Caitlin Martin Newnham
# GitHub username: helloiamcait
# Date: December, 2024
# Description: Program that implements a variant of chess known as Fog of War. When displaying the game board from a
#       player's perspective, the player's pieces and only the opponent's pieces that can be captured are displayed.
#       Opponent pieces that cannot be captured are displayed as '*',


class ChessVar:
    """Represents a game of the Fog of War variant of chess with a game board. Attributes include white player pieces,
    black player pieces, dictionaries for row and column labels, player whose turn it is, game state, a dictionary of
    each player and their respective pieces and opponent's pieces, a dictionary of different board game perspectives
    and a dictionary of moves for each piece type.
    """
    def __init__(self):
        self._game_board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self._white_pieces_set = {'R', 'N', 'B', 'Q', 'K', 'P'}
        self._black_pieces_set = {'r', 'n', 'b', 'q', 'k', 'p'}
        self._row_label_dict = {'8': '0', '7': '1', '6': '2', '5': '3', '4': '4', '3': '5', '2': '6', '1': '7'}
        self._column_label_dict = {'a': '0', 'b': '1', 'c': '2', 'd': '3', 'e': '4', 'f': '5', 'g': '6', 'h': '7'}
        self._player_turn = 'white'
        self._game_state = 'UNFINISHED'
        self._player_pieces_dict = {
            'white': {
                'player_pieces': self._white_pieces_set,
                'opponent_pieces': self._black_pieces_set
            },
            'black': {
                'player_pieces': self._black_pieces_set,
                'opponent_pieces': self._white_pieces_set
            }
        }
        self._board_perspective_dict = {
            'audience': Audience(self._game_board, self._player_pieces_dict),
            'white': White(self._game_board, self._player_pieces_dict),
            'black': Black(self._game_board, self._player_pieces_dict)
        }
        self._move_type_dict = {
            'q': Queen(self._game_board, self._player_pieces_dict),
            'b': Bishop(self._game_board, self._player_pieces_dict),
            'r': Rook(self._game_board, self._player_pieces_dict),
            'n': Knight(self._game_board, self._player_pieces_dict),
            'p': Pawn(self._game_board, self._player_pieces_dict),
            'k': King(self._game_board, self._player_pieces_dict)
        }

    def get_square_index(self, algebraic_pos):
        """
        Returns a tuple with the chess board array row and column indices equivalent to the algebraic location
        on the chess board given as a parameter.

        Returns False if the algebraic location is not within the bounds of the board.
        """
        row_labels = self._row_label_dict
        col_labels = self._column_label_dict
        if algebraic_pos[1] in row_labels and algebraic_pos[0] in col_labels:
            row = int(row_labels[algebraic_pos[1]])
            col = int(col_labels[algebraic_pos[0]])
            return row, col
        return False

    def update_game_state(self, end_square_piece):
        """Changes game_state to 'WHITE_WON' if the piece in the end square is the black king ('k').
        Otherwise, changes game_state to 'BLACK_WON' if the piece in the end square is the white king ('K')."""
        if end_square_piece == 'k':
            self._game_state = 'WHITE_WON'
        elif end_square_piece == 'K':
            self._game_state = 'BLACK_WON'

    def get_game_state(self):
        """Returns the game state ('UNFINISHED', 'WHITE_WON' or 'BLACK_WON'."""
        return self._game_state

    def switch_player_turn(self):
        """Switches turn from 'white' to 'black' or 'black' to 'white'."""
        if self._player_turn == 'white':
            self._player_turn = 'black'
        elif self._player_turn == 'black':
            self._player_turn = 'white'

    def move_piece(self, start_square, end_square):
        """Replaces the value at the end position given as a parameter with the value at the start position
        given as a parameter, and replaces the value at the start position with ' '."""
        start_row = start_square[0]
        start_col = start_square[1]
        end_row = end_square[0]
        end_col = end_square[1]
        game_board = self._game_board

        # set the value at the end square to the value in the start square
        game_board[end_row][end_col] = game_board[start_row][start_col]
        # set the value in the start square to empty: ' '
        game_board[start_row][start_col] = ' '

    def get_board(self, perspective):
        """
        Returns the list of lists representing the game board from the perspective given as a parameter by calling the
        """
        valid_move_set = set()
        # gets the board perspective object for the perspective given as a parameter
        board_perspective_object = self._board_perspective_dict[perspective]
        if perspective == 'audience':
            # return the board from the 'audience' perspective (passing an empty set as the arg)
            return board_perspective_object.get_board_from_perspective(valid_move_set)
        else:
            # get the pieces belonging to the player whose perspective the board is from
            perspective_player_pieces = self._player_pieces_dict[perspective]['player_pieces']
            for row in range(len(self._game_board)):
                for col in range(len(self._game_board[row])):
                    current_piece = self._game_board[row][col]
                    if current_piece != ' ':
                        # get the move type object associated with the current_piece type
                        move_type_object = self._move_type_dict[current_piece.lower()]
                        if current_piece in perspective_player_pieces:
                            valid_move_set.update(move_type_object.is_valid_move((row, col), perspective))
        # get the board from the given perspective, displaying opponent pieces as '*' unless they are at a location
        # in the valid_move_set
        board_from_perspective = board_perspective_object.get_board_from_perspective(valid_move_set)

        return board_from_perspective

    def make_move(self, start_square, end_square):
        """
        If the game state is 'UNFINISHED', there is piece at the start position (given
        by the parameter) that belongs to the player whose turn it is, and the move to the
        end position (given by the parameter) is legal, then makes the indicated
        move, removes the captured piece (if any), updates the game state (if applicable),
        and switches the turn to the other player.

        Returns True if valid move, otherwise returns False.
        """
        # if game state is not 'UNFINISHED', return False
        if self._game_state != 'UNFINISHED':
            return False

        # get the start_square matrix index from the algebraic location given by the parameter
        start_square = self.get_square_index(start_square)
        # get the end_square matrix index from the algebraic location given by the parameter
        end_square = self.get_square_index(end_square)

        # check that the start_square is within the game board bounds, otherwise return False
        if start_square is False:
            return False
        # check that the end_square is within the game board bounds, otherwise return False
        if end_square is False:
            return False

        # get the piece type in the move start square
        start_square_piece = self._game_board[start_square[0]][start_square[1]]
        # get the piece type in the move end square
        end_square_piece = self._game_board[end_square[0]][end_square[1]]

        # if the start square is empty or the piece in the start square belongs to the opponent,
        # return False
        opponent_pieces = self._player_pieces_dict[self._player_turn]['opponent_pieces']
        if start_square_piece == ' ' or start_square_piece in opponent_pieces:
            return False

        # get the move type object associated with the start_square_piece type
        move_type_object = self._move_type_dict[start_square_piece.lower()]

        # get a set of valid positions (end squares) the start_square_piece can move to
        valid_move_set = move_type_object.is_valid_move(start_square, self._player_turn)

        # if end_square is not one of the valid positions in the valid_move_set, return False
        if end_square not in valid_move_set:
            return False

        # move piece from start position to end position
        self.move_piece(start_square, end_square)

        # update the game state
        self.update_game_state(end_square_piece)
        print(self._game_state)

        # switch the player turn to the other player
        self.switch_player_turn()

        return True


class GameBoardDisplay:
    """Represents a game board display format."""
    def __init__(self, game_board, player_pieces_dict):
        self._game_board = game_board
        self._player_pieces_dict = player_pieces_dict


class Audience(GameBoardDisplay):
    """Represents a game board from the audience perspective."""
    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._audience_board = None

    def get_board_from_perspective(self, valid_move_set):
        """Returns a copy of the game board from the audience perspective as a nested list,
        displaying both white and black pieces."""
        self._audience_board = [[self._game_board[row][col] for col in range(len(self._game_board[row]))]
                                for row in range(len(self._game_board))]
        return self._audience_board


class White(GameBoardDisplay):
    """Represents a game board from the 'white player's perspective."""
    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._white_board = None

    def get_board_from_perspective(self, valid_move_set):
        """Returns a copy of the game board from the white player's perspective as a nested list,
        displaying white pieces and only the black pieces that can be captured by white pieces. The remaining
        black pieces are replaced by '*'."""
        self._white_board = [[self._game_board[row][col] for col in range(len(self._game_board[row]))]
                             for row in range(len(self._game_board))]
        opponent_pieces = self._player_pieces_dict['white']['opponent_pieces']

        for row in range(len(self._white_board)):
            for col in range(len(self._white_board[row])):
                # if there is an opponent piece in this position, and this position is not in the valid_move_set,
                # replace the piece at this position with '*'
                if self._white_board[row][col] in opponent_pieces and (row, col) not in valid_move_set:
                    self._white_board[row][col] = '*'

        return self._white_board


class Black(GameBoardDisplay):
    """Represents a game board from the 'black' player's perspective."""
    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._black_board = None

    def get_board_from_perspective(self, valid_move_set):
        """Returns a copy of the game board from the black player's perspective as a nested list,
        displaying black pieces and only the white pieces that can be captured by black pieces. The remaining
        white pieces are replaced by '*'."""
        self._black_board = [[self._game_board[row][col] for col in range(len(self._game_board[row]))]
                             for row in range(len(self._game_board))]
        opponent_pieces = self._player_pieces_dict['black']['opponent_pieces']

        for row in range(len(self._black_board)):
            for col in range(len(self._black_board[row])):
                # if there is an opponent piece in this position, and this position is not in the valid_move_set,
                # replace the piece at this position with '*'
                if self._black_board[row][col] in opponent_pieces and (row, col) not in valid_move_set:
                    self._black_board[row][col] = '*'

        return self._black_board


class Move:
    """
    Represents a move in a game of chess (Fog of War variant). Instantiated as a data member by ChessVar.
    """
    def __init__(self, game_board, player_pieces_dict):
        self._game_board = game_board
        self._valid_move_board = None
        self._player_turn = None
        self._player_pieces_dict = player_pieces_dict

    def get_valid_move_board(self):
        """Returns a copy of the game board to evaluate for valid moves."""
        self._valid_move_board = [[self._game_board[row][col] for col in range(len(self._game_board[row]))]
                                  for row in range(len(self._game_board))]
        return self._valid_move_board

    def get_vertical_moves(self, move_board, start_square, valid_moves_set=None, pos=None):
        """Finds all valid vertical moves for the piece in the start square given by the parameter.
        Adds the index of the end square of all valid moves to a set."""
        if pos is None:
            pos = start_square
            valid_moves_set = set()

        pos_row = pos[0]
        pos_col = pos[1]

        player_pieces = self._player_pieces_dict[self._player_turn]['player_pieces']
        opponent_pieces = self._player_pieces_dict[self._player_turn]['opponent_pieces']

        if pos_row < 0 or pos_row >= len(move_board):  # row is outside board bounds
            return
        if pos_col < 0 or pos_col >= len(move_board[pos_row]):  # col is outside board bounds
            return
        if move_board[pos_row][pos_col] in player_pieces and pos != start_square:  # piece in pos belongs to player
            return
        if move_board[pos_row][pos_col] in opponent_pieces:  # piece in pos belongs to opponent
            valid_moves_set.add(pos)
            return
        if pos in valid_moves_set:  # pos is in valid moves set
            return

        if move_board[pos_row][pos_col] == ' ':  # value at pos is ' '
            valid_moves_set.add(pos)

        # pos row is above or same as the start square row
        if pos_row <= start_square[0]:
            self.get_vertical_moves(move_board, start_square, valid_moves_set, (pos_row - 1, pos_col))  # try up
        # pos row is below or same as the start square row
        if pos_row >= start_square[0]:
            self.get_vertical_moves(move_board, start_square, valid_moves_set, (pos_row + 1, pos_col))  # try down

        return valid_moves_set

    def get_horizontal_moves(self, move_board, start_square, valid_moves_set=None, pos=None):
        """Finds all valid horizontal moves for the piece in the start square given by the parameter.
        Adds the index of the end square of all valid moves to a set."""
        if pos is None:
            pos = start_square
            valid_moves_set = set()

        pos_row = pos[0]
        pos_col = pos[1]

        player_pieces = self._player_pieces_dict[self._player_turn]['player_pieces']
        opponent_pieces = self._player_pieces_dict[self._player_turn]['opponent_pieces']

        if pos_row < 0 or pos_row >= len(move_board):  # row is outside board bounds
            return
        if pos_col < 0 or pos_col >= len(move_board[pos_row]):  # col is outside board bounds
            return
        if move_board[pos_row][pos_col] in player_pieces and pos != start_square:  # piece in pos belongs to player
            return
        if move_board[pos_row][pos_col] in opponent_pieces:  # piece in pos belongs to opponent
            valid_moves_set.add(pos)
            return
        if pos in valid_moves_set:  # pos is in valid moves set
            return

        if move_board[pos_row][pos_col] == ' ':  # value at pos is ' '
            valid_moves_set.add(pos)

        # pos col is left or same as the start square col
        if pos_col <= start_square[1]:
            self.get_horizontal_moves(move_board, start_square, valid_moves_set, (pos_row, pos_col - 1))  # try left
        # pos col is right or same as the start square col
        if pos_col >= start_square[1]:
            self.get_horizontal_moves(move_board, start_square, valid_moves_set, (pos_row, pos_col + 1))  # try right

        return valid_moves_set

    def get_diagonal_moves(self, move_board, start_square, valid_moves_set=None, pos=None):
        """Finds all valid diagonal moves for the piece in the start square given by the parameter.
        Adds the index of the end square of all valid moves to a set."""
        if pos is None:
            pos = start_square
            valid_moves_set = set()

        pos_row = pos[0]
        pos_col = pos[1]

        player_pieces = self._player_pieces_dict[self._player_turn]['player_pieces']
        opponent_pieces = self._player_pieces_dict[self._player_turn]['opponent_pieces']

        if pos_row < 0 or pos_row >= len(move_board):  # row is outside board bounds
            return
        if pos_col < 0 or pos_col >= len(move_board[pos_row]):  # col is outside board bounds
            return
        if move_board[pos_row][pos_col] in player_pieces and pos != start_square:  # piece in pos belongs to player
            return
        if move_board[pos_row][pos_col] in opponent_pieces:   # piece in pos belongs to opponent
            valid_moves_set.add(pos)
            return
        if pos in valid_moves_set:  # pos is in valid moves set
            return

        if move_board[pos_row][pos_col] == ' ':  # value at pos is ' '
            valid_moves_set.add(pos)

        # pos is above and right of start square, or same as start square
        if pos_row <= start_square[0] and pos_col >= start_square[1]:
            # try up, right
            self.get_diagonal_moves(move_board, start_square, valid_moves_set, (pos_row - 1, pos_col + 1))
        # pos is above and left of start square, or same as start square
        if pos_row <= start_square[0] and pos_col <= start_square[1]:
            # try up, left
            self.get_diagonal_moves(move_board, start_square, valid_moves_set, (pos_row - 1, pos_col - 1))
        # pos is below and right of start square, or same as start square
        if pos_row >= start_square[0] and pos_col >= start_square[1]:
            # try down, right
            self.get_diagonal_moves(move_board, start_square, valid_moves_set, (pos_row + 1, pos_col + 1))
        # pos is below and left of start square, or same as start square
        if pos_row >= start_square[0] and pos_col <= start_square[1]:
            # try down, left
            self.get_diagonal_moves(move_board, start_square, valid_moves_set, (pos_row + 1, pos_col - 1))

        return valid_moves_set

    def get_knight_king_moves(self, move_board, valid_directions, start_square):
        """Finds all valid moves for the king or knight piece in the start square given by the parameter.
        Adds the index of the end square of all valid moves to a set."""
        valid_moves_set = set()

        start_row = start_square[0]
        start_col = start_square[1]

        opponent_pieces = self._player_pieces_dict[self._player_turn]['opponent_pieces']

        for pos in range(len(valid_directions)):
            pos_row = start_row + valid_directions[pos][0]
            pos_col = start_col + valid_directions[pos][1]
            if 0 <= pos_row < len(move_board):  # row within board bounds
                if 0 <= pos_col < len(move_board[pos_row]):  # col within board bounds
                    valid_move = move_board[pos_row][pos_col]
                    if valid_move == ' ' or valid_move in opponent_pieces:
                        # add location of valid move end square to valid_moves_set
                        valid_moves_set.add((pos_row, pos_col))

        return valid_moves_set


class Queen(Move):
    """Represents a move made by a Queen and takes the game board list and a dictionary of player pieces as parameters.
    Inherits from Move class."""
    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._valid_queen_moves_set = set()

    def is_valid_move(self, start_square, player):
        """Finds valid moves for the piece in the start_square given by the parameter owned by the player given by the
        parameter. Returns a set of end square position tuples (row, col) for all valid moves."""
        valid_queen_moves_board = self.get_valid_move_board()
        self._player_turn = player
        self._valid_queen_moves_set = set()

        # get set of valid vertical queen move positions
        self._valid_queen_moves_set.update(self.get_vertical_moves(valid_queen_moves_board, start_square))

        # get set of valid horizontal queen move positions
        self._valid_queen_moves_set.update(self.get_horizontal_moves(valid_queen_moves_board, start_square))

        # get set of valid diagonal queen move positions
        self._valid_queen_moves_set.update(self.get_diagonal_moves(valid_queen_moves_board, start_square))

        return self._valid_queen_moves_set


class Bishop(Move):
    """Represents a move made by a Bishop and takes the game board list and a dictionary of player pieces as parameters.
    Inherits from Move class."""
    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._valid_bishop_moves_set = set()

    def is_valid_move(self, start_square, player):
        """Finds valid moves for the Bishop in the start_square given by the parameter owned by the player given by the
        parameter. Returns a set of end square position tuples (row, col) for all valid moves."""
        valid_bishop_moves_board = self.get_valid_move_board()
        self._player_turn = player
        self._valid_bishop_moves_set = set()

        # get set of valid diagonal bishop move positions
        self._valid_bishop_moves_set.update(self.get_diagonal_moves(valid_bishop_moves_board, start_square))

        return self._valid_bishop_moves_set


class Rook(Move):
    """Represents a move made by a Rook and takes the game board and a dictionary of player pieces as parameters.
    Inherits from Move class."""
    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._valid_rook_moves_set = set()

    def is_valid_move(self, start_square, player):
        """Finds valid moves for the Rook in the start_square given by the parameter owned by the player given by the
        parameter. Returns a set of end square position tuples (row, col) for all valid moves."""
        valid_rook_moves_board = self.get_valid_move_board()
        self._player_turn = player
        self._valid_rook_moves_set = set()

        # get set of valid vertical rook move positions
        self._valid_rook_moves_set.update(self.get_vertical_moves(valid_rook_moves_board, start_square))

        # get set of valid horizontal rook move positions
        self._valid_rook_moves_set.update(self.get_horizontal_moves(valid_rook_moves_board, start_square))

        return self._valid_rook_moves_set


class Knight(Move):
    """Represents a move made by a Knight and takes the game board and a dictionary of player pieces as parameters.
    Inherits from Move class."""

    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._valid_knight_moves_set = set()
        self._valid_move_directions = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2]]
#

    def is_valid_move(self, start_square, player):
        """Finds valid moves for the Knight in the start_square given by the parameter owned by the player given by the
            parameter. Returns a set of end square position tuples (row, col) for all valid moves."""
        valid_knight_moves_board = self.get_valid_move_board()
        valid_move_directions = self._valid_move_directions
        self._player_turn = player
        self._valid_knight_moves_set = set()

        valid_knight_moves = self.get_knight_king_moves(valid_knight_moves_board, valid_move_directions, start_square)
        # get set of valid Knight move positions
        self._valid_knight_moves_set.update(valid_knight_moves)

        return self._valid_knight_moves_set


class King(Move):
    """Represents a move made by a King and takes the game board and a dictionary of player pieces as parameters.
    Inherits from Move class."""

    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._valid_king_moves_set = set()
        self._valid_move_directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    def is_valid_move(self, start_square, player):
        """Finds valid moves for the King in the start_square given by the parameter owned by the player given by the
        parameter. Returns a set of end square position tuples (row, col) for all valid moves."""
        king_moves_board = self.get_valid_move_board()
        valid_move_directions = self._valid_move_directions
        self._player_turn = player
        self._valid_king_moves_set = set()

        valid_king_moves = self.get_knight_king_moves(king_moves_board, valid_move_directions, start_square)
        # get set of valid King move positions
        self._valid_king_moves_set.update(valid_king_moves)

        return self._valid_king_moves_set


class Pawn(Move):
    """Represents a move made by a Pawn and takes the game board and a dictionary of player pieces as parameters.
    Inherits from Move class."""
    def __init__(self, game_board, player_pieces_dict):
        super().__init__(game_board, player_pieces_dict)
        self._valid_pawn_moves_set = set()
        self._valid_move_directions = {
            'white': {
                "one_square": (-1, 0),
                "two_squares": (-2, 0),
                "diagonal_capture": [
                    (-1, -1), (-1, 1)
                    ],
                "initial_row": 6
            },
            'black': {
                "one_square": (1, 0),
                "two_squares": (2, 0),
                "diagonal_capture": [
                    (1, -1), (1, 1)
                    ],
                "initial_row": 1
            }
        }

    def is_valid_move(self, start_square, player):
        """Finds valid moves for the Pawn in the start_square given by the parameter owned by the player given by the
        parameter. Returns a set of end square position tuples (row, col) for all valid moves."""
        valid_pawn_moves_board = self.get_valid_move_board()
        valid_move_directions = self._valid_move_directions
        self._player_turn = player
        self._valid_pawn_moves_set = set()
        opponent_pieces = self._player_pieces_dict[player]['opponent_pieces']

        start_row = start_square[0]
        start_col = start_square[1]

        # check square one move "forward" (away from player's side)
        one_square_row = start_row + valid_move_directions[player]["one_square"][0]
        one_square_col = start_col + valid_move_directions[player]["one_square"][1]
        if 0 <= one_square_row < len(valid_pawn_moves_board):
            if 0 <= one_square_col < len(valid_pawn_moves_board[one_square_row]):
                if valid_pawn_moves_board[one_square_row][one_square_col] == ' ':
                    self._valid_pawn_moves_set.add((one_square_row, one_square_col))

        # check square two moves "forward" (away from player's side) from initial position on board
        two_squares_row = start_row + valid_move_directions[player]["two_squares"][0]
        two_squares_col = start_col + valid_move_directions[player]["two_squares"][1]
        initial_row = valid_move_directions[player]["initial_row"]
        if start_row == initial_row:
            if 0 <= two_squares_row < len(valid_pawn_moves_board):
                if 0 <= two_squares_col < len(valid_pawn_moves_board[two_squares_row]):
                    if valid_pawn_moves_board[two_squares_row][two_squares_col] == ' ':
                        self._valid_pawn_moves_set.add((two_squares_row, two_squares_col))

        # check diagonal left capture square (away from player's side)
        diagonal_capture_left_row = start_row + valid_move_directions[player]["diagonal_capture"][0][0]
        diagonal_capture_left_col = start_col + valid_move_directions[player]["diagonal_capture"][0][1]
        if 0 <= diagonal_capture_left_row < len(valid_pawn_moves_board):
            if 0 <= diagonal_capture_left_col < len(valid_pawn_moves_board[diagonal_capture_left_row]):
                if valid_pawn_moves_board[diagonal_capture_left_row][diagonal_capture_left_col] in opponent_pieces:
                    self._valid_pawn_moves_set.add((diagonal_capture_left_row, diagonal_capture_left_col))

        # check diagonal right capture square (away from player's side)
        diagonal_capture_right_row = start_row + valid_move_directions[player]["diagonal_capture"][1][0]
        diagonal_capture_right_col = start_col + valid_move_directions[player]["diagonal_capture"][1][1]
        if 0 <= diagonal_capture_right_row < len(valid_pawn_moves_board):
            if 0 <= diagonal_capture_right_col < len(valid_pawn_moves_board[diagonal_capture_right_row]):
                if valid_pawn_moves_board[diagonal_capture_right_row][diagonal_capture_right_col] in opponent_pieces:
                    self._valid_pawn_moves_set.add((diagonal_capture_right_row, diagonal_capture_right_col))

        return self._valid_pawn_moves_set
