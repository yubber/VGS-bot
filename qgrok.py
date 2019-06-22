import template as t

t.main(
    t.login('grohk'),     # r
    'grohk',              # qui
    'test',               # sub
    t.misspellchk,        # fun
    t.defaultfooter,      # footer
    {"grohk_cash":00.00}, # jsonbackup, misc
    r"(?i)\b(?:ghroc?k|grog?c?k|grochk|grokh|ghroh?c|grog?hc|groghk|grhock|grhoc?k?|groh?nh?k?c?)\b",
    "grohk"
)