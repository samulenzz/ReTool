from typing import List

class Entity(object):
    entities = []       # type: List[Entity]
    ALL = None          # type: Entity
    VOID = None         # type: Entity
    star = None         # type: Entity

    def __init__(self, base: str):
        self.base = base        # type: str
        self.EACH = False       # type: bool
        self.modifier = []      # type: List[str]
        self.dom = []           # type: List[Entity]
        self.containing = []    # type: List[Entity]


    def __str__(self):
        entity_str = self.base
        for item in self.modifier:
            entity_str = item + entity_str
        for entity in self.dom:
            entity_str = str(entity) + '的' + entity_str
        if self.EACH:
            entity_str = '所有的' + entity_str
        return entity_str


    def __eq__(self, other):
        if type(other) != type(self) or self.base != other.base or self.EACH != other.EACH:
            return False
        modifier_set = set(self.modifier) & set(other.modifier)
        if len(modifier_set) != len(self.modifier):
            return False
        for entity in self.dom:
            if entity not in other.dom:
                return False
        return True
    
    def contain(self, other) -> bool:
        if type(other) != type(self) or self.base != other.base or not self.EACH and other.EACH:
            return False
        if other in self.dom:
            return True
        for item in self.modifier:
            if item not in other.modifier:
                return False
        return True


    @classmethod
    def run(cls):
        cls.ALL = Entity('系统')
        cls.VOID = Entity('无')
        cls.star = Entity('*')


    @classmethod
    def add(cls, entity):
        for i in range(len(cls.entities)):
            if entity == cls.entities[i]:
                return cls.entities[i]
        for i in range(len(cls.entities)):
            if cls.entities[i].contain(entity):
                cls.entities[i].containing.append(entity)
        cls.entities.append(entity)
        return entity
