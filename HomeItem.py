# custom
from PosterHelper import PosterHelper
from PosterItem import PosterItem

# libs
import requests
from bs4 import BeautifulSoup

# system
from random import choice


class HomeItem (PosterItem):
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

    def __init__(self, url):
        super().__init__(url)
        self.url = url

    @staticmethod
    def get_id(card):
        id_tag = card.select_one('span#mlsValue')
        return id_tag.string.strip()

    def get_images(self, card):
        tags = card.select('div.primary-carousel img.slider-image')

        images = list()
        for tag in tags:
            image_src = PosterHelper.crop_url(tag['data-lazy'])
            images.append(image_src.strip('/'))

        return images

    @staticmethod
    def get_summary(card):
        summary = str()
        summary_tag = card.select_one('div.summary')
        summary_text = summary_tag.strings
        for string in summary_text:
            string = string.strip()
            if string:
                summary += string + ' '

        return summary[:-1]

    @staticmethod
    def get_price(card):
        price_tag = card.select_one('span.price')
        return price_tag.string.strip()

    @staticmethod
    def get_tags(price: str):
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
            ' ' + choice(HomeItem.tags_map.get(key_all)) + \
            ' ' + choice(HomeItem.tags_map.get(key_price))

    def __get_info(self):
        page = requests.get(super().url)
        soup = BeautifulSoup(page.text, 'html.parser')
        card = soup.select_one('main.main-container div.row')

        self.id = self.get_id(card)
        self.images = self.get_images(card)
        self.summary = self.get_summary(card)
        self.price = self.get_price(card)

        return {
            'link': self.url,
            'images': self.images,
        }

    def get_twitter_info(self):
        info = self.__get_info()

        info['text'] = \
            self.get_tags(self.price) + ' ' + \
            self.price + ': ' + self.summary

        return info

    def get_facebook_info(self):
        info = self.__get_info()

        info['text'] = \
            self.get_tags(self.price) + ' ' + \
            'Price: ' + self.price + '! ' + \
            self.summary

        return info
