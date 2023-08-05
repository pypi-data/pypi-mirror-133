import curses
from game_states import GameStates
from terminal import RenderOrder
from game_messages import Message

def kill_player(player):
    player.char = '%'
    player.color = curses.color_pair(2)
    return Message('You died!', curses.color_pair(2)), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), curses.color_pair(1))


    monster.char = '%'
    monster.color = curses.color_pair(2)
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
