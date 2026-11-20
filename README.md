# news-image-20261119-v2

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ryukaa853/news-image-20261119-v2/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ryukaa853/news-image-20261119-v2/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-image summary of Thursday 19 November 2026's world news, drawn as
a hero-led broadsheet front page (1024x1024 PNG): the first-ever
Trump–Xi–Putin trilateral in Shenzhen, the ICJ's genocide ruling against
Myanmar, GTA VI's record launch, Anthropic's $81bn IPO, a missile strike
on Riyadh's PIF Tower, and tanks crossing Gaza's "yellow line".

This is v2: a full redesign of the v1 front page. The lead story now gets
a full-width hero with the three flags over a round table; every story is
numbered 01–06; the illustrations were redrawn larger and cleaner (proper
flag stars, a drooping palm, a level scales of justice, a steep IPO
arrow); and the facts were re-verified against live reporting and
corrected (90-minute summit, joint statement wording, 9–6 ICJ vote,
$2.36bn day-one GTA VI estimate).

## Stories in the image

1. **Trump, Xi and Putin meet for the first time** — 90 minutes at a
   round table in Shenzhen; joint statement that a nuclear war "cannot
   be won and must never be fought", plus UN reform and oil supply.
   (WSJ, Reuters, CNN, Le Monde)
2. **Myanmar guilty of genocide** — the ICJ ruled 9–6 that Myanmar
   committed genocide against the Rohingya in 2017, the first time the
   court has held a state responsible. Reparations ordered.
   (Human Rights Watch, Reuters, CNN, Le Monde)
3. **GTA VI smashes every record** — launched at midnight; an estimated
   $2.36bn and 24.6m copies on day one, the biggest entertainment launch
   ever. (Sensor Tower estimate via NotebookCheck, Fox5, 80.lv)
4. **The biggest IPO ever** — Anthropic raised a record $81bn at $83 a
   share; "ANT" closed up 17% at $97.17 on Nasdaq.
   (CNN, Reuters, Investopedia)
5. **Missile hits Riyadh tower** — a Houthi missile struck the PIF
   Tower, blowing out windows on 7–8 floors. No injuries; the second
   hit on the financial district in 11 days. (Reuters, WSJ)
6. **Tanks cross the yellow line** — Israeli armour entered central Gaza
   in the first ground crossing since the October 2025 truce; Ukraine
   hit the Crimean Bridge for a third time this week.
   (The Guardian, AP, conflict briefing)

## How it is built

`draw.py` draws the image with Pillow (DejaVu fonts, vector-style panels)
and writes `entry.png`. `main.py` copies `entry.png` to
`/output/entry.png` — no network, fully deterministic.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

Entered on [make.fun](https://make.fun/?ref=8tc4hwe6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards
