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

For one account paying the bills after other income, run the script. It mirrors how the app runs
that plan month by month, and it matched the app's CSV report to within a dollar over 17 years.

```bash
python3 scripts/spend_down.py --balance 380000 --return 7 --start 2026-11-01 --end 2044-04-30 \
  --income 2600 --income-growth 2.5 --income-tax 10 --inflation 3 --withdrawal-tax 12
```

`--start` is the month of the next withdrawal; `--end` is the target month; `--target 50000`
leaves a reserve. It prints the monthly spending, this month's withdrawal (tax included), and the
balance year by year. `--spending 4500` checks a given level instead.

If the plan has more than one account paying bills, or other transfers, use the script for a first
guess, build the plan, and have them import it with **Compare**. Read the account's last value
(tap the end of its line, or a CSV report) and adjust: spending up if money is left, down if it
runs out early. The app is the authority, not the script.

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
  reaching 95 (figures for people alive today run somewhat higher). After the target only lifetime
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
however often they withdraw):

1. They give you the account's **new balance** and the date.
2. Run the script again from that date with the new balance (and today's Social Security amount).
   It returns the new monthly spending and this withdrawal. After the market falls, both go down;
   after it rises, they go up.
3. Give them an updated plan file with **every begin date moved to the new date** and the new
   balance, a new file name, and import it with **Replace** (ask first) so the graph shows the new
   path to the target.

If they'd rather edit the app directly, both changes are needed: the account's balance **and** its
begin date (and the scenario's begin date) set to today. A new balance with an old begin date makes
the app grow it from the old date.

## 8. Things to avoid

- Don't choose the target age, the reserve, or the spending for them. Give the numbers; it's their
  decision. For advice, a qualified financial advisor.
- Don't present the spending as guaranteed. It's an estimate that changes with every update.
