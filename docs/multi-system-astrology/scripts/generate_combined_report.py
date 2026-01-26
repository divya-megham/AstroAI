#!/usr/bin/env python3
"""
Multi-System Astrology Report Generator
Combines Vedic (Sidereal), Western (Tropical), and Chinese astrology
into a comprehensive, actionable report.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Any

def generate_executive_summary(data: Dict[str, Any]) -> str:
    """Generate executive summary section."""
    meta = data["meta"]
    vedic = data["vedic"]
    western = data["western"]
    chinese = data["chinese"]
    dasha = data["vimshottari_dasha"]
    
    moon = vedic["planets"]["moon"]
    sun_w = western["planets"]["sun"]
    asc_w = western["ascendant"]
    asc_v = vedic["ascendant"]
    
    return f"""# {meta['name']}
# 2026 Astrology Report

**Western + Vedic (Sidereal) + Chinese Synthesis**

Birth data: {meta['birth_date']}, {meta['birth_time']}, {meta.get('birth_place', 'N/A')}

*Note: Astrology is interpretive. Use this as a planning lens, not a guarantee.*

---

## Executive Summary

This report blends Western transits (tropical) with Vedic calculations (sidereal, {vedic['ayanamsa_type']} ayanamsa) and Chinese year-cycle themes. The goal is practical: highlight high-signal windows for love, health, career, and money.

### Your Core Signature

| Layer | Summary |
|-------|---------|
| **Western** | {sun_w['sign']['sign']} Sun, {asc_w['sign']['sign']} Rising, {western['planets']['moon']['sign']['sign']} Moon |
| **Vedic** | {asc_v['rashi']['english']} Lagna, {moon['rashi']['english']} Moon in {moon['nakshatra']['name']} Pada {moon['nakshatra']['pada']} |
| **Chinese** | {chinese['full']} birth year |
| **Current Dasha** | {dasha['current_dasha']} Mahadasha |

### 2026 Headline

- **Builder-to-leader year**: Fewer bets, deeper execution, more visibility from mid-year
- **Relationship theme**: Clarity + initiative. Direct communication wins.
- **Health theme**: Fire and pace. Prioritize sleep and nervous-system care.
- **Money theme**: Simplify. Reduce messy obligations, tighten compounding systems.
"""


def generate_vedic_section(data: Dict[str, Any]) -> str:
    """Generate Vedic astrology analysis section."""
    vedic = data["vedic"]
    moon = vedic["planets"]["moon"]
    asc = vedic["ascendant"]
    dasha = data["vimshottari_dasha"]
    
    # Build planetary positions table
    planets_table = "| Planet | Sign | Degree | Nakshatra | Pada | Retrograde |\n"
    planets_table += "|--------|------|--------|-----------|------|------------|\n"
    
    for planet_name in ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]:
        if planet_name in vedic["planets"]:
            p = vedic["planets"][planet_name]
            retro = "Yes ℞" if p.get("retrograde", False) else "No"
            nak = p.get("nakshatra", {})
            planets_table += f"| {p['name']} | {p['rashi']['english']} | {p['rashi'].get('degree_in_sign_dms', p.get('longitude_dms', ''))} | {nak.get('name', 'N/A')} | {nak.get('pada', 'N/A')} | {retro} |\n"
    
    # Dasha periods table
    dasha_table = "| Period | Planet | Start | End |\n"
    dasha_table += "|--------|--------|-------|-----|\n"
    for i, period in enumerate(dasha["periods"][:6]):
        marker = " ← CURRENT" if period["planet"] == dasha["current_dasha"] else ""
        dasha_table += f"| {i+1} | {period['planet']}{marker} | {period['start']} | {period['end']} |\n"
    
    return f"""
---

## Vedic Analysis (Sidereal - {vedic['ayanamsa_type']})

**Ayanamsa:** {vedic['ayanamsa']:.4f}°

### Moon Position - Your Emotional Core

| Attribute | Value |
|-----------|-------|
| **Nakshatra** | {moon['nakshatra']['name']} |
| **Pada** | {moon['nakshatra']['pada']} ({moon['nakshatra']['navamsa']} Navamsa) |
| **Rashi (Sign)** | {moon['rashi']['full_name']} |
| **Degree** | {moon['longitude_dms']} |
| **Nakshatra Deity** | {moon['nakshatra']['deity']} |
| **Nakshatra Ruler** | {moon['nakshatra']['ruler']} |
| **Nature** | {moon['nakshatra']['nature']} |

