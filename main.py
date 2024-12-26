import os  # Importing the os module to handle operating system tasks like clearing the console screen

# DECORATOR FOR LOGGING MOVE
def log_move(func):  # Defining a decorator function to log moves
    def wrapper(self, move):  # Wrapper function to log the move before calling the original function
        print(f"Making move: {move}")  # LOGGING THE MOVE
        return func(self, move)  # Calling the original function with the move
    return wrapper  # Returning the wrapper function

# Base class for chess pieces
class Piece:
    def __init__(self, color):  # Constructor for initializing the color of the piece
        self.color = color  # Assigning color to the piece

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):  # Abstract method to be implemented by subclasses
        raise NotImplementedError("This method should be overridden by subclasses")  # Raise error if not implemented by subclasses

# Class for pawn
class Pawn(Piece):
    def is_valid_move(self, start_row, start_col, end_row, end_col, board):  # Method to check if the pawn's move is valid
        direction = -1 if self.color == 'w' else 1  # Determine the direction based on color: white moves up (-1), black moves down (+1)
        start_rank = 6 if self.color == 'w' else 1  # White pawns start at row 6, black pawns start at row 1

        # Moving 1 square forward (straight)
        if start_col == end_col and board[end_row][end_col] == ' ' and end_row == start_row + direction:
            return True  # Valid move

        # Moving 2 squares forward from the starting position
        if start_col == end_col and board[end_row][end_col] == ' ' and start_row == start_rank and end_row == start_row + 2 * direction:
            if board[start_row + direction][start_col] == ' ':
                return True  # Valid move

        # Capturing diagonally
        if abs(start_col - end_col) == 1 and start_row + direction == end_row and board[end_row][end_col] != ' ':
            if self.color != board[end_row][end_col].lower():  # Check if it's a valid capture (opponent's piece)
                return True  # Valid capture

        return False  # If none of the conditions are met, the move is invalid

# Class for Rook
class Rook(Piece):
    def is_valid_move(self, start_row, start_col, end_row, end_col, board):  # Check if the rook's move is valid
        if start_row == end_row:  # Horizontal move
            step = 1 if start_col < end_col else -1  # Determine the direction (right or left)
            for col in range(start_col + step, end_col, step):  # Loop through the columns between the start and end positions
                if board[start_row][col] != ' ':  # Check if any piece blocks the path
                    return False  # Invalid move if a piece is in the way
            return True  # Valid move

        elif start_col == end_col:  # Vertical move
            step = 1 if start_row < end_row else -1  # Determine the direction (up or down)
            for row in range(start_row + step, end_row, step):  # Loop through the rows between the start and end positions
                if board[row][start_col] != ' ':  # Check if any piece blocks the path
                    return False  # Invalid move if a piece is in the way
            return True  # Valid move

        return False  # If the move is neither horizontal nor vertical, it's invalid

