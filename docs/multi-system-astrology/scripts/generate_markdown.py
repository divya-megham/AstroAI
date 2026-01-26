#!/usr/bin/env python3
"""
Generate Markdown report from Vedic astrology calculation results.
"""

import json
import sys
import argparse
from typing import Dict, Any

# Nakshatra interpretations
NAKSHATRA_INTERPRETATIONS = {
    "Ashwini": "Quick-thinking, pioneering spirit, healing abilities. Natural initiative and energy for new beginnings. The Ashwini Kumaras, divine physicians, bless natives with swift action and recuperative powers.",
    "Bharani": "Creative, transformative energy. Ability to face life's challenges with resilience and emerge stronger. Ruled by Yama, lord of dharma, natives possess strong moral character and creative power.",
    "Krittika": "Sharp intellect, determination, ambitious nature. Leadership qualities with penetrating insight. The fire god Agni grants purifying energy and the courage to cut through obstacles.",
    "Rohini": "Charming, creative, sensuous. Appreciation for beauty and comfort, magnetic personality. Brahma's favorite lunar mansion bestows artistic gifts and material prosperity.",
    "Mrigashira": "Curious, searching nature. Gentle yet restless energy seeking knowledge and new experiences. The deer's head symbolizes the eternal quest for truth and beauty.",
    "Ardra": "Intense emotional depth, transformative power. Ability to weather storms and emerge renewed. Rudra's star brings the power to destroy old patterns and create anew.",
    "Punarvasu": "Optimistic, wise, generous. Ability to restore and renew, spiritual inclinations. Mother Aditi's blessing provides protection and the gift of returning to wholeness.",
    "Pushya": "Nurturing, protective, spiritual. Natural teachers and counselors with wisdom. Considered the most auspicious Nakshatra, governed by Brihaspati (Jupiter's wisdom).",
    "Ashlesha": "Intuitive, mysterious, deep thinker. Powerful transformative abilities and insight. The serpent energy brings kundalini power and psychological depth.",
    "Magha": "Royal bearing, ancestral connections, leadership. Pride in heritage and noble character. The Pitris (ancestors) bestow authority and connection to lineage.",
    "Purva Phalguni": "Creative, romantic, loves pleasure. Artistic talents and appreciation for beauty. Bhaga, god of good fortune, grants enjoyment and creative expression.",
    "Uttara Phalguni": "Generous, helpful, socially conscious. Strong sense of duty and commitment. Aryaman, god of patronage, brings lasting relationships and social success.",
    "Hasta": "Skillful hands, clever, versatile. Ability to manifest ideas into reality. Savitar, the creative sun god, bestows dexterity and the power to grasp opportunities.",
    "Chitra": "Artistic, beautiful, creative vision. Ability to see and create beauty in all things. Vishwakarma, the divine architect, grants artistic genius and aesthetic refinement.",
    "Swati": "Independent, flexible, diplomatic. Natural ability to balance and harmonize. Vayu, the wind god, provides adaptability and the freedom to grow.",
    "Vishakha": "Goal-oriented, determined, patient. Strong willpower and ability to achieve objectives. Indra-Agni's dual rulership brings success through persistent effort.",
    "Anuradha": "Devoted, friendly, successful. Ability to create harmony and maintain relationships. Mitra, god of friendship, blesses with loyal companions and organizational abilities.",
    "Jyeshtha": "Protective, wise, senior energy. Natural authority and responsibility for others. Indra's star brings leadership, though with the weight of responsibility.",
    "Mula": "Investigative, getting to the root. Ability to uncover hidden truths and transform. Nirriti's energy dissolves illusions and reveals fundamental realities.",
    "Purva Ashadha": "Invincible spirit, confident, purifying. Natural ability to inspire and lead. The water deity Apas grants the power to cleanse and invigorate.",
    "Uttara Ashadha": "Universal, victorious, principled. Steady progress toward lasting achievements. The Vishvadevas (universal gods) bestow ultimate success and integrity.",
    "Shravana": "Good listener, learned, connected. Ability to receive and share wisdom. Vishnu's star provides the gift of hearing truth and spreading knowledge.",
    "Dhanishtha": "Musical, wealthy, charitable. Rhythm and harmony in life, material success. The Vasus, gods of abundance, grant prosperity and musical talent.",
    "Shatabhisha": "Healing, secretive, independent. Ability to cure and protect, hidden knowledge. Varuna's star brings the power to heal and access cosmic waters of consciousness.",
    "Purva Bhadrapada": "Passionate, transformative, intense. Ability to purify through spiritual fire. Aja Ekapada (one-footed goat) represents transcendence and spiritual intensity.",
    "Uttara Bhadrapada": "Deep, wise, controlled. Mastery over emotions and spiritual depth. Ahir Budhnya, the serpent of the deep, grants wisdom and emotional stability.",
    "Revati": "Nurturing, protective, prosperous. Ability to guide and protect on life's journey. Pushan, the shepherd god, provides safe passage and nourishment.",
}

