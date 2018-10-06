from HomeItem import *
from PosterMaster import *
from PosterHelper import *

import json
import requests

import random


class HomeMaster (PosterMaster):
    url_base = 'http://homeoftampabay.kwrealty.com'
    url_search = '/ajax/listing/consumermapsearch/'

    search_map = {
        '17835369': 'expensive',
        '17749077': 'expensive',
        '17827006': 'expensive',
        '17827014': 'medium',
        '17827017': 'medium',
        '17827030': 'medium',
        '17827032': 'medium',
        '17827033': 'medium',
        '17827034': 'cheap',
        '17835346': 'cheap',
    }

    tags_map = {
        'all': [
            '#HomeBuying', '#HouseHunting', '#FirstHome', '#HomeSale', '#HomesForSale', '#Property', '#JustListed',
            '#Properties', '#Investment', '#Home', '#Housing', '#Listing', '#Mortgage', '#EmptyNest'],
        'cheap': [
            '#FirstTimeHomeBuyer', '#DIY', '#DIYspecial', '#FixerUpper', '#Flipper', '#FlipHouse', '#TLCneeded',
            '#DesignerSpecial', '#FirstHome', '#PricedToGo', '#BargainHunt', '#Bargain', '#MostBangForYourBuck'],
        'medium': [
            '#GreatValue', '#RightPrice', '#GreatDeal', '#DoneRight', '#PerfectPrice', '#Renovated'],
        'expensive': [
            '#DreamHouse', '#LuxuryRealEstate', '#LuxuryLiving', '#MillionDollarListing']
    }

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
        request_url = \
            HomeMaster.url_base + \
            HomeMaster.url_search

        request_body = HomeMaster.__get_request_body(
            price=random.choice(HomeMaster.__get_price_range()))

        request_headers = HomeMaster.__get_request_headers(
            size=len(request_body))

        response = requests.post(
            url=request_url,
            headers=request_headers,
            data=request_body)

        response_json = json.loads(response.text)
        house_cards = response_json['payload']['listings']

        records = dict()
        for house in house_cards:
            house_id = house['id']
            house_url = house['detailsUrl']
            house_price = house['price']

            house_tags = HomeMaster.__get_house_tags(house_price)
            records[house_id] = \
                HomeItem(house_id, HomeMaster.url_base + house_url, house_tags)

        return records

    @staticmethod
    def __get_request_headers(size: int):
        return {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': str(size),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Host': 'homeoftampabay.kwrealty.com',
            # 'Connection': 'keep-alive',
            # 'Accept': '*/*',
            # 'Origin': 'http://homeoftampabay.kwrealty.com',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
            #               'Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36',
            # 'Referer': 'http://homeoftampabay.kwrealty.com/map/',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
        }

    @staticmethod
    def __get_request_body(price: int):
        price_max = int(price * 1.1)
        price_min = int(price * 0.9)

        return \
            '&lulat=28.3&lulong=-82.8' \
            '&rllat=27.8&rllong=-82.2' \
            '&sort=mlsupdatedate+desc' \
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
    def __get_house_tags(price: str):
        price = int(
            price
            .strip('$')
            .replace(',', str()))

        key_all = 'all'
        key_price = 'expensive' \
            if int(price) > 500000 else 'medium' \
            if int(price) > 200000 else 'cheap'

        return \
            '#RealEstate' + \
            ' ' + random.choice(HomeMaster.tags_map.get(key_all)) + \
            ' ' + random.choice(HomeMaster.tags_map.get(key_price))

    @staticmethod
    def __get_price_range():
        basic = pow(10, 6)
        return [
            basic * 0.15,
            basic * 0.20,
            basic * 0.25,
            basic * 0.30,
            basic * 0.35,
            basic * 0.40,
            basic * 0.50,
            basic * 0.65,
            basic * 1.00,
            basic * 2.00,
        ]
