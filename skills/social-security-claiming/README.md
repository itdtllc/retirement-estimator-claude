# Social Security claiming add-on for the Retirement Estimator skill

**Version 1.0.1.** See `CHANGELOG.md` for what's new in each version.

An add-on skill for Claude that works alongside the **Retirement Estimator** skill. Tell Claude
the monthly benefit at full retirement age from your Social Security statement (my Social Security
at ssa.gov) and your birth date. Claude works out what you'd get at any claiming age from 62 to 70
and adds the ages you choose to your plan, one scenario each, so you can compare them in the app.

It covers your own retirement benefit. Spousal and survivor benefits, the earnings test and tax on
benefits aren't calculated.

## Add it to Claude

You need the Retirement Estimator skill installed first (itdtllc.com/retirement-claude.html).

1. Download **SocialSecurityClaimingSkill.zip**.
2. In claude.ai or the Claude app, tap your name or initials ▸ **Settings**, then under
   **Customize** tap **Skills** ▸ **+ Add** ▸ **Upload skill**, and pick the zip.
3. In a new chat, ask: "My Social Security statement says $2,400 a month at full retirement age and
   I was born June 15, 1965. Compare starting at 62, 67 and 70 in my plan." Attach your plan file.

**Updating to a newer version:** download the new zip, then under **Customize** ▸ **Skills** tap
**social-security-claiming** ▸ **⋯** ▸ **Replace** and choose the new zip.

Because it's a separate skill, updating the Retirement Estimator skill never removes it.

## Suggestions, not financial advice

Claiming-age amounts are estimates from the rules and the statement amount you give. For advice on
when to claim, consult a qualified financial advisor.

© 2026 ITDT LLC.
