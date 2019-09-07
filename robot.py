from config import *


class Robot:
    def __init__(self):
        self.at_goal_location = False
        self.direction = UNINITIALIZED
        self.position = None
        self.just_turned = False
        self.just_picked_up_secret_msg = False

        self.in_box_move_sequence = [SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_MOVE, SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_MOVE, SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_MOVE, SERVER_MOVE, SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_MOVE, SERVER_MOVE, SERVER_MOVE, SERVER_TURN_LEFT,
                                     SERVER_MOVE, SERVER_MOVE, SERVER_MOVE, SERVER_MOVE]

    def search_for_secret_msg(self, x, y):
        if not self.just_picked_up_secret_msg:
            if self.position == (x, y):
                return SERVER_MOVE
            self.just_picked_up_secret_msg = True
            self.position = (x, y)
            return SERVER_PICK_UP
        else:
            command = self.in_box_move_sequence.pop(0)
            if command != SERVER_TURN_LEFT:
                self.just_picked_up_secret_msg = False
            return command

    def get_and_set_direction(self, x, y):
        if x > self.position[0]:
            self.direction = RIGHT
        elif x < self.position[0]:
            self.direction = LEFT
        elif y < self.position[1]:
            self.direction = DOWN
        elif y > self.position[1]:
            self.direction = UP

    def move(self, x, y):
        # initial move, get position
        if self.position is None:
            self.position = (x, y)
            return SERVER_MOVE
        # robot didnt move, move again to find direction
        if self.direction == UNINITIALIZED and self.position == (x, y):
            return SERVER_MOVE

        # find direction since we have 2 coordinates
        if self.direction == UNINITIALIZED:
            self.get_and_set_direction(x, y)

        # robot reached goal location
        if not self.at_goal_location and (x, y) == GOAL_LOCATION:
            self.at_goal_location = True

        if self.at_goal_location:
            return self.search_for_secret_msg(x, y)
        return self.move_to_goal_location(x, y)

    def change_direction(self, correct_direction):
        if self.direction - correct_direction == 1 or self.direction == UP and correct_direction == LEFT:
            self.direction = (self.direction - 1) % 4
            return SERVER_TURN_LEFT
        else:
            self.direction = (self.direction + 1) % 4
            return SERVER_TURN_RIGHT

    def move_to_goal_location(self, x, y):
        correct_direction = None
        if GOAL_LOCATION[0] > x:
            correct_direction = RIGHT
        if GOAL_LOCATION[0] < x:
            correct_direction = LEFT
        if GOAL_LOCATION[1] > y:
            correct_direction = UP
        if GOAL_LOCATION[1] < y:
            correct_direction = DOWN
        self.position = (x, y)
        if correct_direction != self.direction:
            return self.change_direction(correct_direction)
        return SERVER_MOVE
