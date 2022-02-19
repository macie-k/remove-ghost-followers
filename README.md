# May not work
Instagram is constantly making it harder to create any kind of bots, the [instabot](https://github.com/ohld/igbot) API used in this script is not being maintained anymore.  
And I keep getting issues about the `4xx` errors, meaning there is no guarantee this script will work.

<br>

---
---

<br>

# Remove all ghost followers from instagram
Finds and removes everyone who hasn't interacted with the last 100 of your posts

<br>

## Download
Download the latest release [here](http://bit.ly/remove-ghosts-releases)  

<br>

## Preview
![preview](https://user-images.githubusercontent.com/25122875/124366716-fcff8d00-dc51-11eb-8183-e4a7c356776e.png)


<br>

## How to
1. If you're on windows download the the ready to use `.exe` from [here](http://bit.ly/remove-ghosts-releases) or
2. Install [instabot](https://github.com/ohld/igbot) using: `pip install instabot`
3. Locate the package using `pip show instabot` and navigate to the given path
4. Copy files from `to_replace` folder to the opened instabot location and replace the originals
5. Launch the script: `python remove_ghosts.py`

<br>

## Whitelist
- Every username or user ID in the `whitelist.txt` file will be ignored

<br>

## Removing from list
- If you happen to have a list of usernames you want to remove you can use the `--list` or `-l` argument and provide the filename
- Like `python remove_ghosts.py --list yourfilename.txt`

<br>

## Sidenotes
- If you receive a `403` error, you have to wait ~1h before continuing
