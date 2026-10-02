# Required minimum distributions (RMDs)

US rules for traditional (pre-tax) 401(k)s and IRAs. Roth IRAs and, since 2024, Roth 401(k)s have
no RMDs during the owner's life.

- **Starting age:** 73 if born 1951–1959; 75 if born 1960 or later. Someone born before 1951 is
  already taking them.
- **Each year's RMD** = the account's balance on December 31 of the year before ÷ the factor for the
  age the person turns that year (IRS Uniform Lifetime Table, below).
- The first RMD may wait until April 1 of the next year, but then two come out that year. Plans
  take it in the year the person reaches the starting age; mention the April option only if
  they ask.
- Not covered here: inherited accounts, a spouse who is the sole beneficiary and more than 10 years
  younger (a different table), and still-working exceptions. Say so and suggest a tax advisor if
  one applies.

## Ask first

When a plan has a pre-tax account and runs past the starting age, explain what an RMD is and ask
whether they'd like an estimate included (SKILL.md §2, retirement question 10). If they say no,
leave RMDs out of the plan and skip the check. If yes:

- **Nothing else draws from the account:** model the RMDs as transfers (below). If they don't
  have Unlimited Entry, say it's needed for this, and offer the check instead.
- **The account's only withdrawal moves money into savings** (e.g. 401(k) → a measuring expense →
  Savings, SKILL.md "route it through an expense"), and bills are paid from savings: the RMD
  transfers can replace that withdrawal ("Replacing a withdrawal", below).
- **The account pays bills:** do the check below after the import.

## Check the plan against the RMDs

After the import (SKILL.md §6):

1. Get the account's balance at the start of each year from the RMD age onward, and what was
   withdrawn from it that year. A **CSV report** gives both exactly: the investment's balance by
   period, and in TRANSFERS the amount of each transfer out of it by period (use the amount
   including tax). The CSV's January amount is after January's withdrawal, so add that back to
   get the December 31 balance (`csv_report.md`). **Plan Summary** gives balances by year only; estimate the withdrawals as
   start balance × (1 + yearly return) − end balance, and call the result an estimate.
2. RMD for each year = start balance ÷ factor.
3. List the years where the withdrawals are below the RMD, with both numbers. Withdrawals at or
   above the RMD are fine; the RMD is a minimum, not an extra withdrawal.
4. If there are short years, offer a what-if (SKILL.md §7). Usually: move the pre-tax account
   earlier in the drawdown order, or model the RMDs (below) when the account pays no bills.

## Optional: model the RMDs as transfers

Only when **no other transfer takes money out of that account** (it isn't paying bills). Otherwise
the app takes the RMD on top of the other withdrawals, which overstates them; use the check above
instead. Needs **Unlimited Entry** (one transfer per year of age: 28 from age 73 to 100).

- The account: `"compound": "month"`.
- One transfer per age, from the account to where the money goes (usually taxable Savings):
  `"every": "month"`, `"begin": "<year>-01-01"`, `"end": "<year>-12-31"` for the year the person
  turns that age, and `"percent"` from the table for the account's return (columns are its
  `returnPercentPerYear`; for another return, use the formula below).
- Name them "RMD 73", "RMD 74", and so on, and keep them in age order.
- End the scenario on December 31 of the year they turn 100 (not their birthday), so the last
  RMD year is complete.
- Tax: `"taxPercent"` with `"taxMode": "subtract"`. The account gives up exactly the RMD and the
  destination gets the RMD minus the tax.
- Checked in the app (2026-10-01, 7% column): the yearly total matched the true RMD within 0.01% at
  every age from 73 to 100. The other columns come from the same formula. Monte Carlo varies the
  return, so the RMDs there are only approximate.

The monthly percent `p` makes 12 monthly withdrawals add up to balance ÷ factor:
`p × (1 − q¹²) / (1 − q) = 1 / factor`, where `q = (1 − p)(1 + m)` and `m = (1 + yearly return)^(1/12) − 1`.
Solve for `p` numerically (e.g. by bisection) and give it to 4 decimal places as a percent.
Dividing 1 by (12 × factor) is not close enough: it under-withdraws by up to 4% at older ages.

## Replacing a withdrawal

When the account already makes a regular withdrawal into savings and the person wants RMDs in the
plan, adding RMD transfers on top would take both. Instead:

1. End the old withdrawal (the transfers into and out of its measuring expense, and the expense
   itself) on December 31 of the year before the first RMD year.
