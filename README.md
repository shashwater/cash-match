# cash-match

A small, standard-library Python demo for matching incoming payments to open invoices and flagging exceptions for human review.

The matcher uses invoice references, normalized customer names and amounts. It handles exact matches, payments covering multiple invoices, and partial payments. Each decision includes a reason and confidence score.

## Run the sample

Python 3.10 or later. No runtime dependencies.

```bash
python3 cashmatch.py payments.csv invoices.csv
```

The included CSVs use fictional companies and sample payments. Output includes matches and a review queue. Nothing is sent to an accounting system.

## Tests

```bash
python3 -m pip install pytest
python3 -m pytest -q
```

## Limits

This is a local prototype, not production financial software. It uses floating-point amounts and simple name matching. Real deployment would need decimal-safe currency handling, reconciliation controls and review of ambiguous matches. PDF/email remittance parsing and learned customer aliases are not implemented.
