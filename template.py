import praw; import secret
def login(who): # create reddit instance
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

footer = ""
# "\n\n ^^^i'm ^^^working ^^^to ^^^improve ^^^this ^^^bot. ^^^please ^^^participate ^^^in [^^^this ^^^survey!](http://poal.me/3flzg9)"