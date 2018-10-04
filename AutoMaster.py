# system
import random

# custom
from CarAndDriverItem import CarAndDriverItem
from MotorTrendItem import MotorTrendItem
from PosterMaster import PosterMaster
from PosterHelper import PosterHelper


class AutoMaster (PosterMaster):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_twitter_token():
        return {
            'consumer_key': 'Srbw7uxJeNOn2HFrxlDwbbEiz',
            'consumer_secret': 'u6CCnKg2Uf50ShHEfBpqE3Fqv6QMXQqG1o7zCzEhDMlwtrT9Ck',
            'access_key': '753111292857188353-KSRY7RZhkLCM3VzOM0f7HSsWbTmVnu6',
            'access_secret': 'mTcQGX4tMzACWsfhQ6S0JrW8veKFK9ncQo2akgZOr3swz',
        }

    @staticmethod
    def get_facebook_token():
        return PosterHelper.get_facebook_token('835257239940494')

    @staticmethod
    def get_records(count):
        records = dict()
        sources = [
            MotorTrendItem,
            CarAndDriverItem,
        ]

        if count:
            for source in sources:
                records.update(
                    source.get_records())

        return records
