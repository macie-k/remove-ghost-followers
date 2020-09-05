from argparse import ArgumentParser
from getpass import getpass
from instabot import Bot
from time import sleep
from os import system
from os import path
from tqdm import tqdm
from sys import exit

import platform

parser = ArgumentParser()
parser.add_argument('-u', '--username', metavar='username', nargs=1, help='Direct login info')
parser.add_argument('-p', '--password', metavar='password', nargs=1, help='Direct login info')
args = parser.parse_args()

bot = Bot()
clear = 'clear'


def main(username, password):
    bot.login(username=username, password=password)

    sleep(1)
    system(clear)

    if not path.exists('whitelist.txt'):
        with open('whitelist.txt', 'w+') as f:
            f.write('!! USERS MUST BE PROVIDED AS IDs !!')

    print('[OK] Getting followers . . .')
    all_followers = bot.get_user_followers(username)
    print(f'[OK] Found {len(all_followers)} followers\n')
    
    print('[OK] Getting all posts . . .')
    all_posts = bot.get_total_user_medias(username)
    print(f'[OK] Found {len(all_posts)} posts\n')

    print('[OK] Getting all likers . . .')
    all_likers = []
    for post in tqdm(all_posts):
        post_likers = bot.get_media_likers(post)

        for liker in post_likers:
            if liker not in all_likers:
                all_likers.append(liker)

    # print(f'{bot.get_link_from_media_id(post)} ::: {len(post_likers)}')
    print(f'[OK] Found {len(all_likers)} likers\n')

    print('[OK] Getting not-likers . . .')
    not_likers = list(set(all_followers) - set(all_likers))
    print(f'[OK] Found {len(not_likers)} people who didn\'t like any of your posts\n')

    if len(not_likers) > 0:
        while(True):
            block = input('[>] Remove them? [yes/n]: ')
            if(block == 'yes' or block =='Yes' or block == 'YES'):
                break
            if(block == 'n' or block =='N'):
                exit()

        whitelist = ['placeholder']
        with open('whitelist.txt', 'r') as f:
            whitelist = f.read().splitlines()

        print('\n[OK] Removing ghost followers . . .')
        for user in not_likers:
            if user not in whitelist:
                bot.remove_follower(user)
            else:
                print(f'[ ! ] Skipping {user} - whitelisted')

    input('\n[OK] Finished')
    exit()



#####################

OS = platform.system()
if OS == 'Windows':
    clear = 'cls'

system(clear)
username = args.username[0] if args.username else input('[>] Username: ')
password = args.password[0] if args.password else getpass('[>] Password: ')

try:
    main(username, password)
except Exception as e:
    print(f'[ERROR] {e}')

