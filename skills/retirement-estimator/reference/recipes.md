# Recipes for common situations

Patterns that came up when building real plans, each checked in the app (CSV report, 2026-10-14).
SKILL.md §3 has the general rules; these apply them.

## Pay, contributions and taxes

- **What a percent from a paycheck is of.** The income's `taxPercent` comes off each payment first;
  its transfers then share the after-tax amount. A percent into an investment is a percent of the
  **gross** payment. Example: $7,083.33 a month, 22% tax, 10% → 401(k), then 100% → Savings: the
  401(k) gets $708.33 and Savings $4,816.67 ($7,083.33 − $1,558.33 tax − $708.33). So write the
  contribution percent as given (10, not 10 ÷ 0.78). Bills paid straight from the paycheck get at
  most what's left after the tax and earlier transfers (help §2.7, "What a percentage means"). The
  plan taxes the pre-tax contribution too, which makes it a little cautious; say so in a line when
  the contribution is large.
- **The leftover transfer stays at 100%.** A contribution plus the leftover transfer (income → 100%
  → Savings) adds up to more than 100% into investments. That's the intent: the leftover transfer
  gets what's left. Keep it at 100% (90% would leave money in the income every period). The app's
  checker notes it as a warning, which the app's import doesn't show; the **Import Plan** shortcut
  lists warnings ("percent transfers into investments add up to more than 100%..."). If they see it
  there, it's expected and harmless.
- **Employer match.** Its own income item, e.g. "Employer 401(k) Match": the match percent of the
  pay as its amount, the same `every`, `growthPercentPerYear` and `end` as the pay, no `taxPercent`,
  and one transfer 100% → the 401(k). It then rises with raises, stops at retirement, and doesn't
  come out of the pay.
- **Pay every two weeks.** Enter it monthly (yearly pay ÷ 12) when it pays monthly bills or feeds a
  monthly savings transfer, so all its transfers share one schedule (SKILL.md §3, "One source, one
  schedule").

## Accounts

- **Keep a minimum in savings** ("keep $20,000 as an emergency fund"). Split the account into two
  investments: "Savings" (the balance above the minimum, receiving leftover pay) and "Emergency
  Fund" (the minimum), with the Emergency Fund last in the drawdown order. It's then used only when
  everything else is empty, so no bill shows unpaid while money is left. When their statement later
  shows one balance for both (an update file, SKILL.md §7), split it the same way and say so.
- **Fewer transfers: a hub.** Send every income into Savings (after any contributions) and let the
  accounts pay the bills in drawdown order, Savings first, rather than a transfer from every income to
  every bill. This takes the place of SKILL.md §3's income → bill transfers; the result is the same. Bills that
  grow at the same rate and are paid from the same accounts can be one expense (e.g. everyday
  spending + property tax ÷ 12 + insurance ÷ 12 as "Living Expenses"); list what it includes in its
  `notes` and in your summary, so later changes (and update files) use the combined amount.

- **A yearly bill on its own due date.** Every transfer from one account must share a schedule
  (help §2.6), so when Savings also pays monthly bills, a yearly bill is normally spread monthly
  (÷ 12). When the due month matters to the person (e.g. to see December's property tax in the
  graph), give it its own fund instead. List these transfers in this order, after Savings' other
  bill transfers:
  1. Savings → 100% → a monthly expense "Property Tax Set-Aside" (begins with the scenario).
  2. Set-Aside → 100% → an investment "Property Tax Fund" (0% return, so it holds exactly what's
     set aside).
  3. Property Tax Fund → 100% → the yearly Property Tax, with its due date as `begin`.

  If the bill rises, the set-aside's raise falls on a different month from the bill's, so set it to
  **the yearly amount ÷ 12 × (1 + the yearly growth)**, with the same growth: $6,000 at 3% is
  $515 a month. Plain ÷ 12 falls short: checked in the app over 10 years, ÷ 12 left the bill unpaid
  from the fifth year on, while × 1.03 paid it in full every year and left a small surplus in the
  fund ($530 rising to $884). Without growth, ÷ 12 is exact. If the first due date is less than a
  year away, start the fund with a `balance` (taken out of Savings' balance) so the months until
  then fill it. Savings' transfers all stay monthly.

## Dates and amounts

- **A fixed-rate mortgage** doesn't rise: no `growthPercentPerYear`, unlike the other bills.

- **Costs that start later** (health insurance after retiring, Medicare, travel): ask whether the
  amount is today's price or the price when it starts. If it's today's, write the price at its
  start: amount × (1 + inflation)^years from the scenario's begin date (when the other bills' prices
  are set) to its start, and say so. An expense's growth only
  counts from its own begin date.
- **Couples: when the plan ends.** End the scenario at the younger person's 100th birthday unless
  they choose otherwise, and say so. An RMD scenario ends on December 31 of the year the account's
  **owner** turns 100 (`rmd.md`).
