import sys

import my_game_parser


def main(argv):
    parser = my_game_parser.GameParser()
    config_file = "configs/iss_fire.game"
    if len(argv) > 1:
        config_file = argv[1]
    print "Using: %s" % config_file
    parser.Parse(config_file)
    parser.game_interface.Run(parser.player, debug_mode=True)


if __name__ == "__main__":
    main(sys.argv)
