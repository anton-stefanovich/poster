from PIL import Image, ImageColor
from pyshorteners import Shortener, exceptions
import twitter
import facebook
import time
import random


class PosterHelper:
    ATTEMPTS_DEFAULT = 3
    ATTEMPTS_SHORTENER = ATTEMPTS_DEFAULT
    ATTEMPTS_FACEBOOK = ATTEMPTS_DEFAULT
    ATTEMPTS_TWITTER = ATTEMPTS_DEFAULT

    AJAX_DELAY_SHORT = 3
    AJAX_DELAY_NORMAL = 7
    AJAX_DELAY_LONG = 13
    AJAX_DELAY_DEFAULT = AJAX_DELAY_SHORT

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
    def get_short_link(url, shortener='Google', token=None):
        print('Generating short link for \'%s\'' % url)

        if not token:
            if shortener == 'Google':
                token = 'AIzaSyASRIF0WJPftrc-KYtGftWYjUJ8yokqn_c'

            elif shortener == 'Bitly':
                token = '7728f16fbbc67269fca96de5887ec868e9040ff8'

        link = None
        for attempt in range(PosterHelper.ATTEMPTS_SHORTENER):
            print('Attempt #%d' % (attempt + 1))
            try:
                link = Shortener(shortener, api_key=token, bitly_token=token).short(url)
                break

            except (TypeError, ValueError) as error:
                print('Wrong type or value exception: %s' % error)

            except (exceptions.ExpandingErrorException,
                    exceptions.ShorteningErrorException,
                    exceptions.UnknownShortenerException) as error:
                print('Shortener exception: %s' % error)

            except:
                print('Unknown error occur')

        return link

    @staticmethod
    def get_ajax_page(driver, url, delay=AJAX_DELAY_DEFAULT):
        assert driver
        driver.get(url)

        time.sleep(delay)

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

        print('Posting twitter status: \'%s\'' % status_text)
        api.PostUpdate(status_text, media=status_media)

    @staticmethod
    def post_facebook_record(info, token):
        message_length = 256
        api = facebook.GraphAPI(token)
        message = PosterHelper.crop_text(
            info.pop('message'), message_length,
            suffix=' ' + info.get('link'))

        print('Posting facebook message: \'%s\'' % message)
        for attempt in range(PosterHelper.ATTEMPTS_FACEBOOK):
            try:
                api.put_wall_post(message, info)
                break

            except:
                pass

    @staticmethod
    def normalize_image(path):
        print('Normalizing image \'%s\'' % path)
        image = Image.open(path)
        image = PosterHelper.crop_image(image)

        print('Saving image \'%s\'' % path)
        image.save(path)

    @staticmethod
    def crop_image(image, color='white', delta=32):
        pix = image.load()
        crop_factor = sum(ImageColor.getrgb(color)) - delta
        crop_xl, crop_yt, crop_xr, crop_yb = 0, 0, 0, 0

        for crop_xl in range(image.width):
            if sum(pix[crop_xl, image.height * random.random()][:3]) < crop_factor:
                break

        for crop_xr in reversed(range(image.width)):
            if sum(pix[crop_xr, image.height * random.random()][:3]) < crop_factor:
                break

        for crop_yt in range(image.height):
            if sum(pix[image.width * random.random(), crop_yt][:3]) < crop_factor:
                break

        for crop_yb in reversed(range(image.height)):
            if sum(pix[image.width * random.random(), crop_yb][:3]) < crop_factor:
                break

        return image.crop((crop_xl, crop_yt, crop_xr, crop_yb))

    @staticmethod
    def crop_text(text, max_length, prefix=str(), suffix=str()):
        max_length -= len(prefix) + len(suffix)
        if len(text) > max_length:
            text = text[:max_length - 2].strip() + '..'

        text += suffix
        return prefix + text