### {moon['nakshatra']['name']} Nakshatra Interpretation

**Symbol:** {moon['nakshatra']['symbol']}  
**Gana (Temperament):** {moon['nakshatra']['gana']}  
**Animal Symbol:** {moon['nakshatra']['animal']}

**Pada {moon['nakshatra']['pada']} ({moon['nakshatra']['navamsa']} Navamsa) Qualities:**
{"- Aries/Mars: Initiative, leadership, pioneering" if moon['nakshatra']['navamsa'] == "Aries" else ""}{"- Taurus/Venus: Stability, sensuality, material focus" if moon['nakshatra']['navamsa'] == "Taurus" else ""}{"- Gemini/Mercury: Communication, curiosity, adaptability" if moon['nakshatra']['navamsa'] == "Gemini" else ""}{"- Cancer/Moon: Nurturing, emotional depth, intuition" if moon['nakshatra']['navamsa'] == "Cancer" else ""}{"- Leo/Sun: Creativity, confidence, self-expression" if moon['nakshatra']['navamsa'] == "Leo" else ""}{"- Virgo/Mercury: Analytical, detail-oriented, service" if moon['nakshatra']['navamsa'] == "Virgo" else ""}{"- Libra/Venus: Relationships, balance, diplomacy, aesthetics" if moon['nakshatra']['navamsa'] == "Libra" else ""}{"- Scorpio/Mars: Intensity, transformation, research" if moon['nakshatra']['navamsa'] == "Scorpio" else ""}{"- Sagittarius/Jupiter: Philosophy, expansion, teaching" if moon['nakshatra']['navamsa'] == "Sagittarius" else ""}{"- Capricorn/Saturn: Ambition, structure, discipline" if moon['nakshatra']['navamsa'] == "Capricorn" else ""}{"- Aquarius/Saturn: Innovation, humanitarian, unconventional" if moon['nakshatra']['navamsa'] == "Aquarius" else ""}{"- Pisces/Jupiter: Spirituality, imagination, compassion" if moon['nakshatra']['navamsa'] == "Pisces" else ""}

### Ascendant (Lagna)

| Attribute | Value |
|-----------|-------|
| **Rashi** | {asc['rashi']['full_name']} |
| **Nakshatra** | {asc['nakshatra']['name']} Pada {asc['nakshatra']['pada']} |
| **Degree** | {asc['longitude_dms']} |
| **Lagna Lord** | {asc['rashi']['ruler']} |

### Planetary Positions

{planets_table}

### Vimshottari Dasha Timeline

{dasha_table}

**Current Period:** {dasha['current_dasha']} Mahadasha

*The Mahadasha planet colors the overall theme of your life during its period. The Antardasha (sub-period) modifies how this energy manifests.*
"""


def generate_western_section(data: Dict[str, Any]) -> str:
    """Generate Western astrology analysis section."""
    western = data["western"]
    sun = western["planets"]["sun"]
    moon = western["planets"]["moon"]
    asc = western["ascendant"]
    
    planets_table = "| Planet | Sign | Degree | Retrograde |\n"
    planets_table += "|--------|------|--------|------------|\n"
    
    for planet_name in ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]:
        if planet_name in western["planets"]:
            p = western["planets"][planet_name]
            retro = "Yes ℞" if p.get("retrograde", False) else "No"
            planets_table += f"| {p['name']} | {p['sign']['sign']} | {p['sign']['degree_dms']} | {retro} |\n"
    
    return f"""
---

## Western Analysis (Tropical)

### Core Placements

| Position | Sign | Interpretation |
|----------|------|----------------|
| **Sun** | {sun['sign']['sign']} | Core identity, ego, life purpose |
| **Moon** | {moon['sign']['sign']} | Emotions, instincts, inner self |
| **Ascendant** | {asc['sign']['sign']} | Outward persona, first impressions |

### Planetary Positions

{planets_table}

### Element Balance

The distribution of planets across Fire, Earth, Air, and Water signs shapes your temperament and approach to life.
"""


def generate_chinese_section(data: Dict[str, Any]) -> str:
    """Generate Chinese astrology section."""
    chinese = data["chinese"]
    transits = data["transits_2026"]
    
    return f"""
---

## Chinese Astrology

### Your Birth Year

| Attribute | Value |
|-----------|-------|
| **Animal** | {chinese['animal']} |
| **Element** | {chinese['element']} |
| **Polarity** | {chinese['yin_yang']} |
| **Full Sign** | {chinese['full']} |

### 2026: Year of the Fire Horse

