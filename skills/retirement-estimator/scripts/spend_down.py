#!/usr/bin/env python3
"""Spend-down calculator: the monthly spending that brings one account to a target balance
(usually $0) by an end date, and this month's withdrawal.

It mirrors how Retirement Estimator runs a simple plan, month by month:
- The account grows at (1 + yearly return)^(1/12) - 1 per month on last month's balance, less
  any tax on growth, then that month's transfers apply (none of the growth in the first month).
- Bills and income step up once a year, on the anniversary of the plan's begin date.
- Income pays the bills first (after its own tax); the account pays the rest, grossed up for
  the withdrawal tax: amount / (1 - tax), the app's "add" tax mode.
The app is the authority. Use this for a close first answer, then check the account's end
value in the app and adjust (see reference/spend_down.md).

  python3 scripts/spend_down.py --balance 380000 --return 7 --start 2026-11-01 --end 2044-04-30 \
      --income 2600 --income-growth 2.5 --income-tax 10 --inflation 3 --withdrawal-tax 12

Add --spending 4800 to check a given spending level instead of solving for it.
"""
import argparse, json, math


def months_between(start, end):
    (y1, m1), (y2, m2) = start, end
    return (y2 - y1) * 12 + (m2 - m1) + 1  # inclusive of both months


def run(a, spending, detail=False):
    mrate = (1 + a.ret / 100) ** (1 / 12) - 1
    mrate *= (1 - a.growth_tax / 100)
    bal = a.balance
    rows = []
    for k in range(a.months):
        if k > 0:
            bal *= 1 + mrate
        year = k // 12
        bills = spending * (1 + a.inflation / 100) ** year
        income = a.income * (1 + a.income_growth / 100) ** year * (1 - a.income_tax / 100)
        need = max(bills - income, 0.0)
        draw = need / (1 - a.withdrawal_tax / 100)
        bal -= draw
        if detail and (k == 0 or k % 12 == 0 or k == a.months - 1):
            rows.append({"month": k + 1, "bills": round(bills, 2), "incomeAfterTax": round(income, 2),
                         "withdrawal": round(draw, 2), "balanceAfter": round(bal, 2)})
    return bal, rows


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--balance", type=float, required=True, help="Account balance on the start date")
    p.add_argument("--return", dest="ret", type=float, required=True, help="Yearly return %%, e.g. 7")
    p.add_argument("--growth-tax", type=float, default=0, help="Tax on growth %% (0 for an IRA or 401(k))")
    p.add_argument("--start", required=True, help="First withdrawal month, YYYY-MM-DD")
    p.add_argument("--end", required=True, help="Last month, YYYY-MM-DD (e.g. the 90th birthday)")
    p.add_argument("--income", type=float, default=0, help="Other monthly income before tax (e.g. Social Security)")
    p.add_argument("--income-growth", type=float, default=0, help="Yearly raise on that income %%")
    p.add_argument("--income-tax", type=float, default=0, help="Tax on that income %%")
    p.add_argument("--inflation", type=float, default=0, help="Yearly increase in spending %%")
    p.add_argument("--withdrawal-tax", type=float, default=0, help="Tax on withdrawals %% (added on top)")
    p.add_argument("--target", type=float, default=0, help="Balance to leave at the end (default 0)")
    p.add_argument("--spending", type=float, default=None, help="Check this monthly spending instead of solving")
    a = p.parse_args()
    s = [int(x) for x in a.start.split("-")[:2]]
    e = [int(x) for x in a.end.split("-")[:2]]
    a.months = months_between(s, e)

    if a.spending is None:
        lo, hi = 0.0, a.balance  # monthly spending bounds
        for _ in range(200):
            mid = (lo + hi) / 2
            end_bal, _ = run(a, mid)
            if end_bal > a.target:
                lo = mid
            else:
                hi = mid
        # Round down to the cent: rounding up could leave the account a few dollars short in
        # the last month, which the app shows as part of that month's spending unpaid.
        spending = math.floor(lo * 100) / 100
        while run(a, spending)[0] < a.target and spending > 0:
            spending = round(spending - 0.01, 2)
    else:
        spending = a.spending
    end_bal, rows = run(a, spending, detail=True)
    print(json.dumps({"months": a.months, "monthlySpending": spending,
                      "firstWithdrawal": rows[0]["withdrawal"], "endBalance": round(end_bal, 2),
                      "byYear": rows}, indent=2))


if __name__ == "__main__":
    main()
