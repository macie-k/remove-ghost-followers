from argparse import ArgumentParser
from getpass import getpass
from instabot import Bot
from time import sleep
from tqdm import tqdm

import sys
import os
import platform

# parsing the arguments for one-line login
parser = ArgumentParser()
parser.add_argument('-u', '--username', metavar='username', nargs=1, help='Direct login info')
parser.add_argument('-p', '--password', metavar='password', nargs=1, help='Direct login info')
args = parser.parse_args()

bot = Bot() # initialize the bot
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

def main(username, password):
    bot.login(username=username, password=password)
    clear()

    # get all user's followers
    print('[OK] Getting followers . . .')
    all_followers = bot.get_user_followers(username)
    print(f'[OK] Found {len(all_followers)} followers\n')
    
    # get all user's posts
    print('[OK] Getting all posts . . .')
    all_posts = bot.get_total_user_medias(username)
    print(f'[OK] Found {len(all_posts)} posts\n')

    # get every person that ever liked any post
    print('[OK] Getting all likers . . .')
    all_likers = []
    for post in tqdm(all_posts):
        post_likers = bot.get_media_likers(post)

        for liker in post_likers:
            if liker not in all_likers:
                all_likers.append(liker)
    print(f'[OK] Found {len(all_likers)} unique likers\n')

    # substract lists and get everyone that follows the user but didn't like anything
    print('[OK] Getting not-likers . . .')
    not_likers = list(set(all_followers) - set(all_likers))
    print(f'[OK] Found {len(not_likers)} people who didn\'t like any of your posts\n')

    if len(not_likers) > 0:
        while(True):    # wait for the firm confirmation
            block = input('[>] Remove them? [yes/n]: ')
            if(block == 'yes' or block =='Yes' or block == 'YES'):
                break
            if(block == 'n' or block =='N'):
                sys.exit()

        whitelist = ['placeholder']
        with open('whitelist.txt', 'r') as f:
            whitelist = f.read().splitlines()   # get whitelisted users

        # finally remove every follower that is not whitelisted
        print('\n[OK] Removing ghost followers . . .')
        for user in not_likers:
            if user not in whitelist:
                bot.remove_follower(user)
            else:
                print(f'[!] Skipping {user} - whitelisted')

    input('\n[OK] Finished')
    sys.exit()


#####################

clear()
# read the credentials from arguments, if empty ask for them
username = args.username[0] if args.username else input('[>] Username: ')
password = args.password[0] if args.password else getpass('[>] Password: ') # hidden input for password

print()
# check if whitelist exists else create and write first line
if not os.path.exists('whitelist.txt'):
    print('[!] Whitelist not found, creating . . .')
    with open('whitelist.txt', 'w+') as f:
        f.write('!! USERS MUST BE PROVIDED AS IDs !!')
# check if provided users are IDs else inform and exit
else:
    with open('whitelist.txt', 'r') as f:
        lines = f.read().splitlines()
        if len(lines) > 1:
            del lines[0]
            for line in lines:
                if not line.isnumeric():
                    input('[WARNING] Whitelist error - Provided user(s) are not ID(s) -- Change @usernames to numeric IDs')
                    sys.exit()
            print('[OK] Whitelist correct\n')
            sleep(.5)

try:
    main(username, password)
except Exception as e:  # catch any errors and pretty-print them
    print(f'[ERROR] {e}')
