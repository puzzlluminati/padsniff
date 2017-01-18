#!/usr/bin/env python3

from collections import Counter
import padsniff
import json


COUNTER = Counter()


@padsniff.on(action='clear_dungeon')
def log_plus_eggs(request, response):
    cards = json.loads(response.content.decode())['cards']

    for card in cards:
        COUNTER['hp'] += card[6]
        COUNTER['atk'] += card[7]
        COUNTER['rcv'] += card[8]

    COUNTER['runs'] += 1

    print(format_log(COUNTER))


def format_log(d):
    s = (
        'runs: {0[runs]:>3d} | '
        'hp: {0[hp]:>3d} | '
        'atk: {0[atk]:>3d} | '
        'rcv: {0[rcv]:>3d}'
    )

    return s.format(d)
