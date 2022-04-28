""" Conflicts dectecting module """
from typing import List, Union
from core.Event import Event
from core.Entity import Entity
from core.Req import Req

############################################# judge interfaces #############################################
def is_conflict(req1: Req, req2: Req) -> List:
    if _restriction_inconsistency(req1, req2):
        return ['需求矛盾：约束不一致', req1, req2]
    if _operation_inclusion(req1, req2):
        return ['需求冗余：动作包含', req1, req2]
    if _operation_inclusion(req2, req1):
        return ['需求冗余：动作包含', req2, req1]
    if _event_inclusion(req1, req2):
        return ['需求冗余：触发事件包含', req1, req2]
    if _event_inclusion(req2, req1):
        return ['需求冗余：触发事件包含', req2, req1]
    if _operation_inconsistency(req1, req2):
        return ['需求矛盾：动作不一致', req1, req2]
    if _event_inconsistency(req1, req2):
        return ['需求矛盾：触发事件不一致', req1, req2]
    if _event_inconsistency(req2, req1):
        return ['需求矛盾：触发事件不一致', req2, req1]
    return []


# def operation_event_interlock(reqs: List[Req]) -> List:
#     op_chain = {}
#     no_event = []
#     single_event = []
#     multi_event = []
#     for r in reqs:
#         op_chain[r] = []
#         if r.event[0] == Event.ALL:
#             no_event.append(r)
#         elif len(r.event) == 1:
#             single_event.append(r)
#         else:
#             multi_event.append(r)
#
#     for r1 in no_event:
#         for r2 in single_event:
#             if operation_event_condition(r1, r2.event[0]):
#                 op_chain[r1].append(r2)
#
#     return find_loop(op_chain)
#
#
# def input_output_interlock(reqs: List[Req]) -> List:
#     obj_chain = {}
#
#     for i, r1 in enumerate(reqs):
#         for j in range(i, len(reqs)):
#             r2 = reqs[j]
#             if r1 != r2 and input_output_condition(r1, r2):
#                 obj_chain[r1].append(r2)
#
#     return find_loop(obj_chain)


# def find_loop(chain):
#     n = len(chain.keys())
#     visited = [False] * n
#     trace = []
#     result = []
#
#     def findCycle(v):
#         if visited[v]:
#             if v in trace:
#                 j = trace.index(v)
#                 s = set(trace[j:])
#                 flag = True
#                 for r in result:
#                     if len(r & s) == len(s):
#                         flag = False
#                         break
#                 if flag:
#                     for r in result:
#                         if len(r & s) == len(r):
#                             result.remove(r)
#                     result.append(s)
#                 return
#             return
#         visited[v] = True
#         trace.append(v)
#         for i in chain[v]:
#             findCycle(i)
#         if len(trace) > 0:
#             trace.pop()
#
#     for now in range(n):
#         visited = [False] * n
#         trace = []
#         findCycle(now)
#     return result


############################################# judge functions #############################################
def _operation_inclusion(req1: Req, req2: Req) -> bool:
    return _equal(req1.event, req2.event) and req1.agent == req2.agent and _contain(req1.restriction, req2.restriction) and \
           _contain([req1.ABLE, req1.NOT, req1.operation], [req2.ABLE, req2.NOT, req2.operation]) and \
           _contain(req1.input, req2.input) and _contain(req1.output, req2.output)


def _event_inclusion(req1: Req, req2: Req) -> bool:
    return _contain(req1.event, req2.event) and req1.agent == req2.agent and _equal(req1.restriction, req2.restriction) and \
           _equal([req1.ABLE, req1.NOT, req1.operation], [req2.ABLE, req2.NOT, req2.operation]) and \
           _equal(req1.input, req2.input) and _equal(req1.output, req2.output)


def _operation_inconsistency(req1: Req, req2: Req) -> bool:
    return _equal(req1.event, req2.event) and req1.agent == req2.agent and \
           _conflict([req1.ABLE, req1.NOT, req1.operation], [req2.ABLE, req2.NOT, req2.operation]) and \
           ((_contain(req1.input, req2.input) and _contain(req1.output, req2.output)) or
                 (_contain(req2.input, req1.input) and _contain(req2.output, req1.output)))


