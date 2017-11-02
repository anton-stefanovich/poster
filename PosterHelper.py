from pyshorteners import Shortener
import twitter
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
        status_suffix = '.. ' \
            if len(info['status']) > status_length else ' '
        status_link_pattern = 'https://t.co/1234567890'
        status_index_crop = status_length \
            - len(status_link_pattern) \
            - len(status_suffix)

        status_media = info['images'][:4]
        status_link = info['link']  # PosterHelper.get_short_link(info['link'])
        status_short = info['status'][:status_index_crop].strip()
        status_text = status_short + status_suffix + status_link

        api = twitter.Api(
            consumer_key=token.get('consumer_key'),
            consumer_secret=token.get('consumer_secret'),
            access_token_key=token.get('access_key'),
            access_token_secret=token.get('access_secret'))

        api.PostUpdate(status_text, media=status_media)
