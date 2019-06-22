import vgsrc, re, template as t

def kek(comment,misc):

    def makereply(sayer):
        nonlocal tempreply
        for word in comment_words: # for each word in a comment
            match = pattern.search(word) # try to match it with the filter pattern
            if match: # if there is a match
                command = match.group(0) # extract what the command was
                voiceline = commands.get(command) # use it to look up the tuple containing the command's text (T) and voice line link (V)
                if command is None:
                    continue # if VGS key can't be found, move on to next word
                tempreply += ">{} (Evie): [[{}] {}]({}) \n \n".format(sayer, command, *voiceline) # * unpacks tuple and puts all its elements into format()

    tempreply = ''
    commands = vgsrc.poorlynamedvariable
    pattern = re.compile(r"(?i)\b(?:{})\b".format("|".join(list(commands.keys())))) # pattern for searching commands
    tagcheck = re.compile(r"(?i)reevie")

    if bool(tagcheck.search(comment.body)) == False: # only check comments that mention the bot
        return ''

    comment_words = re.compile(r"\b").split(comment.body.upper()) # get a list of words used
    makereply(str(comment.author)) # generate response

    if tempreply == '': # if nothing (but we're still tagged) try to find cmds in parent
        if hasattr(comment.parent(),'body'):
            parentbody = comment.parent().body # if the parent is a comment get its body
        elif hasattr(comment.parent(),'selftext'):
            parentbody = comment.parent().selftext # if it's a post get its content (selftext)
        else:
            print(str(comment)+" parent invalid.")

        if str(comment.parent().author) != "REEvie_bot": # if the parent isn't a selfreply
            comment_words = re.compile(r"\b").split(parentbody.upper()) # split the parent body
            makereply(str(comment.parent().author)) # find tags in the parent

    return tempreply

reefooter = " ^^^^^^^^^".join("\n\n\n i'm a bot! check [this post](https://www.reddit.com/user/yubbber/comments/a8q81v/about_ureevie_bot/) for info.".split(" "))

t.main(t.login('reevie'), 'reevie','test', kek, t.defaultfooter + reefooter)