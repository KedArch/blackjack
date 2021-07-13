#!/usr/bin/env python3
import os
import random
if os.name != "nt":
    import readline


def ai_behavior(deck: list, aideck: list):
    suma = 0
    a = False
    for i in aideck:
        suma += min(i, 10)
        if i == 1:
            a = True
    if a and suma + 10 <= 21:
        suma += 10
    while suma <= 16:
        x = random.choice(deck)
        aideck.append(x)
        deck.remove(x)
        suma += min(x, 10)
        if i == 1:
            a = True
        if a and suma + 10 <= 21:
            suma += 10
        elif a and suma > 21:
            suma -= 10
    return aideck, deck, suma


def reset(ai: int, players: int):
    deck = []
    for i in range(12):
        deck += [i+1]*4
    random.shuffle(deck)
    for i in range(ai):
        playing[f"AI{i+1}"] = []
    for i in range(players):
        playing[f"Player{i+1}"] = []
    playing["Dealer"] = []
    return deck, playing


def print_deal(playing: dict, dturn: bool):
    sums = {}
    for p in playing:
        suma = 0
        a = False
        for i in playing[p]:
            suma += min(i, 10)
            if i == 1:
                a = True
        if a and suma + 10 <= 21:
            suma += 10
        if p == "Dealer":
            color = "\033[38;2;0;0;255m\033[48;2;255;255;255m"
        elif "AI" in p:
            color = "\033[38;2;255;0;0m"
        elif "Player" in p:
            color = "\033[38;2;0;255;0m"
        print(f"{color}{p}: ", end="")
        for i, v in enumerate(playing[p]):
            if not dturn and i == 1 and p == "Dealer":
                print("X ", end="")
                break
            if v == 1:
                print("A ", end="")
            elif v == 11:
                print("J ", end="")
            elif v == 12:
                print("Q ", end="")
            elif v == 13:
                print("K ", end="")
            else:
                print(f"{v} ", end="")
        if (dturn and p == "Dealer") or p != "Dealer":
            print(f"Sum: {suma}", end="")
        print("\033[m")
        sums[p] = suma
    return sums


players = 0
ai = None
playing = {}

inp = ""
while inp != "e":
    switch = True
    if not players:
        print("Give player amount")
    elif ai is None:
        print("Give AI amount")
    inp = input(">")
    if not players:
        try:
            switch = False
            players = int(inp)
            if not (0 < players <= 6):
                raise ValueError
            print(f"Players: {players}")
            if players == 6:
                switch = True
        except ValueError:
            print("Invalid player amount. Should be in <1;6>")
            players = 0
            continue
    if ai is None and players < 6 and switch:
        try:
            ai = int(inp)
            if not (0 <= ai <= 6-players) or (ai == 0 and players == 1):
                raise ValueError
            print(f"AI: {ai}")
        except ValueError:
            print("Invalid AI amount. Should be in "
                  f"<{0 if players > 1 else 1};{6-players}> ")
            ai = None
            continue
    if not playing and switch:
        if ai is None:
            ai = 0
        deck, playing = reset(ai, players)
        break

inp = ""
while inp != "e":
    print("#Deal")
    deck, playing = reset(ai, players)
    for p in playing:
        x = random.choice(deck)
        playing[p].append(x)
        deck.remove(x)
        y = random.choice(deck)
        playing[p].append(y)
        deck.remove(y)
    dturn = False

    for p in playing:
        sums = print_deal(playing, dturn)
        print(f"#{p} turn")
        if "AI" in p or p == "Dealer":
            playing[p], deck, suma = ai_behavior(deck, playing[p])
        elif "Player" in p:
            while True:
                inp = input(f"{p}>")
                if inp in ("e", "s"):
                    break
                elif inp == "h":
                    a = False
                    for i in playing[p]:
                        if i == 1:
                            a = True
                    x = random.choice(deck)
                    playing[p].append(x)
                    deck.remove(x)
                    suma += min(x, 10)
                    if x == 1:
                        a = True
                    if a and suma + 10 <= 21:
                        suma += 10
                    elif a and suma > 21:
                        suma -= 10
                    if suma > 21:
                        inp = "s"
                        break
                    else:
                        sums = print_deal(playing, dturn)
            if inp == "e":
                break
    dturn = True
    sums = print_deal(playing, dturn)
    win = 0
    winner = []
    for p in sums:
        if win == sums[p]:
            winner.append(p)
        if win < sums[p] <= 21:
            win = sums[p]
            winner = [p]
    if len(winner) == 0:
        print("Winner: Dealer")
    elif len(winner) == 1:
        print(f"Winner: {winner[0]}")
    else:
        print("Draw")
    input("Press enter to start new Deal...")
