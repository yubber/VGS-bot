import template as t

t.main(
    t.login('maeve'),
    'maeve',
    'test',
    t.misspellchk,
    t.defaultfooter,
    {"maeve_cash":00.00},
    r"(?i)(?:me?ai?y?u?ve|mayve?)",
    "maeve"
)