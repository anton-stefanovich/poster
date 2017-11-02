# system
import argparse
import time

# custom
from PosterHelper import PosterHelper
from HomeMaster import HomeMaster
from AutoMaster import AutoMaster


# def post_facebook_message(info):
#     # token = 'EAAcD5OvwFogBAJY0zqToOjjBCbekCJMSnx7D9vRKcxrfdMPyRKjPZAwdvQ8mZB8eh7du' \
#     #         '87XzPbCSIsYzmtO5h7JFT39kmA9iM9QIZAbnL6Ep9Tx28DH3wcAiGcXeiXTABXNiZA8LQ' \
#     #         'yZCU8N9eumhZCRaCxIXNFLal7Cv56uOeJdd1eegAbtVYrndF34HNytnVSdJF9rx5KqwZDZD'
#
#     token = '1974606582781576|p3bQ-kRGb0yzLpHspPVxk8M8ywI'
#     client_token = '596c55a2898b8570d56778352656e4bf'
#     app_id = '1974606582781576'
#     app_secret = '718a7c6f39c9d826137f7ef02a37c1e4'
#     graph = facebook.GraphAPI(token)
#     graph.put_wall_post('test')


def test():
    return list()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repeat', type=int, default=1)
    parser.add_argument('-d', '--delay', type=int, default=3600)
    parser.add_argument('-t', '--type', type=str, choices=['home', 'auto'])
    parser.add_argument('--debug', type=bool, nargs='?', const=True, default=False)

    args = parser.parse_args()
    repeat = args.repeat
    delay = args.delay
    master = {
        'home': HomeMaster,
        'auto': AutoMaster,
    }.get(args.type)

    assert master
    records = master.get_records(repeat)
    assert(repeat == len(records))

    for index in range(repeat):
        record = records[index]
        twitter_info = record.get_twitter_info()
        twitter_token = PosterHelper.debug_twitter_token() \
            if args.debug else master.get_twitter_token()

        PosterHelper.post_twitter_status(twitter_info, twitter_token)
        print('%d - %s: done' % (index, twitter_info.get('status')[:32]))

        if repeat - index > 1:
            time.sleep(delay)


if __name__ == "__main__":
    main()
