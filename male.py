# -*- coding: utf-8 -*-

import pygame
import sys
import os
import threading
import math

BG           = (18, 18, 18)
LIGHT_SQ     = (240, 217, 181)
DARK_SQ      = (181, 136,  99)
HIGHLIGHT    = (205, 210,  60, 160)
LAST_MOVE    = (170, 162,  58, 130)
CHECK_CLR    = (220,  50,  50, 160)
PANEL_BG     = (28,  22,  18)
GOLD         = (200, 151,  58)
GOLD2        = (240, 201, 107)
WHITE_CLR    = (240, 232, 214)
DIM          = (120, 104,  80)
GREEN        = ( 46, 204, 113)
RED          = (231,  76,  60)
WOOD         = ( 60,  35,  10)
UNDO_CLR     = (130, 100,  45)
UNDO_HOVER   = (170, 135,  65)
ARROW_CLR    = (255, 170,  30, 190)

SQ  = 80
OFF = 40
PANEL_X = OFF + 8*SQ + 20
PANEL_W = 240
W = PANEL_X + PANEL_W + 16
H = OFF + 8*SQ + OFF

UNDO_BTN = pygame.Rect(PANEL_X + 12, H - 52, PANEL_W - 24, 34)

PIECES_DIR = "pieces"

PIECE_FILES = {
    'wK': 'kunn v.webp',
    'bK': 'kunn.png',
    'wQ': 'queen v.png',
    'bQ': 'quees.png',
    'wR': 'rook v.png',
    'bR': 'rook.png',
    'wB': 'bishop v.png',
    'bB': 'bishop.png',
    'wN': 'horse v.png',
    'bN': 'horse.png',
    'wP': 'pawn v.png',
    'bP': 'pawn.png',
}

def load_pieces():
    pieces = {}
    for key, filename in PIECE_FILES.items():
        path = os.path.join(PIECES_DIR, filename)
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (SQ - 8, SQ - 8))
                pieces[key] = img
            except Exception as e:
                print(f"Viga pildi laadimisel {path}: {e}")
                pieces[key] = None
        else:
            print(f"Fail puudub: {path}")
            pieces[key] = None
    return pieces

START = [
    ['bR','bN','bB','bQ','bK','bB','bN','bR'],
    ['bP','bP','bP','bP','bP','bP','bP','bP'],
    [None]*8,
    [None]*8,
    [None]*8,
    [None]*8,
    ['wP','wP','wP','wP','wP','wP','wP','wP'],
    ['wR','wN','wB','wQ','wK','wB','wN','wR'],
]

