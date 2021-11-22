import itertools
import random
from argparse import ArgumentParser
from pprint import pprint

from events import events
from types_ import Female, Male


parser = ArgumentParser()
parser.add_argument('-w', required=True, type=int, help='Amount of women')
parser.add_argument('-m', required=True, type=int, help='Amount of men')
parser.add_argument('-t', required=True, type=int, help='Years of simulation')
args = parser.parse_args()

women_population = [Female(random.randint(0, 100)) for _ in range(args.w)]
men_population = [Male(random.randint(0, 100)) for _ in range(args.m)]

count_vars = {
    'deaths': 0,
    'pregnancies': 0,
    'deliveries': 0,
    'breakups': 0,
    'pairings': 0,
}

state_vars = {
    'new_pairings': 0,
}

# time is measured in months
T = args.t * 12
t = 0

while t <= T:
    t += 1

    for pers in itertools.chain(women_population, men_population):
        pers.age += 1
    
    random.shuffle(events)
    for event in events:
        event(
            women_population,
            men_population,
            count_vars,
            state_vars
        )

final_w = len(women_population)
final_m = len(men_population)

pprint(count_vars)
print(f'Final Women: {final_w}\t\tFinal Men: {final_m}')
print(f'{(final_w + final_m) / (args.w + args.m) * 100} % of initial population')
