# system
import argparse
import time

# custom
from PosterHelper import PosterHelper
from HomeMaster import HomeMaster
from AutoMaster import AutoMaster


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

        twitter_token = PosterHelper.debug_twitter_token() \
            if args.debug else master.get_twitter_token()

        facebook_token = PosterHelper.debug_facebook_token() \
            if args.debug else master.get_facebook_token()

        if twitter_token:
            twitter_info = record.get_twitter_info()
            PosterHelper.post_twitter_status(twitter_info, twitter_token)
            print('%d - twitter: %s: done' % (index, twitter_info.get('status')[:32]))

        if facebook_token \
                and not index % 3:  # dirty hack!! Fix it!
            facebook_info = record.get_facebook_info()
            PosterHelper.post_facebook_record(facebook_info, facebook_token)
            print('%d - facebook: done' % index)

        if repeat - index > 1:
            time.sleep(delay)


if __name__ == "__main__":
    main()
