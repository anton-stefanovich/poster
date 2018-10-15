from HomeItem import *
from PosterMaster import *
from PosterHelper import *

import json
import hyper

import random


class HomeMaster (PosterMaster):
    request_method = 'POST'
    request_scheme = 'https'
    request_base = 'homeoftampabay.kwrealty.com'
    request_search = '/ajax/listing/consumermapsearch/'

    @staticmethod
    def get_twitter_token():
        return {
            'consumer_key': 'gDGUnKgf7Pj8YInqoeKT4PHDJ',
            'consumer_secret': 'LGjYlSYa5Z6beCnD5WXSY615fXRY9i7eOTp2H8FBUEbfuzIvVZ',
            'access_key': '1411815349-lQy2Om1LVcuRamjRlxLcGgT050CmcjAXJR2UPpX',
            'access_secret': 'CHyauYMUNkypp5S0GxwyehQMno99vt1eM4riKqI8j0v9x',
        }

    @staticmethod
    def get_facebook_token():
        return PosterHelper.get_facebook_token('202051909850508')

    @staticmethod
    def get_records():
        connection = hyper.HTTP20Connection(HomeMaster.request_base)

        request_body = HomeMaster.__get_request_body(
            price=random.choice(HomeMaster.__get_price_range()))

        request_headers = HomeMaster.__get_request_headers()

        stream_id = connection.request(
            method='POST',
            url=HomeMaster.request_search,
            headers=request_headers,
            body=request_body)
        response = connection.get_response(stream_id)

        response_data = response.read()
        response_text = response_data.decode()
        response_json = json.loads(response_text)
        house_cards = response_json['payload']['listings']

        records = dict()
        for house in house_cards:
            house_id = house['id']
            house_url = house['detailsUrl']

            records[house_id] = \
                HomeItem(
                    HomeMaster.request_scheme + '://' +
                    HomeMaster.request_base + house_url)

        return records

    @staticmethod
    def __get_request_headers():
        return {
            ':method': HomeMaster.request_method,
            ':scheme': HomeMaster.request_scheme,
            ':authority': HomeMaster.request_base,
            ':path': HomeMaster.request_search,
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'accept-encoding': 'gzip, deflate, br',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    @staticmethod
    def __get_request_body(price: int):
        price_max = int(price * 1.25)
        price_min = int(price * 0.75)

        return \
            '&lulat=28.3&lulong=-82.8' \
            '&rllat=27.8&rllong=-82.2' \
            '&favoritesonly=0' \
            '&maxprice={price_max}' \
            '&minprice={price_min}' \
            '&daysonwebsite=14' \
            '&propertytype[]=SINGLE' \
            '&propertytype[]=CONDO' \
            '&listingtype%5B%5D=Resale+New' \
            '&hasagerestrictions=2' \
            '&statusfilter=1' \
            '&stories=0'.format(
                price_min=price_min,
                price_max=price_max)
        # '&sort=mlsupdatedate+desc' \
        # '&isCommercial=' \
        # '&moreareas=' \
        # 'areas=' \
        # '&beds=' \
        # '&baths=' \
        # '&geopoints=' \
        # '&minsqft=' \
        # '&maxsqft=' \
        # '&minacres=' \
        # '&maxacres=' \
        # '&minyearbuilt=' \
        # '&maxyearbuilt=' \
        # '&subdivision=' \

    @staticmethod
    def __get_price_range():
        basic = pow(10, 6)  # basic is '$1,000,000'
        return [
            basic * 0.15, basic * 0.20, basic * 0.25, basic * 0.30,  # cheap
            basic * 0.35, basic * 0.40, basic * 0.50, basic * 0.75,  # average
            basic * 1.00, basic * 1.33, basic * 1.67, basic * 2.00,  # expensive
        ]
