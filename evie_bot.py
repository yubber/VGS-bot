import praw
import secret
import vgsrc
import re
import template as temp
# from datetime import datetime
from dataIO import dataIO

# reddit bot tutorial
# https://www.reddit.com/r/learnprogramming/comments/5us049/heres_a_tutorial_i_made_on_creating_a_reddit_bot/

# load settings from the settings file
if dataIO.is_valid_json("settings.json"):
   settings = dataIO.load_json("settings.json")
else:
   settings = {}

commands = vgsrc.poorlynamedvariable
pattern = re.compile(r"(?i)\b(?:{})\b".format("|".join(list(commands.keys()))))
tagcheck = re.compile(r"(?i)reevie")

footer = temp.footer

# print(pattern)

def loboto(r,sub):
    nothings = 0 # for debug
    tags = 0
    last_run = settings.get("reevie_last_run")
    for comment in r.subreddit(sub).comments(limit=7999): # change to 9999 later
        
        if str(comment.author) == "REEvie_bot": # prevents self reply
            continue # skip this iteration and move on to next comment
        
        # skip comments created before the most recent comment from the last run (prevents from replying twice to the same comment)
        if last_run: # can be None if the settings file didn't exist or got corrupted
           if comment.created_utc <= last_run:
               print(str(comment) + " was already replied to, breaking loop. \n");break
        
        # print("evaluating "+str(comment))
        
        if bool(tagcheck.search(comment.body)) == False: # only check comments that mention the bot
            nothings += 1; continue
        
        reply = "" # for each comment, start with an empty reply
        
        comment_words = re.compile(r"\b").split(comment.body.upper()) # get a list of words used
        for word in comment_words: # for each word in a comment
            match = pattern.search(word) # try to match it with the filter pattern 
            if match: # if there is a match
                command = match.group(0) # extract what the command was 
                voiceline = commands.get(command) # use it to look up the tuple containing the command's text (T) and voice line link (V)
                if command is None: 
                    print("couldn't find vgs key"); continue # if VGS key can't be found, move on to next word
                reply += ">{} (Evie): [[{}] {}]({}) \n \n".format(comment.author.name, command, *voiceline) # * unpacks tuple and puts all its elements into format()
        if len(reply) > 0 :# check if the length of the reply is more than 0 - if yes, that means we have something to reply with 
            reply += "\n\n ^^^^^^^^^^^^^i'm ^^^^^^^^^^^^^a ^^^^^^^^^^^^^bot! ^^^^^^^^^^^^^check [^^^^^^^^^^^^^this ^^^^^^^^^^^^^post](https://www.reddit.com/user/yubbber/comments/a8q81v/about_ureevie_bot/) ^^^^^^^^^^^^^for ^^^^^^^^^^^^^info."
            comment.reply(reply) # reply! \o/\o/ (above line is reply footer)
            print("replied to " + comment.body)
        else: # if the comment only has the tag but not vgs, check parent
            if hasattr(comment.parent(),'body'): 
                parentbody = comment.parent().body # if the parent is a comment get its body
            elif hasattr(comment.parent(),'selftext'):
                parentbody = comment.parent().selftext # if it's a post get its content (selftext)
            else:
                print(str(comment)+" parent invalid.")

            if str(comment.parent().author) != "REEvie_bot":
                comment_words = re.compile(r"\b").split(parentbody.upper()) # split the parent body 
                for word in comment_words:
                    match = pattern.search(word) # try to match it with the filter pattern
                    if match: # if we were successful
                        # for i in range(pattern.groups): # uncomment this line for comparing pattern to entire comment body
                        command = match.group(0) # extract what the command was - if above line used, replace 0 with i
                        voiceline = commands.get(command) # use it to look up the tuple containing the command's text (T) and voice line link (V)
                        if command is None:
                            print("couldn't find vgs key")
                            continue # if VGS key can't be found, move on to next word
                        reply += ">{} (Evie): [[{}] {}]({}) \n \n".format(comment.parent().author.name, command, *voiceline) # * unpacks tuple and puts all its elements into format()
                if len(reply) > 0 :# check if the length of the reply is more than 0 - if yes, that means we have something to reply with 
                    reply += "\n\n ^^^^^^^^^^^^^i'm ^^^^^^^^^^^^^a ^^^^^^^^^^^^^bot! ^^^^^^^^^^^^^check [^^^^^^^^^^^^^this ^^^^^^^^^^^^^post](https://www.reddit.com/user/yubbber/comments/a8q81v/about_ureevie_bot/) ^^^^^^^^^^^^^for ^^^^^^^^^^^^^info. \n \n" + footer
                    comment.reply(reply) # reply! \o/\o/
                    print("tag replied to " + parentbody) 
                    tags += 1
                else:
                    nothings += 1
            # print("nothing in "+str(comment)+reply)
    
    # print(settings)
    newest_comment = next(r.subreddit(sub).comments(limit=1)) # get the most recent comment
    settings["reevie_last_run"] = newest_comment.created_utc # store the creation time of it as Unix timestamp
    dataIO.save_json("settings.json", settings) # save to file
    print("oof: {} comments with nothing \n \n \n".format(nothings))

print("running bot...")
r = temp.login("reevie")
loboto(r,"paladins")