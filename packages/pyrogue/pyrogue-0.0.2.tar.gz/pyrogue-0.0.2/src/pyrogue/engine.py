import curses
from curses import wrapper
from terminal import CursesRenderer, RenderOrder
from entity.entity import Entity, get_blocking_entities_at_location
from input_handlers import handle_keys
from gamemap.gamemap import GameMap
from game_states import GameStates
from components.fighter import Fighter
from components.fov import FOV
from death_functions import kill_player, kill_monster
from game_messages import MessageLog

def Rogue(screen):
    max_y, max_x = screen.getmaxyx()

    # These actually define the height of the canvas (game map) not the host terminal
    screen_width = 80
    screen_height = 30
    cy = int((max_y - screen_height) / 2)
    cx = int((max_x - screen_width) / 2)
    #height, width = canvas.getmaxyx()
    map_height = 23
    map_width = 78

    # Values to define status bars and message log
    bar_width = 30
    panel_height = 6
    panel_y = cy + screen_height - panel_height + 1

    # message_x = bar_width + 2
    message_x = 1
    message_width = screen_width - 2
    message_height = cy


    canvas = curses.newwin(screen_height, screen_width, cy, cx)
    renderer = CursesRenderer(canvas)

    #status_win = curses.newwin(80, 3, 24, 0)
    panel = curses.newwin(panel_height, screen_width, panel_y, cx)
    message_panel = curses.newwin(cy, screen_width, 0, cx)

    colors = {
        'dark_wall': curses.color_pair(236)
    }

    fov = FOV(5)
    fighter = Fighter(hp=30, defense=2, power=5)
    player = Entity(5, 5, '@', curses.color_pair(6),
                    'Player', blocks=True, render_order=RenderOrder.ACTOR, fov=fov, fighter=fighter)
    entities = [player]

    game_map = GameMap(map_width, map_height-1)
    game_map.make_map(15, 8, 10, map_width, map_height, player, entities, 3)

    calculate_fov = True

    message_log = MessageLog(message_x, message_width, message_height)
    game_state = GameStates.PLAYER_TURN
    while True:
        key = canvas.getch()
        curses.flushinp()

        renderer.render_all(canvas, panel, message_panel,
                            bar_width, message_log,
                            game_map, fov, calculate_fov,
                            entities, player, colors)

        panel.refresh()
        message_panel.refresh()

        canvas.border()
        canvas.refresh()

        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')

        player_turn_results = []

        if exit:
            return True

        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(player.x + dx, player.y + dy):
                if not game_map.is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)
                    else:
                        player.move(dx, dy)
                        calculate_fov = True

                    game_state = GameStates.ENEMY_TURN

        for result in player_turn_results:
            message = result.get('message')
            dead_entity = result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov, game_map, entities)

                    for result in enemy_turn_results:
                        message = result.get('message')
                        dead_entity = result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYER_TURN

if __name__ == '__main__':
    wrapper(Rogue)
