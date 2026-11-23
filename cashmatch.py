"""cash-match: match incoming payments to open invoices, flag exceptions."""
import csv, sys, re, itertools, difflib

def norm(s):
    s = re.sub(r"\b(inc|llc|ltd|corp|corporation|co|company|the)\b", "", s.lower())
    return re.sub(r"[^a-z0-9 ]", "", s).split()

def name_sim(a, b):
    return difflib.SequenceMatcher(None, " ".join(norm(a)), " ".join(norm(b))).ratio()

def load(path):
    with open(path) as f:
        return list(csv.DictReader(f))

def match(payments, invoices, min_sim=0.6):
    """payments: id,payer,amount,memo ; invoices: id,customer,amount_due.
    Returns list of dicts: payment, invoices, confidence, reason."""
    open_inv = {i["id"]: i for i in invoices}
    out = []
    for p in payments:
        amt = round(float(p["amount"]), 2)
        memo = p.get("memo", "")
        cited = [x for x in re.findall(r"[A-Z]{2,4}-\d+", memo) if x in open_inv]
        cands = [i for i in open_inv.values() if name_sim(p["payer"], i["customer"]) >= min_sim]
        res = None
        if cited:
            tot = round(sum(float(open_inv[c]["amount_due"]) for c in cited), 2)
            if tot == amt:
                res = (cited, 0.99, "memo cites invoice(s), amount matches")
            else:
                res = (cited, 0.6, f"memo cites invoice(s) but total {tot} != paid {amt}: short/over pay")
        if res is None:
            for r in (1, 2, 3):
                for combo in itertools.combinations(cands, r):
                    if round(sum(float(i["amount_due"]) for i in combo), 2) == amt:
                        conf = 0.95 if r == 1 else 0.8
                        res = ([i["id"] for i in combo], conf, f"exact amount on {r} invoice(s) for matching customer")
                        break
                if res: break
        if res is None:
            res = ([], 0.0, "no match: send to exception queue")
        ids, conf, why = res
        for i in ids: open_inv.pop(i, None)
        out.append({"payment": p["id"], "invoices": ids, "confidence": conf, "reason": why,
                    "action": "auto-apply" if conf >= 0.9 else "review"})
    return out

def main(argv):
    for r in match(load(argv[1]), load(argv[2])):
        print(f'{r["payment"]:6} -> {",".join(r["invoices"]) or "-":16} {r["confidence"]:.2f} {r["action"]:10} {r["reason"]}')

if __name__ == "__main__":
    main(sys.argv)
