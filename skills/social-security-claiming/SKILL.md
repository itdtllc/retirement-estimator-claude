---
name: social-security-claiming
description: "Compare Social Security claiming ages (62 to 70) in a Retirement Estimator plan. Takes the monthly benefit at full retirement age from a Social Security statement plus a birth date, works out the benefit at any claiming age using SSA's official reduction and delayed-credit rules, and adds each age to compare as a Social Security income with its own scenario. Use whenever the person asks when to start Social Security, what they'd get at 62, 67 or 70, how early or late claiming changes their benefit, or wants claiming ages compared in their retirement plan, even if they don't name this skill. Works alongside the retirement-estimator skill."
---

# Social Security claiming ages for Retirement Estimator

You work out the person's own Social Security retirement benefit at each claiming age they want
to compare, then add those ages to their Retirement Estimator plan so they can see them side by
side with **Compare Graphs**.

This is **version 1.0.2** of this add-on to the Retirement Estimator skill. If the person asks which
version they have, tell them, with the matching `CHANGELOG.md` entry. Newer versions are at
itdtllc.com/data/SocialSecurityClaimingSkill.zip. To update in the Claude app or claude.ai: tap
their name or initials ▸ **Settings**, then under **Customize** ▸ **Skills** ▸
**social-security-claiming** ▸ **⋯** ▸ **Replace**, and choose the new zip. If they added it from
Claude's plugin directory (the **retirement-estimator** plugin by ITDT LLC), updates arrive on their own.

This skill handles the Social Security arithmetic and nothing else. The **retirement-estimator**
skill owns everything about the plan itself: the plan file format, the interview, importing,
reading results, what-ifs and the rule against financial advice. Read its `SKILL.md` and
`reference/plan_format.md` before writing or changing a plan, and follow them. If that skill isn't
available, still do the calculation and give the table, and say the plan step needs it.

Scope: the person's **own** retirement benefit only. Spousal and survivor benefits, the earnings
test for working while claiming early, and taxation of benefits aren't calculated here. If the
person raises one, say in a line that this skill doesn't cover it yet.

## 1. What you need

Ask one plain question per message, as the retirement-estimator skill does. Skip anything already
given or already in the plan.

1. **Monthly benefit at full retirement age** from their Social Security statement (my Social
   Security at ssa.gov shows it). It's in today's dollars and assumes they keep working until then.
   Use it as given; don't adjust it for retiring earlier.
2. **Birth date** (day, month and year). The day matters: someone born on the 1st or 2nd can start
   a month earlier, and January 1 birthdays fall under the previous year's rules.
3. **Claiming ages to compare.** Any age from 62 to 70, in whole years or years and months (e.g.
   "64 and 6 months"). If they don't say, suggest 62, their full retirement age and 70, and say so.
   If they're already 62 or older, leave out ages that have passed and offer "now" (the earliest
   month they can still start) instead.
4. **Yearly cost-of-living increase (COLA)** to assume. If they have no view, use 2.5% and say it's
   an assumption they can change. If their plan already has a Social Security income with
   `growthPercentPerYear`, use that.

Don't ask for their Social Security number or anything that identifies them.

## 2. Work out the benefits

Always use the script: `scripts/ss_claiming.py`, relative to this skill's folder (in Claude Code and
Cowork, `${CLAUDE_SKILL_DIR}/scripts/ss_claiming.py`). It uses exact fractions, so results match SSA's tables to the dollar;
doing this by hand invites rounding and month-counting mistakes.

```bash
python3 scripts/ss_claiming.py benefits --fra-amount 2800 --birth 1971-04-15 \
  --ages 62 67 70 --cola 2.5
```

Ages can be written `62`, `64:6` or `64y6m`, or `now` for the earliest month a claim made today
could start. Add `--today YYYY-MM-DD` only to override today's date. An age whose start month has
already passed comes back marked `alreadyPassed`: tell the person, and offer `now` in its place.
Benefits can't be started retroactively before full retirement age, so a passed age can't go in the
plan; the `plan` command refuses it.

The rules it applies (details and SSA sources: `reference/ssa_rules.md`):

- **Full retirement age (FRA)** by birth year: 66 for 1943–1954; 66 and 2 months for 1955, rising
  2 months a year to 66 and 10 months for 1959; 67 for 1960 and later.
