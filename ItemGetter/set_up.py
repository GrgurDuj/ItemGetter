import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def set_up(region):
    '''
    Function sets-up the work environment for basic work with the riot api.
    Requires region from which you will extract data.
    Takes the development key from the environmental variables on the system
    '''
    riotapi.set_region(region)
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY"]
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

def set_up2(region):
    '''
    Function sets-up the work environment for basic work with the riot api.
    Requires region from which you will extract data.
    Takes the development key from the environmental variables on the system
    '''
    riotapi.set_region(region)
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY2"]
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

def set_up3(region):
    '''
        Function sets-up the work environment for basic work with the riot api.
        Requires region from which you will extract data.
        Takes the development key from the environmental variables on the system
        '''
    riotapi.set_region(region)
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY3"]
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)
