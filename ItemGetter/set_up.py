import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def set_up(region):
    '''
    Function sets-up the work environment for basic work with the riot api.
    Requires region from which you will extract data.
    Takes the development key from the environmental variables on the system
    Doesn't return anything.
    '''
    riotapi.set_region(region)
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY"]
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)
