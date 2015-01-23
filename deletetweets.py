#!/usr/bin/env python

import argparse
import csv
import twitter
import time
import sys
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "0.1"

API_KEY = ""
API_SECRET = ""

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

def delete(api, dateBefore, dateAfter, r, w, f):
  with open("tweets.csv") as file:
    n = 0

    for row in csv.DictReader(file):
      tweetId = int(row["tweet_id"])
      tweetDate = parse(row["timestamp"], ignoretz=True).date()
      tweetText = row["text"]

      if dateBefore != "" and tweetDate > parse(dateBefore).date(): continue
      if dateAfter != "" and tweetDate < parse(dateAfter).date(): continue

      if (r == "retweet" and row["retweeted_status_id"] == ""
        or r == "reply" and row["in_reply_to_status_id"] == ""): continue

      if w not in tweetText: continue

      try:
        # print "Deleting tweet #{0} ({1})".format(tweetId, tweetDate)
        print "Tweet   #{0} ({1}) {2}".format(tweetId, tweetDate, tweetText)

        # only continue if force is true
        if (f != "true" ): continue;

        status = api.DestroyStatus(tweetId)
        print "Deleted #{0} ({1}) {2}".format(tweetId, tweetDate, tweetText)

        n += 1
        time.sleep(0.5)

      except Exception, e:
        print "Exception: %s\n" % e.message

  print "Number of deleted tweets: %s\n" % n

def error(msg, ec = 1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(ec)

def main():
  parser = argparse.ArgumentParser(description="Delete old tweets.")
  parser.add_argument("-db", dest="dateBefore", required=True, help="Delete tweets before this date")
  parser.add_argument("-da", dest="dateAfter", required=True, help="Delete tweets after this date")
  parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"], help="Restrict to either replies or retweets")
  parser.add_argument("-w", dest="keyword", help="Restrict to a keyword in tweet text")
  parser.add_argument("-f", dest="force", choices=["true", "false"], help="Actually delete")

  args = parser.parse_args()

  if API_KEY == "" or API_SECRET =="":
    error("No API key and/or secret set.")

  if ACCESS_TOKEN == "" or ACCESS_TOKEN_SECRET =="":
    error("No access token and/or secret set.")

  api = twitter.Api(consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token_key=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET)

  delete(api, args.dateBefore, args.dateAfter, args.restrict, args.keyword, args.force)

if __name__ == "__main__":
  main()
