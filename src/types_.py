from __future__ import annotations
import uuid
import random
import math


class Person:

    def __init__(self, age):
        self.uuid = uuid.uuid4()
        self.age = age * 12
        self.couple: Female = None
        self.children_to_have = 0
        self.wait_time = 0
        self.couple_desire_cases = []

        self._update_children_to_have()
        self._update_couple_desire()

    def _update_children_to_have(self):
        p_values = {0.6: 1, 0.75: 2, 0.35: 3, 0.2: 4, 0.1: 5, 0.05: 130}

        for p in p_values:
            v = random.uniform(0, 1)
            if v <= p:
                self.children_to_have = p_values[p]
            else:
                break

    def _update_couple_desire(self):
        self.couple_desire_cases.append(False)

        for p in (0.6, 0.65, 0.8, 0.6, 0.5, 0.2):
            self.couple_desire_cases.append(
                p > random.uniform(0, 1)
            )

    @property
    def couple_desire(self):
        if self.age < 144:              # age < 12
            return self.couple_desire_cases[0]
        if 144 <= self.age < 180:       # 12 <= age < 15
            return self.couple_desire_cases[1] 
        elif 180 <= self.age < 252:     # 15 <= age < 21
            return self.couple_desire_cases[2]
        elif 252 <= self.age < 420:     # 21 <= age < 35
            return self.couple_desire_cases[3]
        elif 420 <= self.age < 540:     # 35 <= age < 45
            return self.couple_desire_cases[4]
        elif 540 <= self.age < 720:     # 45 <= age < 60
            return self.couple_desire_cases[5]
        else:                           # 60 <= age < 125
            return self.couple_desire_cases[6]

    def update_wait_time(self):
        if self.age < 144:              # age < 12
            lambda_ = 0
        if 144 <= self.age < 180:       # 12 <= age < 15
            lambda_ = 3
        elif 180 <= self.age < 420:     # 15 <= age < 35
            lambda_ = 6
        elif 420 <= self.age < 540:     # 35 <= age < 45
            lambda_ = 12
        elif 540 <= self.age < 720:     # 45 <= age < 60
            lambda_ = 24
        else:                           # 60 <= age < 125
            lambda_ = 48
        
        if lambda_ == 0:
            self.wait_time = 0
        else:
            self.wait_time = -(1 / lambda_) * math.log(random.uniform(0, 1))
    
    def decrease_wait_time(self):
        self.wait_time = 0 if self.wait_time - 1 < 0 else self.wait_time - 1

    def death(self):
        if self.couple is not None:
            self.couple.couple = None
            self.couple.update_wait_time()
    
    def __eq__(self, other: Person):
        return self.uuid == other.uuid

class Female(Person):

    def __init__(self, age=0):
        super().__init__(age)
        self.babies = 0
        self.pregnant_countdown = 0

    def update_pregnant(self):
        p_values = {0.7: 1, 0.18: 2, 0.08: 3, 0.04: 4, 0.02: 5}

        for p in p_values:
            v = random.uniform(0, 1)
            if p > v:
                self.babies = p_values[p]
            else:
                break

        # set to 10 by convenience, is decreased inmediately
        if self.babies != 0:
            self.pregnant_countdown = 10     # TODO: make 10

class Male(Person):

    def __init__(self, age=0):
        super().__init__(age)