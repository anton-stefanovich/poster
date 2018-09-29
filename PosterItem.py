from PosterHelper import PosterHelper
from abc import ABC, abstractmethod
import os


class PosterItem(ABC):
    id = None
    __MEDIA_DIR__ = 'media'

    @staticmethod
    def save_images(images, path):
        local_images = list()
        for image in images:
            image_file = PosterItem.save_image(
                image.get('link'), image.get('id'), path)
            local_images.append(image_file)

        return local_images

    def save_image(self, link, name):
        name += link[link.rfind('.'):]
        image_dir = self.__MEDIA_DIR__ + os.sep + self.id
        image_path = PosterHelper.save_file(
                PosterHelper.download_file(link),
                image_dir, name, binary=True)

        PosterHelper.normalize_image(image_path)

        return image_path

    @staticmethod
    def trim_url(url):
        crop_at = url.find('?')
        return url[:crop_at] if crop_at > 0 else url

    @abstractmethod
    def get_facebook_info(self):
        pass

    @abstractmethod
    def get_twitter_info(self):
        pass
