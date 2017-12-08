from CarAndDriverItem import CarAndDriverItem
from MotorTrendItem import MotorTrendItem
from PosterMaster import PosterMaster
from PosterHelper import PosterHelper
from selenium import webdriver

# system
import random


class AutoMaster (PosterMaster):
    url_caranddriver = 'https://blog.caranddriver.com/'
    url_motortrend = 'http://www.motortrend.com/auto-news/'

    @staticmethod
    def get_twitter_token():
        return {
            'consumer_key': 'Srbw7uxJeNOn2HFrxlDwbbEiz',
            'consumer_secret': 'u6CCnKg2Uf50ShHEfBpqE3Fqv6QMXQqG1o7zCzEhDMlwtrT9Ck',
            'access_key': '753111292857188353-KSRY7RZhkLCM3VzOM0f7HSsWbTmVnu6',
            'access_secret': 'mTcQGX4tMzACWsfhQ6S0JrW8veKFK9ncQo2akgZOr3swz',
        }

    @staticmethod
    def get_records(count):
        driver = webdriver.Firefox()

        records = list()
        records += AutoMaster.get_motortrend_news(driver)
        records += AutoMaster.get_caranddriver_news(driver)
        driver.close()

        indexes = random.sample(range(len(records)), count)
        assert count == len(indexes)

        news = list()
        for index in indexes:
            news.append(records[index])

        return news

    @staticmethod
    def get_caranddriver_news(driver):
        PosterHelper.get_ajax_page(driver, AutoMaster.url_caranddriver)
        post_wrapper_objects = driver.find_elements_by_class_name('postWrapper')

        # indexes = random.sample(range(len(post_wrapper_objects)), count)
        # assert count == len(indexes)
        records = list()

        # for index in indexes:
        #     records.append(CarAndDriverItem(
        #         post_wrapper_objects[index]))

        for post_wrapper_object in post_wrapper_objects:
            records.append(CarAndDriverItem(post_wrapper_object))

        # assert count == len(records)

        return records

    @staticmethod
    def get_motortrend_news(driver):
        PosterHelper.get_ajax_page(driver, AutoMaster.url_motortrend)
        post_wrapper_objects = driver.find_elements_by_class_name('entry-article')

        records = list()
        for post_wrapper_object in post_wrapper_objects:
            record = MotorTrendItem(post_wrapper_object)
            if len(record.title):
                records.append(record)

        return records
