from PosterItem import *

import requests
from bs4 import BeautifulSoup


class CarAndDriverItem (PosterItem):
    __URL_BASE__ = 'https://caranddriver.com'
    __URL_LIST__ = 'https://blog.caranddriver.com'
    __URL_IMAGE_BASE__ = 'https://hips.hearstapps.com/'

    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def get_records():
        records = dict()

        page = requests.get(CarAndDriverItem.__URL_LIST__)
        soup = BeautifulSoup(page.text, 'html.parser')

        articles = soup('cd-article-summary')
        for article in articles:
            url_raw = CarAndDriverItem.get_url(article)
            url_full = CarAndDriverItem.__URL_BASE__ + url_raw
            records[url_raw] = CarAndDriverItem(url_full)

        return records

    @staticmethod
    def get_title(wrapper):
        tag = wrapper.select_one('div.max-width-site h1')
        return tag.string.strip()

    @staticmethod
    def get_summary(wrapper):
        tag = wrapper.select_one('div.max-width-site h3')
        return tag.string.strip()

    @staticmethod
    def get_url(wrapper):
        tag = wrapper.find('a')
        return tag['href'] if tag else None

    @staticmethod
    def get_images(wrapper):
        title_image_sources = [
            'div.hover-filter a.gtm-image-link img',
            'picture.gtm-hips-picture img',
            'span.inline-image img',
        ]

        images = list()
        for source in title_image_sources:
            tags = wrapper.select(source)
            for tag in tags:
                src_preload = tag.get('src')
                src_on_show = tag.get('data-src')

                images.append(
                    PosterHelper.crop_url(
                        src_on_show or src_preload))

        return images

    def get_twitter_info(self):
        return self.__get_info()

    def get_facebook_info(self):
        return self.__get_info()

    def __get_info(self):
        page = requests.get(self.url)
        page.encoding = 'UTF-8'
        soup = BeautifulSoup(page.text, 'html.parser')
        article = soup.select_one('div.article-col-width')

        images = self.get_images(article)
        text = CarAndDriverItem.build_summary([
            CarAndDriverItem.get_title(soup),
            CarAndDriverItem.get_summary(soup),
        ])

        return {
            'link':    self.url,
            'images':  images,
            'text':    text,
        }
