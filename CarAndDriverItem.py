from PosterItem import *

import requests
from bs4 import BeautifulSoup


class CarAndDriverItem (PosterItem):
    __URL_BASE__ = 'https://caranddriver.com'
    __URL_LIST__ = 'https://blog.caranddriver.com'
    __URL_IMAGE_BASE__ = 'https://hips.hearstapps.com/'

    def __init__(self, url, text):
        self.url = url
        self.text = text

    @staticmethod
    def get_records():
        records = dict()

        page = requests.get(CarAndDriverItem.__URL_LIST__)
        soup = BeautifulSoup(page.text, 'html.parser')

        articles = soup('cd-article-summary')
        for article in articles:
            url_raw = CarAndDriverItem.get_url(article)
            url_full = CarAndDriverItem.__URL_BASE__ + url_raw

            text = CarAndDriverItem.build_summary(
                summary=CarAndDriverItem.get_summary(article),
                title=CarAndDriverItem.get_title(article))

            records[url_raw] = CarAndDriverItem(url_full, text)

        return records

    @staticmethod
    def get_title(wrapper):
        tag = wrapper.find(class_='gtm-article-title')
        return tag.string

    @staticmethod
    def get_summary(wrapper):
        tag = wrapper.find(class_='text-nero')
        return tag.string

    @staticmethod
    def get_url(wrapper):
        tag = wrapper.find('a')
        return tag['href'] if tag else None

    @staticmethod
    def get_images(wrapper):
        title_image_tag = wrapper.select_one(
            'div.hover-filter a.gtm-image-link img')

        article_image_tags = wrapper.select(
            'span.inline-image img')

        images = [
            PosterHelper.crop_url(
                title_image_tag['src'])]

        for image_tag in article_image_tags:
            images.append(
                PosterHelper.crop_url(
                    CarAndDriverItem.__URL_IMAGE_BASE__ +
                    image_tag['data-src']))

        return images

    def get_twitter_info(self):
        return self.__get_info()

    def get_facebook_info(self):
        return self.__get_info()

    def __get_info(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.images = self.get_images(soup)

        return {
            'images':  self.images,
            'link':    self.url,
            'text':    self.text,
        }
