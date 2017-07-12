import os
from datetime import datetime
from collections import deque
import time as t

from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.core.common import LoadPolicy
from set_up import set_up

set_up('EUNE')

def auto_retry(api_call_method):
    """ A decorator to automatically retry 500s (Service Unavailable)
    and skip 400s (Bad Request) or 404s (Not Found). """
    def call_wrapper(*args, **kwargs):
        try:
            return api_call_method(*args, **kwargs)
        except APIError as error:
            # Try Again Once
            if error.error_code in [500]:
                try:
                    print("Got a 500, trying again...")
                    return api_call_method(*args, **kwargs)
                except APIError as another_error:
                    if another_error.error_code in [500, 400, 404]:
                        pass
                    else:
                        raise another_error

            # Skip
            elif error.error_code in [400, 404]:
                print("Got a 400 or 404")
                pass

            # Fatal
            else:
                raise error
    return call_wrapper

riotapi.get_match = auto_retry(riotapi.get_match)
riotapi.get_summoner_by_id = auto_retry(riotapi.get_summoner_by_id)
riotapi.get_summoner_by_name = auto_retry(riotapi.get_summoner_by_name)

unpulled_summoners = deque(entry.summoner for entry in riotapi.get_challenger())

pulled_summoners = deque()
gather_start = datetime(2017, 7, 9)  # 1 day after patch 5.14
# matchList = open('MatchList.txt', 'a+')
match_set = set()

total_requests = 0


def check_req():
    global total_requests
    if total_requests >= 200:
        print('Taking a pause' + total_requests)
        t.sleep(120)
        total_requests = 0
    return


def inc_req(inc):
    global total_requests
    total_requests += inc


while len(unpulled_summoners) > 0:

    summoner = unpulled_summoners.popleft()
    print
    check_req()
    summMatchList = summoner.match_list(begin_time=gather_start)
    t.sleep(7)
    inc_req(len(summMatchList))
    print('summMatchList', len(summMatchList))
    for match_reference in summMatchList:

        # If you are connected to a database, the match will automatically be stored in it.
        # Simply pull the match, and it's in your database for whenever you need it again!
        # If you pull a match twice, the second time it will be loaded from the database rather than pulled from Riot
        # and therefore will not count against your rate limit. This is true of all datatypes, include Summoner.
        check_req()
        print(total_requests)
        match = riotapi.get_match(match_reference)
        inc_req(1)

        print('match', len(match), match)
        if match is None:  # If the match still fails to load, continue on to the next one
            continue
        elif match in match_set:
            print('Match {} is duplicate'.format(match))
            continue
        else:
            match_set.add(match)
            print("Stored {0} in my database".format(match))
        pulled_summoners.append(summoner)
        t.sleep(7)

    print(len(pulled_summoners))
