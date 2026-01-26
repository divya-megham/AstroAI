#!/usr/bin/env python3
"""
Generate LaTeX/PDF report from Vedic astrology calculation results.
"""

import json
import sys
import argparse
from typing import Dict, Any

# Nakshatra interpretations
NAKSHATRA_INTERPRETATIONS = {
    "Ashwini": "Quick-thinking, pioneering spirit, healing abilities. Natural initiative and energy for new beginnings.",
    "Bharani": "Creative, transformative energy. Ability to face life's challenges with resilience and emerge stronger.",
    "Krittika": "Sharp intellect, determination, ambitious nature. Leadership qualities with penetrating insight.",
    "Rohini": "Charming, creative, sensuous. Appreciation for beauty and comfort, magnetic personality.",
    "Mrigashira": "Curious, searching nature. Gentle yet restless energy seeking knowledge and new experiences.",
    "Ardra": "Intense emotional depth, transformative power. Ability to weather storms and emerge renewed.",
    "Punarvasu": "Optimistic, wise, generous. Ability to restore and renew, spiritual inclinations.",
    "Pushya": "Nurturing, protective, spiritual. Natural teachers and counselors with wisdom.",
    "Ashlesha": "Intuitive, mysterious, deep thinker. Powerful transformative abilities and insight.",
    "Magha": "Royal bearing, ancestral connections, leadership. Pride in heritage and noble character.",
    "Purva Phalguni": "Creative, romantic, loves pleasure. Artistic talents and appreciation for beauty.",
    "Uttara Phalguni": "Generous, helpful, socially conscious. Strong sense of duty and commitment.",
    "Hasta": "Skillful hands, clever, versatile. Ability to manifest ideas into reality.",
    "Chitra": "Artistic, beautiful, creative vision. Ability to see and create beauty in all things.",
    "Swati": "Independent, flexible, diplomatic. Natural ability to balance and harmonize.",
    "Vishakha": "Goal-oriented, determined, patient. Strong willpower and ability to achieve objectives.",
    "Anuradha": "Devoted, friendly, successful. Ability to create harmony and maintain relationships.",
    "Jyeshtha": "Protective, wise, senior energy. Natural authority and responsibility for others.",
    "Mula": "Investigative, getting to the root. Ability to uncover hidden truths and transform.",
    "Purva Ashadha": "Invincible spirit, confident, purifying. Natural ability to inspire and lead.",
    "Uttara Ashadha": "Universal, victorious, principled. Steady progress toward lasting achievements.",
    "Shravana": "Good listener, learned, connected. Ability to receive and share wisdom.",
    "Dhanishtha": "Musical, wealthy, charitable. Rhythm and harmony in life, material success.",
    "Shatabhisha": "Healing, secretive, independent. Ability to cure and protect, hidden knowledge.",
    "Purva Bhadrapada": "Passionate, transformative, intense. Ability to purify through spiritual fire.",
    "Uttara Bhadrapada": "Deep, wise, controlled. Mastery over emotions and spiritual depth.",
    "Revati": "Nurturing, protective, prosperous. Ability to guide and protect on life's journey.",
}