PIECE_VAL = {'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000}

PST = {
'P': [
  [ 0,  0,  0,  0,  0,  0,  0,  0],
  [50, 50, 50, 50, 50, 50, 50, 50],
  [10, 10, 20, 30, 30, 20, 10, 10],
  [ 5,  5, 10, 25, 25, 10,  5,  5],
  [ 0,  0,  0, 20, 20,  0,  0,  0],
  [ 5, -5,-10,  0,  0,-10, -5,  5],
  [ 5, 10, 10,-20,-20, 10, 10,  5],
  [ 0,  0,  0,  0,  0,  0,  0,  0],
],
'N': [
  [-50,-40,-30,-30,-30,-30,-40,-50],
  [-40,-20,  0,  0,  0,  0,-20,-40],
  [-30,  0, 10, 15, 15, 10,  0,-30],
  [-30,  5, 15, 20, 20, 15,  5,-30],
  [-30,  0, 15, 20, 20, 15,  0,-30],
  [-30,  5, 10, 15, 15, 10,  5,-30],
  [-40,-20,  0,  5,  5,  0,-20,-40],
  [-50,-40,-30,-30,-30,-30,-40,-50],
],
'B': [
  [-20,-10,-10,-10,-10,-10,-10,-20],
  [-10,  0,  0,  0,  0,  0,  0,-10],
  [-10,  0,  5, 10, 10,  5,  0,-10],
  [-10,  5,  5, 10, 10,  5,  5,-10],
  [-10,  0, 10, 10, 10, 10,  0,-10],
  [-10, 10, 10, 10, 10, 10, 10,-10],
  [-10,  5,  0,  0,  0,  0,  5,-10],
  [-20,-10,-10,-10,-10,-10,-10,-20],
],
'R': [
  [ 0,  0,  0,  0,  0,  0,  0,  0],
  [ 5, 10, 10, 10, 10, 10, 10,  5],
  [-5,  0,  0,  0,  0,  0,  0, -5],
  [-5,  0,  0,  0,  0,  0,  0, -5],
  [-5,  0,  0,  0,  0,  0,  0, -5],
  [-5,  0,  0,  0,  0,  0,  0, -5],
  [-5,  0,  0,  0,  0,  0,  0, -5],
  [ 0,  0,  0,  5,  5,  0,  0,  0],
],
'Q': [
  [-20,-10,-10, -5, -5,-10,-10,-20],
  [-10,  0,  0,  0,  0,  0,  0,-10],
  [-10,  0,  5,  5,  5,  5,  0,-10],
  [ -5,  0,  5,  5,  5,  5,  0, -5],
  [  0,  0,  5,  5,  5,  5,  0, -5],
  [-10,  5,  5,  5,  5,  5,  0,-10],
  [-10,  0,  5,  0,  0,  0,  0,-10],
  [-20,-10,-10, -5, -5,-10,-10,-20],
],
'K': [
  [-30,-40,-40,-50,-50,-40,-40,-30],
  [-30,-40,-40,-50,-50,-40,-40,-30],
  [-30,-40,-40,-50,-50,-40,-40,-30],
  [-30,-40,-40,-50,-50,-40,-40,-30],
  [-20,-30,-30,-40,-40,-30,-30,-20],
  [-10,-20,-20,-20,-20,-20,-20,-10],
  [ 20, 20,  0,  0,  0,  0, 20, 20],
  [ 20, 30, 10,  0,  0, 10, 30, 20],
],
}

def pst_val(piece, r, c, color):
    t = piece[1]
    if t not in PST:
        return 0
    table = PST[t]
    return table[r][c] if color == 'w' else table[7-r][c]

def color_of(p):
    return p[0] if p else None

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def pseudo_moves(board, r, c, castling_rights=None, en_passant_sq=None):
    p = board[r][c]
    if not p:
        return []
    col = p[0]
    kind = p[1]
    moves = []

    def add(nr, nc):
        if in_bounds(nr, nc):
            target = board[nr][nc]
            if target is None or color_of(target) != col:
                moves.append((nr, nc))

    def slide(drs):
        for dr, dc in drs:
            nr, nc = r+dr, c+dc
            while in_bounds(nr, nc):
                target = board[nr][nc]
                if target is None:
                    moves.append((nr, nc))
                elif color_of(target) != col:
                    moves.append((nr, nc))
                    break
                else:
                    break
                nr += dr; nc += dc

    if kind == 'P':
        d = -1 if col == 'w' else 1
        start_r = 6 if col == 'w' else 1
        if in_bounds(r+d, c) and board[r+d][c] is None:
            moves.append((r+d, c))
            if r == start_r and board[r+2*d][c] is None:
                moves.append((r+2*d, c))
        for dc in [-1, 1]:
            if in_bounds(r+d, c+dc):
                if board[r+d][c+dc] and color_of(board[r+d][c+dc]) != col:
                    moves.append((r+d, c+dc))
                if en_passant_sq and (r+d, c+dc) == en_passant_sq:
                    moves.append((r+d, c+dc))

    elif kind == 'N':
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            add(r+dr, c+dc)
    elif kind == 'B':
        slide([(-1,-1),(-1,1),(1,-1),(1,1)])
    elif kind == 'R':
        slide([(-1,0),(1,0),(0,-1),(0,1)])
    elif kind == 'Q':
        slide([(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)])
    elif kind == 'K':
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0: continue
                add(r+dr, c+dc)

        if castling_rights:
            if col == 'w' and r == 7 and c == 4:
                if (castling_rights.get('wK') and castling_rights.get('wR_k') and
                        board[7][5] is None and board[7][6] is None and
                        board[7][7] == 'wR'):
                    moves.append((7, 6))
                if (castling_rights.get('wK') and castling_rights.get('wR_q') and
                        board[7][3] is None and board[7][2] is None and board[7][1] is None and
                        board[7][0] == 'wR'):
                    moves.append((7, 2))
            elif col == 'b' and r == 0 and c == 4:
                if (castling_rights.get('bK') and castling_rights.get('bR_k') and
                        board[0][5] is None and board[0][6] is None and
                        board[0][7] == 'bR'):
                    moves.append((0, 6))
                if (castling_rights.get('bK') and castling_rights.get('bR_q') and
                        board[0][3] is None and board[0][2] is None and board[0][1] is None and
                        board[0][0] == 'bR'):
                    moves.append((0, 2))

    return moves

def find_king(board, col):
    for r in range(8):
        for c in range(8):
            if board[r][c] == col+'K':
                return r, c
    return None

def is_in_check(board, col, castling_rights=None, en_passant_sq=None):
    kr, kc = find_king(board, col)
    opp = 'b' if col == 'w' else 'w'
    for r in range(8):
        for c in range(8):
            if color_of(board[r][c]) == opp:
                if (kr, kc) in pseudo_moves(board, r, c, None, en_passant_sq):
                    return True
    return False

def apply_move(board, r, c, nr, nc, castling_rights=None, en_passant_sq=None):
    nb = [row[:] for row in board]
    p = nb[r][c]
    new_cr = dict(castling_rights) if castling_rights else {
        'wK': True, 'wR_k': True, 'wR_q': True,
        'bK': True, 'bR_k': True, 'bR_q': True
    }
    new_ep = None

    if p and p[1] == 'K':
        dc = nc - c
        if abs(dc) == 2:
            if dc == 2:
                rook_c = 7
                nb[r][5] = nb[r][rook_c]
                nb[r][rook_c] = None
            else:
                rook_c = 0
                nb[r][3] = nb[r][rook_c]
                nb[r][rook_c] = None

    if p and p[1] == 'P' and en_passant_sq and (nr, nc) == en_passant_sq:
        captured_r = r
        nb[captured_r][nc] = None

    nb[nr][nc] = p
    nb[r][c] = None

    if p and p[1] == 'P':
        if (p[0] == 'w' and nr == 0) or (p[0] == 'b' and nr == 7):
            nb[nr][nc] = p[0] + 'Q'
        if abs(nr - r) == 2:
            new_ep = ((r + nr) // 2, c)

    if p == 'wK': new_cr['wK'] = False
    if p == 'bK': new_cr['bK'] = False
    if p == 'wR' and r == 7 and c == 7: new_cr['wR_k'] = False
    if p == 'wR' and r == 7 and c == 0: new_cr['wR_q'] = False
    if p == 'bR' and r == 0 and c == 7: new_cr['bR_k'] = False
    if p == 'bR' and r == 0 and c == 0: new_cr['bR_q'] = False
    if nr == 7 and nc == 7: new_cr['wR_k'] = False
    if nr == 7 and nc == 0: new_cr['wR_q'] = False
    if nr == 0 and nc == 7: new_cr['bR_k'] = False
    if nr == 0 and nc == 0: new_cr['bR_q'] = False

    return nb, new_cr, new_ep

def legal_moves(board, r, c, castling_rights, en_passant_sq):
    p = board[r][c]
    if not p:
        return []
    col = p[0]
    result = []
    for nr, nc in pseudo_moves(board, r, c, castling_rights, en_passant_sq):
        if p[1] == 'K' and abs(nc - c) == 2:
            if is_in_check(board, col, None, en_passant_sq):
                continue
            mid_c = c + (1 if nc > c else -1)
            nb_mid = [row[:] for row in board]
            nb_mid[r][mid_c] = p
            nb_mid[r][c] = None
            if is_in_check(nb_mid, col, None, en_passant_sq):
                continue
        nb, new_cr, new_ep = apply_move(board, r, c, nr, nc, castling_rights, en_passant_sq)
        if not is_in_check(nb, col, new_cr, new_ep):
            result.append((nr, nc))
    return result

def all_legal_moves(board, col, castling_rights, en_passant_sq):
    moves = []
    for r in range(8):
        for c in range(8):
            if color_of(board[r][c]) == col:
                for nr, nc in legal_moves(board, r, c, castling_rights, en_passant_sq):
                    moves.append((r, c, nr, nc))
    return moves

def is_checkmate(board, col, castling_rights, en_passant_sq):
    return (len(all_legal_moves(board, col, castling_rights, en_passant_sq)) == 0
            and is_in_check(board, col, None, en_passant_sq))

def is_stalemate(board, col, castling_rights, en_passant_sq):
    return (len(all_legal_moves(board, col, castling_rights, en_passant_sq)) == 0
            and not is_in_check(board, col, None, en_passant_sq))

def evaluate(board):
    score = 0
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                val = PIECE_VAL.get(p[1], 0) + pst_val(p, r, c, p[0])
                score += val if p[0] == 'w' else -val
    return score

def minimax(board, depth, alpha, beta, maximizing, castling_rights, en_passant_sq):
    col = 'w' if maximizing else 'b'
    if depth == 0:
        return evaluate(board), None

    moves = all_legal_moves(board, col, castling_rights, en_passant_sq)
    if not moves:
        if is_in_check(board, col, None, en_passant_sq):
            return (-99999 if maximizing else 99999), None
        return 0, None

    best_move = None
    if maximizing:
        best = -float('inf')
        for r,c,nr,nc in moves:
            nb, new_cr, new_ep = apply_move(board, r, c, nr, nc, castling_rights, en_passant_sq)
            score, _ = minimax(nb, depth-1, alpha, beta, False, new_cr, new_ep)
            if score > best:
                best, best_move = score, (r,c,nr,nc)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best, best_move
    else:
        best = float('inf')
        for r,c,nr,nc in moves:
            nb, new_cr, new_ep = apply_move(board, r, c, nr, nc, castling_rights, en_passant_sq)
            score, _ = minimax(nb, depth-1, alpha, beta, True, new_cr, new_ep)
            if score < best:
                best, best_move = score, (r,c,nr,nc)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best, best_move

def sq_to_px(r, c):
    return OFF + c*SQ, OFF + r*SQ

def px_to_sq(x, y):
    c = (x - OFF) // SQ
    r = (y - OFF) // SQ
    if 0 <= r < 8 and 0 <= c < 8:
        return r, c
    return None, None

def col_letter(c):
    return chr(ord('a') + c)

def move_str(r, c, nr, nc, promotion=False, castling=False, en_passant=False):
    if castling:
        return "O-O" if nc == 6 else "O-O-O"
    s = f"{col_letter(c)}{8-r}→{col_letter(nc)}{8-nr}"
    if promotion:
        s += "=Q"
    if en_passant:
        s += " e.p."
    return s

def draw_arrows(screen, arrow_img, arrows, drag_arrow):
    """Joonista kõik salvestatud nooled + aktiivne lohistatav nool."""
    all_arrows = list(arrows)
    if drag_arrow and drag_arrow[0] != drag_arrow[1]:
        all_arrows.append(drag_arrow)

    for (fr, fc), (tr, tc) in all_arrows:
        if (fr, fc) == (tr, tc):
            continue
        # keskpunktid
        x1 = OFF + fc * SQ + SQ // 2
        y1 = OFF + fr * SQ + SQ // 2
        x2 = OFF + tc * SQ + SQ // 2
        y2 = OFF + tr * SQ + SQ // 2

        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            continue
        angle = math.degrees(math.atan2(-dy, dx))

        
        arrow_w = int(length)
        arrow_h = 28
        if arrow_img:
            scaled = pygame.transform.smoothscale(arrow_img, (arrow_w, arrow_h))
            rotated = pygame.transform.rotate(scaled, angle)
        else:
            
            surf = pygame.Surface((arrow_w, arrow_h), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 170, 30, 180), (0, arrow_h//2 - 6, arrow_w, 12))
            rotated = pygame.transform.rotate(surf, angle)

        rx = (x1 + x2) // 2 - rotated.get_width() // 2
        ry = (y1 + y2) // 2 - rotated.get_height() // 2
        screen.blit(rotated, (rx, ry))

def draw_board(screen, pieces, state, arrow_img=None):
    board       = state['board']
    selected    = state['selected']
    legal       = state['legal']
    last_move   = state['last_move']
    check_sq    = state['check_sq']

    for r in range(8):
        for c in range(8):
            x, y = sq_to_px(r, c)
            light = (r+c) % 2 == 0
            pygame.draw.rect(screen, LIGHT_SQ if light else DARK_SQ, (x, y, SQ, SQ))

            if last_move and (r,c) in [(last_move[0],last_move[1]),(last_move[2],last_move[3])]:
                s = pygame.Surface((SQ,SQ), pygame.SRCALPHA)
                s.fill((*LAST_MOVE[:3], 120))
                screen.blit(s, (x,y))

            if check_sq and (r,c) == check_sq:
                s = pygame.Surface((SQ,SQ), pygame.SRCALPHA)
                s.fill((*CHECK_CLR[:3], 160))
                screen.blit(s, (x,y))

            if selected and (r,c) == selected:
                s = pygame.Surface((SQ,SQ), pygame.SRCALPHA)
                s.fill((*HIGHLIGHT[:3], 180))
                screen.blit(s, (x,y))

            if (r,c) in legal:
                s = pygame.Surface((SQ,SQ), pygame.SRCALPHA)
                if board[r][c]:
                    s.fill((200,50,50,100))
                else:
                    pygame.draw.circle(s, (50,50,50,100), (SQ//2,SQ//2), 14)
                screen.blit(s, (x,y))

            ep = state.get('en_passant_sq')
            if ep and (r,c) == ep and (r,c) in legal:
                s = pygame.Surface((SQ,SQ), pygame.SRCALPHA)
                pygame.draw.circle(s, (100,180,100,140), (SQ//2,SQ//2), 14)
                screen.blit(s, (x,y))

    try:
        font_coord_r = pygame.font.SysFont("Courier New", 11)
    except:
        font_coord_r = pygame.font.SysFont(None, 18)

    for i in range(8):
        x0, y0 = sq_to_px(i, 0)
        num = font_coord_r.render(str(8-i), True, DARK_SQ if i%2==0 else LIGHT_SQ)
        screen.blit(num, (x0+3, y0+3))
        x1, y1 = sq_to_px(7, i)
        let = font_coord_r.render(col_letter(i), True, DARK_SQ if (7+i)%2==0 else LIGHT_SQ)
        screen.blit(let, (x1+SQ-14, y1+SQ-16))

    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                x, y = sq_to_px(r, c)
                img = pieces.get(p)
                if img:
                    ix = x + (SQ - img.get_width()) // 2
                    iy = y + (SQ - img.get_height()) // 2
                    screen.blit(img, (ix, iy))
                else:
                    fallback = pygame.font.SysFont("Segoe UI Symbol", 48)
                    UNICODE = {
                        'wK':'♔','wQ':'♕','wR':'♖','wB':'♗','wN':'♘','wP':'♙',
                        'bK':'♚','bQ':'♛','bR':'♜','bB':'♝','bN':'♞','bP':'♟',
                    }
                    ch = UNICODE.get(p, '?')
                    glyph = fallback.render(ch, True,
                        (255,255,255) if p[0]=='w' else (30,30,30))
                    screen.blit(glyph, (x + SQ//2 - glyph.get_width()//2,
                                        y + SQ//2 - glyph.get_height()//2))

    pygame.draw.rect(screen, WOOD, (OFF-2, OFF-2, 8*SQ+4, 8*SQ+4), 3)

    arrows     = state.get('arrows', set())
    drag_arrow = state.get('drag_arrow', None)
    draw_arrows(screen, arrow_img, arrows, drag_arrow)

def draw_undo_button(screen, font_sm, state, mouse_pos):
    can_undo = (not state['over'] and not state['thinking']
                and state['turn'] == 'w' and len(state['undo_stack']) >= 2)

    hovered = UNDO_BTN.collidepoint(mouse_pos) and can_undo
    btn_col = UNDO_HOVER if hovered else UNDO_CLR
    border_col = GOLD if can_undo else (60, 50, 35)
    txt_col = GOLD2 if can_undo else (80, 65, 40)

    pygame.draw.rect(screen, btn_col, UNDO_BTN, border_radius=6)
    pygame.draw.rect(screen, border_col, UNDO_BTN, 1, border_radius=6)

    label = font_sm.render("↩  Võta tagasi", True, txt_col)
    screen.blit(label, label.get_rect(center=UNDO_BTN.center))

def draw_panel(screen, font_sm, font_xs, font_title, state, mouse_pos):
    panel = pygame.Rect(PANEL_X, 0, PANEL_W, H)
    pygame.draw.rect(screen, PANEL_BG, panel)
    pygame.draw.line(screen, WOOD, (PANEL_X, 0), (PANEL_X, H), 2)

    t = font_title.render("MALE", True, GOLD2)
    screen.blit(t, (PANEL_X + PANEL_W//2 - t.get_width()//2, 14))
    sub = font_xs.render("Minimax AI  [R=uus  Q=loobu]", True, DIM)
    screen.blit(sub, (PANEL_X+8, 52))
    pygame.draw.line(screen, WOOD, (PANEL_X+8, 68), (PANEL_X+PANEL_W-8, 68), 1)

    st = state['status']
    col = GREEN if 'võitsid' in st or ('Matt' in st and 'AI' not in st) else \
          RED   if 'AI'      in st or 'kaotasid' in st else GOLD
    stxt = font_sm.render(st, True, col)
    screen.blit(stxt, stxt.get_rect(center=(PANEL_X+PANEL_W//2, 86)))

    if state['thinking']:
        dots = '.' * (pygame.time.get_ticks()//400 % 4)
        th = font_xs.render(f"AI motleb{dots}", True, RED)
        screen.blit(th, th.get_rect(center=(PANEL_X+PANEL_W//2, 104)))

    pygame.draw.line(screen, WOOD, (PANEL_X+8, 116), (PANEL_X+PANEL_W-8, 116), 1)
    wt = font_xs.render("Sina (valge)", True, WHITE_CLR)
    bt = font_xs.render("AI  (must)", True, DIM)
    screen.blit(wt, (PANEL_X+12, 122))
    screen.blit(bt, (PANEL_X+12, 138))

    cr = state['castling_rights']
    cr_txt = "Castle: "
    cr_txt += "O-O " if cr.get('wK') and cr.get('wR_k') else ""
    cr_txt += "O-O-O" if cr.get('wK') and cr.get('wR_q') else ""
    cr_surf = font_xs.render(cr_txt.strip() or "Castle puudub", True, DIM)
    screen.blit(cr_surf, (PANEL_X+12, 152))

    pygame.draw.line(screen, WOOD, (PANEL_X+8, 168), (PANEL_X+PANEL_W-8, 168), 1)
    ht = font_xs.render("KÄIKUDE AJALUGU", True, DIM)
    screen.blit(ht, (PANEL_X+8, 173))

    history = state['history']
    scroll  = state['scroll']
    entry_h = 20
    # space undo buttonile
    clip = pygame.Rect(PANEL_X+4, 190, PANEL_W-8, H - 200 - 60)
    screen.set_clip(clip)

    for i, entry in enumerate(history):
        ey = 190 + i*entry_h - scroll
        if ey + entry_h < clip.top or ey > clip.bottom:
            continue
        is_w = entry['col'] == 'w'
        clr  = WHITE_CLR if is_w else DIM
        bar  = (200,200,200) if is_w else (100,100,100)
        pygame.draw.line(screen, bar, (PANEL_X+6, ey+3), (PANEL_X+6, ey+entry_h-3), 2)
        n_t = font_xs.render(f"#{entry['n']}", True, DIM)
        screen.blit(n_t, (PANEL_X+12, ey+3))
        who = font_xs.render("Sina" if is_w else "AI", True, clr)
        screen.blit(who, (PANEL_X+42, ey+3))
        mv  = font_xs.render(entry['move'], True, GOLD if is_w else GOLD2)
        screen.blit(mv, (PANEL_X+90, ey+3))
        if entry.get('check'):
            ch = font_xs.render("+", True, RED)
            screen.blit(ch, (PANEL_X+170, ey+3))
        if entry.get('mate'):
            ch = font_xs.render("#", True, RED)
            screen.blit(ch, (PANEL_X+180, ey+3))

    screen.set_clip(None)

    vis_h   = H - 200 - 60
    total_h = len(history)*entry_h
    if total_h > vis_h:
        bar_h = max(20, int(vis_h*vis_h/total_h))
        max_s = total_h - vis_h
        bar_y = 190 + int(state['scroll']/max_s*(vis_h-bar_h))
        pygame.draw.rect(screen, WOOD,
                         pygame.Rect(PANEL_X+PANEL_W-6, bar_y, 4, bar_h),
                         border_radius=2)

    # Separator undo buttonile
    pygame.draw.line(screen, WOOD, (PANEL_X+8, H-62), (PANEL_X+PANEL_W-8, H-62), 1)
    draw_undo_button(screen, font_sm, state, mouse_pos)

def draw_gameover(screen, font_big, font_sm, state):
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0,0,0,170))
    screen.blit(ov, (0,0))
    bx = W//2 - 160
    by = H//2 - 90
    box = pygame.Rect(bx, by, 320, 180)
    pygame.draw.rect(screen, (20,14,8), box, border_radius=14)
    pygame.draw.rect(screen, GOLD, box, 2, border_radius=14)
    t1 = font_big.render(state['result_title'], True, GOLD2)
    screen.blit(t1, t1.get_rect(center=(W//2, by+50)))
    t2 = font_sm.render(state['status'], True, WHITE_CLR)
    screen.blit(t2, t2.get_rect(center=(W//2, by+100)))
    t3 = font_sm.render("R = uus mäng", True, DIM)
    screen.blit(t3, t3.get_rect(center=(W//2, by+140)))

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Male")
    clock  = pygame.time.Clock()

    pieces = load_pieces()
    missing = [k for k,v in pieces.items() if v is None]
    if missing:
        print(f"puuduvad pildid: {missing}")
        print(f"Otsin kaustast: {os.path.abspath(PIECES_DIR)}")

    # noole pic
    arrow_img = None
    arrow_path = os.path.join("arrow", "Nool.png")
    if os.path.exists(arrow_path):
        try:
            arrow_img = pygame.image.load(arrow_path).convert_alpha()
        except Exception as e:
            print(f"Viga noole laadimisel: {e}")
    else:
        print(f"Noole fail puudub: {arrow_path}")

    try:
        font_title  = pygame.font.SysFont("Georgia", 32, bold=True)
        font_big    = pygame.font.SysFont("Georgia", 36, bold=True)
        font_sm     = pygame.font.SysFont("Courier New", 13)
        font_xs     = pygame.font.SysFont("Courier New", 12)
        font_coord  = pygame.font.SysFont("Courier New", 11)
    except:
        font_title = font_big = font_sm = font_xs = font_coord = \
            pygame.font.SysFont(None, 28)

    def initial_castling_rights():
        return {'wK': True, 'wR_k': True, 'wR_q': True,
                'bK': True, 'bR_k': True, 'bR_q': True}

    def new_game():
        return {
            'board':           [row[:] for row in START],
            'turn':            'w',
            'selected':        None,
            'legal':           [],
            'last_move':       None,
            'check_sq':        None,
            'history':         [],
            'move_n':          0,
            'status':          "Sinu kord – valge",
            'over':            False,
            'result_title':    '',
            'thinking':        False,
            'ai_result':       None,
            'scroll':          0,
            'castling_rights': initial_castling_rights(),
            'en_passant_sq':   None,
            'undo_stack':      [],
            'arrows':          set(),   
            'drag_arrow':      None,    
        }

    state = new_game()

    def save_snapshot():
        """Save full game state snapshot for undo."""
        return {
            'board':           [row[:] for row in state['board']],
            'turn':            state['turn'],
            'last_move':       state['last_move'],
            'check_sq':        state['check_sq'],
            'history':         list(state['history']),
            'move_n':          state['move_n'],
            'status':          state['status'],
            'castling_rights': dict(state['castling_rights']),
            'en_passant_sq':   state['en_passant_sq'],
            'scroll':          state['scroll'],
        }

    def restore_snapshot(snap):
        state['board']           = [row[:] for row in snap['board']]
        state['turn']            = snap['turn']
        state['last_move']       = snap['last_move']
        state['check_sq']        = snap['check_sq']
        state['history']         = list(snap['history'])
        state['move_n']          = snap['move_n']
        state['status']          = snap['status']
        state['castling_rights'] = dict(snap['castling_rights'])
        state['en_passant_sq']   = snap['en_passant_sq']
        state['scroll']          = snap['scroll']
        state['selected']        = None
        state['legal']           = []
        state['over']            = False
        state['result_title']    = ''
        state['thinking']        = False
        state['ai_result']       = None

    def do_undo():
        # Undo molemad
        if len(state['undo_stack']) >= 1:
            snap = state['undo_stack'].pop()
            restore_snapshot(snap)

    def ai_thread(board, cr, ep):
        _, move = minimax(board, 3, -float('inf'), float('inf'), False, cr, ep)
        state['ai_result'] = move

    def after_move(board, moved_col, cr, ep):
        opp = 'b' if moved_col == 'w' else 'w'
        in_chk = is_in_check(board, opp, None, ep)
        mate   = is_checkmate(board, opp, cr, ep)
        stale  = is_stalemate(board, opp, cr, ep)
        kr     = find_king(board, opp)
        return in_chk, mate, stale, kr

    def add_history(col, r, c, nr, nc, check=False, mate=False,
                    promotion=False, castling=False, en_passant=False):
        state['move_n'] += 1
        state['history'].append({
            'n':    state['move_n'],
            'col':  col,
            'move': move_str(r, c, nr, nc, promotion, castling, en_passant),
            'check': check,
            'mate':  mate,
        })
        entry_h = 20
        vis_h   = H - 200 - 60
        total_h = len(state['history'])*entry_h
        if total_h > vis_h:
            state['scroll'] = total_h - vis_h

    def do_player_move(r, c, nr, nc):
        # Savei snapshot
        state['undo_stack'].append(save_snapshot())

        p = state['board'][r][c]
        promo    = (p == 'wP' and nr == 0)
        castling = (p == 'wK' and abs(nc - c) == 2)
        ep_sq    = state['en_passant_sq']
        en_pass  = (p == 'wP' and ep_sq == (nr, nc))

        nb, new_cr, new_ep = apply_move(
            state['board'], r, c, nr, nc,
            state['castling_rights'], ep_sq
        )
        in_chk, mate, stale, kr = after_move(nb, 'w', new_cr, new_ep)

        add_history('w', r, c, nr, nc, in_chk, mate, promo, castling, en_pass)
        state['board']           = nb
        state['castling_rights'] = new_cr
        state['en_passant_sq']   = new_ep
        state['last_move']       = (r, c, nr, nc)
        state['selected']        = None
        state['legal']           = []
        state['check_sq']        = kr if in_chk else None

        if mate:
            state['over']         = True
            state['result_title'] = "Klassikaline juhtum"
            state['status']       = "Matt type shiiii"
        elif stale:
            state['over']         = True
            state['result_title'] = "Kui sa oled võit, siis mis sa oleks ilma viigita?"
            state['status']       = "viik"
        else:
            state['turn']     = 'b'
            state['status']   = "AI mõtleb"
            state['thinking'] = True
            t = threading.Thread(
                target=ai_thread,
                args=(state['board'], state['castling_rights'], state['en_passant_sq']),
                daemon=True
            )
            t.start()

    running = True
    mouse_pos = (0, 0)

    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        if state['ai_result'] is not None and state['thinking']:
            move = state['ai_result']
            state['ai_result'] = None
            state['thinking']  = False
            if move:
                r,c,nr,nc = move
                p = state['board'][r][c]
                promo    = (p == 'bP' and nr == 7)
                castling = (p == 'bK' and abs(nc - c) == 2)
                ep_sq    = state['en_passant_sq']
                en_pass  = (p == 'bP' and ep_sq == (nr, nc))

                nb, new_cr, new_ep = apply_move(
                    state['board'], r, c, nr, nc,
                    state['castling_rights'], ep_sq
                )
                in_chk, mate, stale, kr = after_move(nb, 'b', new_cr, new_ep)
                add_history('b', r, c, nr, nc, in_chk, mate, promo, castling, en_pass)

                state['board']           = nb
                state['castling_rights'] = new_cr
                state['en_passant_sq']   = new_ep
                state['last_move']       = (r, c, nr, nc)
                wkr = find_king(nb, 'w')
                state['check_sq'] = wkr if is_in_check(nb, 'w', None, new_ep) else None

                if is_checkmate(nb, 'w', new_cr, new_ep):
                    state['over']         = True
                    state['result_title'] = "Kui sa oled õun, siis mis sa oleks koos raamatuga?"
                    state['status']       = "Kaotasid"
                elif is_stalemate(nb, 'w', new_cr, new_ep):
                    state['over']         = True
                    state['result_title'] = "viik"
                    state['status']       = "viik type shi"
                else:
                    state['turn']   = 'w'
                    state['status'] = "Sinu kord – valge"
            else:
                state['over']         = True
                state['result_title'] = "viik"
                state['status']       = "pole käike"

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    state = new_game()
                elif ev.key == pygame.K_q and not state['over']:
                    state['over']         = True
                    state['result_title'] = "Kardad?"
                    state['status']       = "Loobusid"
                elif ev.key == pygame.K_z:
                    if (not state['over'] and not state['thinking']
                            and state['turn'] == 'w'):
                        do_undo()
            elif ev.type == pygame.MOUSEWHEEL:
                entry_h = 20
                vis_h   = H - 200 - 60
                total_h = len(state['history'])*entry_h
                max_s   = max(0, total_h - vis_h)
                state['scroll'] = max(0, min(max_s, state['scroll'] - ev.y*18))
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
                
                mx, my = ev.pos
                r, c = px_to_sq(mx, my)
                if r is not None:
                    state['drag_arrow'] = ((r, c), (r, c))

            elif ev.type == pygame.MOUSEMOTION:
                
                if state.get('drag_arrow'):
                    mx, my = ev.pos
                    r, c = px_to_sq(mx, my)
                    if r is not None:
                        fr, fc = state['drag_arrow'][0]
                        state['drag_arrow'] = ((fr, fc), (r, c))

            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 3:
                # parem
                if state.get('drag_arrow'):
                    (fr, fc), (tr, tc) = state['drag_arrow']
                    state['drag_arrow'] = None
                    if (fr, fc) != (tr, tc):
                        key = ((fr, fc), (tr, tc))
                        if key in state['arrows']:
                            state['arrows'].discard(key) 
                        else:
                            state['arrows'].add(key)

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos

                # vasak
                state['arrows'] = set()
                state['drag_arrow'] = None

                # Undo button click
                if UNDO_BTN.collidepoint(mx, my):
                    if (not state['over'] and not state['thinking']
                            and state['turn'] == 'w'
                            and len(state['undo_stack']) >= 1):
                        do_undo()
                    continue

                if state['over'] or state['thinking'] or state['turn'] != 'w':
                    continue

                r, c = px_to_sq(mx, my)
                if r is None:
                    state['selected'] = None
                    state['legal']    = []
                    continue
                if state['selected']:
                    if (r, c) in state['legal']:
                        do_player_move(*state['selected'], r, c)
                    elif color_of(state['board'][r][c]) == 'w':
                        state['selected'] = (r, c)
                        state['legal']    = legal_moves(
                            state['board'], r, c,
                            state['castling_rights'], state['en_passant_sq']
                        )
                    else:
                        state['selected'] = None
                        state['legal']    = []
                else:
                    if color_of(state['board'][r][c]) == 'w':
                        state['selected'] = (r, c)
                        state['legal']    = legal_moves(
                            state['board'], r, c,
                            state['castling_rights'], state['en_passant_sq']
                        )

        screen.fill(BG)
        draw_board(screen, pieces, state, arrow_img)
        draw_panel(screen, font_sm, font_xs, font_title, state, mouse_pos)
        if state['over']:
            draw_gameover(screen, font_big, font_sm, state)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()