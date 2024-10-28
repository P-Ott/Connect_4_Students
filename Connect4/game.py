import uuid
import random
from enum import Enum
import numpy as np


class Connect4:
    """
    Connect 4 Game Class

        Defines rules of the Game
            - what is a win
            - where can you set / not set a coin
            - how big is the playing field

        Also keeps track of the current game  
            - what is its state
            - who is the active player?

        Is used by the Coordinator
            -> executes the methods of a Game object
    """
    
    def __init__(self) -> None:
        """ 
        Init a Connect 4 Game
            - Create an empty Board
            - Create to (non - registered and empty) players.
            - Set the Turn Counter to 0
            - Set the Winner to False
            - etc.
        """
        self.board = None
        self.registered = {"Player1": None, "Player2": None}
        self.counter = 0
        self.winner = False

    """
    Methods to be exposed to the API later on
    """
    def get_status(self):
        """
        Get the game's status.
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
        """
        if self.winner == True:
            return self.activeplayer
        else:
            return self.activeplayer, self.counter
        
    def register_player(self, player_id:uuid.UUID)->str:
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon:       Player Icon (or None if failed)
        """
        if self.registered["Player1"] == None:
            self.registered["Player1"] = player_id
        else:
            self.registered["Player2"] = player_id

    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board
        """
        self.board = np.ndarray(shape=(7, 8), dtype="<U1")

        if self.activeplayer == self.registered.get("Player1"):
            self.board[self.move] = "X"
            Connect4.__detect_win()
        else:
            self.board[self.move] = "0"
            Connect4.__detect_win()
        return self.board

    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        """
        if column >= 1 and column <= 8:
            col = column - 1
            values = ["X", "0"]
            exists = np.isin(self.board[:,col], values)
            nextrow = np.where(exists)[0]
            self.move = (nextrow, col)
            if nextrow > 0:
                Connect4.get_board(self.move)
                return True
            elif nextrow == 0:
                return f"Game over"
            else:
                raise KeyError(f"This couldn't be")
        else: 
            return False
            
    """ 
    Internal Method (for Game Logic)
    """
    def __update_status(self):
        """ 
        Update all values for the status (after each successful move)
            - active player
            - active ID
            - winner
            - turn_number
        """
        if Connect4.__detect_win() == True:
                self.winner = True
        else:
                # check the next playersturn
            if self.counter % 2 == 0:
                self.activeplayer = self.registered.get("Player1")
            else:
                self.activeplayer = self.registered.get("Player2")
                # add a new turn
            self.counter += 1
    

    def __detect_win(self) -> bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            True if there's a winner, False otherwise
        """    

        Connect4.__update_status()
        