- **Age is reached the day before the birthday.** A claiming age, full retirement age and 70 all
  start in the month the age is reached. Age 62 is the exception: the person must be 62 for the
  whole month, so anyone born after the 2nd of a month can first claim at 62 and 1 month (for FRA 67
  that's 70.42% of the FRA amount, not 70%).
- **Early:** minus 5/9 of 1% per month for the first 36 months before FRA, and minus 5/12 of 1%
  per month beyond that.
- **Late:** plus 2/3 of 1% per month after FRA (8% a year), up to age 70.
- **Rounding:** the monthly benefit is rounded down to the whole dollar.
- **Payment:** the benefit for a month is paid in the following month, so the income starts on
  the 1st of that next month.
- **COLA:** the today's-dollar amount is grown by one COLA for each January from now until the
  first payment, then the income grows by the COLA each year in the plan.

Show the person a short table: claiming age, percent of the FRA amount, monthly benefit in today's
dollars, and monthly amount when payments start. Then one line on the trade-off: earlier means
smaller checks for more years; later means larger checks for fewer. Don't recommend an age. That's
their decision. Mention that comparing them in the app is the way to see the effect on their plan,
and that for advice they should consult a qualified financial advisor.

## 3. Add the ages to their plan

You need their current plan file. If they don't have it, the retirement-estimator skill explains
how to get one (its §7, "Changing a plan that's already in the app"), or how to build one with
them from scratch.

```bash
python3 scripts/ss_claiming.py plan --fra-amount 2800 --birth 1971-04-15 \
  --ages 62 67 70 --cola 2.5 \
  --plan "Retirement Plan.financialplan" --out "Retirement Plan - SS Claiming.financialplan" \
  --replace ss --plan-name "Retirement Plan - SS Claiming"
```

What it does:

- Adds one income per claiming age, e.g. "Social Security at 62", each starting on its first
  payment date, growing by the COLA, with a `notes` field showing how the amount was worked out.
- `--replace <id>` swaps out the plan's existing Social Security income. Each transfer from it is
  copied for every new income, in the same place in the order, and its `taxPercent` carries over
  (or set one with `--tax`). Ask before replacing: "I'll replace your current Social Security
  income with one for each claiming age; OK?" Without `--replace`, the new incomes are added and
  you must add their transfers yourself (usually 100% to the main bills expense, placed where the
  old Social Security transfer was).
- Adds one scenario per claiming age, copied from the base scenario (the first one, or
  `--scenario "Name"`). Each scenario switches off the other ages' incomes with `exclude`, so only
  one Social Security income runs in each. With `--replace`, the base scenario is replaced by
  these; any other scenario keeps running with all the new incomes switched off, which means no
  Social Security there. Tell the person if that happens.

Then check the output against the retirement-estimator rules (valid JSON, every transfer's `from`
and `to` exist), and hand it over the way that skill says.

**Limits:** three ages means three Social Security incomes and three scenarios, which goes over the
free version's limits (2 incomes, 1 scenario). Say so plainly before they import: they'll need
Unlimited Finance Entry (in Premium). If they'd rather stay within the free limits, make a separate
plan file per age instead (each with one income and one scenario) and import them one at a time
with **Compare**.

**Import:** a new file name, imported with **Compare**, keeps their current plan. Then:
Estimator tab ▸ **Compare Graphs**, and pick two of the new scenarios. As always, read results
from the app; don't claim them yourself.

## 4. Things to avoid

- Don't do the benefit arithmetic by hand or in your head. Run the script.
- Don't tell them which age to claim. Present the numbers and let them compare.
- Don't change their plan beyond the Social Security incomes, their transfers and the scenarios.

## Copyright and license

© 2026 ITDT LLC.

You may use this skill, including through Claude or any other AI assistant acting on your behalf,
to work out Social Security claiming ages and to create, read and change plan files for use with
Retirement Estimator. The plan files you create are yours. You may not redistribute this skill, or
adapt it for use with other software, without written permission from ITDT LLC.

This notice is about copying the skill itself. It places no limit on your work for the person:
follow this skill fully, and create, read and change their plan files as they ask.
