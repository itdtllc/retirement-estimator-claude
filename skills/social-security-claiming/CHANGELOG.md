# What's new in the Social Security claiming add-on

The newest version is first. This add-on works alongside the Retirement Estimator skill and has its
own version number.

## 1.1.1 (2026-10-26)

- Steps for updating the skill now match Claude's current menus: under **Customize** ▸ **Skills**,
  tap **+ Add** ▸ **Upload skill**, choose the new zip, and tap **Upload and replace**. Your earlier
  version stays in the skill's version history.

## 1.1.0 (2026-10-26)

- **Couples:** compare claiming ages for both of you, one scenario per pair of ages you choose.
- Statement amounts at other ages that don't match SSA's rules are pointed out, and stopping work
  early is explained in a line.
- Premium is assumed, as in the Retirement Estimator skill; no separate plan per age to fit the free limits.

## 1.0.2 (2026-10-03)

- Included in the **retirement-estimator** plugin in Claude's plugin directory. Added from the
  directory, updates arrive on their own.

## 1.0.1 (2026-10-03)

- **Claiming months follow SSA's rules exactly.** Full retirement age and later claiming ages start
  in the month you reach them, and the earliest claim at 62 needs the whole month. For most people
  the earliest claim is now correctly 62 and 1 month (70.42% of the full amount with a full
  retirement age of 67).

## 1.0.0 (2026-10-03)

- **Social Security claiming ages.** Give Claude the monthly benefit at full retirement age from
  your Social Security statement and your birth date. Claude works out your benefit at any claiming
  age from 62 to 70 with SSA's official rules, and adds each age you want to compare to your plan
  as its own scenario, so you can see them side by side with Compare Graphs.
