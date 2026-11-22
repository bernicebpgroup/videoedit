import sys, math
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
exec(open(sys.argv[1] + "/examples2.py", encoding="utf8").read().split("# E1 拍卖经验")[0].replace("out = sys.argv[2]", ""))
base = frame(0.5)
b1 = base.crop((110, 1470, 560, 1880)).rotate(180); b2 = base.crop((470, 1500, 900, 1900)).rotate(180)
def two_books(c, p):
    if p < 1:
        firefly(c, (1060, 1750), (860, 560), p); firefly(c, (20, 1750), (220, 560), p)
    else:
        place(c, card(b1, "第一本", 280, 330), 225, 560, 1, 1, 5); place(c, card(b2, "第二本", 280, 330), 860, 560, 1, 1, -5)
def expand_panel(c, q):
    """q 0..1: small card at (860,620) grows into glass panel."""
    x0 = 860 - 150 + (50 - 710) * q; y0 = 620 - 180 + (1020 - 440) * q; x1 = 860 + 150 + (1030 - 1010) * q; y1 = 620 + 180 + (1560 - 800) * q
    glass(c, (int(x0), int(y0), int(x1), int(y1)))
    if q > 0.85:
        place(c, T("拍卖房产，不是全部一样", 52), W / 2, 1100)
        for k, (no, tt, ls, bar) in enumerate([("01", "法院拍卖", ["已有地契", "法院程序"], GREEN), ("02", "LACA", ["地契未完成", "银行委托"], GOLDB), ("03", "Tender", ["密封式招标", "最高价得标"], ORANGE)]):
            xx = 80 + k * 310; mini_card(c, (xx, 1180, xx + 290, 1520), no, tt, ls, bar)
f1 = frame(0.2); two_books(f1, 0.6); place(f1, big_title("这2本书", 130), W / 2, 960)
f2 = frame(0.9); two_books(f2, 1.0); place(f2, big_title("这2本书", 130), W / 2, 960)
f3 = frame(3.0); place(f3, card(b1, "拍卖经验", 300, 360), 860, 620, 1, 1, -4); place(f3, big_title("拍卖经验", 150), W / 2, 960)
f4 = frame(3.15); expand_panel(f4, 0.45); place(f4, big_title("拍卖经验", 150), W / 2, 900)
f5 = frame(3.5); expand_panel(f5, 1.0); place(f5, big_title("拍卖经验", 150), W / 2, 900)
board([f1, f2, f3, f4, f5], out + "/ex_E_firefly_flow.jpg"); print("ok")
