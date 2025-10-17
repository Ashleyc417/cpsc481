from games import *
from typing import List, Tuple

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board: List[int] = [3,1]):
        self.initial = GameState(to_move = 'MAX',
                                 utility = 0, 
                                 board = board, 
                                 moves = self.generate_valid_moves(GameState(board)))

    def generate_valid_moves(self, board: List[int]) -> List[Tuple[int, int]]:
        """Generate all valid moves for the current state."""
        moves: List[Tuple[int, int]]= []
        # Go through each row and create a list of possible moves
        for row in range(len(board)):
            # Count up from 1 to the number of objects in that row
            for num_to_remove in range(1, board[row] + 1):
                moves.append((row, num_to_remove))
        return moves
                

    def actions(self, state: GameState) -> List[Tuple[int, int]]:
        """Legal moves are a6t least one object, all from the same row."""
        return state.moves
    
    def result(self, state: GameState, move: Tuple[int, int]) -> GameState:
        """Return the new state after a move."""
        # If the move is not legal, return the current state
        if move not in state.moves:
            return state
        
        # Create a new board configuration
        board = state.board.copy()
        row, num_to_remove = move
        board[row] -= num_to_remove
        
        # Determine the next player
        next_player = 'MIN' if state.to_move == 'MAX' else 'MAX'
        
        # Create the new state
        new_state = GameState(to_move=next_player,
                              utility=self.utility(state, state.to_move),
                              board=board,
                              moves=self.actions(GameState(board)))
        return new_state


    def utility(self, state: GameState, player: str) -> int:
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        if self.terminal_test(state):
            return -1 if state.to_move == player else 1
        else:
            return 0

    def terminal_test(self, state: GameState) -> bool:
        """A state is terminal if there are no objects left"""
        return all(num_in_row == 0 for num_in_row in state.board)

    def display(self, state: GameState) -> None:
        print("board: ", state.board)


if __name__ == "__main__":
    nim = GameOfNim(board=[0, 5, 3, 1]) # Creating the game instance
    #nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    print(nim.initial.board) # must be [0, 5, 3, 1]
    print(nim.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
    print(nim.result(nim.initial, (1,3) ))
    utility = nim.play_game(alpha_beta_player, query_player) # computer moves first 
    if (utility < 0):
        print("MIN won the game")
    else:
        print("MAX won the game")
