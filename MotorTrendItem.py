import os
# from PosterHelper import PosterHelper


class MotorTrendItem:
    # id = str()
    url = str()
    title = str()
    # summary = str()
    images = list()

    def __init__(self, wrapper_node):
        # self.id = MotoTrendItem.get_id(wrapper_node)
        self.url = MotorTrendItem.get_url(wrapper_node)
        self.title = MotorTrendItem.get_title(wrapper_node)
        # self.summary = MotoTrendItem.get_summary(wrapper_node)
        self.images = [MotorTrendItem.get_images(wrapper_node)]

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
            'status': self.title,
            'images': self.images[:4],
            'link':   self.url,
        }
