from PosterHelper import PosterHelper
from abc import ABC, abstractmethod
import os


class PosterItem(ABC):
    id = None
    __MEDIA_DIR__ = 'media'

    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

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
    def build_summary(strings):
        summary = str()

        for string in strings:
            connector = u'. '
            for ch in ['.', ',', '!', '?', ':', ':']:
                if summary.endswith(ch):
                    connector = u' '
                    break

            summary += string + connector

        return summary.strip()

    @abstractmethod
    def get_facebook_info(self):
        pass

    @abstractmethod
    def get_twitter_info(self):
        pass
