from PosterItem import *
from PosterHelper import *


class CarAndDriverItem (PosterItem):

    def __init__(self, wrapper_node):
        self.url = self.get_url(wrapper_node)
        self.title = self.get_title(wrapper_node)
        self.summary = self.get_summary(wrapper_node)
        self.image = self.get_image(wrapper_node)

        self.id = self.url

    @staticmethod
    def get_id(node):
        return node.get_attribute('id')

    @staticmethod
    def get_title(node):
        title_object = node.find_element_by_class_name('gtm-article-title')
        return title_object.text

    @staticmethod
    def get_url(node):
        link_object = node.find_element_by_class_name('gtm-image-link')
        return link_object.get_attribute('href')

    @staticmethod
    def get_image(node):
        image_object = node.find_element_by_tag_name('img')
        image_url = image_object.get_attribute('src')
        return PosterItem.trim_url(image_url) \
            if image_url else image_url

    @staticmethod
    def get_summary(node):
        summary_object = node.find_element_by_class_name('text-nero')
        return summary_object.text

    def get_twitter_info(self):
        return self.__get_info()

    def get_facebook_info(self):
        return self.__get_info()

    def __get_info(self):
        return {
            'image':   self.image,
            'images':  [self.image],
            'link':    self.url,
            'text':    self.title + '. ' + self.summary,
        }
