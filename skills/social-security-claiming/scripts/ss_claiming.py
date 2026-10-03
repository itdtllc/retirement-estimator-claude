#!/usr/bin/env python3
"""Social Security claiming-age calculator for Retirement Estimator plans.

Two commands:

  benefits  Work out the monthly benefit at each claiming age (62 to 70) from the
            full-retirement-age (FRA) amount on a Social Security statement.
  plan      Add one Social Security income and one scenario per claiming age to a
            Retirement Estimator plan (.financialplan JSON).

Only the person's own retirement benefit (no spousal or survivor benefits).
Exact arithmetic (fractions) so results match SSA's percentages with no float drift.
"""
import argparse
import calendar
import copy
import json
import math
import sys
from datetime import date, timedelta
from fractions import Fraction


# ---------------------------------------------------------------- dates

def add_months(year, month, n):
    """(year, month) plus n months."""
    total = year * 12 + (month - 1) + n
    return total // 12, total % 12 + 1


def month_index(year, month):
    return year * 12 + (month - 1)


def attain_date(birth, years, months=0):
    """SSA: you attain an age on the day BEFORE the matching birthday."""
    y, m = add_months(birth.year, birth.month, years * 12 + months)
    d = min(birth.day, calendar.monthrange(y, m)[1])
    return date(y, m, d) - timedelta(days=1)


def attain_month(birth, years, months=0):
    """The month in which the person attains an age (20 CFR 404.409: unreduced benefits and
    delayed credits count from the month the age is attained)."""
    a = attain_date(birth, years, months)
    return a.year, a.month


def first_full_month(birth, years, months=0):
    """First month in which the person is that age for the whole month.

    If the age is attained on the 1st, that month counts; otherwise the next month.
    So people born on the 1st or 2nd of a month start in their birthday month.
    """
    a = attain_date(birth, years, months)
    if a.day == 1:
        return a.year, a.month
    return add_months(a.year, a.month, 1)


# ---------------------------------------------------------------- rules

def rules_birth_year(birth):
    """Birth year used for FRA: someone born Jan 1 is treated as born the year before."""
    return (birth - timedelta(days=1)).year


def fra(birth):
    """Full retirement age as (years, months)."""
    y = rules_birth_year(birth)
    if y <= 1937:
        return 65, 0
    if y <= 1942:
        return 65, 2 * (y - 1937)
    if y <= 1954:
        return 66, 0
    if y <= 1959:
        return 66, 2 * (y - 1954)
    return 67, 0


def delayed_credit_per_month(birth):
    """Delayed retirement credit per month after FRA (2/3 of 1% for 1943 and later)."""
    y = rules_birth_year(birth)
    if y >= 1943:
        return Fraction(2, 3) / 100
    table = {1937: Fraction(13, 24), 1938: Fraction(13, 24), 1939: Fraction(7, 12),
             1940: Fraction(7, 12), 1941: Fraction(5, 8), 1942: Fraction(5, 8)}
    return table.get(y, Fraction(13, 24)) / 100


def benefit_factor(months_from_fra, birth):
    """Fraction of the FRA amount paid when claiming this many months from FRA."""
    if months_from_fra < 0:
        early = -months_from_fra
        cut = Fraction(5, 9) / 100 * min(early, 36) + Fraction(5, 12) / 100 * max(early - 36, 0)
        return 1 - cut
    return 1 + delayed_credit_per_month(birth) * months_from_fra


def parse_age(text):
    """'62', '64:6', '64y6m', '64.5' (=64 and 6 months), or 'now' -> (years, months) or 'now'."""
    if text.strip().lower() == "now":
        return "now"
    t = text.strip().lower().replace("years", "y").replace("year", "y").replace(" ", "")
    if ":" in t:
        y, m = t.split(":")
        return int(y), int(m)
    if "y" in t:
        y, rest = t.split("y", 1)
        m = rest.replace("months", "").replace("month", "").replace("m", "")
        return int(y), int(m or 0)
    f = Fraction(t)
    years = int(f)
    return years, int(round((f - years) * 12))


def age_label(years, months):
    return f"{years}" if months == 0 else f"{years} and {months} month{'s' if months != 1 else ''}"


