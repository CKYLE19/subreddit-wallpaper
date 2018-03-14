import urllib2
import json
import os
import argparse
import subprocess
import shutil
from sys import platform

# CONSTANTS
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SET_WALLPAPER_CMD = """python {}/set_wallpaper.py""".format(CURRENT_DIR)

# ADJUST FOR SPECIFIC PLATFORM
if platform == "darwin":
	TMP_FILE_LOCATION = "/tmp/subreddit_wallpaper"
elif platform == "win32":
	TMP_FILE_LOCATION = "{}/tmp/subreddit_wallpaper".format(CURRENT_DIR)
else:
	raise Exception("Unsupported OS.")

def create_cron_job():
	cron_file = "{}/cronjob.txt".format(CURRENT_DIR)
	with open(cron_file, "w") as file:
		file.write("{}\n".format("*/1 * * * * python {}/set_wallpaper.py".format(CURRENT_DIR)))
		file.write("{}\n".format("0 1 * * * python {}/main.py".format(CURRENT_DIR)))
	file.close()
	subprocess.Popen("crontab {}".format(cron_file), shell=True)

def clear_tmp_dir():
	if os.path.isdir(TMP_FILE_LOCATION):
		shutil.rmtree(TMP_FILE_LOCATION)
	os.makedirs(TMP_FILE_LOCATION)

def download_subreddit(sub_name):
	endpoint = "https://www.reddit.com/r/{}.json".format(sub_name)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(endpoint)
	data = json.load(response)

	images = [x["data"]["url"] for x in data["data"]["children"] if "preview" in x["data"] and "images" in x["data"]["preview"] and x["data"]["preview"]["images"][0]["source"]["width"] >= x["data"]["preview"]["images"][0]["source"]["height"]]

	with open("{}/images.txt".format(TMP_FILE_LOCATION), 'w') as file:
		for image in images:
			file.write("{}\n".format(image))
	file.close()

	with open("{}/metadata.txt".format(TMP_FILE_LOCATION), 'w') as file:
		file.write("0\n")
		file.write("{}".format(images[0]))
	file.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Get wallpapers from the web')
	parser.add_argument('--subreddit', type=str, help="Enter a subreddit to parse", required=True)
	args = parser.parse_args()
	clear_tmp_dir()
	download_subreddit(args.subreddit)
	subprocess.Popen(SET_WALLPAPER_CMD, shell=True)
	create_cron_job()