from HomeItem import HomeItem
from PosterMaster import PosterMaster
from PosterHelper import PosterHelper
from selenium import webdriver

import random


class HomeMaster (PosterMaster):
    url_base = 'http://homeoftampabay.kwrealty.com'
    url_search = '/map/searchid/'
    url_search_ids = ['17749077', '17827006', '17827014', '17827017', '17827030',
                      '17827032', '17827033', '17827034', '17835346', '17835369']

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
        driver = webdriver.Firefox()

        records = list()
        search_size = len(HomeMaster.url_search_ids)
        indexes = random.sample(range(search_size),
                                count if count < search_size else search_size)
        for index in indexes:
            url_search_id = HomeMaster.url_search_ids[index]
            PosterHelper.get_ajax_page(
                driver, HomeMaster.url_base + HomeMaster.url_search + url_search_id)

            elements = driver.find_elements_by_class_name('card-flex-container')
            for element in elements:
                favorite = element.find_element_by_class_name('favorite')
                records.append({
                    'url': HomeMaster.url_base + element.get_attribute('data-link'),
                    'id': favorite.get_attribute('property-number')
                })

        indexes = random.sample(range(len(records)), count)
        assert count == len(indexes)

        homes = list()
        for index in indexes:
            record = records[index]
            homes.append(
                HomeItem(
                    driver=driver,
                    url=record.get('url'),
                    id=record.get('id')))

        assert count == len(homes)
        driver.close()

        return homes
