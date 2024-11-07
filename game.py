from board import Board
from chessman import Pawn, Rook, knight, Bishop, Queen, King


class Game:
    def __init__(self):
        self.board = Board()
        self.white_king = None
        self.black_king = None
        self.is_playing = True

    def remove_chessman(self):
        self.board[input("Square: ")].who_is_here.delete()

    def change_position(self):
        chessman = self.board[input("Square: ")].who_is_here
        next_position = self.board[input("to: ")]
        chessman.delete()
        chessman.position = next_position
        chessman.place()

    def get_king(self):
        pos = input("Position: ")
        print(self.board[pos].who_is_here.king)

    def classic_chessman_position(self):

        #King
        self.board["E1"].who_is_here = King("white", self.board["E1"], "K_")

        self.board["E8"].who_is_here = King("black", self.board["E8"], "k_")

        self.white_king = self.board["E1"].who_is_here
        self.black_king = self.board["E8"].who_is_here

        for column in "ABCDEFGH":
            target = self.board[f"{column}2"]
            target.who_is_here = Pawn("white", target, "P_", self.white_king)

            target = self.board[f"{column}7"]
            target.who_is_here = Pawn("black", target, "p_", self.black_king)

        #Rooks
        self.board["A1"].who_is_here = Rook("white", self.board["A1"], "R_", self.white_king)
        self.board["H1"].who_is_here = Rook("white", self.board["H1"], "R_", self.white_king)

        self.board["A8"].who_is_here = Rook("black", self.board["A8"], "r_", self.black_king)
        self.board["H8"].who_is_here = Rook("black", self.board["H8"], "r_", self.black_king)

        # Knights
        self.board["B1"].who_is_here = knight("white", self.board["B1"], "N_", self.white_king)
        #self.board["G1"].who_is_here = knight("white", self.board["G1"], "N_", self.white_king)

        self.board["B8"].who_is_here = knight("black", self.board["B8"], "n_", self.black_king)
        self.board["G8"].who_is_here = knight("black", self.board["G8"], "n_", self.black_king)

        #Bishop
        self.board["C1"].who_is_here = Bishop("white", self.board["C1"], "B_", self.white_king)
        #self.board["F1"].who_is_here = Bishop("white", self.board["F1"], "B_", self.white_king)

        self.board["C8"].who_is_here = Bishop("black", self.board["C8"], "b_", self.black_king)
        self.board["F8"].who_is_here = Bishop("black", self.board["F8"], "b_", self.black_king)

        #Queen
        self.board["D1"].who_is_here = Queen("white", self.board["D1"], "Q_", self.white_king)

        self.board["D8"].who_is_here = Queen("black", self.board["D8"], "q_", self.black_king)

    def play(self):
        moves = 0
        while True:
            print(self.board)
            key = input("Select a pawn: ")

            if key == "cheat!":
                try:
                    command = eval(input("- "))
                    command()
                except:
                    print("cheat not allowed.")

            else:
                try:
                    pawn_selected = self.board[key].who_is_here
                    if (pawn_selected.color == "white" and (moves %2 == 0)) or (pawn_selected.color == "black" and (moves %2 != 0)):
                        if pawn_selected is not None:
                            new_pos = self.board[input(f"Move to {pawn_selected.get_capturable_destinations()}: ")]
                            pawn_selected.move_to(new_pos)
                            moves += 1
                            self.board.pivot()
                    else: print("Nop")
                    
                except Exception as e:
                    print(e)
                finally:
                    print("White: ", self.white_king.is_check())
                    print("Black: ", self.black_king.is_check())
