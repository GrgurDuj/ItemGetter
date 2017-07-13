import os
from datetime import datetime
from collections import deque
import time as t

from list_of_champs import list_of_champions
from template_one import match_set
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.core.common import LoadPolicy
from set_up import set_up
set_up('KR')

relevMatches = set()
setOfItems = set()


def get_item_set():
    champion = input('Please enter your champion:').capitalize()
    laneChoice = input('Please enter your lane:').upper()
    for match in match_set:
        reqChampId = list_of_champions['data'][champion]['id']
        try:
            if match.participants.lane == laneChoice and match.participants.championId == reqChampId:
                relevMatches.add(match)
        except:
            print('Enter a valid champion name and lane.')
            break

    listOfWinItems = []
    listOfLoseItems = []

    for match in relevMatches:
        if
