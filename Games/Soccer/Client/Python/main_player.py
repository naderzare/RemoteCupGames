from Base.Math import Vector2D
from Games.Soccer.Client.Python.Bhv.BhvGoToPoint import GoToPoint
from Games.Soccer.Client.Python.Bhv.BhvKickToPoint import KickToPoint
from Games.Soccer.Client.Python.World import World
from Games.Soccer.Client.Python.World import Agent


def is_kickable(agent: Agent, wm: World) -> bool:
    if agent.pos().dist(wm.ball().pos()) > agent.kickable_r:
        return False
    return True


def do_move(wm: World):
    return GoToPoint(Vector2D(0, 0), 1).execute(wm.self())

def do_move2(wm: World):
    return GoToPoint(Vector2D(250, 150), 1).execute(wm.self())

def do_kick(wm: World):
    return KickToPoint(Vector2D(0, 0), 1).execute(wm.self())


def get_action(wm: World):
    # if wm.self_id != 1:
    #     return do_move2(wm)
    if is_kickable(wm.self(), wm):
        return do_kick(wm)
    return do_move(wm)
