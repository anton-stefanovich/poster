import os
from PosterHelper import PosterHelper


class PosterItem:
    @staticmethod
    def save_images(driver, images, path):
        local_images = list()
        for image in images:
            image_file = PosterItem.save_image(
                driver, image.get('link'), image.get('id'), path)
            local_images.append(image_file)

        return local_images

    @staticmethod
    def save_image(driver, link, name, path):
        if not os.path.exists(path):
            os.mkdir(path)

        driver.get(link)
        image_object = driver.find_element_by_tag_name('img')

        image_path = path + os.sep + name + '.png'
        image_object.screenshot(image_path)

        return image_path

    def get_twitter_info(self):
        return {
            'status':  None,
            'images':  None,
            'link':    None,
        }

    def get_facebook_info(self):
        return {
            'message': None,
            'picture': None,
            'link':    None,
        }
