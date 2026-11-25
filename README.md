# The World Today — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Kkajasd/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Kkajasd/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page summing up the world's news of Wednesday,
25 November 2026: 26 verified stories across world affairs, markets, the
Americas, technology, sport and life, each with a headline and a one-line
summary, under the masthead "The World Today". Lead stories: the US weighing
new tariffs on China, the EU and 14 partners; Zelenskyy confirming Ukraine's
strike on a Russian ship in the Gulf of Finland; and Shenzhou-24 lifting off
for Tiangong with Pakistan's first astronaut. The image is rendered
deterministically with Pillow by `tools/draw_frontpage.py` and shipped as
`entry.png`; `main.ts` copies it to the output directory. Every story
happened, or was first reported, on 25 November 2026 and is sourced in
`SOURCES.md`.

## Run

```sh
python3 tools/draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