# Rashi interpretations
RASHI_INTERPRETATIONS = {
    "Mesha (Aries)": "The Moon in Aries creates an emotionally dynamic and pioneering personality. You respond to life with courage and initiative, preferring action over deliberation. Your emotional nature is straightforward and honest, though sometimes impulsive. Leadership comes naturally, and you feel most alive when pursuing new challenges.",
    "Vrishabha (Taurus)": "The Moon is exalted in Taurus, creating emotional stability and a deep appreciation for sensory pleasures. You find comfort in material security and beautiful surroundings. Patient and determined, you build lasting foundations in life. Relationships are approached with loyalty and a desire for permanence.",
    "Mithuna (Gemini)": "The Moon in Gemini creates a mentally active and communicative emotional nature. You process feelings through analysis and conversation. Curious and adaptable, you thrive on variety and intellectual stimulation. Your emotions may fluctuate, reflecting your dual nature.",
    "Karka (Cancer)": "The Moon rules Cancer, making this its most powerful placement. Deep emotional sensitivity and strong intuition guide your life. Family and home provide your greatest source of comfort. You possess natural nurturing abilities and a powerful emotional memory.",
    "Simha (Leo)": "The Moon in Leo creates a warm, generous, and expressive emotional nature. You need recognition and appreciation to feel emotionally fulfilled. Creative self-expression comes naturally, and you approach life with dignity and confidence. Leadership in family matters is often your role.",
    "Kanya (Virgo)": "The Moon in Virgo creates an analytical and service-oriented emotional nature. You find comfort in helping others and maintaining order. Attention to detail extends to emotional matters, and you may analyze feelings thoroughly. Health and daily routines significantly affect your emotional well-being.",
    "Tula (Libra)": "The Moon in Libra creates a strong need for harmony and balanced relationships. You process emotions through the lens of fairness and aesthetics. Partnership is essential to your emotional fulfillment. You possess natural diplomatic abilities and refined tastes.",
    "Vrishchika (Scorpio)": "The Moon in Scorpio (debilitated) creates intense emotional depth and transformative experiences. You feel everything deeply and possess powerful intuition. Privacy is important, and you may guard your emotions carefully. Transformation through emotional intensity is a life theme.",
    "Dhanu (Sagittarius)": "The Moon in Sagittarius creates an optimistic and philosophically-inclined emotional nature. You need freedom and meaning to feel emotionally fulfilled. Adventure and learning bring joy. Your emotional approach is honest and expansive, seeking truth and wisdom.",
    "Makara (Capricorn)": "The Moon in Capricorn creates a serious and responsible emotional nature. You find security through achievement and social position. Emotions are controlled and channeled toward practical goals. Maturity comes early, and you often take on responsibility for others.",
    "Kumbha (Aquarius)": "The Moon in Aquarius creates a unique and humanitarian emotional nature. You need intellectual freedom and social connection to thrive. Progressive ideas inspire you, and you value friendship highly. Emotional detachment can provide perspective but may sometimes create distance.",
    "Meena (Pisces)": "The Moon in Pisces creates a deeply intuitive and compassionate emotional nature. You absorb the feelings of others and may need time alone to process. Creative and spiritual pursuits bring emotional fulfillment. Your sensitivity is a gift that connects you to the transcendent.",
}


