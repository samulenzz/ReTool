""" NLP parsing module, including CoreNLP and NLTK """
from typing import List, Union, Dict, Tuple
from core.Event import Event
from core.Entity import Entity
from core.Req import Req
from core.CoreNLP import StanfordCoreNLP

############################################# global variables ##############################################
TYPE_NLP = List[Dict[str, Union[str, int]]]
TYPE_TUPLE = Union[Event, Req]
groupid = 0                 # type: int
Entities = {}               # type: Dict[int, Entity]
nlp = None                  # type: StanfordCoreNLP

############################################# file interfaces ###############################################
def start(directory_path: str) -> None:
    global nlp
    nlp = StanfordCoreNLP(directory_path, lang='zh')

def close() -> None:
    global nlp
    nlp.close()


def _resolve(text: str)\
        -> Tuple[list, list]:
    while len(text) > 3 and (text[-1] == '\n' or text[-1] == ' '):
        text = text[: -1]
    if text[-1] != '。':
        text += '。'
    t = nlp.dependency_parse(text)['sentences'][0]
    tokens = t['tokens']
    dependencies = t['enhancedPlusPlusDependencies']
    return tokens, dependencies


def _preprocess(req: Req, text: str) -> str:
    text = text[:-1] if text[-1] in ['。', '；'] else text

    # search for bracket and ignore things in them
    right_index = 0
    while True:
        left_index = text.find('（', right_index + 1)
        right_index = text.find('）', left_index + 1)
        if left_index >= 0 and right_index >= 0:
            text = text.replace(text[left_index: right_index + 1], '')
        else:
            break

    # recognize some special structure
    for word in ['不能', '不可以', '禁止']:
        if word in text:
            req.NOT = True
            text = text.replace(word, '')
            break
    l_index = text.find('以')
    if l_index > 0:
        for word in ['的方式', '的形式']:
            r_index = text.find(word)
            if r_index > 0:
                res = text[l_index: r_index + len(word)]
                req.restriction.append(res)
                text = text.replace(res, '')
                break

    # split the requirement sentence
    main = []
    split_list = text.split('，')
    for s in split_list:
        # delete some words
        for word in ['并', '或', '且']:
            if s[0] == word:
                s = s[1:]
        # recognize some restrictions
        flag = False
        for word in ['根据', '通过', '依据', '按照']:
            if word in s:
                req.restriction.append(s)
                flag = True
                break
        if flag:
            continue
        # recognize event
        if s[0] == '当':
            condition = _parse(text=s, mode='event')
            req.event.append(_postprocess(condition))
            continue
        # recognize some output
        index = s.find('生成')
        if index >= 0:
            entity_base = s[index + 2:]
            req.output.append(Entity(entity_base))
            continue
        # main clause
        if len(s) > 4:
            main.append(s)

    if len(req.event) == 0 or None in req.event:
        req.event = [Event.ALL]

    text = '，'.join(main)
    return text


def _postprocess(tuples):
    if tuples.agent is None:
        tuples.agent = Entity.ALL
    if len(tuples.input) == 0 or None in tuples.input:
        tuples.input = [Entity.VOID]
    if len(tuples.output) == 0 or None in tuples.output:
        tuples.output = [Entity.VOID]
    if len(tuples.restriction) == 0:
        tuples.restriction = ['VOID']
    return tuples


def parse(text: str) -> Req:
    requirement = Req()
    text = _preprocess(requirement, text)
    result = _parse_pattern2(requirement, text)
    if result is not None:
        return _postprocess(result)
    result = _parse_pattern1(requirement, text)
    if result is not None:
        return _postprocess(result)
    result = _parse(text=text, mode='req', req=requirement)
    return _postprocess(result)


############################################## parsing tuples ###############################################
def _parse_pattern1(req: Req, text: str):
    verbs = ['提供', '支持', '具有', '包括', ]
    flag = False
    verb = ''
    for v in verbs:
        if v in text:
            flag = True
            verb = v
            break
    if flag or '、' in text:
        if '、' in text:
            text_parts = text.split('、')
            head = text_parts[0]
            tail = text_parts[-1]
            text_parts = text_parts[1:-1]
            # head
            if verb == '':
                tokens, dependencies = _resolve(head)
                for t in tokens:
                    if t['pos'][0] == 'V':
                        verb = t['word']
            if verb == '':
                return None
            head_list = head.split(verb)
            if len(head_list) != 2:
                return None
            head = head_list[0]
            text_parts.insert(0, head_list[1])
        else:  # '、' not in text
            head = text.split(verb)[0]
            tail = text.split(verb)[1]
            text_parts = []
        # 和
        and_list = tail.split('和')
        if len(and_list) == 2:
            text_parts.append(and_list[0])
            tail = and_list[1]
        # tail
        tail_list = tail.split('等')
        if len(tail_list) > 2:
                return None
        text_parts.append(tail_list[0])
        if len(tail_list) == 2 and len(tail_list[1]) > 0:
            tail = tail_list[1]
        else:
            tail = ''
        # parse requirement
        req.agent = Entity(head)
        req.operation = verb
        req.input += [Entity(o) for o in text_parts]
        req.output += [Entity(o) for o in text_parts]
        req.output += [Entity(tail)] if tail != '' else []
        return req
    return None


