from PIL import Image, ImageColor
from pyshorteners import Shortener
import twitter
import facebook
import time


class PosterHelper:
    @staticmethod
    def debug_twitter_token():
        return {
            'consumer_key':    'NVVcefxs0QYyapdLKQZXdZ8Hd',
            'consumer_secret': '5Vo1KQ6qTILPLEV69pii0YQywyO5mq9VhpvKtO7t3dcUNUKVvi',
            'access_key':      '168206572-Qc7YjjfzthILxPInAxxL0EO6IhYjEapoBkLEfD8D',
            'access_secret':   'wrkWlL0Txs62wPevV99RUBcBGoW9aOtF5BdYTvo53KUNc',
        }

    @staticmethod
    def debug_facebook_token():
        return PosterHelper.get_facebook_token('373574129759628')

    @staticmethod
    def get_facebook_token(page_id):
        access_token = None
        user_access_token = 'EAAcD5OvwFogBANMvKKkZCtH0KOqsj0mZCaZBj2VAPEUlNWtVVgLZCtKlxni6vwi7MnusJEKdAcnVt7VDwQ1RZBDd9A7ZBMI5o0TmHO7YZClhgRbScB96YtIfMxSOK6OQwDKZCZBJ5Y2nKy1YqjdxHa2uQyKsju2vseiTWLJBLK5y1QQZDZD'

        graph = facebook.GraphAPI(user_access_token)
        accounts = graph.get_object('me/accounts')

        for page in accounts.get('data'):
            if page['id'] == page_id:
                access_token = page['access_token']

        return access_token

    @staticmethod
    def get_short_link(url):
        # shortener = Shortener('Bitly', bitly_token='7728f16fbbc67269fca96de5887ec868e9040ff8')
        return Shortener('Google', api_key='AIzaSyASRIF0WJPftrc-KYtGftWYjUJ8yokqn_c').short(url)

    @staticmethod
    def get_ajax_page(driver, url):
        assert driver
        driver.get(url)

        time.sleep(5)

    @staticmethod
    def post_twitter_status(info, token):
        status_length = 140
        status_link_pattern = 'https://t.co/1234567890'

        status_media = info['images'][:4]
        status_link = info['link']
        status_text = PosterHelper.crop_text(
            info['status'], status_length - len(status_link_pattern),
            suffix=' ') + status_link

        api = twitter.Api(
            consumer_key=token.get('consumer_key'),
            consumer_secret=token.get('consumer_secret'),
            access_token_key=token.get('access_key'),
            access_token_secret=token.get('access_secret'))

        api.PostUpdate(status_text, media=status_media)

    @staticmethod
    def post_facebook_record(info, token):
        message_length = 256
        message = PosterHelper.crop_text(
            info.pop('message'), message_length,
            suffix=' ' + info.get('link'))

        api = facebook.GraphAPI(token)
        api.put_wall_post(message, info)

    @staticmethod
    def normalize_image(path):
        image = Image.open(path)
        image = PosterHelper.crop_image(image)
        image.save(path)

    @staticmethod
    def crop_image(image):
        pix = image.load()
        image_size_x, image_size_y = image.size
        crop_factor = sum(ImageColor.getrgb('white')) - 17
        crop_xl, crop_yt, crop_xr, crop_yb = 0, 0, 0, 0

        for crop_xl in range(image_size_x):
            if sum(pix[crop_xl, image_size_y/2]) < crop_factor:
                break

        for crop_xr in reversed(range(image_size_x)):
            if sum(pix[crop_xr, image_size_y / 2]) < crop_factor:
                break

        for crop_yt in range(image_size_y):
            if sum(pix[image_size_x/2, crop_yt]) < crop_factor:
                break

        for crop_yb in reversed(range(image_size_y)):
            if sum(pix[image_size_x / 2, crop_yb]) < crop_factor:
                break

        return image.crop((crop_xl, crop_yt, crop_xr, crop_yb))

    @staticmethod
    def crop_text(text, max_length, prefix=str(), suffix=str()):
        max_length -= len(prefix) + len(suffix)
        if len(text) > max_length:
            text = text[:max_length - 2] + '..'

        text += suffix
        return prefix + text
