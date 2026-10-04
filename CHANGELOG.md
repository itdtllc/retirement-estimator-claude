# What's new in Retirement Estimator for Claude

The plugin's version is the Retirement Estimator skill's version. The Social Security claiming add-on
has its own version numbers, listed after it. The newest version is first in each list.

## Retirement Estimator skill

The newest version is first. The skill's version is separate from the app's version.

### 1.4.1 (2026-10-03)

- Available as the **retirement-estimator** plugin in Claude's plugin directory, together with the
  Social Security claiming add-on. Added from the directory, updates arrive on their own.

### 1.4.0 (2026-10-03)

- **Spend down by a target age.** Ask how much you can spend each month so an account lasts until
  an age you choose, such as 90. Claude works out the monthly spending and this month's withdrawal,
  builds the plan, and explains the Monte Carlo odds and what to weigh, such as living past
  the age you chose. Before every withdrawal, give Claude the new
  balance: it redoes the numbers so the plan stays on track to the age you chose.

### 1.3.2 (2026-10-03)

- **Social Security claiming add-on.** When you ask when to start Social Security, Claude uses the
  new Social Security claiming add-on if you have it. If you don't, Claude tells you where to get
  it, and can still compare claiming ages using the amounts on your Social Security statement.

### 1.3.1 (2026-10-03)

- Steps for adding and updating the skill now match Claude's current menus: tap your name or
  initials ▸ **Settings**, then under **Customize** ▸ **Skills**. To update, tap
  **retirement-estimator** ▸ **⋯** ▸ **Replace** and choose the new zip.

### 1.3.0 (2026-10-02)

- **Changing a plan that's already in the app.** The app can't export a plan file, so Claude rebuilds
  your plan from a **CSV report**, which lists every item's settings (transfers in priority order).
  Claude reads only the settings rows to keep usage down, makes the changes you ask for, and
  suggests an Export Data backup before you import with Replace.
- **New reference on CSV reports:** their layout, how each column maps to the plan file, and what to
  watch for (investment returns shown per period, percents shown rounded, balances shown
  after that day's transfers).
- **Lower usage with repeat CSV reports.** When you send a new report, Claude compares it with the
  previous one and tells you only what changed, instead of reading the whole file again. It also
  checks a newly imported plan against the file it built.
- **RMDs that replace a withdrawal.** If your 401(k) already sends a regular withdrawal to savings,
  Claude can replace it with RMDs from the first RMD year, at the same priority, so nothing is taken
  twice, then check with a CSV report that the RMDs are the larger amount.
- **Tax on RMDs.** If you ask, Claude estimates an average tax rate for your RMDs and explains its
  assumptions.

### 1.2.2 (2026-10-02)

- Updating the skill: Claude now tells you to use **Replace** in Claude's Settings ▸ Skills
  (⋯ ▸ Replace) to install a newer version, instead of uploading it again.

### 1.2.1 (2026-10-01)

- Example scenarios added to the 1.0.0 notes, to show what Claude does for you.

### 1.2.0 (2026-10-01)

- **Required minimum distributions (RMDs).** If you have a traditional 401(k) or IRA, Claude
  explains what an RMD is and asks whether you'd like your plan to include an estimate. If the
  account isn't paying your bills, Claude adds each year's RMD to the plan. If it is, Claude checks
  after the import that your planned withdrawals reach each year's RMD.
- **Pay left over after bills** is moved into your savings account.
- **Accounts you keep out of the drawdown order.** Claude points out what happens if the accounts
  that pay your bills run out, and offers a what-if.
- New suggested starting values for a bond-heavy account and for tax on savings interest.

### 1.1.0 (2026-10-01)

- **Moving money between accounts that grows each year,** such as an inflation-adjusted withdrawal
  from a 401(k), Roth conversions over a set of years, shifting gradually into bonds, or
  contributing up to a limit that rises each year.

### 1.0.0 (2026-09-26)

- First release. Claude interviews you one question at a time, builds your plan as a file that
  Retirement Estimator imports, and helps you read the results and try what-ifs.
- **Example: planning retirement.** "I'm 62 and want to retire at 65." Claude asks about your
  Social Security, accounts and spending, one question at a time, builds the plan, and after you
  import it shows you how long your money lasts.
- **Example: a monthly budget.** "Does my pay cover my bills, and can I save $300 a month?" Claude
  sets up your pay, bills and savings goal so you can see each month where your money goes.
- **Example: what-ifs.** "What if I retire at 67 instead?" Claude makes a second version of your
  plan with only that change, and you see both on one graph.
- **Example: which account to spend first.** Social Security first, then savings, then the 401(k):
  Claude sets up the order you choose, and you see when each account is drawn down.
- **Example: a couple.** Claude sets up each person's income and accounts, so the plan covers both
  of you.
- **Example: a big one-time cost.** A new car in 2028 or a roof repair: Claude adds it on its date
  and shows the effect on your savings.
- **Example: reading your results.** Send Claude a screenshot of your graph and it explains what
  it shows: whether the money lasts, and the few numbers that matter most.

## Social Security claiming add-on

The newest version is first. This add-on works alongside the Retirement Estimator skill and has its
own version number.

### 1.0.2 (2026-10-03)

- Included in the **retirement-estimator** plugin in Claude's plugin directory. Added from the
  directory, updates arrive on their own.

### 1.0.1 (2026-10-03)

- **Claiming months follow SSA's rules exactly.** Full retirement age and later claiming ages start
  in the month you reach them, and the earliest claim at 62 needs the whole month. For most people
  the earliest claim is now correctly 62 and 1 month (70.42% of the full amount with a full
  retirement age of 67).

### 1.0.0 (2026-10-03)

- **Social Security claiming ages.** Give Claude the monthly benefit at full retirement age from
  your Social Security statement and your birth date. Claude works out your benefit at any claiming
  age from 62 to 70 with SSA's official rules, and adds each age you want to compare to your plan
  as its own scenario, so you can see them side by side with Compare Graphs.
