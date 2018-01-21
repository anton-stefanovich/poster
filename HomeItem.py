# system
import os

# custom
from PosterHelper import PosterHelper
from PosterItem import PosterItem


class HomeItem (PosterItem):
    url = str()
    tags = dict()
    summary = str()
    payment = str()
    images = list()

    def __init__(self, driver, url, id, tags):
        self.id = id
        self.url = url
        self.tags = tags

        PosterHelper.get_ajax_page(driver, url)

        self.images = self.get_images(driver)
        self.summary = self.get_summary(driver)
        self.payment = self.get_payment(driver)

        for image in self.images:
            image.update({
                'file': self.save_image(
                    image.get('link'), image.get('id'),
                    'pictures' + os.sep + self.id)})

    @staticmethod
    def get_images(driver):
        images_block = driver.find_elements_by_class_name('slick-slide')[:5]
        images = list()

        for image_block_object in images_block:
            image_object = image_block_object.find_element_by_tag_name('img')
            image_id = image_block_object.get_attribute('aria-describedby')
            image_lazy = image_object.get_attribute('data-lazy')
            image_src = image_object.get_attribute('src')

            image_link = image_src if image_src else image_lazy
            image_link = image_link[:image_link.find('?') + 1].strip('?')

            if image_id and 'f_' in image_link:
                images.append({
                    'id': image_id,
                    'link': image_link,
                })

        return images

    @staticmethod
    def get_summary(driver):
        summary_object = driver.find_element_by_class_name('summary')
        return summary_object.text

    @staticmethod
    def get_payment(driver):
        payment_object = driver.find_element_by_id('aria-estimatedpayment')
        return payment_object.text

    def get_twitter_info(self):
        images = list()
        if self.images:
            for image in self.images[:4]:
                images.append(image.get('file'))

        return {
            'images': images,
            'status': '#RealEstate ' + self.tags.get('major') +
                      ' ' + self.tags.get('minor') + ' ' + self.payment + '/m: ' + self.summary,
            'link':   PosterHelper.get_short_link(self.url),
        }

    def get_facebook_info(self):
        picture = self.images[0].get('link') \
            if self.images and len(self.images) else None

        message = self.summary
        if len(self.payment):
            message = 'Monthly payment: only ' + self.payment + '! ' + message

        return {
            'message': message,
            'picture': picture,
            'link': PosterHelper.get_short_link(self.url),
        }
