from HomeItem import HomeItem
from PosterMaster import PosterMaster
from PosterHelper import PosterHelper
from selenium import webdriver

import random


class HomeMaster (PosterMaster):
    url_base = 'http://homeoftampabay.kwrealty.com'
    url_search = '/map/searchid/'

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
    def get_records(count):
        print('Getting %d home records' % count)
        driver = webdriver.Chrome()

        records = dict()
        search_size = len(HomeMaster.search_map)
        indexes = random.sample(
            HomeMaster.search_map.keys(),
            count if count < search_size else search_size)
        print('Search indexes: %s' % indexes)

        for url_search_id in random.sample(indexes, count):
            print('Homes search ID: %s' % url_search_id)
            PosterHelper.get_ajax_page(
                driver, HomeMaster.url_base + HomeMaster.url_search + url_search_id)

            elements = driver.find_elements_by_class_name('card-flex-container')
            for element in elements:
                favorite = element.find_element_by_class_name('favorite')
                records[favorite.get_attribute('property-number')] = HomeItem(
                    favorite.get_attribute('property-number'),
                    HomeMaster.url_base + element.get_attribute('data-link'),
                    '#RealEstate' +
                    ' ' + random.choice(HomeMaster.tags_map.get('all')) +
                    ' ' + random.choice(HomeMaster.tags_map.get(
                                            HomeMaster.search_map.get(url_search_id)))
                )

        driver.close()
        return records
