import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import cashmatch as c
P = c.load("payments.csv"); I = c.load("invoices.csv")
R = {r["payment"]: r for r in c.match(P, I)}
def test_memo(): assert R["P1"]["invoices"] == ["INV-101"] and R["P1"]["action"] == "auto-apply"
def test_multi(): assert sorted(R["P2"]["invoices"]) == ["INV-201", "INV-202"] and R["P2"]["action"] == "review"
def test_short(): assert R["P3"]["action"] == "review" and "short/over" in R["P3"]["reason"]
def test_none(): assert R["P4"]["invoices"] == []
def test_name(): assert c.name_sim("Acme Corporation", "Acme Corp") > 0.6
