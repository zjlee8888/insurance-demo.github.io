#!/usr/bin/env python3
"""
Build index.html from agent/app.template.html.

index.html is a single-file bundle. The whole app (HTML + the <x-dc> view
template + the `text/x-dc` component script) lives, JSON-encoded, on ONE line
inside <script type="__bundler/template">...</script>. The runtime does
JSON.parse(textContent) on that line, then Babel-compiles the text/x-dc script.

So the maintainable source is the *decoded* template (agent/app.template.html).
This script re-encodes it and splices it back into that one line, leaving every
other line (asset manifest, unbundler, etc.) untouched. Idempotent & re-runnable.

Encoding notes:
  - json.dumps(..., ensure_ascii=True) emits non-ASCII (Chinese) as \\uXXXX — safe.
  - We then replace '</' with '<\\/'. json.dumps does NOT escape '/', so a literal
    '</script>' inside the string would prematurely close the outer <script> tag.
    '<\\/' is a valid JSON escape that decodes back to '</', so the round-trip is
    byte-for-byte faithful to the decoded value while being HTML-safe.
"""
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
INDEX = os.path.join(REPO, "index.html")
TEMPLATE = os.path.join(HERE, "app.template.html")
TEMPLATE_LINE = 176  # 0-indexed -> file line 177, the __bundler/template payload

def main():
    with open(INDEX, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if len(lines) <= TEMPLATE_LINE:
        sys.exit(f"index.html has only {len(lines)} lines; expected the template on line {TEMPLATE_LINE+1}")

    old = lines[TEMPLATE_LINE]
    if not (old.startswith('"') and old.rstrip().endswith('"')):
        sys.exit("line 177 is not the expected JSON-string template payload — refusing to patch")

    with open(TEMPLATE, encoding="utf-8") as fh:
        template = fh.read()

    encoded = json.dumps(template, ensure_ascii=True).replace("</", "<\\/")

    # sanity: must round-trip back to exactly the template we read
    if json.loads(encoded) != template:
        sys.exit("re-encode round-trip mismatch — aborting")
    for needle in ("class Component", "text/x-dc", "isAssess", "isOnboard"):
        if needle not in template:
            sys.exit(f"template missing expected marker {needle!r} — aborting")

    lines[TEMPLATE_LINE] = encoded
    with open(INDEX, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"OK · template {len(template):,} chars -> line {TEMPLATE_LINE+1} ({len(encoded):,} chars)")
    print(f"index.html now {os.path.getsize(INDEX):,} bytes")

if __name__ == "__main__":
    main()