def generate_markdown_report(data: Dict[str, Any]) -> str:
    """Generate Markdown document from calculation data."""
    
    meta = data["meta"]
    moon = data["moon"]
    asc = data["ascendant"]
    dasha = data["vimshottari_dasha"]
    
    moon_nakshatra = moon["nakshatra"]["name"]
    moon_rashi = moon["rashi"]["name"]
    asc_rashi = asc["rashi"]["name"]
    
    moon_interp = NAKSHATRA_INTERPRETATIONS.get(moon_nakshatra, "")
    rashi_interp = RASHI_INTERPRETATIONS.get(moon_rashi, "")
    
    # Build planet rows for table
    planet_rows = []
    for planet_key in ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]:
        if planet_key in data and "error" not in data[planet_key]:
            p = data[planet_key]
            retro = "R" if p.get("retrograde", False) else ""
            planet_rows.append(
                f"| {p['name']} | {p['rashi']['name']} | {p['longitude_dms']} | "
                f"{p['nakshatra']['name']} | {p['nakshatra']['pada']} | {retro} |"
            )
    
    planets_table = "\n".join(planet_rows)
    
    # Build Dasha rows
    dasha_rows = []
    for period in dasha["periods"]:
        dasha_rows.append(
            f"| {period['planet']} | {period['years']} | {period['start']} | {period['end']} |"
        )
    dasha_table = "\n".join(dasha_rows)
    
    md = f"""# Vedic Astrology Report

## {meta['name']}

**Birth Date:** {meta['birth_date']}  
**Birth Time:** {meta['birth_time']}  
**Location:** {meta['latitude']}° N, {meta['longitude']}° E  
**Timezone:** UTC{'+' if meta['timezone_offset'] >= 0 else ''}{meta['timezone_offset']}

---

## Summary

| Aspect | Value |
|--------|-------|
| **Moon Sign (Rashi)** | {moon_rashi} |
| **Moon Nakshatra** | {moon_nakshatra} (Pada {moon['nakshatra']['pada']}) |
| **Ascendant (Lagna)** | {asc_rashi} |
| **Nakshatra Lord** | {moon['nakshatra']['ruler']} |
| **Ayanamsa** | Lahiri ({meta['ayanamsa']:.4f}°) |

---

## Moon Nakshatra: {moon_nakshatra}

| Attribute | Value |
|-----------|-------|
| **Deity** | {moon['nakshatra']['deity']} |
| **Ruling Planet** | {moon['nakshatra']['ruler']} |
| **Symbol** | {moon['nakshatra']['symbol']} |
| **Nature** | {moon['nakshatra']['nature']} |
| **Pada** | {moon['nakshatra']['pada']} |

### Interpretation

{moon_interp}

---

## Moon Sign: {moon_rashi}

| Attribute | Value |
|-----------|-------|
| **Element** | {moon['rashi']['element']} |
| **Quality** | {moon['rashi']['quality']} |
| **Ruler** | {moon['rashi']['ruler']} |
| **Position** | {moon['rashi']['degree_in_sign_dms']} in sign |

### Interpretation

{rashi_interp}

---

## Planetary Positions

| Planet | Sign | Longitude | Nakshatra | Pada | R |
|--------|------|-----------|-----------|------|---|
{planets_table}

*R = Retrograde*

---

## Vimshottari Dasha Periods

The Vimshottari Dasha system is based on your Moon's Nakshatra ({dasha['moon_nakshatra']}). Your birth Dasha is **{dasha['starting_dasha']}**.

| Mahadasha | Years | Start | End |
|-----------|-------|-------|-----|
{dasha_table}

---

*Generated using Swiss Ephemeris with Lahiri Ayanamsa*  
*Report Date: {meta['generated_at'][:10]}*
"""
    return md


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown report from Vedic astrology data")
    parser.add_argument("input", help="Input JSON file from vedic_calculator.py")
    parser.add_argument("--output", "-o", default="-", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    markdown = generate_markdown_report(data)
    
    if args.output == "-":
        print(markdown)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"Markdown saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
