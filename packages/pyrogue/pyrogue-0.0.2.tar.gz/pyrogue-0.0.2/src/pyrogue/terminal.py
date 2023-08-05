import renderer
import curses
from components.fov import is_in_fov
from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


class CursesRenderer(renderer.Renderer):

    def __init__(self, canvas):
        curses.curs_set(False)
        curses.noecho()

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        curses.cbreak()
        canvas.nodelay(True)
        canvas.keypad(True)

    def render_circle(self, win, cx, cy, radius, name, value, maximum, fg_color, bg_color):
        r=radius
        x=cx
        y=cy+r
        p=1-r
        #print(x,y)
        while x < y:
            if p > 0:
                p = p+2 * (x+1) + 1-(2*y)
                y = y-1
            else:
                p = p+2 * (x+1) + 1
            x += 1
            #print(x,y)

            win.addstr(y, x, chr(9608))
            win.addstr(_refh(cy, y), x, chr(9608))
            win.addstr(y, _refv(cx, x), chr(9608))
            win.addstr(_refh(cy, y), _refv(cx, x), chr(9608))

    def render_bar(self, win, x, y, total_width, name, value, maximum, bar_color, back_color):
        bar_width = int(float(value) / maximum * total_width)

        win.addstr(x, y, chr(9608) * total_width, back_color)

        if bar_width > 0:
            win.addstr(x, y, chr(9608) * bar_width, bar_color)

        label = '{0}: {1}/{2}'.format(name, value, maximum)
        v = len(label)
        nv = total_width - v
        win.addstr(y+1, int(x + nv / 2), label)

    def render_all(self, canvas, panel, message_panel, bar_width, message_log, game_map, fov, calculate_fov, entities, player, colors):
        if calculate_fov:
            for y in range(game_map.height):
                for x in range(game_map.width):
                    tile = game_map.tiles[x][y]
                    wall = tile.block_sight

                    visible = is_in_fov(fov, x, y)
                    if visible:
                        canvas.addnstr(y, x, tile.char, 1)
                        tile.explored = True
                    elif tile.explored:
                        canvas.addnstr(y, x, tile.char, 1, colors['dark_wall'])

        for entity in sorted(entities, key=lambda x: x.render_order.value):
            self.draw_entity(canvas, entity, fov)


        # Panel Rendering
        if message_log.update: # todo add OR to see if bar needs drawn
            panel.erase()
            message_panel.erase()
            self.render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
                        curses.color_pair(10), curses.color_pair(0))
            message_log.messages.reverse()
            y = message_log.height-1
            for message in message_log.messages:
                message_panel.addstr(y, message_log.x, message.text, curses.color_pair(5))
                y-=1
            message_log.update = False

        self.render_circle(canvas, 15, 15, 5, 'Circle', 10, 10, None, None)

    def clear_all(self, term, entities):
        for entity in entities:
            self.clear_entity(term, entity)

    def draw_entity(self, canvas, entity, fov):
        if is_in_fov(fov, entity.x, entity.y):
            canvas.addnstr(entity.y, entity.x, entity.char, 1, entity.color)

    def clear_entity(self, canvas, entity):
        canvas.addch(entity.y, entity.x, ' ')


def _refh(k, y):
    return (2 * k) - y

def _refv(h, x):
    return (2 * h) - x