def _restriction_inconsistency(req1: Req, req2: Req) -> bool:
    return _equal(req1.event, req2.event) and req1.agent == req2.agent and \
           _equal([req1.ABLE, req1.NOT, req1.operation], [req2.ABLE, req2.NOT, req2.operation]) and \
           not _equal(req1.restriction, req2.restriction)


def _event_inconsistency(req1: Req, req2: Req) -> bool:
    if Event.ALL in req1.event:
        return False
    for c in req1.event:
        if c.agent == req2.agent and _conflict([c.ABLE, c.NOT, c.operation], [req2.ABLE, req2.NOT, req2.operation]) and \
                ((_contain(c.input, req2.input) and _contain(c.output, req2.output)) or
                 (_contain(req2.input, c.input) and _contain(req2.output, c.output))):
            return True
    return False

def operation_event_condition(req1: Req, req2_condition: Event) -> bool:
    return req1.agent == req2_condition.agent  and \
           _contain(req1.input, req2_condition.input) and _contain(req1.output, req2_condition.output)


def input_output_condition(req1: Req, req2: Req) -> bool:
    if req1.output[0] == Entity.VOID and req2.input[0] == Entity.VOID:
        return False
    for o2 in req2.input:
        for o1 in req1.output:
            if not o1.contain(o2):
                return False
    return True


############################################# operator functions #############################################
def _contain(item1: Union[List], item2: Union[List]) -> bool:
    if type(item1) != list or type(item2) != list:
        raise TypeError()
    T = type(item1[0])

    if T == Entity:    # object set
        if Entity.VOID in item2:
            return True
        for entity in item2:
            if entity not in item1:
                return False
        return True

    elif T == Event:    # event
        if Event.ALL in item1:
            return True
        if Event.ALL in item2:
            return False
        for c2 in item2:
            flag = False
            for c1 in item1:
                if c1.agent != c2.agent or not _contain([c1.ABLE, c1.NOT, c1.operation], [c2.ABLE, c2.NOT, c2.operation]):
                    continue
                if not _contain(c1.input, c2.input) or not _contain(c1.output, c2.output) or c1.restriction != c2.restriction:
                    continue
                flag = True
                break
            if not flag:
                return False
        return True

    elif T == str:  # restriction
        if 'VOID' in item2:
            return True
        for r in item2:
            if r not in item1:
                return False
        return True

    elif T == bool:   # operation: tuple
        if item1[2] != item2[2]:
            return False
        if item1[0] == item2[0] and item1[1] == item2[1]:
            return True
        if not item1[0] and item2[0]:
            return True
        return False

    else:
        raise TypeError()



def _equal(item1: Union[List], item2: Union[List]) -> bool:
    if type(item1) != list:
        raise TypeError()
    T = type(item1[0])

    if T in [Entity, Event, str]:    # object set, event, restriction
        return _contain(item1, item2) and _contain(item2, item1)

    elif T == bool:   # operation: tuple
        return item1[0] == item2[0] and item1[1] == item2[1] and item1[2] == item2[2]

    else:
        raise TypeError()



def _conflict(item1: Union[List], item2: Union[List]) -> bool:
    if type(item1) != list:
        raise TypeError()
    T = type(item1[0])

    if T == Event:    # event
        if Event.ALL in item1:
            return False
        for i, c1 in enumerate(item1):
            for c2 in item1[i:]:
                if _conflict([c1.ABLE, c1.NOT, c1.operation], [c2.ABLE, c2.NOT, c2.operation]) and \
                        c1.agent == c2.agent and \
                        ((_contain(c1.input, c2.input) and _contain(c1.output, c2.output)) or
                        (_contain(c2.input, c1.input) and _contain(c2.output, c1.output))):
                    return True
        return False

    elif T == bool:   # operation: tuple
        return item1[1] != item2[1] and item1[2] == item2[2]

    else:
        raise TypeError()
