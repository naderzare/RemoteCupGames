from Base.Math import Vector2D, Line2D
from copy import copy
from Conf import Server_Soccer_Conf as Conf


class Object:
    def __init__(self):
        self.M_pos: Vector2D = None
        self.M_vel: Vector2D = None
        self.M_decay: float = None

    def pos(self) -> Vector2D:
        return self.M_pos

    def vel(self) -> Vector2D:
        return self.M_vel

    def decay(self) -> float:
        return self.M_decay

    def predict_pos(self, cycle: int):
        obj_pos: Vector2D = copy(self.pos)
        obj_vel: Vector2D = copy(self.vel)

        while cycle > 0:
            obj_pos += obj_vel
            obj_vel *= self.decay()
            cycle -= 1

        return obj_pos

    def mirror(self):
        field = Field()
        self.M_pos.mirror(Vector2D(field.center.i, self.pos().j))
        self.M_vel.mirror(Vector2D(0, self.vel().j))

    def set_data(self, data: dict):
        self.M_pos = Vector2D(data['pos'][0], data['pos'][1])
        self.M_vel = Vector2D(data['vel'][0], data['vel'][1])
        self.M_decay = data['decay']
        self.more_data(data)

    def more_data(self, data: dict):
        pass


class Ball(Object):
    def __init__(self):
        super().__init__()


class Agent(Object):
    def __init__(self):
        super().__init__()
        self.team_id: int = None
        self.id: int = -1
        self.kickable_r = 0

    def more_data(self, data: dict):
        self.team_id = data['team_id']
        self.kickable_r = data['kickable_r']


class Field:
    def __init__(self):
        self.center: Vector2D = Vector2D(Conf.max_i / 2, Conf.max_j / 2)
        self.field: Vector2D = Vector2D(Conf.max_i, Conf.max_j)


class World:
    def __init__(self):
        self.M_ball: Ball = None
        self.M_agents: list = []
        self.M_cycle: int = 0
        self.self_id: int = 0
        self.self_key = None

    def set_id(self, self_id):
        self.self_id = self_id

    def set_key(self, agents):
        i = 0
        for key, agent in agents.items():
            if agent['id'] == self.self_id:
                self.self_key = i
                break
            i += 1

    def update(self, msg):
        self.M_cycle = msg.cycle

        agents_dict = msg.world['players']
        for key in agents_dict:
            agent = Agent()
            agent.set_data(agents_dict[key])
            self.M_agents.append(agent)
        self.set_key(agents_dict)

        self.M_ball = Ball()
        self.M_ball.set_data(msg.world['ball'])

        if self.self().team_id == 2:
            self.normalize_poses()

    def clear(self):
        while self.M_agents:
            self.M_agents.pop()

    def self(self) -> Agent:
        return self.M_agents[self.self_key]

    def our_players(self) -> list:
        return [agent for agent in self.M_agents if agent.team_id == self.self().team_id]

    def their_players(self) -> list:
        return [agent for agent in self.M_agents if agent.team_id != self.self().team_id]

    def ball(self):
        return self.M_ball

    def cycle(self):
        return self.M_cycle

    def normalize_poses(self):
        self.ball().mirror()
        for i in range(len(self.M_agents)):
            self.M_agents[i].mirror()