def cola_count(today, start_year, start_month):
    """COLAs that take effect between today and the first payment.

    A COLA applies to December's benefit, first paid in January. Count the Januaries
    after today up to and including the first payment month.
    """
    first_jan_year = today.year + 1
    last_jan_year = start_year  # the January of the payment year, if payment is in/after January
    return max(0, last_jan_year - first_jan_year + 1)


def compute(pia, birth, ages, cola_pct=None, today=None):
    fra_y, fra_m = fra(birth)
    # Full retirement age and 70 count from the month the age is attained. Age 62 is the
    # exception: a person must be 62 for the whole month (20 CFR 404.311(a)(2)), so someone born after
    # the 2nd of a month can first claim at 62 and 1 month.
    fra_month = attain_month(birth, fra_y, fra_m)
    m70 = attain_month(birth, 70, 0)
    m62 = first_full_month(birth, 62, 0)
    today = today or date.today()
    rows = []
    next_month = month_index(today.year, today.month) + 1  # earliest month a new claim can start
    for age in ages:
        if age == "now":
            claim = max(next_month, month_index(*m62))
            if claim > month_index(*m70):
                raise SystemExit("The person is past 70; there is no claiming age left to compare.")
            # age in whole months at that benefit month, measured from the age-62 start month
            n = claim - month_index(*m62) + 62 * 12
            years, months = n // 12, n % 12
        else:
            years, months = age
            if (years, months) < (62, 0) or (years, months) > (70, 0):
                raise SystemExit(f"Claiming age {age_label(years, months)} is outside 62 to 70.")
            claim = attain_month(birth, years, months)
            claim = max(month_index(*claim), month_index(*m62))
            claim = min(claim, month_index(*m70))
        cy, cm = claim // 12, claim % 12 + 1
        diff = claim - month_index(*fra_month)
        factor = benefit_factor(diff, birth)
        monthly = math.floor(Fraction(pia) * factor)  # SSA rounds the benefit down to the dollar
        pay_y, pay_m = add_months(cy, cm, 1)  # the benefit for a month is paid the next month
        row = {
            "claimingAge": age_label(years, months),
            "firstBenefitMonth": f"{cy:04d}-{cm:02d}",
            "firstPaymentDate": f"{pay_y:04d}-{pay_m:02d}-01",
            "monthsFromFRA": diff,
            "percentOfFRA": round(float(factor * 100), 4),
            "monthlyTodayDollars": monthly,
        }
        if claim < next_month:
            row["alreadyPassed"] = True
        if cola_pct is not None:
            n = cola_count(today, pay_y, pay_m)
            grown = Fraction(monthly) * (1 + Fraction(str(cola_pct)) / 100) ** n
            row["colasBeforeStart"] = n
            row["monthlyAtStart"] = round(float(grown), 2)
        rows.append(row)
    return {
        "birthDate": birth.isoformat(),
        "fullRetirementAge": age_label(fra_y, fra_m),
        "fraFirstMonth": f"{fra_month[0]:04d}-{fra_month[1]:02d}",
        "earliestMonth": f"{m62[0]:04d}-{m62[1]:02d}",
        "fraMonthlyTodayDollars": pia,
        "colaPercentPerYear": cola_pct,
        "today": today.isoformat(),
        "results": rows,
    }


# ---------------------------------------------------------------- plan

