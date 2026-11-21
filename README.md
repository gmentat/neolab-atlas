# Neolab Atlas

An independent directory of AI research groups with a dedicated list for solo researchers and personal experiments. Each entry describes the work and links to public evidence. The Innovations view links to research code, weights, and papers where those artifacts are documented.

[Browse the Atlas on antonfed.com](https://antonfed.com/neolabs/)

## Preview locally

```sh
python3 build.py
python3 -m http.server 8910 --bind 127.0.0.1 --directory dist
```

Open the [local Atlas](http://127.0.0.1:8910/), [Small teams](http://127.0.0.1:8910/small-teams/), or [Solo projects](http://127.0.0.1:8910/solo-projects/). All three pages build from the same source data.

Each profile has a direct link, such as [Mantic](https://antonfed.com/neolabs/?lab=mantic). The **Profile link** inside a profile points to its main directory page, even when opened from Small teams or Innovations. Profile URLs default to a slug derived from the entry name. Set an explicit `slug` to retain the existing URL when renaming an entry.

## Edit an entry

Edit `data/atlas.json`. Give each lab one featured example. Describe what the team built or tested, what the source reports, and which limits matter for that claim. Add direct links in `innovation.artifacts` with a `kind` (`code`, `weights`, `paper`, `data`, or `report`), a short `label`, and a `url`. Use `related: true` for an artifact from a different result that belongs in the profile. Entries with the `Solo project`, `Solo-led project`, or `Personal experiment` scope appear on Solo projects.

Set `fit` to `Core`, `Mostly`, or `Borderline` for each lab outside Solo projects. Use `scope` for the type of organization. A `fit_note` can explain a judgment where the reason needs context.

Set `innovation.date` to the documented date of the featured example in `YYYY-MM-DD` or `YYYY-MM` format. Use `innovation.date_source` when that date comes from a different link than `innovation.source`. Within each fit group, the default sort orders featured examples newest first. Day-dated examples precede month-only examples in the same month. **Founding year** also sorts within fit groups. Usage signals sort across all filtered entries with positive values first.

Add verified public profiles to `people.links`, keyed by the name as written in `people.names`. Each profile is a `[label, url]` pair, such as `["GitHub", "https://github.com/karpathy"]`.

For a documented team count, record `team.size`, `team.size_kind` (`headcount`, `employee_range`, `roster`, `authors`, or `solo`), its date when known, and the source. Add to `small_teams` when a company’s reported headcount or employee range is at most ten, or when a research group credits at most ten people on a roster or featured release. Set `team.count_upper_bound` to the maximum supported by that count type. Keep the type of count visible in the profile.

Hugging Face downloads and GitHub stars were checked on November 18, 2026. Record the exact repository next to either value. The Vercel snapshot averages daily shares for November 11–17, 2026 and compares them with November 4–10. The [Vercel AI Gateway lab export](https://vercel.com/api/ai/leaderboard-export?dataset=labs) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Linked artifacts carry their respective publishers’ licenses.

## Update antonfed.com

From this repository, regenerate the bundled pages in the personal website checkout.

```sh
python3 build.py --output ../personal_website/public/neolabs --home-href /
```