def _parse_pattern2(req: Req, text: str):
    if '对' in text and '进行' in text:
        # parse requirement
        text = text.replace('对象', '__')
        split_list = text.split('对')
        split_list = [s.replace('__', '对象') for s in split_list]
        if len(split_list) != 2:
            return None
        req.agent = Entity(split_list[0])
        split_list = split_list[1].split('进行')
        if len(split_list) != 2:
            return None
        req.input.append(Entity(split_list[0]))
        req.output.append(Entity(split_list[0]))
        req.operation = split_list[1]
        return req
    return None


def _parse(text: str, mode: str = 'req', req: Req = None) -> TYPE_TUPLE:
    global groupid, Entities
    tokens, dependencies = _resolve(text)
    tuples = Event() if mode == 'event' else req
    op_index, passive, tokens, dependencies = _operation(tuples, tokens, dependencies)
    Entities = {}
    _agent(tuples, op_index, passive, tokens, dependencies)
    # recognize some input
    l_index = text.find('将')
    r_index = text.rfind(tuples.operation)
    if 0 < l_index < r_index:
        tuples.input.append(Entity(text[l_index + 1: r_index]))
        agent_index = text.find(tuples.agent.base)
        tuples.operation = text[agent_index + len(tuples.agent.base):]
    return tuples


def _parse_obj(entity_index: int, tokens: TYPE_NLP, dependencies: TYPE_NLP)\
        -> Entity:
    global Entities
    if entity_index in Entities:
        return Entities[entity_index]

    compound = ''
    right = 0
    for dep in [dep for dep in dependencies if dep['governor'] == entity_index and dep['dep'][:8] == 'compound']:
        word = dep['dependentGloss']
        right = dep['dependent'] -1
        compound = word if compound == '' else compound + word

    temp = tokens[entity_index - 1]
    word = temp['word']
    base = compound + word
    entity = Entity(base)

    for dependency in [dep for dep in dependencies if dep['governor'] == entity_index]:
            if dependency['dep'] == 'det' and dependency['dependentGloss'] in ['所有', '每个']:
                entity.EACH = True
            elif dependency['dep'] in ['nummod', 'amod']:
                if tokens[dependency['dependent'] - 1]['pos'] == 'CD':
                    mod = ''
                    for dep in [dep for dep in dependencies if dep['dep'] == 'advmod' and dep['governor'] == dependency['dependent']]:
                        for token in tokens[dep['dependent'] -1: dep['governor'] -1]:
                            mod += token['word'] + ' '
                    entity.modifier.append(mod + dependency['dependentGloss'])
                else:
                    entity.modifier.append(dependency['dependentGloss'])
            elif dependency['dep'] in ['nmod:poss', 'nmod:of']:
                entity.dom.append(_parse_obj(dependency['dependent'], tokens, dependencies))
            elif dependency['dep'] in ['acl', 'acl:relcl']:
                left = dependency['dependent'] -1
                if right == 0:
                    right = dependency['governor'] -1
                mod = ''
                for s in tokens[left: right]:
                    mod += s['word']
                entity.modifier.append(mod)

    Entities[entity_index] = entity
    entity = Entity.add(entity)

    return entity


