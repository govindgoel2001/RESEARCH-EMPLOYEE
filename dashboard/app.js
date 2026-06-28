/* THE AI DOMINO — rendering logic
 *
 * - Builds D3 force-directed network: OpenAI hub + radiating companies.
 * - Force simulation settles in ~1.4s (alphaDecay tuned) then stops.
 * - Hover tooltip, click drill-down, sortable leaderboard, mobile fallback.
 * - Attempts live-financials fetch; falls back to cached snapshot + banner.
 */

(function () {
  "use strict";

  const D = window.AI_DOMINO_DATA;
  if (!D) {
    console.error("dataset failed to load");
    return;
  }

  // ─────────────── helpers ───────────────

  function formatUsd(n) {
    if (n == null || isNaN(n)) return "—";
    const abs = Math.abs(n);
    if (abs >= 1e12) return "$" + (n / 1e12).toFixed(2) + "T";
    if (abs >= 1e9)  return "$" + (n / 1e9).toFixed(1)  + "B";
    if (abs >= 1e6)  return "$" + (n / 1e6).toFixed(1)  + "M";
    return "$" + Math.round(n).toLocaleString();
  }
  function formatUsdSigned(n) {
    if (n == null || isNaN(n)) return "—";
    return formatUsd(n);
  }
  function formatPct(n) { return n.toFixed(0) + "%"; }
  function formatPrice(n) {
    if (n == null || isNaN(n)) return "—";
    return "$" + n.toFixed(2);
  }
  function exposureColor(pct) {
    if (pct >= 20) return "#ff3b3b";
    if (pct >= 12) return "#ff7a3b";
    if (pct >= 6)  return "#e0b341";
    return "#2ec27e";
  }
  function exposureLabel(pct) {
    if (pct >= 20) return "HIGH";
    if (pct >= 12) return "ELEV.";
    if (pct >= 6)  return "MOD.";
    return "LOW";
  }
  function edgeClass(type) {
    if (type === "hyperscaler_buildout") return "edge edge-buildout";
    if (type === "supply_chain")         return "edge edge-supply";
    if (type === "indirect_microsoft")   return "edge edge-buildout";
    return "edge edge-direct";
  }
  function typeLabel(type) {
    return {
      direct: "DIRECT CONTRACT",
      indirect_microsoft: "VIA MICROSOFT",
      hyperscaler_buildout: "HYPERSCALER BUILDOUT",
      supply_chain: "SUPPLY CHAIN",
    }[type] || type;
  }
  function dollarsAtRisk(c) {
    return (c.exposure_pct / 100) * c.financials.ttm_revenue;
  }
  function estPrefix(isEst) {
    return isEst ? '<span class="est-mark">est.</span>' : "";
  }

  // ─────────────── derived state ───────────────

  function computeHero() {
    const totalCommit = D.COMPANIES.reduce(
      (s, c) => s + (c.openai_commitment_usd || 0),
      0
    );
    const totalRisk = D.COMPANIES.reduce((s, c) => s + dollarsAtRisk(c), 0);
    return { totalCommit, totalRisk };
  }

  function renderHero() {
    const { totalCommit, totalRisk } = computeHero();
    document.getElementById("hero-commitments").textContent =
      formatUsd(totalCommit);
    document.getElementById("hero-at-risk").textContent =
      formatUsd(totalRisk);

    const namedCommit = D.COMPANIES
      .filter(c => c.openai_commitment_usd > 0)
      .map(c => c.ticker).join(", ");
    document.getElementById("hero-commitments-foot").textContent =
      "Across " + D.COMPANIES.filter(c => c.openai_commitment_usd > 0).length +
      " disclosed direct counterparties: " + namedCommit + ".";
    document.getElementById("hero-at-risk-foot").textContent =
      "Sum of (exposure % × TTM revenue) across " +
      D.COMPANIES.length + " covered companies.";
  }

  function renderTimestamp() {
    const t = new Date();
    const iso = t.toISOString().slice(0, 19).replace("T", " ") + " UTC";
    document.getElementById("updated-time").textContent = iso;
    document.getElementById("snapshot-date").textContent = D.SNAPSHOT_DATE;
  }

  // ─────────────── network graph ───────────────

  const HUB_ID = "OPENAI";

  function buildGraph() {
    const svgEl = document.getElementById("graph");
    const width = svgEl.clientWidth || 1000;
    const height = svgEl.clientHeight || 560;

    const svg = d3.select(svgEl)
      .attr("viewBox", "0 0 " + width + " " + height)
      .attr("preserveAspectRatio", "xMidYMid meet");

    svg.selectAll("*").remove();

    const nodes = [
      { id: HUB_ID, kind: "hub" },
      ...D.COMPANIES.map(c => ({
        id: c.ticker,
        kind: "company",
        company: c,
      })),
    ];
    const links = D.COMPANIES.map(c => ({
      source: HUB_ID,
      target: c.ticker,
      type: c.exposure_type,
    }));

    const maxRisk = d3.max(D.COMPANIES, dollarsAtRisk);
    const rscale = d3.scaleSqrt().domain([0, maxRisk]).range([14, 38]);

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(170).strength(0.6))
      .force("charge", d3.forceManyBody().strength(-380))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(d =>
        d.kind === "hub" ? 60 : rscale(dollarsAtRisk(d.company)) + 18
      ))
      .alpha(1)
      .alphaDecay(0.06)   // settles by ~1.3s
      .alphaMin(0.02);

    const linkSel = svg.append("g")
      .attr("stroke-linecap", "round")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", d => edgeClass(d.type));

    const nodeG = svg.append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .attr("class", "node");

    // hub
    nodeG.filter(d => d.kind === "hub")
      .append("circle")
      .attr("r", 36)
      .attr("fill", "var(--bg)")
      .attr("stroke", "var(--accent)")
      .attr("stroke-width", 2);

    nodeG.filter(d => d.kind === "hub")
      .append("text")
      .attr("class", "hub-label")
      .attr("dy", 4)
      .text("OPENAI");

    // companies
    const companyG = nodeG.filter(d => d.kind === "company");

    companyG.append("circle")
      .attr("r", d => rscale(dollarsAtRisk(d.company)))
      .attr("fill", d => exposureColor(d.company.exposure_pct))
      .attr("fill-opacity", 0.18)
      .attr("stroke", d => exposureColor(d.company.exposure_pct))
      .attr("stroke-width", 1.5);

    companyG.append("text")
      .attr("class", "node-label")
      .attr("text-anchor", "middle")
      .attr("dy", 4)
      .text(d => d.company.ticker);

    // interaction
    companyG
      .on("mouseenter", (event, d) => showTooltip(event, d.company))
      .on("mousemove", moveTooltip)
      .on("mouseleave", hideTooltip)
      .on("click", (event, d) => openDrilldown(d.company));

    simulation.on("tick", () => {
      linkSel
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      nodeG.attr("transform", d => "translate(" + d.x + "," + d.y + ")");
    });

    // freeze hub at center for stability
    nodes[0].fx = width / 2;
    nodes[0].fy = height / 2;

    // hard-stop the simulation after 1.5s so it doesn't keep wobbling
    setTimeout(() => simulation.stop(), 1500);
  }

  // ─────────────── tooltip ───────────────

  const ttEl = document.getElementById("graph-tooltip");

  function showTooltip(event, c) {
    const atRisk = dollarsAtRisk(c);
    ttEl.innerHTML =
      '<div class="tt-row"><span class="tt-ticker">' + c.ticker + '</span>' +
      '<span class="tt-label">' + typeLabel(c.exposure_type) + '</span></div>' +
      '<div class="tt-row"><span class="tt-label">Exposure</span>' +
      '<span>' + (c.is_estimate ? "est. " : "") + formatPct(c.exposure_pct) +
      '</span></div>' +
      '<div class="tt-row"><span class="tt-label">$ at risk</span>' +
      '<span>' + formatUsd(atRisk) + '</span></div>' +
      '<div class="tt-row"><span class="tt-label">TTM rev</span>' +
      '<span>' + formatUsd(c.financials.ttm_revenue) + '</span></div>';
    ttEl.hidden = false;
    moveTooltip(event);
  }
  function moveTooltip(event) {
    const wrap = document.querySelector(".graph-wrap");
    const r = wrap.getBoundingClientRect();
    const x = event.clientX - r.left + 14;
    const y = event.clientY - r.top + 14;
    ttEl.style.left = x + "px";
    ttEl.style.top  = y + "px";
  }
  function hideTooltip() { ttEl.hidden = true; }

  // ─────────────── drill-down ───────────────

  const dd = document.getElementById("drilldown");

  function openDrilldown(c) {
    document.getElementById("dd-ticker").textContent = c.ticker;
    document.getElementById("dd-name").textContent = c.name;

    const expoEl = document.getElementById("dd-exposure");
    expoEl.innerHTML =
      estPrefix(c.is_estimate) + formatPct(c.exposure_pct) +
      ' <span class="muted">of TTM revenue</span>';

    document.getElementById("dd-type").textContent = typeLabel(c.exposure_type);
    document.getElementById("dd-verified").textContent =
      "as of " + c.last_verified;

    // breakdown
    const bd = document.getElementById("dd-breakdown");
    bd.innerHTML = "";
    c.breakdown.forEach(b => {
      const item = document.createElement("div");
      item.className = "breakdown-item";
      const labelRow = document.createElement("div");
      labelRow.className = "breakdown-label";
      labelRow.innerHTML =
        '<span>' + b.label + '</span>' +
        '<span>' + (b.pct ? formatPct(b.pct) : "—") + '</span>';
      const barWrap = document.createElement("div");
      barWrap.className = "breakdown-bar-wrap";
      const bar = document.createElement("div");
      bar.className = "breakdown-bar";
      bar.style.width = Math.min(100, b.pct || 0) + "%";
      bar.style.background = exposureColor(b.pct || 0);
      barWrap.appendChild(bar);
      item.appendChild(labelRow);
      item.appendChild(barWrap);
      if (b.note) {
        const n = document.createElement("div");
        n.className = "breakdown-note";
        n.textContent = b.note;
        item.appendChild(n);
      }
      bd.appendChild(item);
    });

    // citation
    document.getElementById("dd-citation-text").textContent = c.citation.text;
    const link = document.getElementById("dd-citation-link");
    link.href = c.citation.url;
    link.textContent = c.citation.url;
    document.getElementById("dd-citation-meta").textContent =
      "Source: " + c.citation.source + " · verified " + c.last_verified;

    // financials
    document.getElementById("dd-price").textContent =
      formatPrice(c.financials.price);
    document.getElementById("dd-mcap").textContent =
      formatUsd(c.financials.market_cap);
    document.getElementById("dd-rev").textContent =
      formatUsd(c.financials.ttm_revenue);

    document.getElementById("dd-atrisk").innerHTML =
      estPrefix(c.is_estimate) + formatUsd(dollarsAtRisk(c));

    document.getElementById("dd-snapshot-foot").textContent =
      (window.AI_DOMINO_LIVE ? "Live snapshot · " : "Cached snapshot · ") +
      "as of " + c.financials.snapshot_date;

    document.getElementById("dd-blurb").textContent = c.why_it_matters;

    dd.hidden = false;
    dd.setAttribute("aria-hidden", "false");
  }
  function closeDrilldown() {
    dd.hidden = true;
    dd.setAttribute("aria-hidden", "true");
  }
  document.getElementById("dd-close").addEventListener("click", closeDrilldown);
  document.getElementById("drilldown-backdrop")
    .addEventListener("click", closeDrilldown);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeDrilldown();
  });

  // ─────────────── leaderboard ───────────────

  let sortKey = "dollars_at_risk";
  let sortDir = "desc";

  function renderLeaderboard() {
    const body = document.getElementById("leaderboard-body");
    body.innerHTML = "";

    const rows = D.COMPANIES.map(c => ({
      c,
      dollars_at_risk: dollarsAtRisk(c),
      ttm_revenue: c.financials.ttm_revenue,
      market_cap: c.financials.market_cap,
      exposure_pct: c.exposure_pct,
      ticker: c.ticker,
    }));

    rows.sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey];
      if (typeof av === "string") {
        return sortDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
      }
      return sortDir === "asc" ? av - bv : bv - av;
    });

    rows.forEach(r => {
      const c = r.c;
      const tr = document.createElement("tr");
      tr.innerHTML =
        '<td class="lb-ticker">' + c.ticker + '</td>' +
        '<td>' + c.name + '</td>' +
        '<td class="lb-type">' + typeLabel(c.exposure_type) + '</td>' +
        '<td class="num">' +
          '<span class="exposure-pill" style="background:' +
          exposureColor(c.exposure_pct) + '22;color:' +
          exposureColor(c.exposure_pct) + '">' +
          (c.is_estimate ? 'est. ' : '') + formatPct(c.exposure_pct) +
          '</span></td>' +
        '<td class="num">' + formatUsd(c.financials.ttm_revenue) + '</td>' +
        '<td class="num">' + (c.is_estimate ? '<span class="est-mark">est.</span>' : '') +
          formatUsd(r.dollars_at_risk) + '</td>' +
        '<td class="num">' + formatUsd(c.financials.market_cap) + '</td>' +
        '<td>' + c.last_verified + '</td>';
      tr.addEventListener("click", () => openDrilldown(c));
      body.appendChild(tr);
    });

    document.querySelectorAll(".leaderboard th.sortable").forEach(th => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === sortKey) {
        th.classList.add(sortDir === "asc" ? "sort-asc" : "sort-desc");
      }
    });
  }

  document.querySelectorAll(".leaderboard th.sortable").forEach(th => {
    th.addEventListener("click", () => {
      const k = th.dataset.sort;
      if (sortKey === k) {
        sortDir = sortDir === "asc" ? "desc" : "asc";
      } else {
        sortKey = k;
        sortDir = k === "ticker" ? "asc" : "desc";
      }
      renderLeaderboard();
    });
  });

  // ─────────────── mobile list ───────────────

  function renderMobile() {
    const wrap = document.getElementById("mobile-list");
    wrap.innerHTML = "";
    const sorted = [...D.COMPANIES].sort((a, b) => b.exposure_pct - a.exposure_pct);
    sorted.forEach(c => {
      const card = document.createElement("div");
      card.className = "mobile-card";
      card.innerHTML =
        '<div class="mobile-card-head">' +
          '<span class="mobile-card-ticker">' + c.ticker + ' · ' + c.name + '</span>' +
          '<span class="mobile-card-pct" style="color:' +
          exposureColor(c.exposure_pct) + '">' +
          (c.is_estimate ? 'est. ' : '') + formatPct(c.exposure_pct) +
        '</span></div>' +
        '<div class="mobile-card-meta">' +
          '<span>' + typeLabel(c.exposure_type) + '</span>' +
          '<span>$ at risk: ' + formatUsd(dollarsAtRisk(c)) + '</span>' +
        '</div>';
      card.addEventListener("click", () => openDrilldown(c));
      wrap.appendChild(card);
    });
  }

  // ─────────────── live financials (best-effort) ───────────────
  //
  // Yahoo Finance JSON requires CORS approval. We try a single batched call
  // through Yahoo's public quote endpoint. On any failure — CORS, timeout,
  // HTTP error — we fall back to the cached snapshot and surface the banner
  // so the user knows the data is stale.

  async function tryLiveFinancials() {
    const tickers = D.COMPANIES.map(c => c.ticker).join(",");
    const url =
      "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + tickers;
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 4000);
      const resp = await fetch(url, { signal: controller.signal });
      clearTimeout(timeout);
      if (!resp.ok) throw new Error("HTTP " + resp.status);
      const data = await resp.json();
      const results = (data.quoteResponse && data.quoteResponse.result) || [];
      if (!results.length) throw new Error("empty response");
      const today = new Date().toISOString().slice(0, 10);
      results.forEach(q => {
        const c = D.COMPANIES.find(x => x.ticker === q.symbol);
        if (!c) return;
        if (typeof q.regularMarketPrice === "number") c.financials.price = q.regularMarketPrice;
        if (typeof q.marketCap === "number") c.financials.market_cap = q.marketCap;
        c.financials.snapshot_date = today;
      });
      window.AI_DOMINO_LIVE = true;
      return true;
    } catch (e) {
      console.warn("Live financials unavailable, using cached snapshot:", e.message);
      return false;
    }
  }

  function showCacheBanner(text) {
    const b = document.getElementById("cache-banner");
    if (text) document.getElementById("cache-banner-text").textContent = text;
    b.hidden = false;
  }

  // ─────────────── boot ───────────────

  async function boot() {
    renderTimestamp();
    const live = await tryLiveFinancials();
    if (!live) showCacheBanner(D.SNAPSHOT_NOTE);
    renderHero();
    renderLeaderboard();
    renderMobile();
    if (window.innerWidth > 820) buildGraph();

    // re-render graph on resize (debounced)
    let t;
    window.addEventListener("resize", () => {
      clearTimeout(t);
      t = setTimeout(() => {
        if (window.innerWidth > 820) buildGraph();
      }, 250);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
