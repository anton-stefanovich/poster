# system
import random

# custom
from PosterHelper import PosterHelper
from PosterItem import PosterItem
from selenium import webdriver


class HomeItem (PosterItem):
    def __init__(self, id, url, tags):
        self.id = id
        self.url = url
        self.tags = tags

    @staticmethod
    def get_images(driver):
        images_block = driver.find_elements_by_class_name('slick-slide')[:5]
        images = dict()

        for image_block_object in images_block:
            image_object = image_block_object.find_element_by_tag_name('img')
            image_id = image_block_object.get_attribute('aria-describedby')

            image_lazy = image_object.get_attribute('data-lazy')
            image_src = image_object.get_attribute('src')
            image_link = image_src if image_src else image_lazy

            if 'f_' in image_link:
                images[image_id] = PosterItem.trim_url(image_link)

        return images

    @staticmethod
    def get_summary(driver):
        summary_object = driver.find_element_by_class_name('summary')
        return summary_object.text

    @staticmethod
    def get_payment(driver):
        payment_object = driver.find_element_by_id('aria-estimatedpayment')
        return payment_object.text

    def __get_info(self):
        driver = webdriver.Chrome()
        PosterHelper.get_ajax_page(driver, self.url)

        # images_local = dict()
        images_remote = self.get_images(driver)
        # for key in images_remote.keys():
        #     images_local[key] = self.save_image(
        #         images_remote[key], key)

        self.images = list(images_remote.values())
        self.summary = self.get_summary(driver)
        self.deal = self.get_payment(driver)

        driver.close()

    def get_twitter_info(self):
        self.__get_info()

        message = self.tags
        if len(self.deal):
            message += ' ' + self.deal + '/m: '

        message += self.summary

        return {
            'link': self.url,
            'text': message,
            'images': self.images,
        }

    def get_facebook_info(self):
        self.__get_info()

        message = self.tags
        if len(self.deal):
            message += ' Monthly payment: only ' + self.deal + '! '

        message += self.summary

        return {
            'link': self.url,
            'text': message,
            'image':
                self.images[0] if len(self.images) else None,
        }
