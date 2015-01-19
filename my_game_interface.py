import functools
import os

class GameInterface(object):
    """Command line interface for the game.

    Main interaction between the player and the game.

    NOTE: Much of this class is tested by the parser.
    """

    EXIT_CMD = "exit"
    DEBUG_CMD = "debug"

    def __init__(self):
        self._command_history = []
        self._action_aliases = {}
        self._move_aliases = []
        self._direction_aliases = {}
        self._game_text = {}

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
    def help(self):
        return self._game_text.get("help", None)

    @help.setter
    def help(self, n):
        self._game_text["help"] = n

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
                "HELP: %s" % self.help]

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

    def Run(self, player, debug_mode=False):
        """Main method of interaction.

        This method takes as a parameter the primary game interaction element,
        the player object.  It translates the user input commands and applies
        them to the player object.

        Args:
          player:  A my_game_player.Player object.
        """
        player.Start()
        os.system('cls')
        os.system('clear')
        print self.exposition
        curr_command = None
        while curr_command != self.EXIT_CMD:
            if debug_mode:
                player.PrintDebugOutput()
            curr_command = raw_input("> ").strip(".,!? ").lower()
            action, arguments = self.LookupAction(curr_command)
            if action is not None:
                if arguments:
                    success, msg = action(player, arguments)
                else:
                    success, msg = action(player)
                os.system('cls')
                os.system('clear')
                print msg
            elif curr_command == "help":
                print self.help
            elif curr_command != self.EXIT_CMD:
                print "I don't understand that.  Try 'help'."
            self._command_history.append(curr_command)
        print "Goodbye!"
        if debug_mode:
            print "\n".join(self._command_history)
