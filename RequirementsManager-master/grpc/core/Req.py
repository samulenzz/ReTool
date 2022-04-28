from typing import List, Union
from core.Event import Event
from core.Entity import Entity

class Req(object):
    """
    Requirement (8 tuples): (id, groupid, event, agent, operation, input, output, restriction)
    """
    reqs = []       # type: List[Req]

    def __init__(self):
        self.ID = ''                # type: str
        self.groupid = 0            # type: int
        self.event = []             # type: List[Event]
        self.conj = []              # type: List[str]
        self.agent = Entity.ALL        # type: Entity
        self.operation = None       # type: str
        self.ABLE = False           # type: bool
        self.NOT = False            # type: bool
        self.input = []             # type: List[Union[Entity, Req]]
        self.output = []            # type: List[Entity]
        self.restriction = []       # type: List[str]

    ####################################### class interfaces #######################################
    @classmethod
    def run(cls):
        Event.run()
        Entity.run()

    @classmethod
    def output(cls, output_file: str):
        with open(output_file, 'w') as f:
            for req in cls.reqs:
                if req.groupid >= 0:
                    print(req, file = f)
