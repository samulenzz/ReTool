from core.RCD_NLP import parse
from core.Event import Event
from core.Entity import Entity

class FReq:
    def __init__(self):
        self.groupid = ''
        self.event = ''
        self.agent = ''
        self.operation = ''
        self.input = ''
        self.output = ''
        self.restriction = ''

    @classmethod
    def parse_req(cls, text: str):
        try:
            reqs = parse(text)
            return cls.serialization(reqs)
        except BaseException:
            return None

    @classmethod
    def serialization(cls, old):
        new = FReq()
        new.groupid = str(old.groupid)
        if old.event[0] == Event.ALL:
            new.event = '无条件'
        else:
            conditions = []
            for cond in old.event:
                _agent = '系统' if cond.agent == Entity.ALL else str(cond.agent)
                _operation = '不能 ' + cond.operation if cond.NOT else cond.operation
                _input = '无输入' if cond.input[0] == Entity.VOID else ', '.join([str(entity) for entity in cond.input])
                _output = '无输出' if cond.output[0] == Entity.VOID else ', '.join([str(entity) for entity in cond.output])
                _restriction = '无约束' if cond.restriction[0] == 'VOID' else ', '.join(cond.restriction)
                conditions.append(', '.join(['(', _agent, _operation, _input, _output, _restriction, ')']))
                new.event = ' // '.join(conditions)
        new.agent = '系统' if old.agent == Entity.ALL else str(old.agent)
        new.operation = '不能 ' + new.operation if old.NOT else old.operation
        new.input = '无输入' if old.input[0] == Entity.VOID else ', '.join([str(entity) for entity in old.input])
        new.output = '无输出' if old.output[0] == Entity.VOID else ', '.join([str(entity) for entity in old.output])
        new.restriction = '无约束' if old.restriction[0] == 'VOID' else ', '.join(old.restriction)
        return new
