# Spending an account down by a target age

For questions like "How much can I spend each month so my IRA lasts until I'm 90?" or "I want to
use up my savings by 90, not leave most of it unspent." The person picks the age and what to leave
at the end (usually $0). You find the monthly spending that gets there, and the withdrawal for this
month. Then you explain why they redo it before every withdrawal.

## 1. What you need

Ask one plain question at a time, skipping anything the plan or the conversation already gives.

1. **The account and today's balance** (from their latest statement), and today's date.
2. **Its yearly return.** For a broad stock index fund such as an S&P 500 fund, suggest 7% a year
   as a conservative long-term figure (the S&P 500's long-run average has been about 10%) and say
   it's a suggestion they can change. For bonds or a mix, use SKILL.md's starting values.
3. **Their other income** (Social Security, pensions): monthly amount, yearly raise, tax.
4. **The target age** (or date) and **what to leave** at that point. Convert the age to the month
   of that birthday.
5. **Tax on withdrawals** from the account (SKILL.md's starting values), and **yearly inflation**
   for their spending (3% unless they say otherwise).

## 2. Find the spending

For one account paying the bills after other income, run the script: `scripts/spend_down.py`,
relative to this skill's folder (in Claude Code and Cowork, `${CLAUDE_SKILL_DIR}/scripts/spend_down.py`). It mirrors how the app runs
that plan month by month, and it matched the app's CSV report to within a dollar over 17 years.

```bash
python3 scripts/spend_down.py --balance 380000 --return 7 --start 2026-11-01 --end 2044-04-30 \
  --income 2600 --income-growth 2.5 --income-tax 10 --inflation 3 --withdrawal-tax 12
```

`--start` is the month of the next withdrawal; `--end` is the target month; `--target 50000`
leaves a reserve. It prints the monthly spending, this month's withdrawal (tax included), and the
balance year by year. `--spending 4500` checks a given level instead. For a redo that goes into the
app through Update Balances or an update file, add `--update-balances` (§7).

If the plan has more than one account paying bills, or other transfers, use the script for a first
guess, build the plan, and have them import it with **Compare**. Read the account's last value
(tap the end of its line, or a CSV report) and adjust: spending up if money is left, down if it
runs out early. The app is the authority, not the script.

**Not retired yet, or a full plan** (pay until retirement, several accounts, gaps before Social
Security): the script can't model it. Read the question as extra spending on top of the plan, from
retirement on. From a CSV report of their scenario, take the account's balance at the target month,
B. Work out what $1 a month of extra spending, rising with inflation, withdrawn from the account
from retirement to the target month (grossed up by its withdrawal tax), would have grown to by then
at the account's return, F. The extra is about B ÷ F a month. Add it as one expense, "Extra
Spending", paid in the same order as the other bills, and check it with a Compare import as above.
Checked in the app (2026-10-14): the account was within $15 of $0 at the target month.

## 3. Build the plan

- Every item and the scenario **begin on the same date**: the month of the next withdrawal. An
  account's `balance` is its value on its begin date, so the begin date must be today's.
- The scenario ends on the target month.
- One spending expense at the solved amount, growing with inflation.
- Transfers in this order: other income → spending first, then the account → spending with the
  withdrawal tax (`taxMode: "add"`).
- A traditional IRA or 401(k) at RMD age: check the withdrawals against the RMD
  (`reference/rmd.md`). A spend-down usually withdraws more than the RMD; say so in a line.

## 4. Tell them

- The monthly spending, and how it compares with what they spend now.
- **This month's withdrawal**, tax included, and the amount that reaches their bills.
- That the account is planned to reach the amount they chose (e.g. about $0) by the target month.
- Then §5 (the odds) and §6 (what to weigh), and offer to compare a later target age.

## 5. The risk, and Monte Carlo

A plan aimed at exactly $0 on the average return **runs short before the target in more than half
of the market paths**, because returns vary and bad years early on hurt the most. Have them run
**Monte Carlo Simulation** on the scenario (§3.5): for a plan like the example above it showed
about **40%**. Say this plainly, without alarm, and explain that the routine in §7 is what keeps
the plan on track. If they want better odds without updating as often, offer a cushion: a later
target age, or a reserve at the end (`--target`), and they can run Monte Carlo again to compare.

Market history, if they ask how bad it can get: in about 100 years the S&P 500 has fallen by half
or more three times (1929–32, about −86%; 1937–38, about −55%; 2007–09, about −57%) and came close
twice more (1973–74, about −48%; 2000–02, about −49%). These are price declines without dividends.
It recovered from each, sometimes over many years. Don't predict what the market will do.

## 6. Things to explain before they choose

Say these briefly, as facts to weigh, not advice:

- **Living past the target age is the main risk.** The target is a choice, not a forecast. In the
  2022 US life table, a woman of 72 has about a 1 in 3 chance of reaching 90 and about 1 in 7 of
  reaching 95 (figures for people alive today run somewhat higher). For other ages, look the odds up
  in SSA's current period life table rather than from memory, or say it in general terms. After the target only lifetime
  income is left, which is why Social Security or a pension matters. Offer a later age (e.g. 95),
  a reserve (`--target`), or moving the target later as they get older.
- **Spending moves with the market.** The account can't run dry before the target if they update
  every time, but spending drops after a fall, and the last few years swing the most because each
  withdrawal is a bigger share of a smaller balance. It works best when lifetime income covers the
  essential bills.
- **The return assumption shapes the path.** A higher assumed return means more spending now that
  tends to drift down with updates; a more conservative one starts lower and tends to rise.
- **Big late-life costs** (long-term care, a new roof) aren't in a smooth spending line. A separate
  reserve, outside the spend-down, covers them.
- It takes the discipline to cut spending after a bad year.

## 7. Before every withdrawal: update and redo

The right spending changes every time the balance changes. Before each withdrawal (monthly, or
however often they withdraw), they give you the account's **new balance** (from the statement, at
the start of the withdrawal date) and the date. Then the new balance goes into the app one of three
ways. The first two use Update Balances (app 1.8.0 or later) and are the quickest. Ask which they'd
like if they haven't said; the update file is the least typing for them.

**An update file (you fill Update Balances in for them).** Run the script from the withdrawal date
with the new balance and **`--update-balances`**:

```bash
python3 scripts/spend_down.py --balance 362000 --update-balances --return 7 --start 2026-11-01 \
  --end 2049-04-30 --income 2600 --income-growth 2.5 --income-tax 10 --inflation 3 --withdrawal-tax 12
```

Then write `Update <date>.financialplan` (SKILL.md, "an update file"; `reference/plan_format.md`)
with `asOf` = the withdrawal date, the account's statement balance under `balances`, and the new
monthly spending under `amounts` for the spending expense, using the names exactly as in the app.
They open it, check the values, and tap **Review** ▸ **Apply**.

**Update Balances by hand.** Same script run, with `--update-balances`. Give them the three values to
enter: Money ▸ **Update Balances**, the date = the withdrawal date, the account's balance = the
statement balance, and the spending expense's amount = the new monthly spending. Then **Review** ▸
**Apply**.

Why `--update-balances`: Update Balances keeps the account's compounding day. It stores the balance
entered for the start of that day with that day's interest added (Review shows it, e.g. "Balance
$364,046.80 … That is $362,000.00 at the start of 11/01/2026 with its interest"), so the account
also grows in the first month. Solving without the flag leaves money at the end: about $9,300 at 95
on a $362,000 IRA (checked in the app, 2026-10-26). Use the withdrawal date, which for a monthly
plan is the account's compounding day; another date carries the balance to the next compounding
date and the numbers won't match.

**A new plan file.** Run the script without `--update-balances`. Give them an updated plan file with
**every begin date moved to the withdrawal date** and the new balance, a new file name, and have
them import it with **Replace** (ask first). This route also suits app versions before 1.8.0.

Whichever route: after the market falls, the spending and the withdrawal both go down; after it
rises, they go up. Tell them this month's withdrawal (the script's `firstWithdrawal`), and remind
them to send the next balance before the next withdrawal. A new balance typed into the account's
own form with its old begin date is wrong: the app grows it from the old date. Use one of the
routes above.

## 8. Things to avoid

- Don't choose the target age, the reserve, or the spending for them. Give the numbers; it's their
  decision. For advice, a qualified financial advisor.
- Don't present the spending as guaranteed. It's an estimate that changes with every update.
