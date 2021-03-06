from glob import glob
from sys import argv
from os import chdir, mkdir
from pathlib import Path
from instaloader import Instaloader, Post, Profile, load_structure_from_file

L = Instaloader()

try:
    TARGET = argv[1]
except IndexError:
    raise SystemExit("Pass profile name as argument.")

# Check to see if directory exists for TARGET
if Path(TARGET).is_dir() == False:
    mkdir(TARGET)

chdir(TARGET)

# Check to see if history file exists for TARGET
if Path(f"{TARGET}deletionhistory.txt").is_file() == False:
    file = open(f"{TARGET}deletionhistory.txt", "w")

# Obtain set of posts on HD
offline_posts = set(filter(lambda s: isinstance(s, Post),
                           (load_structure_from_file(L.context, file)
                            for file in (glob('*.json.xz') + glob('*.json')))))
# Obtain set of posts that are currently online
post_iterator = Profile.from_username(L.context, TARGET).get_posts()
online_posts = set(post_iterator)

#List new posts if any
if online_posts - offline_posts:
    print("New posts:")
    print(" ".join(str(p) for p in (online_posts - offline_posts)))

# Write list of deleted posts if any to history file
if offline_posts - online_posts:
    file.write("Deleted posts:")
    file.write(" ".join(str(p) for p in (offline_posts - online_posts)))
    
# Download new posts:
for post in Profile.from_username(L.context, TARGET).get_posts():
    L.download_post(post, TARGET)
