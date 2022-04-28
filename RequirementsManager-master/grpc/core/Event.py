from typing import List
from core.Entity import Entity

class Event(object):
    """
    event clause (5 tuples): (agent, operation, input, output, restriction)
    """
    ALL = None          # type: Event

    def __init__(self):
        self.agent = Entity.ALL     # type: Entity
        self.operation = ''         # type: str
        self.ABLE = False           # type: bool
        self.NOT = False            # type: bool
        self.input = []             # type: List[Entity]
        self.output = []            # type: List[Entity]
        self.restriction = []       # type: List[str]


    def __str__(self):
        clauses = ''

        operation = self.operation
        if self.ABLE:
            operation = 'ABLE ' + operation
        if self.NOT:
            operation = 'NOT ' + operation

        if type(self.input[0]) != Entity:
            Input = 'OBJ'
            clauses = '[OBJ]' + str(self.input[0])
        elif len(self.input) == 1:
            Input = str(self.input[0])
        else:
            Input = '{'
            for entity in self.input[:-1]:
                Input += str(entity) + ', '
            Input += str(self.input[-1]) + '}'

        if len(self.output) == 1:
            output = str(self.output[0])
        else:
            output = '{'
            for entity in self.output[:-1]:
                output += str(entity) + ', '
            output += str(self.output[-1]) + '}'

        if len(self.restriction) == 1:
            restriction = str(self.restriction[0])
        else:
            restriction = '{'
            for s in self.restriction[:-1]:
                restriction += s + ', '
            restriction += self.restriction[-1] + '}'

        return '*({}, {}, {}, {}, {})\n'.format(str(self.agent), operation, Input, output, restriction) + clauses


    @classmethod
    def run(cls):
        cls.ALL = Event()
