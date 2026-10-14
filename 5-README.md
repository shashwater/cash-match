# cash-match

Match incoming payments to open invoices and flag the ones a human should look at.

Cash application is the slow part of accounts receivable: payments show up with messy payer names, partial amounts, and one check covering several invoices. This tool scores each payment (invoice number in the memo, exact amount for a fuzzy-matched customer, one-to-three invoice combinations), auto-applies the confident ones, and sends the rest to a review queue with a reason.

    python3 cashmatch.py payments.csv invoices.csv

Next: read remittance PDFs and emails, learn customer name aliases from past matches.
