from PosterItem import *
from PosterHelper import *


class MotorTrendItem (PosterItem):
    url = str()
    title = str()
    images = list()

    def __init__(self, wrapper_node):
        if not MotorTrendItem.is_sponsored_content(wrapper_node):
            self.id = MotorTrendItem.get_id(wrapper_node)
            self.url = MotorTrendItem.get_url(wrapper_node)
            self.title = MotorTrendItem.get_title(wrapper_node)
            self.images = [MotorTrendItem.get_images(wrapper_node)]

    @staticmethod
    def is_sponsored_content(node):
        return len(node.find_elements_by_class_name('prx-promoted'))

    @staticmethod
    def get_id(node):
        return node.get_attribute('id')

    @staticmethod
    def get_title(node):
        title_object = node.find_element_by_class_name('entry-title')
        return title_object.text

    @staticmethod
    def get_url(node):
        post_link_object = node.find_element_by_class_name('link')
        return post_link_object.get_attribute('data-href')

    @staticmethod
    def get_images(node):
        image_object = node.find_element_by_class_name('wp-post-image')
        image_src = image_object.get_attribute('data-base')
        if image_src and not len(image_src):
            image_src = image_object.get_attribute('src')

        return image_src

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
            'status': self.title,
            'images': self.images[:4],
            'link':   self.url,
        }

    def get_facebook_info(self):
        picture = self.images.pop() \
            if self.images else None

        return {
            'message': self.title,
            'picture': picture,
            'link': PosterHelper.get_short_link(self.url),
        }
