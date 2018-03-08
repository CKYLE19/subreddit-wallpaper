#!/usr/local/env python

import subprocess
import os
import urllib
from sys import platform

WALLPAPER_SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "{filename}"
end tell
END"""

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

if platform == "darwin":
	TMP_FILE_LOCATION = "/tmp/subreddit_wallpaper"
elif platform == "win32":
	TMP_FILE_LOCATION = "{}/tmp/subreddit_wallpaper".format(CURRENT_DIR)
else:
	raise Exception("Unsupported OS.")

if __name__ == "__main__":
	index = 0
	old_img = ""
	with open("{}/metadata.txt".format(TMP_FILE_LOCATION), "r") as idx_file:
		index = int(idx_file.readline())
		old_img = idx_file.readline()
	idx_file.close()

	if os.path.isfile("{}/{}".format(TMP_FILE_LOCATION, old_img)):
		os.remove("{}/{}".format(TMP_FILE_LOCATION, old_img))

	images = open("{}/images.txt".format(TMP_FILE_LOCATION)).read().splitlines()
	img_url = images[index]
	img_name = "{}.png".format(img_url.split(".")[-2].split("/")[-1])

	urllib.urlretrieve(img_url, "{}/{}".format(TMP_FILE_LOCATION, img_name))

	subprocess.Popen(WALLPAPER_SCRIPT.format(filename="{}/{}".format(TMP_FILE_LOCATION, img_name)), shell=True)

	if index+1 == len(images):
		index = 0
	else:
		index += 1

	with open("{}/metadata.txt".format(TMP_FILE_LOCATION), "w") as idx_file:
		idx_file.write("{}\n".format(str(index)))
		idx_file.write(img_name)
	idx_file.close()
