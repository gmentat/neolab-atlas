"""Render the directory and small-teams view as static HTML."""

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE_URL = "https://antonfed.com/neolabs/"


def build(output: Path) -> None:
    data = json.loads((ROOT / "data/atlas.json").read_text(encoding="utf-8"))
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    updated = date.fromisoformat(data["updated"])
    small_teams = set(data["small_teams"])
    labs = data["labs"]
    names = {lab["name"] for lab in labs}
    if len(names) != len(labs) or small_teams - names:
        raise ValueError("Lab names must be unique and all small-team entries must exist in the directory.")

    for small in (False, True):
        entries = [lab for lab in labs if not small or lab["name"] in small_teams]
        metrics = {
            key: metric
            for key, metric in data["metrics"].items()
            if any(key in lab["metrics"] for lab in entries)
        }
        title = "Small teams & solos" if small else "AI neolab directory"
        description = (
            "Small teams, solo researchers, and independent groups with documented model research."
            if small else "Explore original work on AI models, architectures, and training."
        )
        cohort = (
            '<button type="button" data-cohort="solo" aria-label="Solos &amp; solo-led" '
            'title="Includes solo-led projects">Solos</button>'
            '<button type="button" data-cohort="small">Small teams</button>'
            if small else '<button type="button" data-cohort="startup">Research startups</button>'
        )
        content = {
            "TITLE": escape(title),
            "DESCRIPTION": escape(description, quote=True),
            "CANONICAL": SITE_URL + ("small-teams/" if small else ""),
            "UPDATED_DATE": updated.isoformat(),
            "UPDATED_LABEL": f"{updated:%B} {updated.day}, {updated.year}",
            "DIRECTORY_HREF": "../" if small else "./",
            "SMALL_HREF": "./" if small else "small-teams/",
            "CURRENT_DIRECTORY": "" if small else ' aria-current="page"',
            "CURRENT_SMALL": ' aria-current="page"' if small else "",
            "COHORT": cohort,
            "DATA": json.dumps({"labs": entries, "metrics": metrics}, ensure_ascii=False,
                               separators=(",", ":")).replace("<", "\\u003c"),
        }
        directory = output / "small-teams" if small else output
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(
            re.sub(r"@@([A-Z_]+)@@", lambda match: content[match[1]], template), encoding="utf-8"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    build(parser.parse_args().output)
