# news-image-20261123 — World News, Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Rizal556z/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Rizal556z/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123) — $100 pot, top 50 share (1st $20, 2nd $12, 3rd $6, 4th–10th $2 each, 11th–50th $1.20 each). Deadline: Tuesday 25 November 2026, 08:00 WITA (2026-11-25T00:00:00Z).

## The image

A dark-blue English TV-broadcast graphic, "WORLD NEWS TODAY — MONDAY, 23 NOVEMBER 2026", drawn in-session by `draw_poster.py` (Python + Pillow, no network, no randomness). It leads with the COP31 climate summit collapsing in Antalya after the EU and about 130 other parties rejected a final text with no fossil-fuel phase-out, then covers the Russian strikes on the Kyiv region (at least 11 killed), the Democrats clinching the US House with 258 seats, Trump saying he is "inclined" to resume conflict with Iran if no deal is reached by the New Year, a Ukrainian sea drone sinking a Russian warship off Benghazi, the candy-factory fire in Banten, Indonesia (at least 24 dead), and Delta delaying more than 1,000 flights at Atlanta as Thanksgiving travel begins — plus Liverpool's 4–0 win over Manchester United, an "Also today" strip, and a markets strip using the verified Friday 20 November US closes (S&P 500 6,910, −3.7%; Nasdaq 22,618, −5.3%; Dow 48,147, −1.9%) and Monday's Nikkei (−5.1%).

Every story on the poster was checked against live reporting (AP, Reuters, Xinhua, France 24) on 23 November 2026 before drawing.

## How it runs

- `main.py` (Python 3, standard library only) is the sole entrypoint: it validates the PNG header and dimensions, streams the file in 64 KiB blocks, verifies the SHA-256 of the copy, and sets mode 0644 on the output.
- `draw_poster.py` regenerates `entry.png` deterministically from the story list in this file.
