#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import shogi
from shogi import CSA
import random
import sys
import time


if len(sys.argv) != 4:
    print('Usage: {0} host_name user_name password'.format(sys.argv[0]))
    sys.exit(1)


ct = CSA.TCPProtocol(sys.argv[1], 4081)
ct.login(sys.argv[2], sys.argv[3])
game_summary = ct.wait_match()
sfen = game_summary['summary']['sfen']
my_color = game_summary['my_color']
board = shogi.Board(sfen)
ct.agree()


while True:
    print("\n"*3)
    print("[battle.py]: pc turn")
    moves = []
    for move in board.legal_moves:
        moves.append(move)

    if len(moves) == 0:
        ct.resign()
        break

    next_move = random.choice(moves)
    board.push(next_move)
    print(board.kif_str())
    print('[battle.py]: pc turn end. and waiting Player')
    recieved_cmd = ct.move(board.pieces[next_move.to_square], my_color, next_move)
    
    print("\n"*3)
    print('[battle.py]: Player moved')
    #相手ターンの処理
    (_, usi, spend_time, message) = ct.parse_server_message(recieved_cmd, board)
    move = shogi.Move.from_usi(usi)
    board.push(move)
    print(board.kif_str())
    print('[battle.py]: Player moving handle end. and now pc turn')


