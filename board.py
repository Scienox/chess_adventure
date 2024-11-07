class _Case:
    def __init__(self):
        self.name = ""
        self.who_is_here = None
        self.top = None
        self.right = None
        self.down = None
        self.left = None
        self.top_left = None
        self.top_right = None
        self.down_left = None
        self.down_right = None

    def set_top(self, rowNumber, columnNumber, matrix):
        if rowNumber > 0:
            self.top = matrix[rowNumber-1][columnNumber]
            if columnNumber > 0:
                self.top_left = matrix[rowNumber-1][columnNumber-1]
            if columnNumber < 7:
                self.top_right = matrix[rowNumber-1][columnNumber+1]
            
    def set_right(self, rowNumber, columnNumber, matrix):
        if columnNumber < 7:
            self.right = matrix[rowNumber][columnNumber+1]

    def set_down(self, rowNumber, columnNumber, matrix):
        if rowNumber < 7:
            self.down = matrix[rowNumber+1][columnNumber]
            if columnNumber > 0:
                self.down_left = matrix[rowNumber+1][columnNumber-1]
            if columnNumber < 7:
                self.down_right = matrix[rowNumber+1][columnNumber+1]

    def set_left(self, rowNumber, columnNumber, matrix):
        if columnNumber > 0:
            self.left = matrix[rowNumber][columnNumber-1]

    def set_neighbors(self, rowNumber, columnNumber, matrix, name):
        self.name = name
        self.set_top(rowNumber, columnNumber, matrix)
        self.set_right(rowNumber, columnNumber, matrix)
        self.set_down(rowNumber, columnNumber, matrix)
        self.set_left(rowNumber, columnNumber, matrix)

    def forget_pawn(self):
        self.who_is_here = None
    
    def set_pawn(self, newPawn):
        self.who_is_here = newPawn

    def __repr__(self):
        return self.name


class Board:
    def __init__(self):
        self.matrix = [[_Case() for _ in range(8)] for _ in range(8)]
        self.__geometry = 8
        self.__build_matrix()


    def __build_matrix(self):
        nameListW = "ABCDEFGH"
        for row in range(self.__geometry):
            for colmun in range(self.__geometry):
                self.matrix[row][colmun].set_neighbors(row, colmun, self.matrix, f"{nameListW[colmun]}{7-row+1}")

    def pivot(self):
        self.matrix = (list(reversed(self.matrix)))

    def __getitem__(self, name):
        if isinstance(name, str):
            for row in range(self.__geometry):
                for column in range(self.__geometry):
                    step = self.matrix[row][column]
                    if step.name == name:
                        return step

    def __repr__(self):
        itemView = " " + "---"*8 + "\n"
        for row in range(self.__geometry):
            for column in range(self.__geometry):
                content = self.matrix[row][column].who_is_here
                itemView += ("| "if column == 0 else "") + ("__" if content is None else content.__str__()) + (" " if column < 7 else " |\n")
        itemView += " " + "---"*8
        return itemView
