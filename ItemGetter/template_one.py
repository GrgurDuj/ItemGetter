import os
from datetime import datetime
from collections import deque
import time as t
import pickle
from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.core.common import LoadPolicy
from set_up import set_up, set_up2, set_up3

set_up('KR')

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
                    elif another_error.error_code in [503]:
                        print('Found a 503')
                        t.sleep(120)
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

gather_start = datetime(2017, 7, 12)
total_req = 0


def check_req():
    global total_req
    print('check print', total_req)
    if total_req >= 190:
        print('Request overload, sleeping.')
        t.sleep(120)
        total_req = 0
    return


def inc_req(inc):
    global total_req

    total_req += inc
    print('inc print::new', total_req)

pulled_summoners = deque()
match_set = set()
i = 1
while len(unpulled_summoners) > 0:
    try:
        if i in range(1,201,3):
            set_up('KR')
            print('set_up1')
        elif i in range(2,201,3):
            set_up2('KR')
            print('set_up2')
        elif i in range(3,201,3):
            set_up3('KR')
            print('set_up3')
        summoner = unpulled_summoners.popleft()
        summMatchList = summoner.match_list(begin_time=gather_start)
        print('summMatchList' , len(summMatchList))
        for match_reference in summMatchList:
        # If you are connected to a database, the match will automatically be stored in it.
        # Simply pull the match, and it's in your database for whenever you need it again!
        # If you pull a match twice, the second time it will be loaded from the database rather than pulled from Riot
        # and therefore will not count against your rate limit. This is true of all datatypes, include Summoner.
            match = riotapi.get_match(match_reference)
            # t.sleep(15)
            if match is None:  # If the match still fails to load, continue on to the next one
                continue
            elif str(match) in match_set:
                print('Found duplicate' + match)
                continue
            else:
                match_set.add(match)
                print("Stored {0} in my database".format(match))
                #t.sleep(15)
                with open('match.pickle', 'wb') as handle:
                    pickle.dump(match, handle, protocol=pickle.HIGHEST_PROTOCOL)
        pulled_summoners.append(summoner)
        i+=1
        #print('Sleeping')
        #t.sleep(60)
        print(len(pulled_summoners))
    except:
        i+=1
        print('503')
        t.sleep(30)
        continue
print('Done')