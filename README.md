# Sun Life · GovVerify — Interactive demo

A self-contained, front-end-only interactive demo that shows how a single tap of a
government ID can fill Sun Life's onboarding and claims forms in seconds — every field
stamped **Entered**, **Verified at source**, or **Assessed**.

It mirrors real Sun Life Hong Kong (永明金融) processes for a cross-border / Mainland
Chinese Visitor (MCI) context:

- **New client onboarding** — life application, Financial Needs Analysis (FNA), health
  declaration and underwriting; SunJoy Global, signed in Hong Kong.
- **New agent onboarding** — e-Recruitment「易招募」application, GL23 fit-and-proper review,
  and IA licence + Form N2 appointment via「保險中介一站通」, contract e-signing and agent code.
- **Claims** — claim form, itemised hospital bill and line-by-line assessment.

Data is pulled (in simulation) from authoritative registries — Ministry of Public Security,
Immigration, 學信網/CHSI, IIQE, the Insurance Authority (保險業監管局), TransUnion, Factiva,
Shenzhen Data Exchange, NHC/NHSA and others.

## Running it

It's a single `index.html`. Open it in a browser, or serve the folder:

```
python3 -m http.server 8000
# then visit http://localhost:8000
```

> Fully simulated · fixed data · no backend · no network calls beyond loading the
> React/Babel runtime from a CDN. Nothing entered is sent anywhere.
