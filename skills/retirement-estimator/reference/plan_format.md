# Plan file format (planFormat 1)

A plan file is plain JSON saved with the extension **`.financialplan`**. Retirement Estimator (1.7.0 or
later) imports it directly. Write amounts and rates the way people say them; the app converts them
into what it stores and checks the whole plan before saving anything. If there is a problem,
nothing is imported and every problem is listed. See `examples/Retirement Plan Age 67.financialplan` for a
complete plan.

The file must be valid JSON: no comments, no trailing commas. (The comments in the outline below
are only for explanation.)

```json
{
  "planName": "Retirement Plan",          // name the file after it: "Retirement Plan.financialplan"
  "planFormat": 1,
  "income": [...], "investments": [...], "expenses": [...], "transfers": [...], "scenarios": [...]
}
```

Any object may also have a `"notes"` field. The app ignores it, so use it to record why a value
was chosen. Any other unknown field is an error.

## Schedules (`every`, `compound`, `reportBy`)

Text such as `"month"`, `"monthly"`, `"year"`, `"quarter"`, `"week"`, `"day"`, `"2 weeks"`, or
`"every 3 months"`.

## Dates (`begin`, `end`)

- Format is `"YYYY-MM-DD"` (or `"YYYY-MM"`, which means the 1st).
- Leave a date out to use the scenario's begin or end date.
- Start things on the **1st of a month** unless there's a reason not to (see the Transfers rules).

## Income

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Short label that transfers use to refer to this item, e.g. `"ss"` |
| `name` | yes | Shown in the app |
| `amount`, `every` | yes | e.g. `3000`, `"month"` |
| `growthPercentPerYear` | | Yearly raise, e.g. `2.5` for a 2.5% COLA. Compounds once a year |
| `fixedIncrease` | | `{"amount": 50, "every": "year"}` adds $50 to **each payment** every year. On a monthly income that is +$600 a year. Usually use `growthPercentPerYear` instead |
| `taxPercent` | | Percent taken out of each payment |
| `begin`, `end` | | e.g. Social Security starts at claiming age; a paycheck ends at retirement |

## Investments

| Field | Required | Meaning |
|---|---|---|
| `id`, `name` | yes | |
| `balance` | yes | Balance at the item's begin date (or the scenario begin date) |
| `returnPercentPerYear` | | Effective yearly return, e.g. `7`. The app converts it to its per-period rate (7%/yr compounded monthly is stored as 0.5654% per month). **Never convert it yourself** |
| `compound` | | Default `"month"` |
| `taxOnGrowthPercent` | | Percent of each gain taken as tax (e.g. interest on a taxable savings account) |
| `contribution` | | `{"amount": 500, "every": "month"}`: a regular deposit that doesn't come from any item in the plan |
| `begin`, `end` | | |

## Expenses

| Field | Required | Meaning |
|---|---|---|
| `id`, `name` | yes | |
| `amount`, `every` | yes | |
| `growthPercentPerYear` | | Yearly inflation, e.g. `3` |
| `fixedIncrease` | | Same as for income: added to **each** cost payment |
| `begin`, `end` | | e.g. a mortgage ends at its payoff date |

## Transfers

The order of the list is the **priority**: the first transfer fires first. Where money comes from
first (the drawdown order) is set by this order.

| Field | Required | Meaning |
|---|---|---|
| `from` | yes | id of an income, investment or expense |
| `to` | yes | id of an investment or expense. A transfer from an expense can only go to an investment |
| `percent` **or** `amount` | yes | Exactly one of the two |
| `every` | | Into an expense: always the expense's schedule (don't set it). Into an investment: default is the source's schedule |
| `taxPercent` | | Tax on the transfer |
| `taxMode` | | `"add"` (default): the source pays the tax on top and the destination gets the full amount (401(k) withdrawal paying a bill). `"subtract"`: the tax comes out of the transfer |
| `name` | | Default `"<from> to <to>"` |
| `begin`, `end` | | |

How the app applies a transfer (HowToUse.html §2.5, §2.7, §3.7):

- **Into an expense, the transfer is capped** at what the expense still owes. `"percent": 100` means
  "pay whatever this bill still needs."
- **Into an investment there is no cap.** The full percent or amount moves.
- **Percent from an income or expense** is a percent of the total earned (or accumulated) to date,
  minus prior transfers (help §2.7 and the §3.7 worked example). The schedule doesn't change it.
- **Percent from an investment** is a percent of the balance at that moment, recalculated each time.
- **Transfers never grow.** A fixed `amount` stays the same forever. To pay a bill that rises with
  inflation, use `"percent": 100` into the expense and give the expense its
  `growthPercentPerYear`.
- **Transfers never overdraw.** If the source is short, the transfer moves what is there and the
  expense carries an unpaid balance.
- **Same source means same schedule and same start day.** All transfers from one source must share
  one schedule and start on the same day of the period. Otherwise the app reports a scheduling
  conflict and the priority order isn't applied. The import stops with an error if not. The usual
  fix is to put a yearly bill on a monthly schedule (divide by 12).
- A percent transfer from an income or expense pays evenly only when it runs on that source's own
  schedule. The import warns otherwise.

## Scenarios (Estimator Configurations)

| Field | Required | Meaning |
|---|---|---|
| `name` | yes | |
| `begin`, `end` | yes | The projection period, e.g. next month to age 100 |
| `reportBy` | | `day`/`week`/`month`/`quarter`/`year`. Default is the most frequent transfer schedule |
| `exclude` | | Item ids switched off in this scenario (their transfers switch off too). Use for "what if I didn't have X" |

## Limits

- **Free version:** 2 income, 2 investments, 3 expenses, 5 transfers, 1 scenario. Above any of
  these, importing needs **Unlimited Entry**, which is included in **Premium**.
- **Size:** at most 500 items of each kind; names up to 100 characters.
- **Importing at all** needs the **Import/Export** purchase (also in Premium).

---

© 2026 ITDT LLC.

You may use this skill, including through Claude or any other AI assistant acting on your behalf,
to create, read and change plan files for use with Retirement Estimator. The plan files you create
are yours. You may not redistribute this skill, or adapt it for use with other software, without
written permission from ITDT LLC.
