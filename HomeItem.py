import os
from PosterHelper import PosterHelper


class HomeItem:
    id = str()
    url = str()
    summary = str()
    payment = str()
    images = list()

    def __init__(self, driver, url, id):
        self.id = id
        self.url = url

        PosterHelper.get_ajax_page(driver, url)

        self.images = self.get_images(driver)
        self.summary = self.get_summary(driver)
        self.payment = self.get_payment(driver)

        self.images = self.save_images(
            driver, self.images, 'pictures' + os.sep + self.id)

    @staticmethod
    def get_images(driver):
        images_block = driver.find_elements_by_class_name('slick-slide')[:5]
        images = list()

        for image_block_object in images_block:
            image_object = image_block_object.find_element_by_tag_name('img')
            image_id = image_block_object.get_attribute('aria-describedby')
            image_lazy = image_object.get_attribute('data-lazy')
            image_src = image_object.get_attribute('src')

            image_link = image_src \
                if image_src else image_lazy

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

    @staticmethod
    def save_images(driver, images, path):
        if not os.path.exists(path):
            os.mkdir(path)

        local_images = list()
        for image in images:
            link = image.get('link')
            name = image.get('id') + '.png'

            driver.get(link)
            image_object = driver.find_element_by_tag_name('img')

            image_path = path + os.sep + name
            image_object.screenshot(image_path)
            local_images.append(image_path)

        return local_images

    def get_twitter_info(self):
        return {
            'status': self.summary,
            'images': self.images[:4],
            'link':   PosterHelper.get_short_link(self.url),
        }
