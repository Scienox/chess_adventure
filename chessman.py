class _ChessmanStructure:
    def __init__(self, color, position, type_, king=None):
        self.king = king
        self.position = position
        self.type = type_
        self.color = color
        self.line_of_sight = []
        self.capturable_destinations = []

    def change_position(self, newPosition):
        #if newPosition in self.line_of_sight: """ I forgot why this condition existe. It produces errors """
        self.position.forget_pawn()
        newPosition.set_pawn(self)
        self.position = newPosition

    def place(self):
        self.position.who_is_here = self

    def delete(self):
        self.position.who_is_here = None

    def is_capturable(self, chessman_case):
        chessman = chessman_case.who_is_here
        if chessman:
            # the king it's not capturable
            if isinstance(chessman, King):
                return False
        # return if the next move is in check - return false if check is true
        return not self.next_placement_is_check(chessman_case)

    def uncapturable_check(self):
        capturable_square = self.line_of_sight.copy()
        line_of_sight_current = 0
        while line_of_sight_current < len(capturable_square):
            target = capturable_square[line_of_sight_current]
            if not self.is_capturable(target):
                capturable_square.pop(line_of_sight_current)
                line_of_sight_current -= 1
            line_of_sight_current += 1
        self.capturable_destinations = capturable_square.copy()

    def get_capturable_destinations(self):
        self.get_line_of_sight()  # subclass function
        self.uncapturable_check()
        return self.capturable_destinations

    def move_to(self, position):
        if position in self.capturable_destinations:
            if isinstance(self, (Pawn, Rook, King)):
                self.start = False
                if isinstance(self, King):
                    if position == self.queenside_castling():
                        rook_left = position.left.left.who_is_here
                        if rook_left:
                            rook_left.delete()
                            rook_left.position = position.right
                            rook_left.place()
                    if position == self.kingside_castling():
                        rook_right = position.right.who_is_here
                        if rook_right:
                            rook_right.delete()
                            rook_right.position = position.left
                            rook_right.place()

            self.change_position(position)
            if isinstance(self, Pawn):
                self.trans()

    def check_alliance(self):
        destination_iter = 0
        while destination_iter != len(self.line_of_sight):
            destination_current = self.line_of_sight[destination_iter].who_is_here
            if isinstance(destination_current, _ChessmanStructure):
                if self.color == destination_current.color:
                    self.line_of_sight.pop(destination_iter)
                    destination_iter -= 1
            destination_iter += 1

    def pawn_move(self):
        if self.color == "white":
            if self.position.top and self.position.top.who_is_here is None:
                self.line_of_sight.append(self.position.top)
            if self.start is True:
                self.line_of_sight.append(self.position.top.top)
            if self.position.top_left and self.position.top_left.who_is_here is not None:
                self.line_of_sight.append(self.position.top_left)
            if self.position.top_right and self.position.top_right.who_is_here is not None:
                self.line_of_sight.append(self.position.top_right)
        else:
            if self.position.down and self.position.down.who_is_here is None:
                self.line_of_sight.append(self.position.down)
            if self.start is True:
                self.line_of_sight.append(self.position.down.down)
            if self.position.down_left and self.position.down_left.who_is_here is not None:
                self.line_of_sight.append(self.position.down_left)
            if self.position.down_right and self.position.down_right.who_is_here is not None:
                self.line_of_sight.append(self.position.down_right)
        self.check_alliance()

    def vertical_and_horizontal_move(self):
        topTarget = self.position.top
        while topTarget:
            if topTarget.who_is_here is not None:
                self.line_of_sight.append(topTarget)
                break
            self.line_of_sight.append(topTarget)
            topTarget = topTarget.top

        downTarget = self.position.down
        while downTarget:
            if downTarget.who_is_here is not None:
                self.line_of_sight.append(downTarget)
                break
            self.line_of_sight.append(downTarget)
            downTarget = downTarget.down
        leftTarget = self.position.left
        while leftTarget:
            if leftTarget.who_is_here is not None:
                self.line_of_sight.append(leftTarget)
                break
            self.line_of_sight.append(leftTarget)
            leftTarget = leftTarget.left
        rightTarget = self.position.right
        while rightTarget:
            if rightTarget.who_is_here is not None:
                self.line_of_sight.append(rightTarget)
                break
            self.line_of_sight.append(rightTarget)
            rightTarget = rightTarget.right
        self.check_alliance()

    def y_move(self):
        if self.position.top:
            if self.position.top.top:
                if self.position.top.top_left:
                    self.line_of_sight.append(self.position.top.top_left)
                if self.position.top.top_right:
                    self.line_of_sight.append(self.position.top.top_right)
        if self.position.left:
            if self.position.left.left:
                if self.position.left.top_left:
                    self.line_of_sight.append(self.position.left.top_left)
                if self.position.left.down_left:
                    self.line_of_sight.append(self.position.left.down_left)

        if self.position.down:
            if self.position.down.down:
                if self.position.down.down_left:
                    self.line_of_sight.append(self.position.down.down_left)
                if self.position.down.down_right:
                    self.line_of_sight.append(self.position.down.down_right)
        if self.position.right:
            if self.position.right.right:
                if self.position.right.top_right:
                    self.line_of_sight.append(self.position.right.top_right)
                if self.position.right.down_right:
                    self.line_of_sight.append(self.position.right.down_right)
        self.check_alliance()

    def diagonal_move(self):
        top_left_target = self.position.top_left
        while top_left_target:
            if top_left_target.who_is_here is not None:
                self.line_of_sight.append(top_left_target)
                break
            self.line_of_sight.append(top_left_target)
            top_left_target = top_left_target.top_left
        top_right_target = self.position.top_right
        while top_right_target:
            if top_right_target.who_is_here is not None:
                self.line_of_sight.append(top_right_target)
                break
            self.line_of_sight.append(top_right_target)
            top_right_target = top_right_target.top_right
        down_left = self.position.down_left
        while down_left:
            if down_left.who_is_here is not None:
                self.line_of_sight.append(down_left)
                break
            self.line_of_sight.append(down_left)
            down_left = down_left.down_left
        down_right = self.position.down_right
        while down_right:
            if down_right.who_is_here is not None:
                self.line_of_sight.append(down_right)
                break
            self.line_of_sight.append(down_right)
            down_right = down_right.down_right
        self.check_alliance()

    def neighbor_move(self):
        if self.position.top:
            self.line_of_sight.append(self.position.top)
            if self.position.top_left:
                self.line_of_sight.append(self.position.top_left)
            if self.position.top_right:
                self.line_of_sight.append(self.position.top_right)
        if self.position.left:
            self.line_of_sight.append(self.position.left)
        if self.position.right:
            self.line_of_sight.append(self.position.right)
        if self.position.down:
            self.line_of_sight.append(self.position.down)
            if self.position.down_left:
                self.line_of_sight.append(self.position.down_left)
            if self.position.down_right:
                self.line_of_sight.append(self.position.down_right)
        self.check_alliance()

    def read_board(self):
        target_top = self.position
        while target_top.top:
            target_top = target_top.top
        target_left = target_top
        while target_left.left:
            target_left = target_left.left
        row = 0
        row_target = target_left
        column_target = target_left
        while row < 8:
            for _ in range(8):
                yield column_target
                column_target.right
                column_target = column_target.right
            row += 1
            row_target = row_target.down
            column_target = row_target

    def who_has_me_in_his_sights(self, position):
        bad_places = []
        for square in self.read_board():
            chessman = square.who_is_here
            if chessman and (chessman.color != self.color):
                 for _position in chessman.get_line_of_sight():
                    if _position == position:
                        bad_places.append(_position)
        return bad_places

    def who_checks_me(self):
        return self.who_has_me_in_his_sights(self.position)
    
    def next_placement_is_check(self, next_position):
        return_value = None
        def reset():
            self.change_position(save_self_position)
            if save_next_position_who_is_here:
                save_next_position_who_is_here.change_position(next_position)
        if isinstance(self, King):
            k = self
        else:
            k = self.king
        save_next_position_who_is_here = next_position.who_is_here
        save_self_position = self.position
        self.change_position(next_position)
        if k.is_check():
            return_value = True
        else:
            return_value = False
        reset()
        return return_value

    def is_check(self):
        return len(self.who_checks_me())
    
    def __eq__(self, other):
        if isinstance(other, _ChessmanStructure):
            return self.position == other.position
        else: return NotImplemented

    def __str__(self):
        return str(self.type)

    def __repr__(self):
        return f"{self.type} | {self.color} | {self.position}"


