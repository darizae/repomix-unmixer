#!/usr/bin/env bash
# Regenerate the synthetic Repomix parser fixtures.
# Requires Node.js; downloads the pinned Repomix version via npx.
set -euo pipefail

REPOMIX_VERSION="1.19.0"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SAMPLE="$HERE/sample"
OUT="$HERE/repomix-$REPOMIX_VERSION"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/repomix-fixtures-XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

run_repomix() {
    local source_dir="$1" output_file="$2" style="$3"
    shift 3
    ( cd "$source_dir" && npx --yes "repomix@$REPOMIX_VERSION" \
        --quiet --style "$style" --no-git-sort-by-changes "$@" \
        --output "$output_file" . )
}

mkdir -p "$OUT/markdown" "$OUT/markdown-parsable" "$OUT/xml" "$OUT/xml-parsable" \
    "$OUT/json" "$OUT/line-numbers" "$OUT/edge/markdown" "$OUT/edge/xml" \
    "$OUT/edge/xml-parsable" "$OUT/edge/json"

run_repomix "$SAMPLE" "$OUT/markdown/repomix-output.md" markdown
run_repomix "$SAMPLE" "$OUT/markdown-parsable/repomix-output.md" markdown --parsable-style
run_repomix "$SAMPLE" "$OUT/xml/repomix-output.xml" xml
run_repomix "$SAMPLE" "$OUT/xml-parsable/repomix-output.xml" xml --parsable-style
run_repomix "$SAMPLE" "$OUT/json/repomix-output.json" json
run_repomix "$SAMPLE" "$OUT/line-numbers/markdown.md" markdown --output-show-line-numbers
run_repomix "$SAMPLE" "$OUT/line-numbers/xml.xml" xml --output-show-line-numbers
run_repomix "$SAMPLE" "$OUT/line-numbers/json.json" json --output-show-line-numbers

# Edge tree: fence lengths, trailing spaces, and XML-special characters.
EDGE="$TMP/edge"
mkdir -p "$EDGE"
printf 'before\n`````\nafter\n' > "$EDGE/five.md"
printf 'before\n``````\nafter\n' > "$EDGE/six.md"
printf 'before\n``````````\nafter\n' > "$EDGE/ten.md"
printf 'before\n`````  \nafter\n' > "$EDGE/trailing-spaces.md"
printf 'text ending with `````' > "$EDGE/ends-fence.md"
printf 'space path\n' > "$EDGE/with space.txt"
printf 'weird path\n' > "$EDGE/amp&quote\"name.txt"

run_repomix "$EDGE" "$OUT/edge/markdown/repomix-output.md" markdown
run_repomix "$EDGE" "$OUT/edge/xml/repomix-output.xml" xml
run_repomix "$EDGE" "$OUT/edge/xml-parsable/repomix-output.xml" xml --parsable-style
run_repomix "$EDGE" "$OUT/edge/json/repomix-output.json" json

echo "Regenerated fixtures with repomix@$REPOMIX_VERSION in $OUT"
