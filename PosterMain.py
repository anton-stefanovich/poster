# system
import argparse
import random
import time

# custom
from PosterHelper import PosterHelper
from TestMaster import TestMaster
from HomeMaster import HomeMaster
from AutoMaster import AutoMaster


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repeat', type=int, default=1)
    parser.add_argument('--delay',  type=int, default=0)

    parser.add_argument('--type',  type=str, choices=['test', 'home', 'auto'])
    parser.add_argument('--media', type=str, choices=['twitter', 'facebook'])

    bool_true = ['true', 'yes', '1']
    parser.add_argument('--debug', default=False,
                        type=lambda s: s.lower() in bool_true)
    args = parser.parse_args()

    return TestMaster.run() if args.type == 'test' else action(args)


def action(args):
    assert args

    master_class = {
        'test': TestMaster,
        'home': HomeMaster,
        'auto': AutoMaster,
    }.get(args.type, None)

    assert master_class
    master = master_class()

    publisher = {
        'twitter': {
            'method': PosterHelper.post_twitter_status,
            'token':  PosterHelper.debug_twitter_token
            if args.debug else master.get_twitter_token, },
        'facebook': {
            'method': PosterHelper.post_facebook_record,
            'token':  PosterHelper.debug_facebook_token
            if args.debug else master.get_facebook_token, }
    }.get(args.media, None)

    assert publisher

    records = master.get_records()
    assert len(records)

    publisher_method = publisher.get('method', None)
    assert publisher_method

    publisher_token = publisher.get('token', None)
    assert publisher_token

    repeats = list(range(args.repeat))
    while len(records) and len(repeats):
        rec_id = random.choice(list(records.keys()))
        record = records.pop(rec_id)

        print("Record '{rec_id}' publish started".format(rec_id=rec_id))

        if master.is_record_exists(rec_id):
            print('\t' 'Record was published earlier. Skipping it...')

        else:
            publisher_method(record, publisher_token())
            master.insert_record(rec_id)

            repeats.pop()

            # delay
            if len(repeats):
                print('Waiting %d minutes' % (args.delay / 60))
                time.sleep(args.delay)


if __name__ == "__main__":
    main()