- **Starts:** February 17, 2026
- **Element:** Fire
- **Animal:** Horse

**{chinese['animal']} + Horse Compatibility:**

{"Tiger and Horse are traditionally compatible (both bold, action-oriented, independent). Fire amplifies speed and risk, so the win condition is discipline: pick one direction and move fast, instead of scattering." if chinese['animal'] == "Tiger" else f"The {chinese['animal']} interacting with the Fire Horse year brings dynamic energy. Adapt to the fast pace while staying grounded."}
"""


def generate_2026_predictions(data: Dict[str, Any]) -> str:
    """Generate 2026 predictions section."""
    transits = data["transits_2026"]
    dasha = data["vimshottari_dasha"]
    vedic = data["vedic"]
    
    # Mercury retrograde table
    merc_retro = "| Period | Sign | Guidance |\n"
    merc_retro += "|--------|------|----------|\n"
    retro_guidance = [
        "Review, revise, close loops. Avoid new contracts.",
        "Relationship communication misfires. Double-check plans.",
        "Intense review of values and priorities. Go slow on commitments."
    ]
    for i, r in enumerate(transits["mercury_retrogrades"]):
        merc_retro += f"| {r['start']} to {r['end']} | {r['sign']} | {retro_guidance[i]} |\n"
    
    # Major transits
    transit_table = "| Date | Event | Impact |\n"
    transit_table += "|------|-------|--------|\n"
    
    transit_impacts = {
        "Neptune enters Aries": "Dreams meet action. Idealism in new ventures.",
        "Saturn enters Aries": "Discipline and structure in new beginnings.",
        "Uranus enters Gemini": "Sudden changes in communication, tech, daily routines.",
        "Jupiter enters Leo (Tropical)": "Expansion through visibility, creativity, leadership.",
        "Jupiter enters Cancer (Vedic/Sidereal)": "Growth through home, emotions, nurturing.",
        "Jupiter enters Leo (Vedic/Sidereal)": "Visibility, recognition, leadership opportunities.",
        "Rahu-Ketu shift to Capricorn-Cancer": "Karmic axis shifts to career vs. home/family.",
    }
    
    for t in transits["major_transits"]:
        impact = transit_impacts.get(t["event"], "Significant shift in energy.")
        transit_table += f"| {t['date']} | {t['event']} | {impact} |\n"
    
    # Eclipses
    eclipse_table = "| Date | Type | Sign | Theme |\n"
    eclipse_table += "|------|------|------|-------|\n"
    eclipse_themes = {
        "Aquarius": "Innovation, community, self-worth",
        "Virgo": "Health, routines, service, details",
        "Leo": "Creativity, romance, self-expression",
        "Pisces": "Spirituality, endings, imagination",
    }
    for e in transits["eclipses"]:
        theme = eclipse_themes.get(e["sign"], "Transformation")
        eclipse_table += f"| {e['date']} | {e['type']} | {e['sign']} | {theme} |\n"
    
    return f"""
---

## 2026 Predictions

### Current Dasha Influence

You are in **{dasha['current_dasha']} Mahadasha**, which sets the backdrop for all 2026 experiences. This planetary period emphasizes the themes of {dasha['current_dasha']} in your life.

### Mercury Retrograde Periods

{merc_retro}

**General Mercury Retrograde Guidance:**
- Back up data and double-check travel plans
- Great for RE- activities: review, revise, reconnect, reflect
- Avoid signing major contracts or launching new ventures
- Past people and situations may return for resolution

### Major 2026 Transits

{transit_table}

### 2026 Eclipses

{eclipse_table}

**Eclipse Guidance:**
- Avoid major decisions within 1 week of eclipses
- Eclipses reveal what's hidden and accelerate change
- Best used for reflection, not initiation
"""


def generate_quarterly_playbook(data: Dict[str, Any]) -> str:
    """Generate quarterly action playbook."""
    return """
---

## 2026 Quarter-by-Quarter Playbook

### Q1 (January - March): Foundations & Reality Checks

**Key Dates:**
- Jan 26: Neptune → Aries (dreams meet action)
- Feb 13: Saturn → Aries (discipline kicks in)
- Feb 17-20: Eclipse + Chinese New Year (high-impact reset)
- Feb 26 - Mar 20: Mercury Retrograde (review mode)

**Best Use:**
- Redefine your base: living setup, health baseline, daily systems
- Close loops from 2025
- Re-negotiate rather than push forward
- Set boundaries on what you will NOT compromise on

