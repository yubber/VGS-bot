import praw
import secret
import re
import template as temp
from dataIO import dataIO

if dataIO.is_valid_json("settings.json"):
   settings = dataIO.load_json("settings.json")
   print("loaded json")
else:
   settings = {"maeve_cash":00.00}
   print("couldn't load json")

footer = temp.footer # this is for any announcements, etc

# scoping smh my head

pattern = re.compile(r"(?i)maeve,? ?not,? ?(?:\"|\'|) ?(?:me?ai?y?u?ve|mayve?) ?(?:\"|\'|)")
misspell = re.compile(r"(?i)(?:me?ai?y?u?ve|mayve?)")

def lobot(r,sub):
    nothings = 0
    monies = settings["maeve_cash"]
    last_run = settings.get("maeve_last_run")
    print("now at ${}, last run was {} \n \n \n".format(monies,last_run))
    for comment in r.subreddit(sub).comments(limit=9999):
        # somehow comment.author.name isn't working
        if str(comment.author) == "REEvie_bot":
            continue # skip this iteration and move on to next comment

        # skip comments created before the most recent comment from the last run (prevents from replying twice to the same comment)
        if last_run: # can be None if the settings file didn't exist or got corrupted
            if comment.created_utc <= last_run:
               print(str(comment) + " was already replied to, breaking loop.")
               break

        if pattern.search(comment.body): # search for people correctiong others' spelling
                comment.reply("Thank you! You've saved someone a quarter.")
                print("thanked "+str(comment))
        elif misspell.search(comment.body): # search for a misspell
            monies += 0.25
            comment.reply("If I had a quarter for every time someone misspelled Maeve, I would have $"+(str(monies) if str(monies)[-3] == "." else str(monies)+"0")+"."+footer)
            print("fined "+str(comment))
        else:
            nothings += 1

    newest_comment = next(r.subreddit(sub).comments(limit=1)) # get the most recent comment
    settings["maeve_last_run"] = newest_comment.created_utc # store the creation time of it as Unix timestamp
    # print(settings)
    settings["maeve_cash"] = monies # save current amount of hypothetical quarters
    dataIO.save_json("settings.json", settings) # save to file
    print("oof: {} comments with nothing \n \n \n".format(nothings))

print("running bot...")
r = temp.login("maevie")
lobot(r,"paladins")
print("oof")