# Rashi interpretations
RASHI_INTERPRETATIONS = {
    "Mesha (Aries)": "Courageous, pioneering, independent. Natural leadership with dynamic energy.",
    "Vrishabha (Taurus)": "Stable, sensual, patient. Appreciation for beauty and material comfort.",
    "Mithuna (Gemini)": "Communicative, versatile, intellectual. Quick mind and adaptable nature.",
    "Karka (Cancer)": "Nurturing, emotional, protective. Deep intuition and family orientation.",
    "Simha (Leo)": "Royal, creative, confident. Natural charisma and leadership qualities.",
    "Kanya (Virgo)": "Analytical, practical, service-oriented. Attention to detail and helping others.",
    "Tula (Libra)": "Balanced, diplomatic, aesthetic. Seeking harmony and beauty in relationships.",
    "Vrishchika (Scorpio)": "Intense, transformative, powerful. Deep emotional nature and investigative mind.",
    "Dhanu (Sagittarius)": "Philosophical, optimistic, adventurous. Seeking truth and higher meaning.",
    "Makara (Capricorn)": "Ambitious, disciplined, practical. Building lasting structures and achievements.",
    "Kumbha (Aquarius)": "Innovative, humanitarian, independent. Progressive thinking and social consciousness.",
    "Meena (Pisces)": "Intuitive, compassionate, spiritual. Deep connection to the transcendent.",
}


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '°': r'$^\circ$',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def generate_latex_report(data: Dict[str, Any]) -> str:
    """Generate LaTeX document from calculation data."""
    
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
                f"        {escape_latex(p['name'])} & "
                f"{escape_latex(p['rashi']['name'])} & "
                f"{escape_latex(p['longitude_dms'])} & "
                f"{escape_latex(p['nakshatra']['name'])} & "
                f"{p['nakshatra']['pada']} & "
                f"{retro} \\\\"
            )
    
    planets_table = "\n".join(planet_rows)
    
    # Build Dasha rows
    dasha_rows = []
    for period in dasha["periods"]:
        dasha_rows.append(
            f"        {escape_latex(period['planet'])} & "
            f"{period['years']} & "
            f"{period['start']} & "
            f"{period['end']} \\\\"
        )
    dasha_table = "\n".join(dasha_rows)
    
    latex = rf"""
\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{geometry}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{xcolor}}
\usepackage{{fancyhdr}}
\usepackage{{titlesec}}
\usepackage{{parskip}}

\geometry{{margin=1in}}

\definecolor{{headerblue}}{{RGB}}{{41, 65, 114}}
\definecolor{{accentgold}}{{RGB}}{{197, 164, 103}}

\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[L]{{\textcolor{{headerblue}}{{\small Vedic Astrology Report}}}}
\fancyhead[R]{{\textcolor{{headerblue}}{{\small {escape_latex(meta['name'])}}}}}
\fancyfoot[C]{{\thepage}}

\titleformat{{\section}}{{\Large\bfseries\color{{headerblue}}}}{{}}{{0em}}{{}}[\titlerule]
\titleformat{{\subsection}}{{\large\bfseries\color{{headerblue}}}}{{}}{{0em}}{{}}

\begin{{document}}

\begin{{center}}
    {{\Huge\bfseries\textcolor{{headerblue}}{{Vedic Astrology Report}}}}
    
    \vspace{{0.5cm}}
    
    {{\LARGE {escape_latex(meta['name'])}}}
    
    \vspace{{0.3cm}}
    
    {{\large Born: {meta['birth_date']} at {meta['birth_time']}}}
    
    {{\small Location: {meta['latitude']}$^\circ$ N, {meta['longitude']}$^\circ$ E | Timezone: UTC{'+' if meta['timezone_offset'] >= 0 else ''}{meta['timezone_offset']}}}
\end{{center}}

\vspace{{0.5cm}}

\section{{Summary}}

\begin{{tabular}}{{@{{}}ll@{{}}}}
    \textbf{{Moon Sign (Rashi):}} & {escape_latex(moon_rashi)} \\
    \textbf{{Moon Nakshatra:}} & {escape_latex(moon_nakshatra)} (Pada {moon['nakshatra']['pada']}) \\
    \textbf{{Ascendant (Lagna):}} & {escape_latex(asc_rashi)} \\
    \textbf{{Nakshatra Lord:}} & {escape_latex(moon['nakshatra']['ruler'])} \\
    \textbf{{Ayanamsa:}} & Lahiri ({meta['ayanamsa']:.4f}$^\circ$) \\
\end{{tabular}}

\section{{Moon Nakshatra: {escape_latex(moon_nakshatra)}}}

\begin{{tabular}}{{@{{}}ll@{{}}}}
    \textbf{{Deity:}} & {escape_latex(moon['nakshatra']['deity'])} \\
    \textbf{{Ruling Planet:}} & {escape_latex(moon['nakshatra']['ruler'])} \\
    \textbf{{Symbol:}} & {escape_latex(moon['nakshatra']['symbol'])} \\
    \textbf{{Nature:}} & {escape_latex(moon['nakshatra']['nature'])} \\
    \textbf{{Pada:}} & {moon['nakshatra']['pada']} \\
\end{{tabular}}

\subsection{{Interpretation}}

{escape_latex(moon_interp)}

\section{{Moon Sign: {escape_latex(moon_rashi)}}}

\begin{{tabular}}{{@{{}}ll@{{}}}}
    \textbf{{Element:}} & {escape_latex(moon['rashi']['element'])} \\
    \textbf{{Quality:}} & {escape_latex(moon['rashi']['quality'])} \\
    \textbf{{Ruler:}} & {escape_latex(moon['rashi']['ruler'])} \\
    \textbf{{Position:}} & {escape_latex(moon['rashi']['degree_in_sign_dms'])} in sign \\
\end{{tabular}}

\subsection{{Interpretation}}

{escape_latex(rashi_interp)}

\section{{Planetary Positions}}

\begin{{table}}[h]
    \centering
    \begin{{tabular}}{{lccccc}}
        \toprule
        \textbf{{Planet}} & \textbf{{Sign}} & \textbf{{Longitude}} & \textbf{{Nakshatra}} & \textbf{{Pada}} & \textbf{{R}} \\
        \midrule
{planets_table}
        \bottomrule
    \end{{tabular}}
\end{{table}}

\small R = Retrograde

\section{{Vimshottari Dasha Periods}}

The Vimshottari Dasha system is based on your Moon's Nakshatra ({escape_latex(dasha['moon_nakshatra'])}). Your birth Dasha is {escape_latex(dasha['starting_dasha'])}.

\begin{{table}}[h]
    \centering
    \begin{{tabular}}{{lccc}}
        \toprule
        \textbf{{Mahadasha}} & \textbf{{Years}} & \textbf{{Start}} & \textbf{{End}} \\
        \midrule
{dasha_table}
        \bottomrule
    \end{{tabular}}
\end{{table}}

\vfill

\begin{{center}}
    \small\textit{{Generated using Swiss Ephemeris with Lahiri Ayanamsa}}
    
    \small {meta['generated_at'][:10]}
\end{{center}}

\end{{document}}
"""
    return latex


def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX report from Vedic astrology data")
    parser.add_argument("input", help="Input JSON file from vedic_calculator.py")
    parser.add_argument("--output", "-o", default="-", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    latex = generate_latex_report(data)
    
    if args.output == "-":
        print(latex)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(latex)
        print(f"LaTeX saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