**Focus Ratings:**
| Area | Intensity |
|------|-----------|
| Career | ⭐⭐⭐ |
| Love | ⭐⭐⭐ |
| Health | ⭐⭐⭐⭐ |
| Money | ⭐⭐⭐ |

---

### Q2 (April - June): System Upgrades

**Key Dates:**
- Apr 25: Uranus → Gemini (sudden upgrades to routines, tech, communication)
- Jun 1: Jupiter → Cancer (Vedic) - emotional/home expansion
- Jun 29: Mercury Retrograde begins
- Jun 30: Jupiter → Leo (Western) - visibility boost

**Best Use:**
- Upgrade your tools, workflows, and daily systems
- If launching, stress-test in May before Mercury Rx
- Confidence grows - use it for bold asks
- Partnerships and collaborations especially favored

**Focus Ratings:**
| Area | Intensity |
|------|-----------|
| Career | ⭐⭐⭐⭐⭐ |
| Love | ⭐⭐⭐⭐ |
| Health | ⭐⭐⭐ |
| Money | ⭐⭐⭐⭐ |

---

### Q3 (July - September): Momentum & Visibility

**Key Dates:**
- Jun 29 - Jul 23: Mercury Retrograde (relationship/communication review)
- Aug 12: Total Solar Eclipse (Leo) - identity transformation
- Aug 28: Partial Lunar Eclipse

**Best Use:**
- July: Clean up Mercury Rx messes, clarify agreements
- Aug: Eclipse month - observe, don't force outcomes
- Sep: Stabilize. Turn experiments into repeatable routines.
- Peak months for visibility, presenting, leading

**Focus Ratings:**
| Area | Intensity |
|------|-----------|
| Career | ⭐⭐⭐⭐⭐ |
| Love | ⭐⭐⭐⭐ |
| Health | ⭐⭐⭐ |
| Money | ⭐⭐⭐⭐ |

---

### Q4 (October - December): Consolidation & Pruning

**Key Dates:**
- Oct 3 - Nov 13: Venus Retrograde (relationships, values, money review)
- Oct 24 - Nov 13: Mercury Retrograde (overlaps with Venus Rx - intense!)
- Oct 31: Jupiter → Leo (Vedic) - leadership emphasis
- Dec 5: Rahu-Ketu shift (karmic reset)

**Best Use:**
- Oct-Nov: Relationship and value reckoning. Don't buy shiny distractions.
- Review what actually worked in 2026
- Prune friendships, projects, and habits that drain you
- Dec: Integrate lessons, set 2027 intentions

**Focus Ratings:**
| Area | Intensity |
|------|-----------|
| Career | ⭐⭐⭐⭐ |
| Love | ⭐⭐⭐⭐⭐ |
| Health | ⭐⭐⭐ |
| Money | ⭐⭐⭐⭐ |
"""


def generate_month_playbook() -> str:
    """Generate month-by-month quick reference."""
    return """
---

## Month-by-Month Quick Reference

| Month | Focus | Key Action |
|-------|-------|------------|
| **Jan** | Clean up loose ends | Quiet preparation; don't force outcomes |
| **Feb** | High-impact reset | Eclipse week Feb 17-20; decisions after dust settles |
| **Mar** | Review and revise | Mercury Rx; sleep + health discipline |
| **Apr** | New tools, new habits | Upgrade work systems; expect surprise inputs |
| **May** | Build with consistency | Stress-test launches; momentum builds |
| **Jun** | Confidence grows | Mercury Rx late month; double-check everything |
| **Jul** | Partnership friction possible | Clear written agreements; patience required |
| **Aug** | Eclipse month | Avoid impulsive financial moves; observe patterns |
| **Sep** | Stabilize | Turn experiments into repeatable routines |
| **Oct** | Venus Rx begins | Relationship/value review; don't buy distractions |
| **Nov** | Double retrograde | Slow down labels/commitments; reconnect with long-term people |
| **Dec** | Integration | Set 2027 goals based on what actually worked |
"""


def generate_remedies_section(data: Dict[str, Any]) -> str:
    """Generate remedies and recommendations section."""
    dasha = data["vimshottari_dasha"]
    vedic = data["vedic"]
    moon = vedic["planets"]["moon"]
    
    current_planet = dasha["current_dasha"]
    
    remedies = {
        "Sun": ("Ruby", "Om Hraam Hreem Hraum Sah Suryaya Namah", "Red, Orange", "Sunday"),
        "Moon": ("Pearl/Moonstone", "Om Shraam Shreem Shraum Sah Chandraya Namah", "White, Silver", "Monday"),
        "Mars": ("Red Coral", "Om Kraam Kreem Kraum Sah Bhaumaya Namah", "Red, Orange", "Tuesday"),
        "Mercury": ("Emerald", "Om Braam Breem Braum Sah Budhaya Namah", "Green", "Wednesday"),
        "Jupiter": ("Yellow Sapphire", "Om Graam Greem Graum Sah Gurave Namah", "Yellow, Gold", "Thursday"),
        "Venus": ("Diamond/White Sapphire", "Om Draam Dreem Draum Sah Shukraya Namah", "White, Pink", "Friday"),
        "Saturn": ("Blue Sapphire", "Om Praam Preem Praum Sah Shanaischaraya Namah", "Blue, Black", "Saturday"),
        "Rahu": ("Hessonite", "Om Bhraam Bhreem Bhraum Sah Rahave Namah", "Smoky Brown", "Saturday"),
        "Ketu": ("Cat's Eye", "Om Sraam Sreem Sraum Sah Ketave Namah", "Grey, Smoky", "Tuesday"),
    }
    
    planet_remedy = remedies.get(current_planet, remedies["Jupiter"])
    moon_remedy = remedies.get(moon["nakshatra"]["ruler"], remedies["Moon"])
    
    return f"""
