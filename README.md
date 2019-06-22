# VGS-bot
posts a vgs comms command link every time sb's comment in r/paladins contains one

/u/REEvie_bot comments VGS messages with a link to the corresponding evie voiceline. it only searches r/paladins and doesn't check posts unless you comment on the post with reevie - then it will check the post body (not title).

huge thanks to /u/DevilXD for helping with the regex, datetime and dataIO module. basically the entire bot lol.

*something something JusticeForCelerity*

**the about on /u/yubbber's profile page is now outdated and archived.**
you can find more old files [here](https://repl.it/@yubber1337/REEVIE)

i run the bot on my computer, not on a server i pay to host the bot, so it runs every ~12h.
you're more than welcome to copy/adapt the code to host it yourself, just lmk and link here on your project.

## what does this bot do?
> REEvie responds to comments containing VGS commands with a link to Evie's voiceline for it and what the voiceline means (well, most of the time)

> QuarterMaeveBot is similar to WilloQuarterBot. it corrects maeve misspells and thanks others for doing its job. it does not correct "gurk" since it's the name of the spray and i don't want my sweet summer child to get wooshed.

> QuarterGrohkBot is QMB but for grohk.

all bots are run from the same reddit account due to reddit's ratelimit on new accounts.

### files
voicegetter.js is for you to copy and paste into the developer console on any paladins wiki voiceline page. it'll copy a list of all the relevant urls. you'll have to get the joke voicelines and VVGM yourself as they're not in table cells though. **WILL BREAK IF WIKI CHANGES LAYOUT DRAMATICALLY**

making a file that replaces the old links in the dict is on my to-do, but i haven't made any work on it yet.

### changes to bot

due to people complaining about the bot getting annoying and spammy, i'll limit the replies to comments that mention /u/REEvie_bot or contain the string "reevie" (case insensitive).

if your comment contains the word reevie the bot will search your comment for vgs commands. if there aren't any in your comment it searches the parent comment (maybe you don't know what someone was meaning by the vgs and want to check) and replies to yours if it finds vgs.

## about the code restructure

i made the template.py file allow you to only have to design a function that returns a string which will be used for reply. this made the other files dramatically shorter due to removing duplicate code. however, me being the potato that i am, i forgot to reset the reply string after every comment, which led to a disaster in r/test. it's been cleaned up though.

### about the maeve quarter function
i originally created an alt account (/u/maevequarterbot) for this, but due to frequent rate limits i've used the REEvie account instead. ~~in the spirit of sticking with /u/willoquarterbot's design i chose not to leave a footer on the maeve comments.~~ i'll leave important footers here, but i'll probably leave out the "i'm a bot, here's my about" kind of footer.

### about the grohk quarter function
i just copied maevequarter's code and replaced the regex lol

there's been an error with the regex on the first run though, so i've confiscated the bot's illegally obtained hypothetical money. sorey

##### for the people who had to put up with my potato on r/test
context: on 22/6/2019 i did a test run of restructured code on r/test. the bot replied to every comment with the saved someone a quarter message, which should only appear on "grohk not grokh" or "maeve not meave" comments.

the old was supposed to be displayed in the footer but i messed up the param and initial string for str.split() so it didn't show. the reason why it spammed everyone is because i forgot to set the reply variable to an empty string and the bot comments if the string is nonempty.
