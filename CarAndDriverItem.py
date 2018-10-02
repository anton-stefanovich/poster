from PosterItem import *
from selenium import webdriver


class CarAndDriverItem (PosterItem):

    def __init__(self, wrapper_node):
        self.url = self.get_url(wrapper_node)
        self.id = self.url

        self.text = self.build_summary(
            self.get_summary(wrapper_node),
            title=self.get_title(wrapper_node))

    @staticmethod
    def get_title(node):
        title_object = node.find_element_by_class_name('gtm-article-title')
        return title_object.text

    @staticmethod
    def get_url(node):
        link_object = node.find_element_by_class_name('gtm-image-link')
        return link_object.get_attribute('href')

    @staticmethod
    def get_summary(node):
        summary_object = node.find_element_by_class_name('text-nero')
        return summary_object.text

    @staticmethod
    def get_images(page):
        title_image_object = page.find_element_by_css_selector('div.hover-filter a.gtm-image-link img')
        article_image_objects = page.find_elements_by_css_selector('span.inline-image img')

        images = [
            PosterHelper.crop_url(title_image_object.get_attribute('src'))]

        for image_object in article_image_objects:
            images.append(
                PosterHelper.crop_url(image_object.get_attribute('src')))

        return images

    def get_twitter_info(self):
        return self.__get_info()

    def get_facebook_info(self):
        return self.__get_info()

    def __get_info(self):
        driver = webdriver.Chrome()
        PosterHelper.get_ajax_page(driver, self.url)
        body_object = driver.find_element_by_tag_name('body')
        self.images = self.get_images(body_object)
        driver.close()

        return {
            'images':  self.images,
            'link':    self.url,
            'text':    self.text,
        }