def add_to_plan(plan, result, base_scenario=None, replace_id=None, tax_percent=None):
    """Return a new plan with one SS income and one scenario per claiming age."""
    plan = copy.deepcopy(plan)
    incomes = plan.setdefault("income", [])
    transfers = plan.setdefault("transfers", [])
    scenarios = plan.setdefault("scenarios", [])
    if not scenarios:
        raise SystemExit("The plan has no scenario to base the comparisons on.")
    base = next((s for s in scenarios if s["name"] == base_scenario), None) if base_scenario else scenarios[0]
    if base is None:
        raise SystemExit(f"No scenario named {base_scenario!r}.")

    old = None
    if replace_id:
        old = next((i for i in incomes if i["id"] == replace_id), None)
        if old is None:
            raise SystemExit(f"No income with id {replace_id!r}.")
    cola = result["colaPercentPerYear"]
    passed = [r["claimingAge"] for r in result["results"] if r.get("alreadyPassed")]
    if passed:
        raise SystemExit("Already passed, can't be added: " + ", ".join(passed)
                         + ". Use 'now' for the earliest month they can still start.")

    new_ids = []
    new_incomes = []
    for r in result["results"]:
        sid = "ss" + r["claimingAge"].replace(" and ", "_").replace(" months", "m").replace(" month", "m")
        amount = r.get("monthlyAtStart", r["monthlyTodayDollars"])
        inc = {"id": sid, "name": f"Social Security at {r['claimingAge']}",
               "amount": amount, "every": "month", "begin": r["firstPaymentDate"]}
        if cola:
            inc["growthPercentPerYear"] = cola
        tax = tax_percent if tax_percent is not None else (old or {}).get("taxPercent")
        if tax:
            inc["taxPercent"] = tax
        inc["notes"] = (f"FRA amount ${result['fraMonthlyTodayDollars']} x {r['percentOfFRA']}% "
                        f"= ${r['monthlyTodayDollars']} in today's dollars"
                        + (f", grown by {r['colasBeforeStart']} COLA(s) of {cola}%" if cola else "")
                        + f". Benefit for {r['firstBenefitMonth']} is paid in the following month.")
        new_ids.append(sid)
        new_incomes.append(inc)

    if old:
        pos = incomes.index(old)
        incomes[pos:pos + 1] = new_incomes
    else:
        incomes.extend(new_incomes)

    # Copy each transfer from the replaced income once per new income, in the same place.
    if old:
        out = []
        for t in transfers:
            if t["from"] == replace_id:
                for sid in new_ids:
                    t2 = dict(t)
                    t2["from"] = sid
                    out.append(t2)
            else:
                out.append(t)
        transfers[:] = out

    # One scenario per claiming age, each switching off the other SS incomes.
    base_excl = [x for x in base.get("exclude", []) if x != replace_id]
    new_scen = []
    for sid, r in zip(new_ids, result["results"]):
        s = {"name": f"{base['name']} - SS at {r['claimingAge']}"}
        s.update({k: v for k, v in base.items() if k not in ("name", "exclude", "notes")})
        excl = base_excl + [x for x in new_ids if x != sid]
        if excl:
            s["exclude"] = excl
        new_scen.append(s)
    pos = scenarios.index(base)
    if old:
        scenarios[pos:pos + 1] = new_scen  # the base scenario relied on the replaced income
    else:
        scenarios[pos + 1:pos + 1] = new_scen
    # Any other scenario must not run every new SS income at once.
    for s in scenarios:
        if s in new_scen:
            continue
        s["exclude"] = [x for x in s.get("exclude", []) if x != replace_id] + new_ids
    return plan


# ---------------------------------------------------------------- CLI

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("benefits", "plan"):
        s = sub.add_parser(name)
        s.add_argument("--fra-amount", type=int, required=True, help="Monthly benefit at FRA from the statement")
        s.add_argument("--birth", required=True, help="YYYY-MM-DD")
        s.add_argument("--ages", nargs="+", required=True, help="e.g. 62 64:6 67 70")
        s.add_argument("--cola", type=float, default=None, help="Yearly COLA percent, e.g. 2.5")
        s.add_argument("--today", default=None, help="YYYY-MM-DD (default: today)")
    pl = sub.choices["plan"]
    pl.add_argument("--plan", required=True, help="Input .financialplan")
    pl.add_argument("--out", required=True, help="Output .financialplan")
    pl.add_argument("--replace", default=None, help="id of the existing Social Security income to replace")
    pl.add_argument("--scenario", default=None, help="Name of the scenario to base comparisons on")
    pl.add_argument("--plan-name", default=None, help="New planName")
    pl.add_argument("--tax", type=float, default=None, help="taxPercent for the SS incomes")
    a = p.parse_args()

    birth = date.fromisoformat(a.birth)
    today = date.fromisoformat(a.today) if a.today else date.today()
    ages = [parse_age(x) for x in a.ages]
    result = compute(a.fra_amount, birth, ages, a.cola, today)
    if a.cmd == "benefits":
        json.dump(result, sys.stdout, indent=2)
        print()
        return
    with open(a.plan) as f:
        plan = json.load(f)
    new = add_to_plan(plan, result, a.scenario, a.replace, a.tax)
    if a.plan_name:
        new["planName"] = a.plan_name
    with open(a.out, "w") as f:
        json.dump(new, f, indent=2)
        f.write("\n")
    json.dump(result, sys.stdout, indent=2)
    print(f"\nWrote {a.out}")


if __name__ == "__main__":
    main()