def _operation(obj: TYPE_TUPLE, tokens: TYPE_NLP, dependencies: TYPE_NLP)\
        -> Tuple[int, bool, TYPE_NLP, TYPE_NLP]:
    op_index = 0
    passive = False     # whether the sentence is passive voice

    if type(obj) == Req and obj.groupid >= 0:
        # the word after modal verbs is recognized as verb
        for i, token in enumerate(tokens[:-1]):
            if token['word'] in ['应', '应当', '应该', '必须', '可以', '能', '能够', '不可以', '不能', '无法']:
                if token['word'] in ['可以', '能', '能够']:
                    obj.ABLE = True
                elif token['word'] in ['不可以', '不能', '无法']:
                    obj.NOT = True
                op_index = i + 2
                break
    else:  # Event & Object clause
        # the word which ROOT point to is recognized as verb
        op_index = dependencies[0]['dependent']

    # # find copula
    for dependency in dependencies:
        if dependency['dep'] == 'cop' and dependency['governor'] == op_index and dependency['dependentGloss'] == '被':
            be_index = dependency['dependent']
            operation = '被'
            new_sentence = ''
            for i, token in enumerate(tokens):
                if i + 1 < be_index:
                    new_sentence += token['word'] + ' '
                elif i + 1 == be_index:
                    pass
                elif be_index < i + 1 < op_index:
                    operation += ' ' + token['word']
                elif i + 1 == op_index:
                    operation += ' ' + token['word']
                    new_sentence += 'do '
                else:
                    new_sentence += token['word'] + ' '
            obj.operation = operation
            op_index = be_index
            (tokens, dependencies) = _resolve(new_sentence)
            break

    # passive
    if op_index-2 > 0 and tokens[op_index - 2]['word'] == '被':  # passive
        passive = True

    # if Req and find the wrong verb
    if tokens[op_index-1]['pos'][:1] != 'V':
        op_index = dependencies[0]['dependent']
    if obj.operation is None:
        obj.operation = tokens[op_index - 1]['word']

    # open complement (including to do)
    for dep in [dep for dep in dependencies if dep['governor'] == op_index and dep['dep'] == 'xcomp']:
        complement_index = dep['dependent']
        for _ in tokens[op_index -1: complement_index -1]:
            obj.operation += ' ' + dep['dependentGloss']

    return op_index, passive, tokens, dependencies


def _agent(obj: TYPE_TUPLE, op_index: int, passive: bool, tokens: TYPE_NLP, dependencies: TYPE_NLP)\
        -> int:
    agent_index = -1
    true_agent = -1

    if passive:  # passive voice
        for dependency in dependencies:
            if dependency['governor'] == op_index and dependency['dep'] == 'nsubjpass':
                agent_index = dependency['dependent']
    else:
        for dependency in dependencies:
            if dependency['governor'] == op_index and dependency['dep'][:5] == 'nsubj':
                agent_index = dependency['dependent']
                break
        if agent_index == -1 and tokens[dependencies[0]['dependent'] - 1]['pos'] == 'NN':
            agent_index = dependencies[0]['dependent']

    if passive:
        if true_agent != -1:
            obj.agent = _parse_obj(true_agent, tokens, dependencies)
        if agent_index == -1:   # omit the subject, which is the agent of main clause
            obj.input.append(Entity.star)
            obj.output.append(Entity.star)
        else:
            obj.input.append(_parse_obj(agent_index, tokens, dependencies))
            obj.output.append(_parse_obj(agent_index, tokens, dependencies))
    elif agent_index != -1:
        obj.agent = _parse_obj(agent_index, tokens, dependencies)

    return agent_index


def _input_output(obj: TYPE_TUPLE, op_index: int, tokens: TYPE_NLP, dependencies: TYPE_NLP) -> None:
    index = []

    for dep in dependencies:
        if dep['governor'] == op_index and dep['dep'] == 'dobj' and dep['dependent'] not in index:
            index.append(dep['dependent'])
            o = _parse_obj(dep['dependent'], tokens, dependencies)
            obj.input.append(o)
            obj.output.append(o)
        if dep['dep'][:4] == 'nmod':
            if dep['dep'] in ['nmod:poss', 'nmod:of', 'nmod:agent', 'nmod:by']:
                pass
            elif dep['dep'] == 'nmod:at' and dep['dependentGloss'] == 'time':
                pass
            elif dep['dependent'] not in index:
                index.append(dep['dependent'])
                obj.input.append(_parse_obj(dep['dependent'], tokens, dependencies))

    for dep in dependencies:
        if dep['dep'] == 'nummod' and dep['governor'] not in index:
            index.append(dep['governor'])
            obj.input.append(_parse_obj(dep['governor'], tokens, dependencies))
        if dep['dep'] == 'compound' and dep['governor'] not in index and dep['dependent'] not in index:
            index.append(dep['governor'])
            index.append(dep['dependent'])
            obj.input.append(_parse_obj(dep['governor'], tokens, dependencies))

    if len(obj.input) == 0:
        obj.input.append(Entity.VOID)
    if len(obj.output) == 0:
        obj.output.append(Entity.VOID)


def _restriction(obj: TYPE_TUPLE, tokens: TYPE_NLP, dependencies: TYPE_NLP) -> None:
    words = ['当', '之后', '不可以', '未', '无法']
    for dependency in [d for d in dependencies if d['dep'] == 'advmod' and d['dependentGloss'] not in words]:
        if tokens[dependency['governor'] - 1]['pos'] == 'CD':
            continue
        restriction = dependency['dependentGloss']
        obj.restriction.append(restriction)

    if len(obj.restriction) == 0:
        obj.restriction.append('VOID')
