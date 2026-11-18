# Neolab Atlas

An independent directory of AI research groups, from solo projects to frontier labs. Each entry describes the group’s research focus and cites a concrete public result or the closest available evidence. The Innovations view links to research code, weights, and papers where those artifacts are documented.

[Browse the Atlas on antonfed.com](https://antonfed.com/neolabs/)

## Preview locally

```sh
python3 build.py
python3 -m http.server 8910 --bind 127.0.0.1 --directory dist
```

Open [the local Atlas](http://127.0.0.1:8910/). The two views build from the same source data. The directory can be served by any static host.

## Edit an entry

Edit `data/atlas.json`. Add artifact links to the relevant `innovation.artifacts` array. Each has a `kind` (`code`, `weights`, `paper`, `data`, or `report`), a short `label`, and a direct `url`. Use the author's repository or model card and describe what it contains. Use `small_teams` to maintain the small-team view. For corrections, include a source for the specific change.

The site snapshot uses public usage data with different coverage by metric. Hugging Face downloads and GitHub stars were checked on November 18, 2026. The Vercel AI Gateway lab export is attributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked artifacts carry their respective publishers’ licenses.

## Update antonfed.com

From this repository, regenerate the bundled pages in the personal website checkout.

```sh
python3 build.py --output ../personal_website/public/neolabs
```
