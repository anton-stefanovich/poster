from PosterItem import *
from PosterHelper import *

import requests
from bs4 import BeautifulSoup


class MotorTrendItem (PosterItem):
    __URL_BASE__ = 'https://www.motortrend.com'
    __URL_LIST__ = 'https://www.motortrend.com/auto-news/'

    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def get_records():
        page = requests.get(MotorTrendItem.__URL_LIST__)
        soup = BeautifulSoup(page.text, 'html.parser')
        articles = soup.select('.entry-article')

        records = dict()
        for article in articles:
            article_id = MotorTrendItem.get_id(article)
            article_url = MotorTrendItem.get_url(article)
            records[article_id] = MotorTrendItem(article_url)

            # if len(topic_elements) and topic_elements.pop().text.upper().count('NEWS'):
            #     record = MotorTrendItem(post_wrapper_object)
            #     if len(record.title):
            #         records[record.id] = record

        return records

    @staticmethod
    def is_sponsored_content(node):
        return len(node.find_elements_by_class_name('prx-promoted'))

    @staticmethod
    def get_id(article):
        return article['id']

    @staticmethod
    def get_url(article):
        return article.select_one('.link')['data-href']

    @staticmethod
    def get_title(article):
        tag = article.select_one('div.entry-header h1.entry-title.-title')
        return tag.get_text().strip()

    @staticmethod
    def get_summary(article):
        tag = article.select_one(
            'div.entry-header span.entry-title.-subtitle')
        return tag.get_text().strip()

    @staticmethod
    def get_images(article):
        title_image_tag = article.select_one(
            'div.featured-image div.image')

        article_image_tags = article.select(
            'figure.imagecontainer img')

        images = [
            PosterHelper.crop_url(
                title_image_tag['data-src'])]

        for image_tag in article_image_tags:
            images.append(
                PosterHelper.crop_url(
                    image_tag['data-src']))

        return images

    def get_twitter_info(self):
        return self.__get_info()

    def get_facebook_info(self):
        return self.__get_info()

    def __get_info(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')

        images = self.get_images(soup)
        text = self.build_summary([
            MotorTrendItem.get_title(soup),
            MotorTrendItem.get_summary(soup)
        ])

        return {
            'link':    self.url,
            'images':  images,
            'text':    text,
        }
