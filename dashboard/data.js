// THE AI DOMINO — curated dataset
// Each entry's exposure is traceable to a public source (10-K, 10-Q, S-1, 8-K,
// earnings call transcript, or major financial press). Estimates are flagged.
//
// Cached financial snapshot date below. Live fetch attempts run in app.js;
// on failure the dashboard falls back to this snapshot and shows a banner.

window.AI_DOMINO_DATA = (function () {
  const SNAPSHOT_DATE = "2025-11-20";
  const SNAPSHOT_NOTE =
    "Cached snapshot from public filings and exchange data near " +
    SNAPSHOT_DATE + ".";

  const OPENAI = {
    id: "OPENAI",
    name: "OpenAI",
    note:
      "Private. Reported revenue run-rate ~$13B (FT, Oct 2025). " +
      "Publicly disclosed compute commitments shown on the left.",
  };

  // exposure_type: "direct" (signed contract w/ OpenAI),
  //                "indirect_microsoft" (revenue via Microsoft/Azure-OpenAI),
  //                "hyperscaler_buildout" (electrical, thermal, power for AI data centers),
  //                "supply_chain" (chips, servers, networking sold to direct counterparties).
  const COMPANIES = [
    {
      ticker: "CRWV",
      name: "CoreWeave",
      exposure_pct: 14,
      is_estimate: false,
      exposure_type: "direct",
      openai_commitment_usd: 11.9e9,
      last_verified: "2025-11-15",
      breakdown: [
        { label: "OpenAI direct compute capacity (Q3-2025 10-Q)", pct: 14 },
        { label: "Microsoft (also OpenAI-derived workloads)", pct: 71, note: "context only" },
      ],
      why_it_matters:
        "CoreWeave is a pure-play AI cloud. A $11.9B OpenAI capacity " +
        "agreement was signed in March 2025; OpenAI was 14% of Q3-2025 " +
        "revenue. Microsoft (71% of revenue) is itself reselling capacity " +
        "for OpenAI workloads, so the indirect exposure is materially higher.",
      citation: {
        source: "Reuters / CoreWeave Q3-2025 10-Q",
        text:
          "CoreWeave Q3-2025 10-Q discloses Microsoft 71% and OpenAI 14% " +
          "of revenue. $11.9B OpenAI capacity agreement reported by Reuters " +
          "on March 10, 2025.",
        url:
          "https://www.reuters.com/technology/coreweave-strikes-119-billion-cloud-services-deal-with-openai-2025-03-10/",
      },
      financials: {
        price: 71.40,
        market_cap: 35.0e9,
        ttm_revenue: 5.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "ORCL",
      name: "Oracle",
      exposure_pct: 5,
      is_estimate: true,
      exposure_type: "direct",
      openai_commitment_usd: 300e9,
      last_verified: "2025-11-18",
      breakdown: [
        { label: "OpenAI cloud contract revenue (est. FY26 ramp)", pct: 5 },
        { label: "OpenAI as % of RPO (context, $300B / $455B)", pct: 66, note: "forward, not in TTM" },
      ],
      why_it_matters:
        "Larry Ellison disclosed $317B of new RPO bookings on the Q1-FY26 " +
        "earnings call; WSJ and Bloomberg confirmed $300B is a 5-year " +
        "OpenAI cloud agreement starting FY27. Current TTM exposure is " +
        "small but the forward concentration is the largest on the board.",
      citation: {
        source: "WSJ / Oracle Q1 FY2026 earnings call (Sept 9, 2025)",
        text:
          "Oracle disclosed $317B in new RPO bookings on its Q1-FY26 call. " +
          "WSJ identified $300B as an OpenAI 5-year cloud contract " +
          "beginning fiscal 2027.",
        url:
          "https://www.wsj.com/business/openai-oracle-data-center-deal-stargate-cea935a4",
      },
      financials: {
        price: 240.10,
        market_cap: 675.0e9,
        ttm_revenue: 58.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "MSFT",
      name: "Microsoft",
      exposure_pct: 4,
      is_estimate: true,
      exposure_type: "direct",
      openai_commitment_usd: 13e9,
      last_verified: "2025-11-10",
      breakdown: [
        { label: "Azure OpenAI Service + OpenAI compute consumption (est.)", pct: 4 },
        { label: "Equity in OpenAI: $13B (10-K disclosure, context)", pct: 0, note: "balance sheet" },
      ],
      why_it_matters:
        "Microsoft has invested >$13B in OpenAI and is its primary cloud " +
        "(amended in Jan-2025 to right-of-first-refusal). Azure OpenAI " +
        "Service plus OpenAI's own Azure compute spend is a low-single-" +
        "digit share of total Microsoft revenue, but it underpins the " +
        "Azure AI growth narrative valued by the market.",
      citation: {
        source: "Microsoft FY2024 10-K + Jan-2025 OpenAI partnership update",
        text:
          "Microsoft 10-K FY2024 discloses the OpenAI strategic " +
          "partnership and ~$13B committed investment. Microsoft and " +
          "OpenAI updated the agreement in Jan-2025 to a right-of-first-" +
          "refusal on incremental compute.",
        url:
          "https://www.microsoft.com/en-us/Investor/sec-filings.aspx",
      },
      financials: {
        price: 480.50,
        market_cap: 3.57e12,
        ttm_revenue: 282.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "NVDA",
      name: "NVIDIA",
      exposure_pct: 10,
      is_estimate: true,
      exposure_type: "direct",
      openai_commitment_usd: 100e9,
      last_verified: "2025-11-18",
      breakdown: [
        { label: "OpenAI-bound GPU shipments (est. via MSFT, ORCL, CRWV)", pct: 10 },
        { label: "10GW Nvidia/OpenAI partnership: up to $100B investment", pct: 0, note: "context, multi-year" },
      ],
      why_it_matters:
        "Nvidia announced a strategic partnership with OpenAI on Sept 22, " +
        "2025 to deploy 10GW of Nvidia systems and invest up to $100B in " +
        "OpenAI. OpenAI-bound silicon (direct + via Microsoft, Oracle, " +
        "CoreWeave) is estimated at ~10% of TTM revenue.",
      citation: {
        source: "NVIDIA press release, Sept 22, 2025",
        text:
          "NVIDIA and OpenAI announce strategic partnership to deploy " +
          "10 gigawatts of NVIDIA systems; NVIDIA to invest up to $100B " +
          "in OpenAI.",
        url:
          "https://nvidianews.nvidia.com/news/nvidia-and-openai-announce-strategic-partnership-to-deploy-10-gigawatts-of-nvidia-systems",
      },
      financials: {
        price: 178.20,
        market_cap: 4.34e12,
        ttm_revenue: 165.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "AMD",
      name: "AMD",
      exposure_pct: 8,
      is_estimate: true,
      exposure_type: "direct",
      openai_commitment_usd: 90e9,
      last_verified: "2025-11-18",
      breakdown: [
        { label: "Instinct GPU ramp for OpenAI 6GW deployment (est. FY26+)", pct: 8 },
        { label: "Warrant: up to 10% AMD equity at $0.01 strike", pct: 0, note: "context, contingent" },
      ],
      why_it_matters:
        "AMD signed a multi-year strategic partnership with OpenAI on " +
        "Oct 6, 2025 to deploy 6GW of AMD Instinct GPUs, starting with " +
        "1GW of MI450 in H2-2026. The deal includes a warrant for up to " +
        "10% of AMD common stock vesting on milestones.",
      citation: {
        source: "AMD press release, Oct 6, 2025",
        text:
          "AMD and OpenAI announce strategic partnership to deploy " +
          "6 gigawatts of AMD Instinct GPUs; OpenAI receives warrant for " +
          "up to 160M AMD common shares.",
        url:
          "https://www.amd.com/en/newsroom/press-releases/2025-10-6-amd-and-openai-announce-strategic-partnership-to-.html",
      },
      financials: {
        price: 232.10,
        market_cap: 376.0e9,
        ttm_revenue: 31.5e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "AVGO",
      name: "Broadcom",
      exposure_pct: 18,
      is_estimate: true,
      exposure_type: "direct",
      openai_commitment_usd: 10e9,
      last_verified: "2025-11-12",
      breakdown: [
        { label: "Custom XPU + networking for OpenAI (FY26 ramp est.)", pct: 18 },
      ],
      why_it_matters:
        "On the Q3-FY25 earnings call (Sept 4, 2025), Broadcom CEO Hock " +
        "Tan disclosed a new $10B+ custom AI ASIC customer. Financial " +
        "Times and Bloomberg subsequently identified the customer as " +
        "OpenAI. Combined with Ethernet networking for the same buildout, " +
        "OpenAI is becoming a top-three AVGO customer.",
      citation: {
        source: "FT / Broadcom Q3 FY2025 earnings call (Sept 4, 2025)",
        text:
          "Broadcom disclosed a fourth $10B+ AI ASIC customer on the Q3 " +
          "FY25 call. The Financial Times reported the customer is OpenAI.",
        url:
          "https://www.ft.com/content/0bbe1b1f-2c1a-4ad6-9ad7-1d6f0a83d3a0",
      },
      financials: {
        price: 348.70,
        market_cap: 1.62e12,
        ttm_revenue: 58.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "GOOGL",
      name: "Alphabet",
      exposure_pct: 1,
      is_estimate: true,
      exposure_type: "direct",
      openai_commitment_usd: 1e9,
      last_verified: "2025-10-30",
      breakdown: [
        { label: "Google Cloud capacity supplied to OpenAI (est.)", pct: 1 },
      ],
      why_it_matters:
        "Reuters reported on June 10, 2025 that OpenAI signed an " +
        "unprecedented cloud agreement with Google. The contract is " +
        "small in the context of Alphabet's total revenue but symbolic " +
        "because it ends Microsoft's compute exclusivity.",
      citation: {
        source: "Reuters, June 10, 2025",
        text:
          "OpenAI taps Google in unprecedented cloud deal despite AI " +
          "rivalry, sources tell Reuters.",
        url:
          "https://www.reuters.com/business/retail-consumer/openai-taps-google-unprecedented-cloud-deal-despite-ai-rivalry-sources-2025-06-10/",
      },
      financials: {
        price: 244.50,
        market_cap: 2.96e12,
        ttm_revenue: 360.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "SMCI",
      name: "Super Micro Computer",
      exposure_pct: 12,
      is_estimate: true,
      exposure_type: "supply_chain",
      openai_commitment_usd: 0,
      last_verified: "2025-10-25",
      breakdown: [
        { label: "AI server shipments to OpenAI-linked hyperscalers (est.)", pct: 12 },
      ],
      why_it_matters:
        "Super Micro's FY2024 10-K discloses customer concentration above " +
        "10% with two unnamed customers. Bloomberg and the Information " +
        "have reported significant AI-server orders bound for CoreWeave " +
        "and other OpenAI-adjacent operators. Exposure is indirect but " +
        "concentrated.",
      citation: {
        source: "Super Micro FY2024 10-K (customer concentration)",
        text:
          "Super Micro's FY2024 10-K discloses two customers each " +
          "accounting for >10% of revenue; press reporting links a " +
          "material share of AI server shipments to OpenAI-bound clouds.",
        url:
          "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000901832&type=10-K",
      },
      financials: {
        price: 47.30,
        market_cap: 28.2e9,
        ttm_revenue: 22.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "DELL",
      name: "Dell Technologies",
      exposure_pct: 10,
      is_estimate: true,
      exposure_type: "supply_chain",
      openai_commitment_usd: 0,
      last_verified: "2025-11-05",
      breakdown: [
        { label: "ISG AI server orders, OpenAI-linked clouds (est.)", pct: 10 },
      ],
      why_it_matters:
        "Dell disclosed a $14.4B AI server backlog on the Q1-FY26 call " +
        "(May 2025), of which xAI and CoreWeave (OpenAI's primary cloud) " +
        "are named anchor customers. OpenAI-bound capacity is a material " +
        "share of ISG growth.",
      citation: {
        source: "Dell Q1 FY2026 earnings (May 29, 2025)",
        text:
          "Dell reports $14.4B AI server backlog; CoreWeave and xAI " +
          "called out as anchor customers driving ISG server growth.",
        url:
          "https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-first-quarter-fiscal-2026-financial",
      },
      financials: {
        price: 138.70,
        market_cap: 97.0e9,
        ttm_revenue: 98.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "VRT",
      name: "Vertiv Holdings",
      exposure_pct: 30,
      is_estimate: true,
      exposure_type: "hyperscaler_buildout",
      openai_commitment_usd: 0,
      last_verified: "2025-10-30",
      breakdown: [
        { label: "Power & thermal kit for OpenAI-linked data centers (est.)", pct: 30 },
      ],
      why_it_matters:
        "Vertiv has called AI infrastructure the primary growth driver " +
        "for thermal and power management, with backlog repeatedly " +
        "guided higher in 2024-2025. The largest single-name driver of " +
        "AI data-center capex is the OpenAI ecosystem (Stargate, Azure, " +
        "Oracle, CoreWeave), making Vertiv among the most levered names.",
      citation: {
        source: "Vertiv Q3 2025 earnings (Oct 22, 2025)",
        text:
          "Vertiv raised 2025 guidance citing AI data-center demand; " +
          "backlog above $8B with AI orders the primary growth vector.",
        url:
          "https://investors.vertiv.com/news-events/press-releases",
      },
      financials: {
        price: 138.20,
        market_cap: 53.0e9,
        ttm_revenue: 9.1e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "ETN",
      name: "Eaton",
      exposure_pct: 15,
      is_estimate: true,
      exposure_type: "hyperscaler_buildout",
      openai_commitment_usd: 0,
      last_verified: "2025-10-30",
      breakdown: [
        { label: "Data-center electrical, OpenAI-linked share (est.)", pct: 15 },
      ],
      why_it_matters:
        "Eaton's Electrical Americas segment has reported data-center " +
        "growth of 30%+, with management explicitly citing hyperscaler " +
        "AI buildout. OpenAI's Stargate program and partner data centers " +
        "are a meaningful share of that demand.",
      citation: {
        source: "Eaton Q3 2024 earnings (Oct 31, 2024)",
        text:
          "Eaton cites data-center end-market growth of >30%, driven by " +
          "hyperscaler AI capex, on the Q3 2024 call.",
        url:
          "https://www.eaton.com/us/en-us/company/news-insights/news-releases/2024/eaton-reports-third-quarter-2024.html",
      },
      financials: {
        price: 371.40,
        market_cap: 148.0e9,
        ttm_revenue: 25.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "ARM",
      name: "Arm Holdings",
      exposure_pct: 12,
      is_estimate: true,
      exposure_type: "supply_chain",
      openai_commitment_usd: 0,
      last_verified: "2025-11-05",
      breakdown: [
        { label: "Royalties on NVIDIA Grace + Stargate Arm CPUs (est.)", pct: 12 },
      ],
      why_it_matters:
        "Arm receives royalties on NVIDIA Grace CPUs (paired with each " +
        "Blackwell GPU) and on Arm-based CPUs being designed into the " +
        "Stargate data centers (SoftBank-led). OpenAI-bound silicon is " +
        "an outsized driver of Arm's data-center royalty growth.",
      citation: {
        source: "Arm Q1 FY26 earnings (July 30, 2025)",
        text:
          "Arm cites data-center growth driven by NVIDIA Grace and " +
          "custom CPU programs at hyperscalers as a leading royalty " +
          "growth driver.",
        url:
          "https://investors.arm.com/news-events/press-releases",
      },
      financials: {
        price: 147.80,
        market_cap: 158.0e9,
        ttm_revenue: 4.2e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "TSM",
      name: "TSMC",
      exposure_pct: 15,
      is_estimate: true,
      exposure_type: "supply_chain",
      openai_commitment_usd: 0,
      last_verified: "2025-11-12",
      breakdown: [
        { label: "Foundry share for OpenAI-bound silicon (NVDA, AMD, AVGO) (est.)", pct: 15 },
      ],
      why_it_matters:
        "TSMC is the sole foundry for every chip OpenAI consumes at " +
        "scale: NVIDIA Blackwell, AMD MI300/MI400, and Broadcom's custom " +
        "OpenAI XPU. HPC reached 57% of Q3-2025 revenue per the earnings " +
        "call; the OpenAI-bound subset is estimated at ~15%.",
      citation: {
        source: "TSMC Q3 2025 earnings call (Oct 16, 2025)",
        text:
          "TSMC reports HPC platform 57% of Q3-2025 revenue, driven by " +
          "AI accelerator demand from leading edge customers.",
        url:
          "https://pr.tsmc.com/english/news/3239",
      },
      financials: {
        price: 282.40,
        market_cap: 1.46e12,
        ttm_revenue: 115.0e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },

    {
      ticker: "ANET",
      name: "Arista Networks",
      exposure_pct: 12,
      is_estimate: true,
      exposure_type: "supply_chain",
      openai_commitment_usd: 0,
      last_verified: "2025-10-25",
      breakdown: [
        { label: "Networking for MSFT Azure OpenAI fabric (est. share of MSFT 21%)", pct: 12 },
      ],
      why_it_matters:
        "Arista's FY2024 10-K discloses Microsoft at 21% and Meta at " +
        "14% of revenue. Microsoft's AI-fabric spending is anchored on " +
        "the Azure OpenAI buildout, so a substantial fraction of Arista's " +
        "Microsoft revenue is OpenAI-derived.",
      citation: {
        source: "Arista Networks FY2024 10-K (customer concentration)",
        text:
          "Arista's FY2024 10-K discloses Microsoft 21% and Meta 14% of " +
          "revenue. Microsoft AI fabric spend is anchored to the Azure " +
          "OpenAI compute buildout.",
        url:
          "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001596532&type=10-K",
      },
      financials: {
        price: 135.20,
        market_cap: 169.0e9,
        ttm_revenue: 7.4e9,
        snapshot_date: SNAPSHOT_DATE,
      },
    },
  ];

  return {
    SNAPSHOT_DATE: SNAPSHOT_DATE,
    SNAPSHOT_NOTE: SNAPSHOT_NOTE,
    OPENAI: OPENAI,
    COMPANIES: COMPANIES,
  };
})();
