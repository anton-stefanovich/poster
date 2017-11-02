import os
from PosterHelper import PosterHelper


class CarAndDriverItem:
    id = str()
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
            'status': self.title + '. ' + self.summary,
            'images': self.images[:4],
            'link':   self.url,
        }
