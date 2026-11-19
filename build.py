"""Render the Atlas, small teams, and solo projects as static HTML."""

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
from shutil import copyfile

ROOT = Path(__file__).resolve().parent
HOME_URL = "https://antonfed.com/"
SITE_URL = HOME_URL + "neolabs/"
SHARE_IMAGE = "share-preview.png"
ATLAS_SUMMARY = (
    "Browse independent AI research labs and solo projects, what they’ve demonstrated, "
    "and links to their papers, code, and model weights."
)
SOLO_SCOPES = {"Solo project", "Solo-led project", "Personal experiment"}
FIT_LABELS = {"Core", "Mostly", "Borderline"}
INNOVATION_KINDS = {"method", "application", "artifact", "unproven"}
ROSTER_SCOPES = {"Academic research project", "Independent collective", "Independent lab", "Independent project", "Small team"}


def build(output: Path, home_href: str) -> None:
    data = json.loads((ROOT / "data/atlas.json").read_text(encoding="utf-8"))
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    updated = date.fromisoformat(data["updated"])
    small_teams = set(data["small_teams"])
    labs = data["labs"]
    names = {lab["name"] for lab in labs}
    if len(names) != len(labs) or small_teams - names:
        raise ValueError("Lab names must be unique and all small-team entries must exist in the directory.")
    for lab in labs:
        is_solo = lab["scope"] in SOLO_SCOPES
        innovation = lab["innovation"]
        if (innovation.get("kind") not in INNOVATION_KINDS
                or not all(innovation.get(key, "").strip() for key in ("example", "assessment", "source"))):
            raise ValueError(f"Incomplete featured innovation for {lab['name']}.")
        if not is_solo and lab.get("fit") not in FIT_LABELS:
            raise ValueError(f"Missing or unknown fit for {lab['name']}.")
        if lab["name"] in small_teams:
            team = lab.get("team") or {}
            count_types = {"headcount", "employee_range"}
            if lab["scope"] in ROSTER_SCOPES:
                count_types |= {"roster", "authors"}
            upper_bound = team.get("count_upper_bound")
            source = team.get("size_source") or team.get("source")
            if (is_solo or team.get("size_kind") not in count_types or not team.get("size") or not source
                    or type(upper_bound) is not int or not 1 <= upper_bound <= 10):
                raise ValueError(f"Small-team entry requires documented team count evidence: {lab['name']}.")
        research_date = innovation.get("date")
        if research_date:
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}(?:-[0-9]{2})?", research_date):
                raise ValueError(f"Invalid featured research date for {lab['name']}: {research_date}.")
            date.fromisoformat(research_date + "-01" if len(research_date) == 7 else research_date)

    team_labs = [lab for lab in labs if lab["scope"] not in SOLO_SCOPES]
    views = (
        ("", "Neolab Atlas",
         "A neolab is an independent AI research team that tests new ways to build, train, or run models. "
         "That might mean designing a new architecture, training a model with less data, "
         "or getting the same results with less computing power.",
         team_labs),
        ("small-teams/", "Small teams",
         "Companies reporting up to ten staff, plus research groups with up to ten people credited on a team roster "
         "or featured release. Profiles show each count’s source and what it covers.",
         [lab for lab in team_labs if lab["name"] in small_teams]),
        ("solo-projects/", "Solo projects",
         "Model research and personal experiments led by individual developers.",
         [lab for lab in labs if lab["scope"] in SOLO_SCOPES]),
    )
    navigation = (
        ("", "Atlas", "atlas"),
        ("?view=innovations", "Innovations", "innovations"),
        *((route, title, "") for route, title, *_ in views if route),
    )
    output.mkdir(parents=True, exist_ok=True)
    copyfile(ROOT / "article-header.css", output / "article-header.css")
    copyfile(ROOT / SHARE_IMAGE, output / SHARE_IMAGE)
    for route, title, description, entries in views:
        directory_href = "../" if route else "./"
        share_title = f"{title} · Neolab Atlas" if route else title
        page_title = share_title if route else f"{title} — Independent AI Research Labs"
        solo_view = route == "solo-projects/"
        entry_name = "project" if solo_view else "lab"
        count_name = "team" if route == "small-teams/" else entry_name
        count_label = f"{len(entries)} {count_name}{'s' if len(entries) != 1 else ''}"
        nav_links = []
        for target, label, view in navigation:
            current = ' aria-current="page"' if target == route else ""
            view_attr = f' data-view="{view}"' if not route and view else ""
            nav_links.append(f'<a href="{directory_href}{target}"{current}{view_attr}>{escape(label)}</a>')
        metrics = {
            key: metric
            for key, metric in data["metrics"].items()
            if any(lab["metrics"].get(key, {}).get("value", 0) > 0 for lab in entries)
        }
        content = {
            "TITLE": escape(title),
            "PAGE_TITLE": escape(page_title),
            "SHARE_TITLE": escape(share_title),
            "META_DESCRIPTION": escape(description if route else ATLAS_SUMMARY),
            "DESCRIPTION": escape(description, quote=True),
            "CANONICAL": SITE_URL + route,
            "SHARE_IMAGE_URL": SITE_URL + SHARE_IMAGE,
            "HOME_HREF": escape(home_href, quote=True),
            "UPDATED_DATE": updated.isoformat(),
            "UPDATED_LABEL": f"{updated:%B} {updated.day}, {updated.year}",
            "ENTRY_COUNT": count_label,
            "DIRECTORY_HREF": directory_href,
            "ATLAS_LINKS": "".join(nav_links),
            "ENTRY_NAME": entry_name.capitalize(),
            "ENTRY_PLURAL": f"{entry_name}s",
            "PEOPLE_LABEL": "Creators" if solo_view else "Founders",
            "DATA": json.dumps({"labs": entries, "metrics": metrics, "entryName": entry_name}, ensure_ascii=False,
                               separators=(",", ":")).replace("<", "\\u003c"),
        }
        directory = output / route
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(
            re.sub(r"@@([A-Z_]+)@@", lambda match: content[match[1]], template), encoding="utf-8"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--home-href", default=HOME_URL, help="Home link for the article header")
    args = parser.parse_args()
    build(args.output, args.home_href)
