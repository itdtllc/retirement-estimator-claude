# Retirement Estimator for Claude

Plan your finances with Claude and the [**Retirement Estimator**](https://apps.apple.com/app/id1448396456) app by ITDT LLC (iPhone,
iPad, and Mac with Apple silicon, [on the App Store](https://apps.apple.com/app/id1448396456)). Tell Claude about your income, savings, investments and expenses in plain
words. Claude asks questions one at a time, builds your plan as a file, and you import it into the
app to see your graphs, compare what-ifs, and run Monte Carlo simulations.

This plugin contains two skills:

- **retirement-estimator**: set up a retirement plan, a budget, or any plan of money coming in,
  saved and spent. Change a plan that's already in the app (from a CSV report), add required
  minimum distributions, and spend an account down by an age you choose, with the amount to
  withdraw redone before every withdrawal.
- **social-security-claiming**: from the full-retirement-age amount on your Social Security
  statement and your birth date, work out your benefit at any claiming age from 62 to 70 with SSA's
  rules, and add the ages you want to compare to your plan.

## Use it

1. Get **Retirement Estimator** from the [App Store](https://apps.apple.com/app/id1448396456). Importing a plan needs the Import/Export Data
   purchase (included in Premium).
2. In Claude, choose **Opus** (Opus 5.5 or later is recommended) and make sure code execution and
   file creation are on.
3. Ask, for example: "Help me set up my retirement plan in Retirement Estimator." or "How much can my
   mom spend each month so her IRA lasts until she's 95?"
4. Download the plan file Claude makes and open it. Retirement Estimator checks it and imports it.

More, including videos: https://itdtllc.com/retirement-claude.html

## Versions

See [CHANGELOG.md](CHANGELOG.md) for what's new in each version of both skills. Each version is also a
tag and a [GitHub release](https://github.com/itdtllc/retirement-estimator-claude/releases) with that
version's skill zip, and there's a video for most versions on the
[What's New page](https://itdtllc.com/retirement-skill-whats-new.html).

## Data

The skills run only inside your Claude conversation. They send nothing anywhere and store nothing
themselves. What you tell Claude stays in your Claude account under Anthropic's privacy settings.
The plan files Claude makes are plain JSON that you download and open in the app, which keeps your
data on your device. ITDT LLC does not receive or collect any of your information.

The bundled Python scripts (`spend_down.py`, `ss_claiming.py`) only do arithmetic on the numbers
Claude passes them and read or write the plan file you're working on. They make no network calls.

## Not financial advice

Claude and Retirement Estimator are estimation tools. Values Claude suggests are suggestions you can
change. For financial or tax advice, consult a qualified professional.

Privacy policy: https://itdtllc.com/privacy.html · Support: https://itdtllc.com