---

## Remedies & Recommendations

### For {current_planet} Mahadasha (Current Period)

| Remedy Type | Recommendation |
|-------------|----------------|
| **Gemstone** | {planet_remedy[0]} (consult astrologer before wearing) |
| **Mantra** | {planet_remedy[1]} |
| **Colors** | {planet_remedy[2]} |
| **Best Day** | {planet_remedy[3]} |

### For Moon in {moon['nakshatra']['name']} (Ruled by {moon['nakshatra']['ruler']})

| Remedy Type | Recommendation |
|-------------|----------------|
| **Gemstone** | {moon_remedy[0]} |
| **Mantra** | {moon_remedy[1]} |
| **Colors** | {moon_remedy[2]} |
| **Best Day** | {moon_remedy[3]} |

### General 2026 Recommendations

**Health & Energy:**
- Prioritize sleep consistency (Fire Horse year runs hot)
- 3-4 days strength training + 2 days zone-2 cardio
- During Mercury Rx: avoid extreme sports, double-check travel

**Relationships:**
- Lead with clarity: state what you want, what you give, what you won't tolerate
- Best matches respect your independence and ambition
- Venus Rx (Oct-Nov): review, don't rush commitments

**Career & Money:**
- Ship with collaborators in H1; go deep on hard problems in H2
- Prefer compounding assets over dopamine bets
- Late-year: full cleanup of subscriptions, debts, automation

**Spiritual Practice:**
- Regular meditation (especially around eclipses)
- Journaling during retrograde periods
- Gratitude practice on your Moon nakshatra's ruling day
"""


def generate_sources_section() -> str:
    """Generate sources section."""
    return """
---

## Sources & Methodology

### Calculation Methods

- **Vedic positions:** Swiss Ephemeris (pyswisseph) with Raman ayanamsa
- **Western positions:** Swiss Ephemeris (tropical/Placidus)
- **Chinese zodiac:** Traditional lunar calendar calculations

### Transit Data Sources

- Timeanddate.com (eclipses, Mercury retrogrades)
- Drik Panchang (Vedic Jupiter/Rahu-Ketu transits)
- Major ephemeris listings for outer-planet ingresses

### Disclaimer

This report synthesizes multiple astrological traditions for self-reflection and planning purposes. Astrology is interpretive, not deterministic. Major life decisions should consider multiple factors beyond astrological timing. The author is not a licensed financial, medical, or legal advisor.

---

*Report generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""


def generate_full_report(data: Dict[str, Any]) -> str:
    """Generate complete multi-system report."""
    sections = [
        generate_executive_summary(data),
        generate_vedic_section(data),
        generate_western_section(data),
        generate_chinese_section(data),
        generate_2026_predictions(data),
        generate_quarterly_playbook(data),
        generate_month_playbook(),
        generate_remedies_section(data),
        generate_sources_section(),
    ]
    
    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Generate multi-system astrology report")
    parser.add_argument("input", help="Input JSON file from multi_system_calculator.py")
    parser.add_argument("--output", "-o", default="-", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    # Load input data
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Generate report
    report = generate_full_report(data)
    
    # Output
    if args.output == "-":
        print(report)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
