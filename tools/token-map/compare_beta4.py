"""Compare a supplied documentary versions.txt with exact canonical values.

No automatic prefix repair or profile selection. Input is never executed.
"""
import argparse
import importlib.util
import json
import re
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("token_map_generator", Path(__file__).with_name("generate.py"))
GEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEN)


def compare(text, records):
    listed = set(re.findall(r"\s-\s+((?:GSERV|SERV|GNW|G3D|NW)[A-Za-z0-9]+)\b", text))
    known = {r["token"] for r in records if r["state"] == "known"}
    matches = sorted(listed & known)
    # Suggestions are displayed separately; they are never used for matching.
    prefix_discrepancies = {token: "G" + token for token in sorted(listed - known)
                            if token.startswith(("SERV", "NW")) and "G" + token in known}
    unresolved = sorted(listed - known - prefix_discrepancies.keys())
    return dict(documentary_values=len(listed), exact_matches=matches,
                raw_prefix_discrepancies=prefix_discrepancies, unmatched=unresolved,
                canonical_values_not_in_raw_list=sorted(known - listed),
                ambiguous_matches={token: [dict(build=r["build"], platform=r["platform"], role=r["role"])
                                           for r in records if r["token"] == token]
                                   for token in matches if sum(r["token"] == token for r in records) > 1})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("versions", type=Path)
    args = parser.parse_args()
    records = GEN.parse(GEN.SOURCE.read_text(encoding="utf-8"))
    print(json.dumps(compare(args.versions.read_text(encoding="utf-8-sig"), records), indent=2))


if __name__ == "__main__":
    main()
