#!/usr/bin/env python3
"""Generate per-site local map SVGs for 10 haunted places."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

sites = [
    dict(
        num=1, name="Bhangarh Fort", region="Alwar, Rajasthan",
        coord="27.09°N 76.28°E",
        hub="Jaipur", hub_dist="85 km", hub_dir="W",
        hub2="Alwar", hub2_dist="56 km", hub2_dir="SW",
        rail="Dausa / Alwar Station",
        nearby=["Sariska Tiger Reserve (10 km)", "Siliserh Lake (48 km)", "Alwar Fort (56 km)"],
        description="Dense scrub forest; ruined fort complex on hilltop above plain",
        river="—",
        color="#8B4513",
    ),
    dict(
        num=2, name="Kuldhara Village", region="Jaisalmer, Rajasthan",
        coord="26.88°N 70.73°E",
        hub="Jaisalmer", hub_dist="18 km", hub_dir="NE",
        hub2="Barmer", hub2_dist="115 km", hub2_dir="S",
        rail="Jaisalmer Railway Station (18 km)",
        nearby=["Sam Sand Dunes (40 km)", "Jaisalmer Fort (18 km)", "Gadisar Lake (19 km)"],
        description="Ruined stone village in Thar Desert scrubland; ~83 roofless houses",
        river="Surrounded by sand dunes",
        color="#D4A017",
    ),
    dict(
        num=3, name="Dumas Beach", region="Surat, Gujarat",
        coord="21.06°N 72.71°E",
        hub="Surat", hub_dist="21 km", hub_dir="NW",
        hub2="Vadodara", hub2_dist="130 km", hub2_dir="N",
        rail="Surat Railway Station (21 km)",
        nearby=["Dumas Village (0 km)", "Tithal Beach (60 km)", "Udvada Fire Temple (80 km)"],
        description="Black sand beach on Arabian Sea; historically a Hindu cremation ground",
        river="Arabian Sea (west)",
        color="#5b8db5",
    ),
    dict(
        num=4, name="Dow Hill / Victoria Boys School", region="Kurseong, West Bengal",
        coord="26.88°N 88.28°E",
        hub="Siliguri", hub_dist="35 km", hub_dir="S",
        hub2="Darjeeling", hub2_dist="26 km", hub2_dir="N",
        rail="Kurseong Railway Station (2 km) — Toy Train",
        nearby=["Darjeeling (26 km)", "Tiger Hill (30 km)", "Batasia Loop (28 km)"],
        description="Dense forested hillside at 1,458 m elevation; colonial school building",
        river="Balasan River (below hill)",
        color="#2d5a2d",
    ),
    dict(
        num=5, name="Shaniwarwada Fort", region="Pune, Maharashtra",
        coord="18.52°N 73.86°E",
        hub="Pune", hub_dist="1 km", hub_dir="Central",
        hub2="Mumbai", hub2_dist="160 km", hub2_dir="NW",
        rail="Pune Junction (1.5 km)",
        nearby=["Aga Khan Palace (7 km)", "Sinhagad Fort (26 km)", "Lonavala (65 km)"],
        description="Walled fort complex in Pune city centre; partially ruined after 1828 fire",
        river="Mutha River (1 km south)",
        color="#8B0000",
    ),
    dict(
        num=6, name="Agrasen ki Baoli", region="New Delhi",
        coord="28.63°N 77.22°E",
        hub="Connaught Place", hub_dist="0.5 km", hub_dir="N",
        hub2="IGI Airport", hub2_dist="18 km", hub2_dir="SW",
        rail="Janpath Metro (500 m)",
        nearby=["India Gate (1.8 km)", "Humayun's Tomb (7 km)", "Qutub Minar (14 km)"],
        description="108-step ancient stepwell; 3 levels descending; dark water at base",
        river="Yamuna River (8 km east)",
        color="#4a3a6a",
    ),
    dict(
        num=7, name="Jamali Kamali Mosque & Tomb", region="Mehrauli, Delhi",
        coord="28.52°N 77.18°E",
        hub="Qutub Minar", hub_dist="0.5 km", hub_dir="N",
        hub2="IGI Airport", hub2_dist="12 km", hub2_dir="NW",
        rail="Qutub Minar Metro (800 m)",
        nearby=["Qutub Minar (0.5 km)", "Mehrauli Archaeological Park (0 km)", "Adham Khan's Tomb (1 km)"],
        description="16th c. mosque + twin tomb in Mehrauli Archaeological Park; forested complex",
        river="—",
        color="#4a5a3a",
    ),
    dict(
        num=8, name="Brij Raj Bhavan Palace", region="Kota, Rajasthan",
        coord="25.18°N 75.83°E",
        hub="Kota", hub_dist="1 km", hub_dir="Central",
        hub2="Jaipur", hub2_dist="247 km", hub2_dir="N",
        rail="Kota Junction (2 km)",
        nearby=["Chambal Garden (3 km)", "Garadia Mahadev (30 km)", "Ramgarh Bhand Devra (40 km)"],
        description="Heritage palace on Chambal riverbank; now a boutique hotel",
        river="Chambal River (adjacent)",
        color="#7a4a2a",
    ),
    dict(
        num=9, name="Savoy Hotel", region="Mussoorie, Uttarakhand",
        coord="30.45°N 78.07°E",
        hub="Dehradun", hub_dist="35 km", hub_dir="S",
        hub2="Haridwar", hub2_dist="89 km", hub2_dir="SE",
        rail="Dehradun Railway Station (35 km)",
        nearby=["Gun Hill (2 km)", "Kempty Falls (14 km)", "Landour (4 km)"],
        description="Colonial-era hill station hotel on the Mussoorie ridge; 2,005 m elevation",
        river="—",
        color="#3a5a6a",
    ),
    dict(
        num=10, name="Fernhill Hotel (Heritage)", region="Ooty, Tamil Nadu",
        coord="11.41°N 76.68°E",
        hub="Ooty (Udhagamandalam)", hub_dist="1 km", hub_dir="Central",
        hub2="Coimbatore", hub2_dist="88 km", hub2_dir="E",
        rail="Ooty Nilgiri Mountain Railway Station (1 km)",
        nearby=["Botanical Garden (3 km)", "Doddabetta Peak (9 km)", "Pykara Falls (20 km)"],
        description="Former Mysore royal summer palace; Gothic architecture at 2,240 m; Nilgiris",
        river="—",
        color="#5a3a6a",
    ),
]

for s in sites:
    n = s["num"]
    name = s["name"]
    region = s["region"]
    coord = s["coord"]
    hub = s["hub"]
    hd = s["hub_dist"]
    hub2 = s["hub2"]
    hd2 = s["hub2_dist"]
    rail = s["rail"]
    nearby = s["nearby"]
    desc = s["description"]
    river = s["river"]
    col = s["color"]

    # clamp nearby to 3 items
    nearby3 = nearby[:3]
    nearby_lines = "".join(
        f'<text x="22" y="{415 + i*14}" font-size="9" fill="#1a1a1a">• {item}</text>\n'
        for i, item in enumerate(nearby3)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 500" font-family="Georgia, serif">
  <rect width="760" height="500" fill="#f4f0ea"/>

  <!-- Title -->
  <text x="380" y="28" font-size="14" font-weight="bold" text-anchor="middle" fill="#1a1a1a">SITE {n:02d} — LOCAL CONTEXT MAP</text>
  <text x="380" y="46" font-size="11" font-weight="bold" text-anchor="middle" fill="{col}">{name}</text>
  <text x="380" y="62" font-size="9" font-style="italic" text-anchor="middle" fill="#555">{region} · {coord}</text>

  <!-- Map area -->
  <rect x="40" y="80" width="420" height="330" fill="#e8e0d0" stroke="#5a4030" stroke-width="1.5"/>

  <!-- Terrain filler (subtle) -->
  <rect x="40" y="80" width="420" height="330" fill="#ddd5bc" opacity="0.4"/>

  <!-- Site marker (star) -->
  <g transform="translate(250, 245)">
    <polygon points="0,-18 5,-6 18,-6 8,3 12,16 0,8 -12,16 -8,3 -18,-6 -5,-6"
             fill="{col}" stroke="#1a1a1a" stroke-width="1.5"/>
    <circle cx="0" cy="0" r="3" fill="#1a1a1a"/>
  </g>
  <text x="250" y="278" font-size="12" font-weight="bold" text-anchor="middle" fill="{col}">{name.upper()}</text>
  <text x="250" y="292" font-size="9" font-style="italic" text-anchor="middle" fill="#5a3030">{desc[:55]}{"..." if len(desc) > 55 else ""}</text>

  <!-- Hub city 1 (left of site) -->
  <circle cx="100" cy="200" r="8" fill="#3a2a20" stroke="#1a1a1a" stroke-width="1"/>
  <text x="100" y="220" font-size="10" font-weight="bold" text-anchor="middle" fill="#1a1a1a">{hub}</text>
  <!-- Road from hub to site -->
  <path d="M 108,200 L 232,242" fill="none" stroke="#888" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="162" y="228" font-size="8" fill="#555" transform="rotate(15 162 228)">{hd}</text>

  <!-- Hub city 2 (right of site) -->
  <circle cx="390" cy="160" r="7" fill="#3a2a20" stroke="#1a1a1a" stroke-width="1"/>
  <text x="390" y="178" font-size="10" font-weight="bold" text-anchor="middle" fill="#1a1a1a">{hub2}</text>
  <!-- Road from hub2 to site -->
  <path d="M 383,163 L 268,242" fill="none" stroke="#888" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="330" y="205" font-size="8" fill="#555" transform="rotate(-20 330 205)">{hd2}</text>

  <!-- Railway symbol -->
  <g transform="translate(130, 310)">
    <rect x="-15" y="-6" width="30" height="12" fill="none" stroke="#3a2a20" stroke-width="1"/>
    <line x1="-15" y1="0" x2="15" y2="0" stroke="#3a2a20" stroke-width="0.8"/>
    <circle cx="-10" cy="0" r="3" fill="#3a2a20"/>
    <circle cx="10" cy="0" r="3" fill="#3a2a20"/>
  </g>
  <text x="152" y="314" font-size="8" fill="#1a1a1a">{rail[:38]}{"..." if len(rail) > 38 else ""}</text>

  <!-- Compass -->
  <g transform="translate(430, 110)">
    <circle cx="0" cy="0" r="18" fill="#fff" stroke="#5a4030" stroke-width="1.2"/>
    <polygon points="0,-12 4,0 0,12 -4,0" fill="{col}"/>
    <text x="0" y="-22" font-size="10" font-weight="bold" text-anchor="middle" fill="#3a2a20">N</text>
  </g>

  <!-- Right panel: info boxes -->
  <rect x="478" y="80" width="242" height="330" fill="#fff" stroke="#5a4030" stroke-width="1.2"/>

  <rect x="478" y="80" width="242" height="28" fill="{col}"/>
  <text x="599" y="99" font-size="10" font-weight="bold" text-anchor="middle" fill="#fff">QUICK FACTS</text>

  <text x="490" y="126" font-size="9" font-weight="bold" fill="#8B0000">REGION</text>
  <text x="490" y="140" font-size="9" fill="#1a1a1a">{region}</text>
  <line x1="490" y1="148" x2="710" y2="148" stroke="#ddd" stroke-width="0.8"/>

  <text x="490" y="163" font-size="9" font-weight="bold" fill="#8B0000">COORDINATES</text>
  <text x="490" y="177" font-size="9" fill="#1a1a1a">{coord}</text>
  <line x1="490" y1="185" x2="710" y2="185" stroke="#ddd" stroke-width="0.8"/>

  <text x="490" y="200" font-size="9" font-weight="bold" fill="#8B0000">NEAREST HUB</text>
  <text x="490" y="214" font-size="9" fill="#1a1a1a">{hub} · {hd}</text>
  <line x1="490" y1="222" x2="710" y2="222" stroke="#ddd" stroke-width="0.8"/>

  <text x="490" y="237" font-size="9" font-weight="bold" fill="#8B0000">RAIL</text>
  <text x="490" y="251" font-size="9" fill="#1a1a1a">{rail[:38]}{"..." if len(rail) > 38 else ""}</text>
  <line x1="490" y1="259" x2="710" y2="259" stroke="#ddd" stroke-width="0.8"/>

  <text x="490" y="274" font-size="9" font-weight="bold" fill="#8B0000">RIVER NEARBY</text>
  <text x="490" y="288" font-size="9" fill="#1a1a1a">{river}</text>
  <line x1="490" y1="296" x2="710" y2="296" stroke="#ddd" stroke-width="0.8"/>

  <text x="490" y="311" font-size="9" font-weight="bold" fill="#8B0000">NEARBY ATTRACTIONS</text>
  {nearby_lines}

  <text x="380" y="490" font-size="8" font-style="italic" text-anchor="middle" fill="#888">
    Stylized map — positions approximate; for orientation only
  </text>
</svg>"""

    path = os.path.join(OUT, f"map_{n:02d}.svg")
    with open(path, "w") as fh:
        fh.write(svg)
    print(f"Written: {path}")

print("All maps generated.")
