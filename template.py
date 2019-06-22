import importlib, praw, re

defaultfooter = " ^^^^^^^^^^^".join("i'm restructuring the code to make it more compact. if you run into any errors please let /u/yubbber know".split(" ") )

def login(who): # create reddit instance
    import secret
    print("fbi open up")
    r = praw.Reddit(
        username = secret.ev_username,
        password = secret.password,
        client_id = secret.ev_client_id,
        client_secret = secret.ev_client_secret,
        user_agent = "/u/yubbber's evie bot"
    )
    print(who + " logged in \n")
    return r

def misspellchk(comment, misc):
    '''
    inbuilt function for WQB-style misspell bots. use as main's filterfun param.
    remember to put cash in jsonbackup

    Args (in sequence, passed by misc)

    wrong - the expression used to check for misspells. provide as string, not compiled!
    right - the correct spelling
    '''

    misspell = re.compile(misc[0])
    correct = re.compile(fr"(?i){misc[1]},? ?not,? ?(?:\"|\'|) ?{misc[0]} ?(?:\"|\'|)")

    monies = main.settings[f"{misc[1]}_cash"]

    if correct.search(comment.body): # search for people correctiong others' spelling
        print("thanked "+str(comment))
        return "Thank you! You've saved someone a quarter."
    elif misspell.search(comment.body) and misc[1] not in comment.body.lower(): # search for a misspell and make sure it wasn't a fat finger
        print("fined "+str(comment)); monies += 0.25
        return f"If I had a quarter for every time someone misspelled {misc[1].title()}, I would have ${str(monies) if str(monies)[-3] == '.' else str(monies)+'0'}."+footer
    main.settings[f"{misc[1]}_cash"] = monies
    return ''


def main(r,qui,sub,filterfun,footer=defaultfooter,jsonbackup={}, *misc):
    '''
    template function for comment checking and looping.

    iterates through last 7999 comments of sub. if their author is not reevie_bot and was made after last run, call fun and add returned value to reply, then reply if reply is not empty

    Args

    r - val from login()
    qui - str (reevie, maeve, grohk)
    sub - which subreddit to run the bot in
    fun - function for bot logic. must return string, which will be added to reply (no reply if end up empty)

    Kwargs

    footer - text to put at the bottom of the comment. value of template.defaultfooter by default
    jsonbackup - dict to replace json when it's unloadable. {} by default.
    misc - additional args.
    '''

    import praw; from dataIO import dataIO

    # defaults = 'praw dataIO'.split(" ") # the prereqs we need for every bot
    # rd = {} # requisite dictionary
    # for i in defaults:
    #     rd[i] = importlib.import_module(i) # import every module we need
    # # if using reqdict replace module names with rd['modulename']

    login(qui) # log us in

    if dataIO.is_valid_json("settings.json"): # check file integrity then load it
        main.settings = dataIO.load_json("settings.json")
        print("loaded json")
    else:
        main.settings = jsonbackup # use our backup dict if our file is fucked
        print("couldn't load json")

    # init
    nothings = 0
    reply = ''

    # main
    main.last_run = main.settings.get("{}_last_run".format(qui))
    for comment in r.subreddit(sub).comments(limit=7999): # change to 9999 later

        reply = ''

        if str(comment.author) == "REEvie_bot": # prevents self reply
            continue # skip this iteration and move on to next comment

        # skip comments created before the most recent comment from the last run (prevents from replying twice to the same comment)
        if main.last_run: # can be None if the settings file didn't exist or got corrupted
           if comment.created_utc <= main.last_run:
               print(str(comment) + " was already replied to, breaking loop. \n");break

        reply = filterfun(comment, misc)

        if reply: # reply only if str is nonempty
            comment.reply(reply+footer)
        else:
            nothings += 1

    newest_comment = next(r.subreddit(sub).comments(limit=1)) # get the most recent comment
    main.settings["{}_last_run".format(qui)] = newest_comment.created_utc # store the creation time of it as Unix timestamp
    dataIO.save_json("settings.json", main.settings) # save to file
    print("oof: {} comments with nothing \n \n \n".format(nothings))

footer = ""
# "\n\n ^^^i'm ^^^working ^^^to ^^^improve ^^^this ^^^bot. ^^^please ^^^participate ^^^in [^^^this ^^^survey!](http://poal.me/3flzg9)"