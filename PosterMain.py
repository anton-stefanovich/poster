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
    parser.add_argument('--destination', type=str, choices=['twitter', 'facebook'])
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

    twitter_token = PosterHelper.debug_twitter_token() \
        if args.debug else master.get_twitter_token()

    facebook_token = PosterHelper.debug_facebook_token() \
        if args.debug else master.get_facebook_token()

    token = twitter_token if args.destination == 'twitter' else (
            facebook_token if args.destination == 'facebook' else None)
    assert token

    records = master.get_records(repeat)
    assert repeat == len(records)

    while len(records):
        record = records.pop()
        print('%s - Record \'%s\' publish started' % (datetime.now(), record.id))

        if args.destination == 'twitter':
            PosterHelper.post_twitter_status(record.get_twitter_info(), token)

        if args.destination == 'facebook':
            PosterHelper.post_facebook_record(record.get_facebook_info(), token)

        print('%s - Record publish completed' % datetime.now())

        if len(records):
            time.sleep(delay)


if __name__ == "__main__":
    main()