class Pawn(_ChessmanStructure):
    def __init__(self, *options):
        super().__init__(*options)
        self.start = True
        self.transCapacity = "8" if self.color == "white" else "1"

    def get_line_of_sight(self):
        self.line_of_sight.clear()
        self.pawn_move()
        return self.line_of_sight
            
    def trans(self):
        if self.position.name[1] == self.transCapacity:
            newClass = input("Class: ")
            self.delete()
            newTrans = eval(newClass)
            newTrans(self.color, self.position, input('Type: ')).place()


class Rook(_ChessmanStructure):
    def __init__(self, *options):
        super().__init__(*options)
        self.start = True

    def get_line_of_sight(self):
        self.line_of_sight.clear()
        self.vertical_and_horizontal_move()
        return self.line_of_sight


class knight(_ChessmanStructure):
    def __init__(self, *options):
        super().__init__(*options)

    def get_line_of_sight(self):
        self.line_of_sight.clear()
        self.y_move()
        return self.line_of_sight


class Bishop(_ChessmanStructure):
    def __init__(self, *options):
        super().__init__(*options)

    def get_line_of_sight(self):
        self.line_of_sight.clear()
        self.diagonal_move()
        return self.line_of_sight


class Queen(_ChessmanStructure):
    def __init__(self, *options):
        super().__init__(*options)

    def get_line_of_sight(self):
        self.line_of_sight.clear()
        self.vertical_and_horizontal_move()
        self.diagonal_move()
        return self.line_of_sight


