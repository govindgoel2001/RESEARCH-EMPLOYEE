#!/usr/bin/env python3
"""Generate per-site historical timeline SVGs for 10 haunted places."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

sites = [
    dict(num=1, name="Bhangarh Fort", color="#8B4513",
         events=[
             ("1573", "above", "Built by Raja\nBhagwant Das"),
             ("1613", "below", "Abandoned after\nchief Ajab Singh"),
             ("1720", "above", "Mughal decline;\nfort falls quiet"),
             ("1947", "below", "Post-Independence;\nASI takes over"),
             ("1990s", "above", "Night ban issued;\nmost haunted label"),
             ("Present", "below", "Tourist site;\nASI managed"),
         ]),
    dict(num=2, name="Kuldhara Village", color="#D4A017",
         events=[
             ("~1291", "above", "Palliwal Brahmins\nsettle Kuldhara"),
             ("~1825", "below", "Overnight mass\nexodus; village abandoned"),
             ("1947", "above", "Post-Independence;\nsite undisturbed"),
             ("2000s", "below", "Rajasthan tourism\ndevelops the site"),
             ("2010", "above", "Entry fee; light &\nsound show added"),
             ("Present", "below", "Managed ruins;\npopular day-trip from Jaisalmer"),
         ]),
    dict(num=3, name="Dumas Beach", color="#5b8db5",
         events=[
             ("Medieval", "above", "Hindu cremation\nground established"),
             ("British era", "below", "Beach used for\ncremations; taboo grows"),
             ("1960s-80s", "above", "Beach becomes\npopular picnic spot"),
             ("2000s", "below", "Night restriction\nreportedly imposed"),
             ("2010s", "above", "Viral internet\nhaunted beach fame"),
             ("Present", "below", "Beach open by day;\nnight visits discouraged"),
         ]),
    dict(num=4, name="Dow Hill / Victoria Boys School", color="#2d5a2d",
         events=[
             ("1879", "above", "Victoria Boys School\nfounded by British"),
             ("1900s", "below", "Worker deaths\nduring school holidays"),
             ("1947", "above", "School renamed;\ncontinues under state"),
             ("1980s", "below", "Paranormal stories\ncirculate locally"),
             ("2000s", "above", "TV & YouTube\nexplorations popularise"),
             ("Present", "below", "Functioning school;\nforest path still feared"),
         ]),
    dict(num=5, name="Shaniwarwada Fort", color="#8B0000",
         events=[
             ("1736", "above", "Built by Peshwa\nBajirao I"),
             ("1773", "below", "Narayanrao Peshwa\nmurdered inside"),
             ("1818", "above", "Peshwa power ends;\nBritish take Pune"),
             ("1828", "below", "Mysterious fire\ndamages most of fort"),
             ("1858", "above", "Full British control;\nfort as barracks"),
             ("Present", "below", "ASI protected ruins;\nnightly light show"),
         ]),
    dict(num=6, name="Agrasen ki Baoli", color="#4a3a6a",
         events=[
             ("~10th c.", "above", "Original baoli\nbuilt (Agrawal legend)"),
             ("~14th c.", "below", "Rebuilt/expanded by\nAgrawal community"),
             ("Mughal era", "above", "Used as water\nstep-well; city expands"),
             ("British era", "below", "Falls out of use;\npartially filled"),
             ("1968", "above", "ASI declares it\nprotected monument"),
             ("Present", "below", "Open to visitors;\npopular photography spot"),
         ]),
    dict(num=7, name="Jamali Kamali Mosque & Tomb", color="#4a5a3a",
         events=[
             ("~1528", "above", "Jamali (Shaikh\nFazlullah) builds mosque"),
             ("1535", "below", "Jamali dies; buried\nin twin tomb"),
             ("1535+", "above", "Kamali buried;\nidentity never recorded"),
             ("Mughal era", "below", "Tomb maintained by\nMughal court patronage"),
             ("1947", "above", "ASI takes over\nMehrauli complex"),
             ("Present", "below", "Mosque locked to\nvisitors; tomb open"),
         ]),
    dict(num=8, name="Brij Raj Bhavan, Kota", color="#7a4a2a",
         events=[
             ("~1830s", "above", "Palace built by\nMaharao Kishore Singh"),
             ("1857", "below", "Major Burton killed\nduring Sepoy Mutiny"),
             ("1858", "above", "British resume\ncontrol of Kota"),
             ("1947", "below", "Palace handed over\nto Kota royal family"),
             ("1980s", "above", "Converted to\nheritage hotel"),
             ("Present", "below", "Operating WelcomHeritage\nhotel; Room 1 famous"),
         ]),
    dict(num=9, name="Savoy Hotel, Mussoorie", color="#3a5a6a",
         events=[
             ("1902", "above", "Hotel opened by\nFrederick Wilson"),
             ("1911", "below", "Frances Clubb dies\n(poisoning suspected)"),
             ("1912", "above", "John Eastman murder\ncase at the hotel"),
             ("1926", "below", "Agatha Christie visits;\ninspires fiction"),
             ("1947", "above", "Post-Independence;\ncontinues as hotel"),
             ("Present", "below", "Operating hotel;\nhistoric reputation intact"),
         ]),
    dict(num=10, name="Fernhill Hotel, Ooty", color="#5a3a6a",
         events=[
             ("~1844", "above", "Built as Mysore\nroyal summer palace"),
             ("1947", "below", "Post-Independence;\npassed to new owners"),
             ("1976", "above", "Converted to\nheritage hotel"),
             ("1992", "below", "Featured in Mani\nRatnam's Roja"),
             ("2000s", "above", "Haunted stories\ngo viral online"),
             ("2010s+", "below", "Hotel operational\nbut visitor numbers fall"),
         ]),
]

for s in sites:
    n = s["num"]
    name = s["name"]
    color = s["color"]
    events = s["events"]

    # 6 events spread across a horizontal line
    x_positions = [80, 178, 280, 380, 480, 580]
    line_y = 220

    event_svgs = ""
    for i, (year, direction, label) in enumerate(events):
        x = x_positions[i]
        lines = label.split("\n")
        if direction == "above":
            # Text above line
            y_text_start = line_y - 60 - (len(lines) - 1) * 12
            connector_y1 = line_y - 8
            connector_y2 = line_y - 30
            text_block = ""
            for j, line in enumerate(lines):
                text_block += f'<text x="{x}" y="{y_text_start + j*13}" font-size="9" text-anchor="middle" fill="#1a1a1a">{line}</text>\n'
            event_svgs += f"""
    <!-- Event {i+1} above -->
    <circle cx="{x}" cy="{line_y}" r="6" fill="{color}" stroke="#1a1a1a" stroke-width="1.2"/>
    <line x1="{x}" y1="{connector_y1}" x2="{x}" y2="{connector_y2}" stroke="{color}" stroke-width="1.2"/>
    <text x="{x}" y="{line_y - 68}" font-size="10" font-weight="bold" text-anchor="middle" fill="{color}">{year}</text>
    {text_block}"""
        else:
            # Text below line
            y_text_start = line_y + 35
            connector_y1 = line_y + 8
            connector_y2 = line_y + 28
            text_block = ""
            for j, line in enumerate(lines):
                text_block += f'<text x="{x}" y="{y_text_start + j*13}" font-size="9" text-anchor="middle" fill="#1a1a1a">{line}</text>\n'
            event_svgs += f"""
    <!-- Event {i+1} below -->
    <circle cx="{x}" cy="{line_y}" r="6" fill="{color}" stroke="#1a1a1a" stroke-width="1.2"/>
    <line x1="{x}" y1="{connector_y1}" x2="{x}" y2="{connector_y2}" stroke="{color}" stroke-width="1.2"/>
    <text x="{x}" y="{line_y + 22}" font-size="10" font-weight="bold" text-anchor="middle" fill="{color}">{year}</text>
    {text_block}"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 380" font-family="Georgia, serif">
  <rect width="700" height="380" fill="#f9f4ed"/>

  <text x="350" y="28" font-size="15" font-weight="bold" text-anchor="middle" fill="#1a1a1a">SITE {n:02d} — HISTORICAL TIMELINE</text>
  <text x="350" y="46" font-size="11" font-weight="bold" text-anchor="middle" fill="{color}">{name}</text>

  <!-- Timeline backbone -->
  <line x1="60" y1="{line_y}" x2="640" y2="{line_y}" stroke="#3a2a20" stroke-width="2.5"/>
  <polygon points="640,{line_y} 630,{line_y - 5} 630,{line_y + 5}" fill="#3a2a20"/>

  {event_svgs}

  <text x="350" y="370" font-size="8" font-style="italic" text-anchor="middle" fill="#888">
    Timeline is approximate; some dates inferred from regional history
  </text>
</svg>"""

    path = os.path.join(OUT, f"timeline_{n:02d}.svg")
    with open(path, "w") as fh:
        fh.write(svg)
    print(f"Written: {path}")

print("All timelines generated.")
