import sys


class GameInterface(object):

    EXIT_CMD = "exit"
    
    def __init__(self):
        self._curr_command = None
        self._command_history = []
        self._action_aliases = {}
        self._move_aliases = []
        self._direction_aliases = {}
        self._game_text = {}
        self._nouns = {}

    @property
    def name(self):
        return self._game_text.get("name", None)

    @name.setter
    def name(self, n):
        self._game_text["name"] = n

    @property
    def exposition(self):
        return self._game_text.get("exposition", None)

    @exposition.setter
    def exposition(self, n):
        self._game_text["exposition"] = n

    @property
    def noun_room(self):
        return self._nouns.get("noun_room", None)

    @noun_room.setter
    def noun_room(self, n):
        self._nouns["noun_room"] = n

    @property
    def noun_up(self):
        return self._nouns.get("noun_up", None)

    @noun_up.setter
    def noun_up(self, n):
        self._nouns["noun_up"] = n

    @property
    def noun_down(self):
        return self._nouns.get("noun_down", None)

    @noun_down.setter
    def noun_down(self, n):
        self._nouns["noun_down"] = n

    @property
    def noun_left(self):
        return self._nouns.get("noun_left", None)

    @noun_left.setter
    def noun_left(self, n):
        self._nouns["noun_left"] = n

    @property
    def noun_right(self):
        return self._nouns.get("noun_right", None)

    @noun_right.setter
    def noun_right(self, n):
        self._nouns["noun_right"] = n

    @property
    def command_history(self):
        return self._command_history

    def AddMoveAlias(self, verb):
        """Aliase from the confirmation file for known move verbs.

        These verbs have to later be combined with the direction nouns to
        specify a direction to move in.

        Args:
          verb:  String representing an alias for 'move'.
        """
        self._move_aliases.append(verb)

    def AddActionAlias(self, verb, action):
        """Aliases from the configuration file for known game actions.

        Args:
          verb:  String name for verb.
          action:  A method of my_game_player.Player
        """
        self._action_aliases[verb] = action

    def AddDirectionAlias(self, direction, action):
        """Sub-set of directions for the my_game_player.Player.Move() method
        
        Args:
          direction:  String representing a direction to move.
          action:  A Move* method of my_game_player.Player
        """
        self._direction_aliases[direction] = action

    def DebugInfo(self):
        return ["GAME: %s" % self.name,
                "EXPOSITION: %s" % self.exposition,
                ("NOUNS: room=%(room)s,"
                 " up=%(up)s, down=%(down)s, left=%(left)s, right=%(right)s"
                 % {"room": self.noun_room,
                    "up": self.noun_up,
                    "down": self.noun_down,
                    "left": self.noun_left,
                    "right": self.noun_right})]

    def LookupAction(self, command):
        """Look up the action to perform for the given command.

        Args:
          command:  String representing the command issued by the player.

        Returns:
          A tuple of (action, arguments) where action is a method of
          my_game_player.GamePlayer and arguments are the arguments to that
          method.  Returns (None, None) if we do not understand the action.
        """
        # Strip punctuation as well as whitespace.
        command = command.strip(".,!? ").lower()
        command_parts = command.split()
        # First check if it is a move command.
        for m in self._move_aliases:
            if command.startswith(m) and m.split()[0] == command_parts[0]:
                # If it is a move command, but we do not understand the
                # direction, we return None.
                # Directional move commands do not take arguments.
                return (self._direction_aliases.get(command_parts[1], None),
                        None)
        # Next check for other actions
        for a in self._action_aliases:
            if command.startswith(a) and a.split()[0] == command_parts[0]:
                arguments = command.replace(a, "").strip()
                return (self._action_aliases[a], arguments)
        return (None, None)

    def GetInputCommand(self):
        self._curr_command = raw_input("> ")
        return self._curr_command != self.EXIT_CMD

    def Run(self):
        while self.GetInputCommand():
            self._command_history.append(self._curr_command)
        print "Goodbye!"
        print self._command_history



def main(argv):
    game_interface = GameInterface()
    game_interface.Run()


if __name__ == '__main__':
    main(sys.argv)
            

