from typing import List, Dict
import math
import random
import itertools

import numpy

from types_ import Female, Male


def make_pairing(
    women: List[Female],
    men: List[Male],
    count_vars: Dict[str, int],
    state_vars: Dict[str, int]
):
    available_women = []
    available_men = []

    for pers in itertools.chain(women, men):
        pers.decrease_wait_time()

        if pers.couple is None and pers.couple_desire and pers.wait_time == 0:
            if isinstance(pers, Female):
                available_women.append(pers)
            else:
                available_men.append(pers)

    # match pairs
    for aw in available_women:
        for am in available_men:
            age_dif = abs(aw.age - am.age) / 12

            if age_dif < 5:
                p = 0.45
            elif 5 <= age_dif < 10:
                p = 0.4
            elif 10 <= age_dif < 15:
                p = 0.35
            elif 15 <= age_dif < 20:
                p = 0.25
            else:
                p = 0.15

            if p > random.uniform(0, 1):
                count_vars['pairings'] += 1
                state_vars['new_pairings'] += 1
                aw.couple = am
                am.couple = aw
                available_men.remove(am)
                break


def make_breakups(
    women: List[Female],
    men: List[Male],
    count_vars: Dict[str, int],
    state_vars: Dict[int, str]
):
    breakups = state_vars['new_pairings'] // 5   # = new_pairings * 0.2
    
    if breakups > 0:
        married = [w for w in women if w.couple is not None]
        for _ in range(breakups):
            w = random.choice(married)
            married.remove(w)
            w.couple.couple = None
            w.couple.update_wait_time()
            w.couple = None
            w.update_wait_time()
            count_vars['breakups'] += 1

        state_vars['new_pairings'] = 0


def make_pregnancies_and_deliveries(
    women: List[Female],
    men: List[Male],
    count_vars: Dict[str, int],
    state_vars: Dict[int, str]
):

    def preg_pos_per_month(n, p):
        eq = [
            math.comb(n - 8 * i, i + 1) * (-1) ** i
            for i in range(math.ceil((n - 8) / 9))
        ][::-1] + [-p]

        roots = numpy.roots(eq)
        root = 1
        for r in roots:
            if r.imag == 0 and r.real >= 0 and r.real <= root:
                root = r.real

        return root

    for w in women:
        if w.couple is not None and \
        w.children_to_have > 0 and w.couple.children_to_have > 0 and \
        w.pregnant_countdown == 0:
            if w.age < 144:             # age < 12
                p = 0
            elif 144 <= w.age < 180:    # 12 <= age < 15
                p = preg_pos_per_month(180 - 144, 0.2)
            elif 180 <= w.age < 252:    # 15 <= age < 21
                p = preg_pos_per_month(252 - 180, 0.45)
            elif 252 <= w.age < 420:    # 21 <= age < 35
                p = preg_pos_per_month(420 - 252, 0.8)
            elif 420 <= w.age < 540:    # 35 <= age < 45
                p = preg_pos_per_month(540 - 420, 0.4)
            elif 540 <= w.age < 720:    # 45 <= age < 60
                p = preg_pos_per_month(720 - 540, 0.2)
            else:                       # 60 <= age < 125
                p = preg_pos_per_month(720 - 1500, 0.05)
            
            if p > random.uniform(0, 1):
                count_vars['pregnancies'] += 1
                w.update_pregnant()

        if w.pregnant_countdown > 0:
            w.pregnant_countdown -= 1

            if w.pregnant_countdown == 0:
                count_vars['deliveries'] += w.babies
                for i in range(w.babies):
                    if 0.5 > random.uniform(0, 1):
                        men.append(Male())
                    else:
                        women.append(Female())
                    
                w.children_to_have -= w.babies
                if w.couple is not None:
                    w.couple.children_to_have -= w.babies
                w.babies = 0


def make_deaths(
    women: List[Female],
    men: List[Male],
    count_vars: Dict[str, int],
    state_vars: Dict[int, str]
):
    for w in women:
        if 0 <= w.age < 144:        # 0 - 12
            p = 0.25 / 144
        elif 144 <= w.age < 540:    # 12 - 45
            p = 0.15 / (540 - 144)
        elif 540 <= w.age < 912:    # 45 - 76
            p = 0.35 / (912 - 540)
        else:                       # 76 - 125
            p = 0.65 / (1500 - 912)
        
        if p > random.uniform(0, 1):
            w.death()
            women.remove(w)
        
    for m in men:
        if 0 <= m.age < 144:        # 0 - 12
            p = 0.25 / 144
        elif 144 <= m.age < 540:    # 12 - 45
            p = 0.1 / (540 - 144)
        elif 540 <= m.age < 912:    # 45 - 76
            p = 0.3 / (912 - 540)
        else:                       # 76 - 125
            p = 0.7 / (1500 - 912)
        
        if p > random.uniform(0, 1):
            count_vars['deaths'] += 1
            m.death()
            men.remove(m)


events = [
    make_pairing,
    make_breakups,
    make_pregnancies_and_deliveries,
    make_deaths,
]
