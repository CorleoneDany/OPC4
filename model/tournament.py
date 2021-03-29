'''Represents the tournament'''

import datetime
from tinydb import TinyDB, Query

class Tournament:
    '''Represents the tournament'''

        def __init__(self):
        """Init class with attributes."""
        id = int
        name = ''
        location = ''
        turns = 4
        player_list = []
        beginning_date = datetime.datetime()
        ending_date = datetime.datetime()
        desc = ''
        db = TinyDB(f'{name}.json')