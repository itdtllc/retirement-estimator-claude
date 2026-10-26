# Reading a CSV report

A CSV report (Estimator tab ▸ scenario ▸ **Generate/View CSV Reports**, needs the **CSV Reports**
purchase) holds **both** every item's settings and the projection for every period. So it serves
two purposes:

- **Checking results** (SKILL.md §6), and
- **Rebuilding a plan that's already in the app** (SKILL.md §7, "Changing a plan that's already in the app"). The app can't export a
  `.financialplan` file, and its **Export Data** file is encrypted, so the CSV is how you see
  what's in the app.

All values in the example below are invented.

## Layout

The file is a series of blocks separated by blank lines:

```
Report Name,Estimator Configuration Name,Begin Date,End Date,Schedule Type
"My Report","My Retirement","01/01/2027","12/01/2060",Monthly

TRANSFERS
Transfer Name,Begin Date,End Date,From,To,Percentage Of Investment,Percentage Transfer Schedule,Percentage Transfer Schedule Type,Transfer Tax,Add/Subtract Tax To/From Transfer Amount
"Brokerage to Bills","01/01/2027","12/01/2060","Brokerage","Bills","100.00%","1",Monthly,"15.00%","Add"

Transfer Date >,,02/01/2027,03/01/2027,...
Taxed Transfer Amount From Investment >,,$4,705.88,...
Transfer Amount To Expense >,,$4,000.00,...
Percentage Of Investment Amount >,,0.52%,...

INCOME
Income Name,Begin Date,End Date,Payment,Payment Schedule,Payment Schedule Type,Percentage Increase,Percentage Increase Schedule,Percentage Increase Schedule Type,Fixed Increase,Fixed Increase Schedule,Fixed Increase Schedule Type,Income Payment Tax
"Pension","06/01/2029","12/01/2060","$1,850.00","1",Monthly,"1.50%","1",Yearly,"","","","15.00%"
Income Report Date >,...
Income Payment >,...

INVESTMENTS
Investment Name,Begin Date,End Date,Initial Investment,Percentage Increase,Percentage Increase Scedule,Percentage Increase Schedule Type,Fixed Increase,Fixed Increase Schedule,Fixed Increase Schedule Type,Investment Increase Tax
"Brokerage","01/01/2027","12/01/2060","$900,000.00","6.00%","1",Yearly,"","","",""
Investment Report Date >,01/01/2027,02/01/2027,...
Investment Amount >,$900,000.00,$895,294.12,...

EXPENSES
Expense Name,Begin Date,End Date,Cost,Cost Schedule,Cost Schedule Type,Percentage Increase,Percentage Increase Schedule,Percentage Increase Schedule Type,Fixed Increase,Fixed Increase Schedule,Fixed Increase Schedule Type
"Bills","02/01/2027","12/01/2060","$4,000.00","1",Monthly,"3.00%","1",Yearly,"","",""
Expense Report Date >,...
Expense Amount >,...
Total Accumulated Expense After Payments >,...
```

## Reading it cheaply

Reports are often 150–250 KB. Don't read the whole file. With code:

- **Settings rows** are the short rows (14 cells or fewer) that follow each header row. Print only
  those to see every item's settings in a few hundred tokens.
- **Series rows** start with a label ending in ` >` and have one cell per period. Pull out only the
  dates you need (e.g. each January, the last period).
- **When a new report arrives after an earlier one, compare the two first** instead of reading the
  new one: diff the settings rows (by item name, plus the order of the names, which is the transfer
  priority), then the series rows. Report only what changed. If nothing changed but the report
  name, say so; the person's edits in the app may not have been saved, or the report may be from
  another scenario. This costs almost nothing however large the files are.
- After a plan you built is imported, check its report's settings rows against the plan file
  rather than re-reading everything.
- Ask a focused question first (SKILL.md §6), and say you're working from a summary of the file.
  For scale: about 4 characters make a token, so a 200 KB report read whole is about 50,000 tokens;
  pulling out the rows you need is usually a few thousand.

## Mapping to the plan file

| CSV | Plan file |
|---|---|
| Header row, scenario name, begin/end, schedule | `scenarios[]`: `name` (the **Estimator Configuration Name**, not the report name), `begin`, `end`, `reportBy` |
| Income: Payment, Payment Schedule Type | `amount`, `every` |
| Income: Percentage Increase (Yearly) | `growthPercentPerYear` |
| Income Payment Tax | `taxPercent` |
| Investment: Initial Investment | `balance` |
| Investment: Percentage Increase, Percentage Increase Schedule, Schedule Type | `returnPercentPerYear` **converted to a yearly rate** (below), `compound` (Yearly → `"year"`, Monthly → `"month"`) |
| Investment Increase Tax | `taxOnGrowthPercent` |
| Expense: Cost, Cost Schedule Type, Percentage Increase | `amount`, `every`, `growthPercentPerYear` |
| Transfer: From, To | `from`, `to` (make up short ids; the CSV uses item names) |
| Transfer: the percentage column (its header says "of investment", "of income payment" or "of expense cost") | `percent` |
| Transfer Tax, Add/Subtract | `taxPercent`, `taxMode` (`"add"` / `"subtract"`); blank or 0.00% means no tax |
| Fixed Increase columns | `fixedIncrease` (usually blank) |