class King(_ChessmanStructure):
    def __init__(self, *options):
        super().__init__(*options)
        self.start = True
        self.check = False

    def kingside_castling(self):
        bishop_right = self.position.right
        knight_right = bishop_right.right
        rook_right = knight_right.right
        if rook_right.who_is_here and isinstance(rook_right.who_is_here, Rook):
            if not bishop_right.who_is_here and not knight_right.who_is_here:
                if not self.is_check() and rook_right.who_is_here.start:
                    if (bishop_right not in self.who_has_me_in_his_sights(bishop_right)) and \
                        (knight_right not in self.who_has_me_in_his_sights(knight_right)): 
                        return knight_right
                
    def queenside_castling(self):
        queen = self.position.left
        bishop_left = queen.left
        knight_left = bishop_left.left
        rook_left = knight_left.left
        if  rook_left.who_is_here and isinstance(rook_left.who_is_here, Rook) and self.color == rook_left.who_is_here.color:
            if not queen.who_is_here and not bishop_left.who_is_here and not knight_left.who_is_here:
                if rook_left.who_is_here.start:
                    return bishop_left

    def castlings_destination(self):
        if self.start:
            kingside_castling = self.kingside_castling()
            if kingside_castling:
                self.line_of_sight.append(kingside_castling)
            queenside_castling = self.queenside_castling()
            if queenside_castling:
                self.line_of_sight.append(queenside_castling)

    def get_line_of_sight(self):
        self.line_of_sight.clear()
        self.neighbor_move()
        self.castlings_destination()
        return self.line_of_sight
