# -*- coding: utf-8 -*-

import random
import threading
import twitter
import yaml
from datetime import datetime


interval_min = float()
status_filename = str()
settings_filename = 'settings.yml'


def loadauth(filename=settings_filename):
    global auth
    global interval_min
    global status_filename
    try:
        f = open(filename, 'r', encoding='utf-8')
        p = yaml.load(f)
        auth = twitter.OAuth(
            consumer_key=p['consumer_key'],
            consumer_secret=p['consumer_secret'],
            token=p['token'],
            token_secret=p['token_secret']
        )
        interval_min = int(p['interval_min'])
        status_filename = p['status_filename']
        f.close()
        return False
    except FileNotFoundError:
        f = open(filename, 'w', encoding='utf-8')
        settings = {}
        for deta in ('consumer_key', 'consumer_secret', 'token', 'token_secret'):
            print('Enter your twitter {}...'.format(deta))
            settings.update({deta: input('>>>')})
        for deta in ('interval_min', 'status_filename'):
            print('Enter {} setting...'.format(deta))
            settings.update({deta: input('>>>')})
        f.write(yaml.dump(settings, default_flow_style=False))
        f.close()
        return True


def loadstatus(filename):
    f = None
    try:
        f = open(filename, 'r', encoding='utf-8').readlines()
        for line in f:
            if line[0] == '#':
                f.remove(line)
    except FileNotFoundError:
        open(filename, 'w', encoding='utf-8').close()
        f = open(filename, 'r', encoding='utf-8').readlines()
    finally:
        return f


def tweet(t, statuslist):
    status = random.choice(statuslist)
    t.statuses.update(status='Bot tweeted at '+str(datetime.now().strftime('%H:%M'))+')'+status)
    print('tweeted on ' + str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + ':' + status, end='')
    thread = threading.Timer(60.0 * interval_min, lambda: tweet(t, statuslist))
    thread.start()


def main():
    random.seed()
    if loadauth():
        exit()
    statuslist = loadstatus(status_filename)
    t = twitter.Twitter(auth=auth)
    thread = threading.Thread(target=lambda: tweet(t, statuslist))
    thread.start()


if __name__ == '__main__':
    main()
