from random import randint
from ezfsm import *
tfs = [
    ["yyj", "zhx", lambda: randint(1, 10) % 2 == 0, lambda: print("YYJ-->ZHX")],
    ["zhx", "yyj", lambda: randint(1, 10) % 2 == 0, lambda: print("<--")],
    ["zhx", "O", lambda: 1, lambda: ...]
]
sm = SM(tfs)
sm.Build()
while not sm.IsFinish():
    sm.Execute()

sm.StateGraph().view()