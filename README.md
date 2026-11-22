# news-image-20261122-entry

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/kaybae46/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/kaybae46/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page summing up the world news of Sunday, 22 November 2026: the COP31 climate talks running into overtime in Antalya, Iran's strike on Bahrain, Mexico's capture of cartel boss "El Chapo Isidro", the Trump–Xi–Putin meeting in Shenzhen, and the AI sell-off that pushed stocks into correction — plus the EU–Indonesia trade deal, the Banda Sea quake, the Kryvyi Rih strike and Denmark's expulsion of a Russian attaché. The hero illustration is a generated editorial drawing of a climate summit hall; every headline and caption was written from that day's reporting, and all text is drawn by the program so it stays legible.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) verifies `entry.png` is a whole PNG inside the competition's limits and copies it to the output directory. `compose.py` is the build script that drew the front page from `assets/hero.png` with PIL; re-running it writes the same bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=69skdbw5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