2. Add the RMD transfers (below) from January 1 of the first RMD year, into the same savings
   account, at the **top** of the priority list (the old withdrawal's place). Bill transfers from
   savings stay after them, so each month's RMD has arrived before bills are paid.
3. Only one withdrawal comes out of the account at a time, so nothing is taken twice.

This is exact when the RMD is at least what the old withdrawal would have taken; the RMD is a
minimum. After the import, check it with a CSV report: compare the first RMD year's total with the
old withdrawal's last full year. If the RMD is smaller in some years, the person would withdraw
more than the minimum then; keep the old withdrawal running for those years instead.

**Two owners, one account item:** if a couple's pre-tax accounts are one investment item and they
ask to treat it as one person's, use that person's birth year. It's exact if one person owns it
all, and close if they're near in age; say so in one line. Otherwise give each person's account its
own item.

## Tax on the RMDs

RMDs are taxed as ordinary income, and large ones usually push the rate above what the person used
for smaller withdrawals. If they ask you to choose a rate, estimate the **average rate on the RMD
alone**: tax on all income with the RMD, minus tax without it, divided by the RMD. Use their filing
status (ask if unknown), the standard deduction, current brackets indexed for inflation (about
2.5% a year), 85% of Social Security taxable at these incomes, and their state's income tax. Say
it's an estimate, list the assumptions, mention that a surviving spouse files as single (narrower
brackets) and that tax law can change, and suggest a tax professional. Because each RMD transfer
covers one year, each can get its own `taxPercent` if the rate changes much over the years;
otherwise one rounded rate for all keeps it simple.

Example (invented numbers): a married couple with a $30,000 pension, $25,000 of Social Security and a
$200,000 RMD, in today's brackets. Most of the RMD falls in the 22% bracket and some in lower ones,
so the average rate on it comes out near 18%, well above the 12% often used for smaller withdrawals.

## Factors and monthly percents

Monthly `percent` for each age, by the account's yearly return:

| Age | Factor | 3% | 4% | 5% | 6% | 7% | 8% |
|---|---|---|---|---|---|---|---|
| 73 | 26.5 | 0.3157 | 0.3143 | 0.3129 | 0.3115 | 0.3101 | 0.3088 |
| 74 | 25.5 | 0.3283 | 0.3268 | 0.3253 | 0.3239 | 0.3225 | 0.3211 |
| 75 | 24.6 | 0.3405 | 0.3390 | 0.3375 | 0.3360 | 0.3345 | 0.3330 |
| 76 | 23.7 | 0.3537 | 0.3521 | 0.3505 | 0.3490 | 0.3475 | 0.3459 |
| 77 | 22.9 | 0.3663 | 0.3647 | 0.3630 | 0.3614 | 0.3598 | 0.3583 |
| 78 | 22.0 | 0.3816 | 0.3799 | 0.3782 | 0.3765 | 0.3749 | 0.3732 |
| 79 | 21.1 | 0.3983 | 0.3965 | 0.3947 | 0.3930 | 0.3912 | 0.3895 |
| 80 | 20.2 | 0.4164 | 0.4146 | 0.4127 | 0.4109 | 0.4091 | 0.4073 |
| 81 | 19.4 | 0.4340 | 0.4321 | 0.4301 | 0.4282 | 0.4263 | 0.4245 |
| 82 | 18.5 | 0.4557 | 0.4536 | 0.4516 | 0.4496 | 0.4476 | 0.4456 |
| 83 | 17.7 | 0.4768 | 0.4747 | 0.4725 | 0.4704 | 0.4684 | 0.4663 |
| 84 | 16.8 | 0.5031 | 0.5008 | 0.4986 | 0.4964 | 0.4942 | 0.4920 |
| 85 | 16.0 | 0.5290 | 0.5266 | 0.5243 | 0.5219 | 0.5196 | 0.5173 |
| 86 | 15.2 | 0.5577 | 0.5552 | 0.5527 | 0.5502 | 0.5478 | 0.5454 |
| 87 | 14.4 | 0.5898 | 0.5871 | 0.5844 | 0.5818 | 0.5792 | 0.5767 |
| 88 | 13.7 | 0.6209 | 0.6181 | 0.6153 | 0.6126 | 0.6099 | 0.6072 |
| 89 | 12.9 | 0.6609 | 0.6579 | 0.6549 | 0.6520 | 0.6491 | 0.6462 |
| 90 | 12.2 | 0.7003 | 0.6972 | 0.6940 | 0.6909 | 0.6878 | 0.6848 |
| 91 | 11.5 | 0.7448 | 0.7414 | 0.7380 | 0.7347 | 0.7314 | 0.7282 |
| 92 | 10.8 | 0.7953 | 0.7916 | 0.7880 | 0.7845 | 0.7810 | 0.7775 |
| 93 | 10.1 | 0.8531 | 0.8492 | 0.8453 | 0.8415 | 0.8377 | 0.8340 |
| 94 | 9.5 | 0.9098 | 0.9056 | 0.9015 | 0.8974 | 0.8934 | 0.8894 |
| 95 | 8.9 | 0.9745 | 0.9701 | 0.9656 | 0.9613 | 0.9569 | 0.9527 |
| 96 | 8.4 | 1.0360 | 1.0312 | 1.0265 | 1.0219 | 1.0173 | 1.0127 |
| 97 | 7.8 | 1.1209 | 1.1157 | 1.1106 | 1.1056 | 1.1006 | 1.0956 |
| 98 | 7.3 | 1.2030 | 1.1975 | 1.1920 | 1.1865 | 1.1812 | 1.1759 |
| 99 | 6.8 | 1.2982 | 1.2922 | 1.2862 | 1.2803 | 1.2745 | 1.2688 |
| 100 | 6.4 | 1.3860 | 1.3795 | 1.3731 | 1.3668 | 1.3606 | 1.3544 |
