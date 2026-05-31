#!/usr/bin/env python3
"""Generate per-site evidence pyramid SVGs."""

import os

def make_pyramid(site_num, site_name, verified_items, documented_items, theory_items, folklore_items, speculation_items, out_dir):
    """Render an evidence pyramid SVG for one site."""

    def wrap(items, max_w=52):
        """Wrap item list into ≤max_w-char lines for SVG text."""
        lines = []
        for item in items:
            if len(item) <= max_w:
                lines.append(item)
            else:
                words = item.split()
                cur = ""
                for w in words:
                    if not cur:
                        cur = w
                    elif len(cur) + 1 + len(w) <= max_w:
                        cur += " " + w
                    else:
                        lines.append(cur)
                        cur = w
                if cur:
                    lines.append(cur)
        return lines

    v = wrap(verified_items)
    d = wrap(documented_items)
    t = wrap(theory_items)
    f = wrap(folklore_items)
    s = wrap(speculation_items)

    def lines_svg(items_lines, x, y_start, dy=11, color="#1a1a1a", font_size=8):
        out = ""
        for i, line in enumerate(items_lines):
            out += f'<text x="{x}" y="{y_start + i*dy}" font-size="{font_size}" fill="{color}">{line}</text>\n'
        return out

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" font-family="Georgia, serif">
  <rect width="800" height="480" fill="#f9f4ed"/>

  <text x="400" y="28" font-size="15" font-weight="bold" text-anchor="middle" fill="#1a1a1a">SITE {site_num} — EVIDENCE PYRAMID</text>
  <text x="400" y="46" font-size="11" font-style="italic" text-anchor="middle" fill="#8B0000">{site_name}</text>

  <!-- Tier 1: VERIFIED (top, narrow) -->
  <polygon points="355,75 445,75 462,110 338,110" fill="#2c5a2c" stroke="#1a1a1a" stroke-width="1"/>
  <text x="400" y="97" font-size="11" font-weight="bold" text-anchor="middle" fill="#fff">VERIFIED</text>

  <!-- Tier 2: DOCUMENTED -->
  <polygon points="338,114 462,114 482,152 318,152" fill="#5b8db5" stroke="#1a1a1a" stroke-width="1"/>
  <text x="400" y="137" font-size="11" font-weight="bold" text-anchor="middle" fill="#fff">DOCUMENTED</text>

  <!-- Tier 3: THEORY/INFERRED -->
  <polygon points="318,156 482,156 505,197 295,197" fill="#d4a574" stroke="#1a1a1a" stroke-width="1"/>
  <text x="400" y="181" font-size="11" font-weight="bold" text-anchor="middle" fill="#1a1a1a">INFERRED / THEORY</text>

  <!-- Tier 4: FOLKLORE -->
  <polygon points="295,201 505,201 532,245 268,245" fill="#c97a5a" stroke="#1a1a1a" stroke-width="1"/>
  <text x="400" y="227" font-size="11" font-weight="bold" text-anchor="middle" fill="#fff">FOLKLORE</text>

  <!-- Tier 5: SPECULATION (base) -->
  <polygon points="268,249 532,249 565,295 235,295" fill="#888" stroke="#1a1a1a" stroke-width="1"/>
  <text x="400" y="276" font-size="11" font-weight="bold" text-anchor="middle" fill="#fff">SPECULATION / RUMOUR</text>

  <!-- Right column: examples -->
  <text x="578" y="93" font-size="8" font-weight="bold" fill="#2c5a2c">VERIFIED</text>
  {lines_svg(v, 578, 103, color="#1a1a1a")}
  <line x1="462" y1="93" x2="575" y2="93" stroke="#2c5a2c" stroke-width="0.6"/>

  <text x="578" y="{"133"}" font-size="8" font-weight="bold" fill="#5b8db5">DOCUMENTED</text>
  {lines_svg(d, 578, 143, color="#1a1a1a")}
  <line x1="482" y1="133" x2="575" y2="133" stroke="#5b8db5" stroke-width="0.6"/>

  <text x="578" y="180" font-size="8" font-weight="bold" fill="#8a6532">INFERRED</text>
  {lines_svg(t, 578, 190, color="#1a1a1a")}
  <line x1="505" y1="180" x2="575" y2="180" stroke="#8a6532" stroke-width="0.6"/>

  <text x="578" y="222" font-size="8" font-weight="bold" fill="#8b3a1a">FOLKLORE</text>
  {lines_svg(f, 578, 232, color="#1a1a1a")}
  <line x1="532" y1="222" x2="575" y2="222" stroke="#8b3a1a" stroke-width="0.6"/>

  <text x="578" y="268" font-size="8" font-weight="bold" fill="#555">SPECULATION</text>
  {lines_svg(s, 578, 278, color="#1a1a1a")}
  <line x1="565" y1="268" x2="575" y2="268" stroke="#555" stroke-width="0.6"/>

  <!-- Left column: criteria -->
  <line x1="338" y1="93" x2="222" y2="93" stroke="#2c5a2c" stroke-width="0.6"/>
  <text x="220" y="96" font-size="8" text-anchor="end" fill="#2c5a2c">→ multi-source, physical evidence</text>

  <line x1="318" y1="133" x2="222" y2="133" stroke="#5b8db5" stroke-width="0.6"/>
  <text x="220" y="136" font-size="8" text-anchor="end" fill="#5b8db5">→ newspaper/official records</text>

  <line x1="295" y1="180" x2="222" y2="180" stroke="#8a6532" stroke-width="0.6"/>
  <text x="220" y="183" font-size="8" text-anchor="end" fill="#8a6532">→ logical inference</text>

  <line x1="268" y1="222" x2="222" y2="222" stroke="#8b3a1a" stroke-width="0.6"/>
  <text x="220" y="225" font-size="8" text-anchor="end" fill="#8b3a1a">→ oral tradition only</text>

  <line x1="235" y1="268" x2="222" y2="268" stroke="#555" stroke-width="0.6"/>
  <text x="220" y="271" font-size="8" text-anchor="end" fill="#555">→ no verifiable source</text>

  <text x="400" y="470" font-size="8" font-style="italic" text-anchor="middle" fill="#888">
    All claims in Site {site_num}'s section are tagged with one of these tiers
  </text>
