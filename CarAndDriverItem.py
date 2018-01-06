from PosterItem import *
from PosterHelper import *


class CarAndDriverItem (PosterItem):
    url = str()
    title = str()
    summary = str()
    images = list()

    def __init__(self, wrapper_node):
        self.id = CarAndDriverItem.get_id(wrapper_node)
        self.url = CarAndDriverItem.get_url(wrapper_node)
        self.title = CarAndDriverItem.get_title(wrapper_node)
        self.summary = CarAndDriverItem.get_summary(wrapper_node)

        post_node = wrapper_node.find_element_by_class_name('post')
        self.images = [CarAndDriverItem.get_images(post_node)]

    @staticmethod
    def get_id(node):
        return node.get_attribute('id')

    @staticmethod
    def get_title(node):
        title_object = node.find_element_by_class_name('postTitle')
        return title_object.text

    @staticmethod
    def get_url(node):
        link_object = node.find_element_by_tag_name('a')
        return link_object.get_attribute('href')

    @staticmethod
    def get_images(node):
        image_object = node.find_element_by_tag_name('img')
        return image_object.get_attribute('src')

    @staticmethod
    def get_summary(node):
        summary = str()
        post_text_objects = node.find_elements_by_tag_name('p')
        for text_object in post_text_objects:
            paragraph_text = text_object.text.strip()
            summary += ' ' + paragraph_text
            summary = summary.strip()

        return summary

    def get_twitter_info(self):
        return {
            'status': self.title + '. ' + self.summary,
            'images': self.images[:4],
            'link':   self.url,
        }

    def get_facebook_info(self):
        picture = self.images.pop() \
            if self.images else None

        return {
            'message': self.summary,
            'picture': picture,
            'link': PosterHelper.get_short_link(self.url),
        }
