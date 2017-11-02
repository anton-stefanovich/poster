from HomeItem import HomeItem
from PosterHelper import PosterHelper
from selenium import webdriver

import random


class HomeMaster:
    url_base = 'http://homeoftampabay.kwrealty.com'
    url_search = '/map/searchid/'
    url_search_ids = ['17749077']

    @staticmethod
    def get_twitter_token():
        return {
            'consumer_key': 'gDGUnKgf7Pj8YInqoeKT4PHDJ',
            'consumer_secret': 'LGjYlSYa5Z6beCnD5WXSY615fXRY9i7eOTp2H8FBUEbfuzIvVZ',
            'access_key': '1411815349-lQy2Om1LVcuRamjRlxLcGgT050CmcjAXJR2UPpX',
            'access_secret': 'CHyauYMUNkypp5S0GxwyehQMno99vt1eM4riKqI8j0v9x',
        }

    @staticmethod
    def get_records(count):
        driver = webdriver.Firefox()
        PosterHelper.get_ajax_page(
            driver, HomeMaster.url_base + HomeMaster.url_search + HomeMaster.url_search_ids[0])

        elements = driver.find_elements_by_class_name('card-flex-container')
        indexes = random.sample(range(len(elements)), count)
        assert count == len(indexes)

        records = list()
        for index in indexes:
            element = elements[index]
            favorite = element.find_element_by_class_name('favorite')
            records.append({
                'url': HomeMaster.url_base + element.get_attribute('data-link'),
                'id':  favorite.get_attribute('property-number')
            })

        homes = list()
        assert count == len(records)
        for apartment in records:
            homes.append(
                HomeItem(
                    driver=driver,
                    url=apartment.get('url'),
                    id=apartment.get('id')))

        assert count == len(homes)
        driver.close()

        return homes
