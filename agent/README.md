# GovVerify advisor/client demo — build notes (white-label)

The site is a single-file bundle (`../index.html`). The whole app (HTML, the
`<x-dc>` view template, and the `text/x-dc` component script) lives JSON-encoded
on **one line** inside `<script type="__bundler/template">`. Editing that line by
hand is impractical, so the readable source of truth is kept here:

- **`app.template.html`** — the decoded template. Edit the app here (screens,
  the `Component` class, journey data, i18n, styling).
- **`build.py`** — re-encodes `app.template.html` and splices it back into
  `index.html` (only that one line changes). Idempotent and re-runnable.

```sh
python3 agent/build.py      # run from the repo root after editing app.template.html
```

## White-label — the `BRAND` config

This bundle is brand-neutral. **All visible brand strings derive from a single
`BRAND` object** at the very top of the `text/x-dc` script in `app.template.html`.
To re-skin the demo for another prospect, edit that one object:

```js
const BRAND = {
  platform: { name:'Fill Easy', nameZh:'填鴨', product:'GovVerify' }, // the demo tool (outer chrome)
  insurer:  { name:'Meridian Life', nameZh:'子午人壽', short:'Meridian Life HK' }, // placeholder carrier
  accent:   '#FED200',
  programs: { entry/pro/exp/assoc/bank … },  // generic signup-bonus program names + tiers
  terms:    { licDesk, eRecruit … },         // generic back-office process names
};
```

- The **outer rail** shows the *platform* (`Fill Easy · 填鴨 / GovVerify`); the
  **phone header** shows the *insurer* (`Meridian Life`). The i18n strings,
  `recommend()` program names, the due-diligence labels and the system-output
  screen all read from `BRAND` (via template literals / the `brand` view-model).
- Program names are generic (**New Advisor Plan / Professional Entry Scheme /
  Experienced Advisor Plan / Associate Plan / Banker Transition Plan**) with
  numbered tiers — no carrier-proprietary program codes.
- `recruitment-file.html` is a standalone page; it hard-codes the same neutral
  brand (swap its strings directly if you re-skin).
- Industry-standard regulatory terms (IIQE, CHESICC, IA, HKFI, MPS, NIA, MOHRSS,
  PBOC, …) are **not** brand-specific and remain as-is.

## Journeys

**New client onboarding (Whole Life)** — three selectable client personas
(`CLIENT_PROFILES()`): *Straight-through* (approved this session), *Low income*
(premium above the affordability ceiling → review) and *Medical issues*
(disclosures → manual underwriting). The four result forms + decision banner are
built from the chosen persona.

**New advisor onboarding** — reuses the eID **tap → consent → pull** component,
then routes to `assess` (eligibility verdict + signup-bonus recommendation),
`onboard` (eID-prefilled application + gap fields + document checklist) and
`done` (system-output view). Three demo profiles (`AGENT_PROFILES()`): *Basic*,
*High income*, *Has issues*. Bilingual (EN / 繁體中文) via the in-app toggle. The
pre-assessment is a due-diligence set (identity, right-to-work, academic via
CHESICC, credit & litigation, agent-debt, Factiva/PEP, blacklist, IA registration,
IIQE), each labelled **Automated / Part-auto / Manual** with its data source.

**Claims** — eID-prefilled claim form, itemised bill and assessment.

All personas are Mainland-Chinese candidates who moved to HK (Mainland 居民身份證
via MPS, 港澳通行證 via NIA, CHSI/CHESICC degrees, `+86`); right-to-work is an HK
visa shown per profile. All figures are **indicative only** — a demo, no backend.

## vendor/

`react`, `react-dom` (18.3.1) and `@babel/standalone` (7.26.4) are vendored in
`../vendor/` and preloaded, so the page boots without the unpkg CDN.
