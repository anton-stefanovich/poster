from PosterHelper import PosterHelper


class PosterItem:
    id = None

    @staticmethod
    def save_images(images, path):
        local_images = list()
        for image in images:
            image_file = PosterItem.save_image(
                image.get('link'), image.get('id'), path)
            local_images.append(image_file)

        return local_images

    @staticmethod
    def save_image(link, name, path):
        name += link[link.rfind('.'):]
        image_path = PosterHelper.save_file(
                PosterHelper.download_file(link),
                path, name, binary=True)

        PosterHelper.normalize_image(image_path)

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
