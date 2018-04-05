# system
from datetime import datetime
import argparse
import time

# custom
from PosterHelper import PosterHelper
from TestMaster import TestMaster
from HomeMaster import HomeMaster
from AutoMaster import AutoMaster


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repeat', type=int, default=1)
    parser.add_argument('--delay', type=int, default=3600)
    parser.add_argument('--media', '--destination', type=str, choices=['twitter', 'facebook'])
    parser.add_argument('--type', type=str, choices=['test', 'home', 'auto'])
    parser.add_argument('--debug', type=bool, nargs='?', const=True, default=False)
    args = parser.parse_args()

    return TestMaster.run() if args.type == 'test' else action(args)


def action(args):
    repeat = args.repeat
    delay = args.delay
    master = {
        'test': TestMaster,
        'home': HomeMaster,
        'auto': AutoMaster,
    }.get(args.type, None)
    assert master

    # action = {
    #     'twitter':  PosterHelper.post_twitter_status,
    #     'facebook': PosterHelper.post_facebook_record,
    # }.get(args.destination)

    twitter_token = PosterHelper.debug_twitter_token() \
        if args.debug else master.get_twitter_token()

    facebook_token = PosterHelper.debug_facebook_token() \
        if args.debug else master.get_facebook_token()

    token = twitter_token if args.media == 'twitter' else (
            facebook_token if args.media == 'facebook' else None)
    assert token

    records = master.get_records(repeat)
    assert repeat == len(records)

    while len(records):
        record = records.pop()
        print('%s - Record \'%s\' publish started' % (datetime.now(), record.id))

        try:
            if args.media == 'twitter':
                PosterHelper.post_twitter_status(record.get_twitter_info(), token)

            if args.media == 'facebook':
                PosterHelper.post_facebook_record(record.get_facebook_info(), token)

            print('%s - Record published' % datetime.now())

        except:
            print('Unknown error occur')

        if len(records):
            print('Waiting %d minutes' % (delay / 60))
            time.sleep(delay)


if __name__ == "__main__":
    main()