**Investment returns are per compounding period, not per year.** The app stores and shows an
investment's rate for one compounding period: 6% a year compounded monthly is shown as
`"0.49%","1",Monthly`. Convert it back: `returnPercentPerYear` = ((1 + p/100)^n − 1) × 100, where
`n` is the periods per year (Monthly 12, Quarterly 4, Weekly 52.18, Daily 365.24, Yearly 1; divide
by the schedule count, e.g. every 3 months → 4). Because `p` is shown rounded (0.49% → 6.04%),
round the yearly rate to the nearest 0.1% and confirm it with the person ("0.49% a month is about
6% a year"). Income and expense increases on a 1-Yearly schedule map directly to
`growthPercentPerYear`.

**Rounded percents lose precision in a rebuild.** Transfer percents are shown to 2 decimals, so
copying them can change a plan that used finer ones. Recompute RMD transfer percents from
`rmd.md` (e.g. 0.3390, not 0.34) rather than copying the rounded value, and say so for any other
percent that was rounded.

Keep each item's name exactly as it appears, so the rebuilt plan looks the same in the app.

**Items with no date.** An item whose Begin Date or End Date is empty in the app follows the scenario,
and the report shows the scenario's date for it. Reports from app 1.8.0 on say so in that item's own
header row: `Transfer Name,Begin Date (Scenario Begin),End Date (Scenario End),...`; the date cell
stays a plain date. A plain `Begin Date` / `End Date` header means the date was set on the item.
Older reports have no label (and their Income header reads ` EndDate`), so there a date equal to the
scenario's begin or end usually means no date. In the rebuilt plan, **leave out every date under a
labeled header, and in an older report every `begin` equal to the scenario's begin and every `end`
equal to its end**; the item then follows the scenario, as it
did in the app. Copy the other dates (e.g. a pension starting in 2032). Never give an undated item a date: a
transfer dated to the scenario's begin looks like it starts years before the income it carries, and
when the plan is moved forward (Update Balances, or a new start date) it moves with the date instead of
following the scenario.

## Spotting a measuring expense

An expense that is the **From** of a transfer into an investment is a **measuring expense**, not a
cost (SKILL.md §3, "route it through an expense"). People build these to make a withdrawal grow
each year, since transfers can't grow. It can have any name, e.g. "IRA Draw" or "Retirement
Income". In a rebuild:

- **Rebuild every transfer into and out of it exactly**, with the same percents, tax, tax mode and
  priority order. Don't replace the chain with a direct transfer between the accounts; that drops
  the growth.
- **Describe it as the chain it is:** "IRA → IRA Draw ($5,000/month, +2%/yr) → Savings". Don't call
  it a bill, and don't count it as spending when you explain results.
- **A tax top-up is part of it.** With `taxMode: "subtract"` on the transfer into the expense, the
  expense receives less than it costs, and a second transfer (often from Savings) pays the rest.
  Example (invented): a $5,000 expense, IRA → expense 100% with 15% subtracted ($5,000 leaves the
  IRA, $4,250 arrives), then Savings → expense 100% ($750), then expense → Savings 100% ($5,000).
  Savings gains $4,250 net. Keep the top-up transfer and its place in the order: without it the
  expense is short every period, shows as unpaid, and Monte Carlo counts a failure. Don't switch
  the tax mode to `"add"` either; that changes what leaves the account.

**Not in the report, so ask or keep:**
- **Transfer priority.** Transfers are listed in priority order, highest first (confirmed by an
  app user). Say that you're using that order and let the person correct it.
- Notes, and items switched off in other scenarios (a report covers one scenario).

## Things to know when reading values

- **Percents are displayed rounded** to 2 decimals (0.3345% shows as 0.33%), but the app calculates
  with the full value. Check results with the amounts, not the displayed percent.
- **An investment's amount on a date is after that date's transfers.** To get the balance at the
  end of the year before (for an RMD), add back that January's withdrawal: Dec 31 balance ≈
  the Jan 1 amount + Jan's "Taxed Transfer Amount From Investment".
- **"Taxed Transfer Amount From Investment"** is what left the account, tax included. With
  `"subtract"`, **"Transfer Amount To Investment"** (or "To Expense") is what arrived after tax.
- **Unpaid bills:** an expense's "Total Accumulated Expense After Payments" above $0.00 means it
  went unpaid in that period.
- Income and transfer cells are blank in periods before an item starts.