</svg>"""

    path = os.path.join(out_dir, f"pyramid_{site_num:02d}.svg")
    with open(path, "w") as fh:
        fh.write(svg)
    print(f"Written: {path}")


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))

    data = [
        (1, "Bhangarh Fort, Alwar, Rajasthan",
         ["Fort ruins physically exist", "Built ~1573 CE by Raja Bhagwant Das", "Part of Sariska Tiger Reserve"],
         ["ASI maintains site; notice board warns against night visits", "Listed as most haunted place by ASI signage", "Filming by media channels documented"],
         ["Singhia the sorcerer placed a curse (inferred from legend pattern)"],
         ["Sorcerer cursed princess, entire city died overnight", "Princess Ratnawati's spirit wanders the ruins"],
         ["Visitors go missing overnight", "Certain death awaits night visitors"]),

        (2, "Kuldhara Village, Jaisalmer, Rajasthan",
         ["~83 ruined stone houses exist", "Village abandoned overnight in ~1825 CE", "Archaeological evidence of sudden desertion"],
         ["Palliwal Brahmin settlement documented in historical records", "Entry managed by state tourism; ₹10 fee"],
         ["Diwan Salim Singh demanded the chief's daughter", "Mass migration overnight to preserve honor"],
         ["Paliwalas cursed the land so no one would ever live there", "Anyone who tries to settle dies within days"],
         ["Screams heard at night", "Paranormal investigators' equipment fails here"]),

        (3, "Dumas Beach, Surat, Gujarat",
         ["Beach physically exists on Arabian Sea coast", "Known as a Hindu cremation ground historically"],
         ["Cremation history documented in local records", "Police reportedly restricted night access (unverified single-source)"],
         ["Spirits of the cremated dead wander the beach at night"],
         ["Whispers and voices heard near the shore at night", "People reported to vanish walking on the beach"],
         ["Treasure buried under the beach", "Entire stretch is supernaturally dangerous"]),

        (4, "Dow Hill, Kurseong, West Bengal",
         ["Victoria Boys School (1879) physically exists", "Death Road (forest path) is real"],
         ["Several workers' deaths reported during school holidays", "Locals documented fear of the forest stretch"],
         ["Headless boy ghost is a reinterpretation of logging/worker accidents"],
         ["Headless boy seen walking in the forest", "Red eyes seen in the dark", "Footsteps in the school corridors during holidays"],
         ["Mass hauntings every December", "The forest drives people to suicide"]),

        (5, "Shaniwarwada Fort, Pune, Maharashtra",
         ["Fort built 1736 CE by Peshwa Bajirao I", "Ruins exist; under ASI protection", "Narayanrao Peshwa murdered here in 1773"],
         ["Murder of Narayanrao by Raghoba faction is historically documented", "Fort partially destroyed by fire in 1828"],
         ["Ghost screams are an echo of the murder night"],
         ["Narayanrao's ghost screams 'Kaka mala vachwa' (Uncle save me) on full moon nights", "Ghost of the murdered boy prince walks the ruins"],
         ["Fort emits supernatural energy", "Anyone staying past midnight faces death"]),

        (6, "Agrasen ki Baoli, New Delhi",
         ["Stepwell (baoli) physically exists", "Located on Hailey Road, Connaught Place, New Delhi", "Under ASI protection; open to visitors"],
         ["Baoli dated to ~10th century (rebuilt by Agrawal community ~14th c.)", "108 steps, 3 levels; architecturally significant"],
         ["Dark water historically present in baoli created 'pull' sensation (physics)"],
         ["Black water pulls people in psychologically", "People feel compelled to jump into the well"],
         ["Djinn/evil spirits live in the water", "Cameras malfunction inside"]),

        (7, "Jamali Kamali Mosque & Tomb, Delhi",
         ["Mosque and twin tomb physically exist in Mehrauli", "Jamali = Shaikh Fazlullah (poet-saint, d. 1535 CE)", "Under ASI protection"],
         ["Jamali's poetry exists (Persian; in museums)", "Kamali's identity undocumented even in official records"],
         ["Kamali's identity mystery generates paranormal speculation"],
         ["Red marks appear on visitors' skin", "Strange laughter heard", "Evil entity attacks lone visitors"],
         ["Kamali was Jamali's male lover (unverified)", "Djinns guard the tomb"]),

        (8, "Brij Raj Bhavan, Kota, Rajasthan",
         ["Palace built ~1830s by Maharao Kishore Singh", "Now a heritage hotel under WelcomHeritage group", "Major Burton was killed here in 1857 Mutiny"],
         ["Burton's death in 1857 Mutiny is historically documented", "Hotel still operational; guests report encounters"],
         ["Colonial-era British officer ghost is a recurring post-Mutiny archetype"],
         ["Major Burton's ghost roams Room 1 and the verandah", "Ghost slaps sleeping guests", "Footsteps and cold presence felt at night"],
         ["Ghost protects the palace from harm", "Multiple Burtons (whole family) still haunt"]),

        (9, "Savoy Hotel, Mussoorie, Uttarakhand",
         ["Hotel built 1902 by Frederick 'Mustapha' Wilson", "Agatha Christie visited; inspired mystery fiction", "Frances Garnet Clubb murdered/died here 1911"],
         ["Frances Clubb's death in 1911 is on record (poisoning case)", "John Eastman murder case 1912 also documented here", "Agatha Christie's connection documented"],
         ["Hotel's early violent deaths created lingering reputation"],
         ["Frances Clubb's ghost seen in white on the corridors", "Cold spots and moving objects in rooms"],
         ["Entire hotel is haunted on certain dates", "Locked rooms open by themselves overnight"]),

        (10, "Fernhill Hotel, Ooty, Tamil Nadu",
         ["Built as summer palace for Maharaja of Mysore (~1844)", "Heritage hotel; operational until ~2000s", "Colonial architecture intact"],
         ["Palace history documented in Mysore royal records", "Hotel featured in Mani Ratnam's Roja (1992)"],
         ["Isolated hill location + colonial history generates atmosphere"],
         ["White figure seen at the end of corridors at night", "Piano plays by itself in the ballroom"],
         ["Maharaja's ghost roams the property", "Entire wing sealed due to paranormal activity"]),
    ]

    for item in data:
        make_pyramid(*item, out_dir=out)
    print("All pyramids generated.")
