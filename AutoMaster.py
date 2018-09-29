from CarAndDriverItem import CarAndDriverItem
from MotorTrendItem import MotorTrendItem
from PosterMaster import PosterMaster
from PosterHelper import PosterHelper
from selenium import webdriver


class AutoMaster (PosterMaster):
    url_caranddriver = 'https://blog.caranddriver.com/'
    url_motortrend = 'http://www.motortrend.com/auto-news/'

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

    def get_records(self, count=0):
        records = dict()
        driver = webdriver.Chrome()

        records.update(AutoMaster.get_motortrend_news(driver))
        records.update(AutoMaster.get_caranddriver_news(driver))
        driver.close()

        return records

    @staticmethod
    def get_caranddriver_news(driver):
        PosterHelper.get_ajax_page(driver, AutoMaster.url_caranddriver)
        post_wrapper_objects = driver.find_elements_by_class_name('cd-article-summary')

        records = dict()
        for post_wrapper_object in post_wrapper_objects:
            record = CarAndDriverItem(post_wrapper_object)
            if record.image:  # ToDo Upload all content!
                records[record.id] = record

        return records

    @staticmethod
    def get_motortrend_news(driver):
        PosterHelper.get_ajax_page(driver, AutoMaster.url_motortrend)
        post_wrapper_objects = driver.find_elements_by_class_name('entry-article')

        records = dict()
        for post_wrapper_object in post_wrapper_objects:
            topic_elements = post_wrapper_object.find_elements_by_css_selector('.entry-topic')
            if len(topic_elements) and topic_elements.pop().text.upper().count('NEWS'):
                record = MotorTrendItem(post_wrapper_object)
                if len(record.title):
                    records[record.id] = record

        return records
