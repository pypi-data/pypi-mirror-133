from random import randint
import curses
from entity.entity import Entity
from components.fighter import Fighter
from components.ai import BasicMonster
from terminal import RenderOrder

class Tile:
    def __init__(self, char, blocked, block_sight=None, explored=False):
        self.blocked = blocked
        self.char = char
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = explored

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(chr(9608), True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def _make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        room1 = Rect(2, 3, 10, 15)
        room2 = Rect(15, 10, 4, 4)

        self.create_room(room1)
        self.create_room(room2)

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height,
                 player, entities, max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                        # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                    # finally, append the new room to the list
                self.place_entities(new_room, entities, max_monsters_per_room)
                rooms.append(new_room)
                num_rooms += 1

    def place_entities(self, room, entities, max_monsters_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    f = Fighter(hp=10, defense=0, power=3)
                    a = BasicMonster()
                    monster = Entity(x, y, 'o', curses.color_pair(11), 'Orc',
                                     blocks=True, render_order=RenderOrder.ACTOR, fighter=f, ai=a)
                else:
                    f = Fighter(hp=16, defense=1, power=4)
                    a = BasicMonster()
                    monster = Entity(x, y, 'T', curses.color_pair(3), 'Troll', 
                                     blocks=True, render_order=RenderOrder.ACTOR, fighter=f, ai=a)

                entities.append(monster)

    def _clear_tile(self, tile):
        tile.blocked = False
        tile.block_sight = False
        tile.char = ' '

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self._clear_tile(self.tiles[x][y])

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self._clear_tile(self.tiles[x][y])

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self._clear_tile(self.tiles[x][y])

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

