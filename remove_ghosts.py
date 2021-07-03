from instabot import Bot
from argparse import ArgumentParser
from getpass import getpass
from time import sleep
from tqdm import tqdm
from colorama import Fore
from colorama import Style

import subprocess
import sys
import os

# parsing the arguments for one-line login
parser = ArgumentParser()
parser.add_argument('-u', '--username', metavar='username', nargs=1, help='Direct login info')
parser.add_argument('-p', '--password', metavar='password', nargs=1, help='Direct login info')
parser.add_argument('-l', '--list', metavar='list', nargs=1, help='Provide path to list of usernames or users to remove')
args = parser.parse_args()

bot = Bot()
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
whitelist = []

def remove_ghots():

    # get all user's followers
    success('Getting followers...')
    all_followers = bot.get_user_followers(username)
    success(f'Found {len(all_followers)} followers\n')

    # get all user's posts
    success('Getting all posts...')
    all_posts = bot.get_total_user_medias(username)
    total_posts = len(all_posts)

    # trim posts to avoid rate limit
    success(f'Found {total_posts} posts\n')
    if(total_posts > 100):
        success('Limiting search to last 100 posts only')
        all_posts = all_posts[:100]

    # get every person that ever liked any post
    success('Getting all likers...')
    all_likers = []

    for post in tqdm(all_posts):
        post_likers = bot.get_media_likers(post)

        for liker in post_likers:
            if liker not in all_likers:
                all_likers.append(liker)

    success(f'Found {len(all_likers)} unique likers\n')

    # substract lists and get everyone that follows the user but didn't like anything
    success('Getting not-likers...')
    not_likers = list(set(all_followers) - set(all_likers))
    success(f'Found {len(not_likers)} people who didn\'t like any of your posts\n')

    if len(not_likers) > 0:
        while(True):    # wait for the firm confirmation
            block = input('[>] Remove them? [yes/n]: ')
            if(block == 'yes' or block =='Yes' or block == 'YES'):
                break
            if(block == 'n' or block =='N'):
                sys.exit()

        # remove every follower that is not whitelisted
        print()
        success('Removing ghost followers...')
        for user in not_likers:
            if user not in whitelist:
                remove_user(user)
            else:
                warning(f'Skipping {user} - whitelisted')

    print()
    success('Finished', True)
    sys.exit()

def remove_from_list(filename):
    with open(filename, 'r') as f:
        users = f.read().splitlines()
        for user in users:
            if user.isnumeric():
                remove_user(user)
            else:
                remove_user(bot.get_username_from_user_id(user))

def remove_user(user):
    error = 0
    while True:
        if bot.remove_follower(user):
            success(f'Removed {user}' + ' '*10)
            error = 0
            sleep(.3)
            break
        else:
            if error == 0:
                error('Could not remove user, possible rate limit, retrying...')
            error += 1
            sleep(10)
            continue

##########################################

def success(str, as_input=False):
    output = f'{Fore.GREEN}[OK]{Style.RESET_ALL} {str}'
    if as_input:
        input(output)
    else:
        print(output)

def warning(str, as_input=False):
    output = f'{Fore.YELLOW}[!]{Style.RESET_ALL} {str}'
    if as_input:
        input(output)
    else:
        print(output)

def error(str, e='', as_input=False):
    output = f'{Fore.RED}[ERROR]{Style.RESET_ALL} {str}: {e}'
    if as_input:
        input(output)
    else:
        print(output)

##########################################

def parse_whitelist():
    global whitelist

    # check if whitelist exists else create and write first line
    if not os.path.exists('whitelist.txt'):
        warning('Whitelist not found, creating...')

        with open('whitelist.txt', 'w+') as f:
            f.write('!! PROVIDE USERNAMES OR IDs IN SEPARATE LINES !!')

    # check if provided users are IDs else inform and exit
    else:
        with open('whitelist.txt', 'r') as f:
            lines = f.read().splitlines()
            if len(lines) > 1:
                del lines[0]
                for line in lines:
                    if not line.isnumeric():
                        try:
                            line = bot.get_user_id_from_username(line)
                        except:
                            return False
                    whitelist.append(line)
                return True

def check_files():
    try:
        bot.check_if_replaced()
        return True
    except:
        return False

print()
if not check_files():
    res = subprocess.run('pip show instabot', stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()
    for line in res:
        if line.split(' ')[0] == 'Location:':
            path = line.split(' ')[1]
            error(f'Make sure you replaced "bot_block.py" & "bot.py" files in {path}', True)
            sys.exit()
    error('Something is wrong with "instabot" library', True)
    sys.exit()

# read the credentials from arguments, if empty ask for them
username = args.username[0] if args.username else input('[>] Username: ')
password = args.password[0] if args.password else getpass('[>] Password: ') # hidden input for password

##########################################

try:
    print()
    bot.login(username=username, password=password)

    if parse_whitelist():
        success('Whitelist correct')
    else:
        error('Error parsing whitelist, make sure IDs and usernames are correct', True)
        sys.exit()

    sleep(1)
    clear()

    if args.list:
        remove_from_list(args.list[0])
    else:
        remove_ghots()

except Exception as e:
    if str(e) == "'ds_user'":
        error('Delete "config" folder and try again')
    else:
        error('Error occured', e)