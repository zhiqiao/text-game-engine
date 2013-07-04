text-game-engine
================

This is a game engine for the purpose of playing text-based games.

================

General notes below...

================

Supported Verb Types:
  Move [up the map]
  Move [down the map]
  Move [left the map]
  Move [right the map]
  Use [object]
  Add [object]
  Drop [object]
  Inspect [room state]

Config File:
- Sections ("[SECTION]") can be in any order.
- Order within some sections is necessary, e.g. a map has to be defined before
  adding rooms.
- Hashbangs represent comments.
- Lines are colon-deliminated.
- Duplicates are not handled very well.
- Exceptions fail out of the game if parsing is not possible.

Design Decisions:
- The game map is represented as a two-dimensional list with the origin [i.e.
  (0, 0)] located at the top left.  Coordinates are represented as (Y, X) where
  Y is the vertical distance from the origin and X is the horizontal.
  The reason for this decision was mostly for sanity so that I could easily
  visualize the data-structure underlying the game.

- Interactions with the rooms in the game are handled with states.  Each room
  has a state at any given time.  Using objects changes the state of a room
  from one state to another.  This means the universe of room states may
  contain the power set of individual attributes.  E.g. In order to have two
  possible scenarios involving if a room is on fire or has power, a room must
  be able to represent the following states:
    (1) No fire, power
    (2) Fire, power
    (3) No fire, no power
    (4) Fire, no power
  The reasoning for this was to create as much flexibility as possible for the
  configuration of the game.  Each room can be marked with an initial game state
  (or be chosen randomly).  Each object a player can use to interact with a room
  can be implemented as a map between possible states, e.g. from above, a "Fire
  Extinguisher" can transition a room from state 2 to state 1 and from state 4
  to state 1, but has no effect on states 1 and 3.

- Return Types:
  None:  Return None to signal an invalid state or return value, e.g. something
    has not been correct set or the value is missing.
  Boolean:  Return boolean to signal a negative result which is expected
    behavior, e.g. a negative result, but one which can be anticipated.

- Logging
  I was hoping do do some logging, but that didn't pan out.  Ideally, the parsing
  module would log errors and data about the configuration, and the gameplay
  modules would log data about game interactions.

- Exceptions vs. Errors
  Fundamental game concepts (set up, building game state, parsing config file)
  should all result in non-recoverable exceptions.
  Game play which results in exceptions or error states should be logged as
  such, but as much as possible, the game should not crash.

- Mappings
  A lot of game models are data-store like representations.  Some data need only
  be stored once, e.g. description of a room given state, ability of items.  Thus
  it is necessary to use a mapping instead of copying this data between all
  objects of the same class.

- Objects:
  Player:
  - Contains object inventory.
  - Stores position.
  - All major game functions are here:
    - Change position.
    - Add/Drop objects.
    - Users objects.
    - Inspects both surroundings and inventory.
  - Contains:
    - Map of the game.
    - Current room.
    - Mapping of items to abilities.
    - Mapping of room states to descriptions.
  - Contains these elements so it can interact with them directly.
    - Moving is first enforced by the map, then the new room state is acquired
      from the map.
    - Adding and dropping items are interactions with the current room.
    - Using items and inspecting are actions done to the current room.
  Map:
  - Enforce movement on the map.
  - Store state of every room.
  Room:
  - Key by coordinate.
  - Contains items.
  - Contains game state.
  Room State:
  - Key by ID.
  - Has description.
    - Requires a mapping from state to list of description items.
  Object:
  - Key by name.
  - Abilities.
    - Determined by being able to change a room from one state to another.
    - Also have no-op abilities.
    - Requires a mapping from name to abilities.
  - Can be one-use or reusable. 
  Interface
  - Maintain user interaction with game.  Loosely couple with a Player object.
  - Debugging information.
  - History of commands.
  - Stores a mapping of various command aliases to game actions.  These are
    defined in the config file.