# Class for Knight
class Knight(Piece):
    def is_valid_move(self, start_row, start_col, end_row, end_col, board):  # Check if the knight's move is valid
        # A knight moves in an L shape: 2 squares in one direction and 1 in the other
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
           (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True  # Valid knight move
        return False  # Invalid move

# Class for Bishop
class Bishop(Piece):
    def is_valid_move(self, start_row, start_col, end_row, end_col, board):  # Check if the bishop's move is valid
        if abs(start_row - end_row) == abs(start_col - end_col):  # Bishop moves diagonally
            step_row = 1 if start_row < end_row else -1  # Determine the direction (down or up)
            step_col = 1 if start_col < end_col else -1  # Determine the direction (right or left)
            row, col = start_row + step_row, start_col + step_col
            while row != end_row and col != end_col:  # Check each square along the diagonal path
                if board[row][col] != ' ':  # If a piece is blocking the path, it's an invalid move
                    return False
                row += step_row  # Move along the diagonal
                col += step_col  # Move along the diagonal
            return True  # Valid move if no pieces are in the way

        return False  # If the move isn't diagonal, it's invalid

# Class for Queen
class Queen(Piece):
    def is_valid_move(self, start_row, start_col, end_row, end_col, board):  # Check if the queen's move is valid
        rook = Rook(self.color)  # Create a rook object to check vertical and horizontal moves
        bishop = Bishop(self.color)  # Create a bishop object to check diagonal moves
        return rook.is_valid_move(start_row, start_col, end_row, end_col, board) or \
               bishop.is_valid_move(start_row, start_col, end_row, end_col, board)  # Queen can move like both a rook and bishop

# Class for King
class King(Piece):
    def is_valid_move(self, start_row, start_col, end_row, end_col, board):  # Check if the king's move is valid
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:  # King moves one square in any direction
            return True  # Valid move
        return False  # Invalid move if the king moves more than one square

# Main class for the chess game
class ChessGame:
    def __init__(self):  # Constructor to initialize the game state
        self.board = [  # Setting up the initial chessboard
            [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')],  # Black pieces
            [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],  # Black pawns
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # Empty row
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # Empty row
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # Empty row
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # Empty row
            [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],  # White pawns
            [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')]  # White pieces
        ]
        self.turn = 'w'  # White starts the game

    def print_board(self):  # Method to print the chessboard
        print("  +---+---+---+---+---+---+---+---+")  # Print board separator
        for i, row in enumerate(self.board):  # Loop through each row
            print(8 - i, end=" | ")  # Print row number (from top to bottom)
            for piece in row:  # Loop through each piece in the row
                print(type(piece).__name__[0] + " | ", end="")  # Print the piece type (first letter)
            print(8 - i)  # Print row number again (from top to bottom)
            print("  +---+---+---+---+---+---+---+---+")  # Print board separator
        print("    a   b   c   d   e   f   g   h  ")  # Print column labels

    def convert_position(self, pos):  # Convert chess notation (e.g., e2) to matrix coordinates
        col = ord(pos[0]) - ord('a')  # Convert column letter to index (e.g., 'a' -> 0)
        row = 8 - int(pos[1])  # Convert row number to index (e.g., '8' -> 0)
        return row, col  # Return the row and column indices

    def get_move(self):  # Get the user's move input
        while True:  # Loop until a valid move is entered
            move = input(f"{self.turn.upper()}'s move (e.g., e2e4): ").lower()  # Get the move from user
            if len(move) == 4 and move[0] in 'abcdefgh' and move[1] in '12345678' and move[2] in 'abcdefgh' and move[3] in '12345678':
                return move  # Return the move if it's in the correct format
            print("Invalid move format. Use e.g., e2e4")  # Print error message for invalid format

    @log_move  # Decorator for logging moves
    def make_move(self, move):  # Make the move on the board
        start_pos = move[:2]  # Extract the start position (e.g., e2)
        end_pos = move[2:]  # Extract the end position (e.g., e4)
        start_row, start_col = self.convert_position(start_pos)  # Convert start position to indices
        end_row, end_col = self.convert_position(end_pos)  # Convert end position to indices

        piece = self.board[start_row][start_col]  # Get the piece at the start position

        if piece == ' ':  # Check if there is no piece at the start position
            print("No piece to move")  # Print error message
            return False  # Return false

        if (piece.color == 'w' and self.turn == 'b') or (piece.color == 'b' and self.turn == 'w'):  # Check if it's the wrong player's turn
            print("Wrong color piece")  # Print error message
            return False  # Return false

        if not piece.is_valid_move(start_row, start_col, end_row, end_col, self.board):  # Check if the move is valid
            print(f"Invalid move for {type(piece).__name__}")  # Print error message
            return False  # Return false

        self.board[end_row][end_col] = piece  # Move the piece to the new position
        self.board[start_row][start_col] = ' '  # Clear the old position
        self.turn = 'b' if self.turn == 'w' else 'w'  # Switch the turn to the other player
        return True  # Return true if the move was successful

    def play(self):  # Main game loop
        while True:  # Continuously run the game until it's over
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console screen based on the operating system
            self.print_board()  # Print the board to the screen
            move = self.get_move()  # Get the player's move
            self.make_move(move)  # Make the move

if __name__ == "__main__":  # Check if the script is being run directly
    game = ChessGame()  # Create a new game object
    game.play()  # Start the game