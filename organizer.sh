#!/usr/bin/env bash
# organizer.sh — Archives grades.csv with a timestamp, resets the workspace,
#                and logs the operation to organizer.log.

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────────
SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# ── 1. Ensure the archive directory exists ───────────────────────────────────
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
else
    echo "Archive directory already exists: $ARCHIVE_DIR"
fi

# ── 2. Check that grades.csv exists (non-empty run guard) ────────────────────
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi

# ── 3. Generate timestamp ────────────────────────────────────────────────────
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# ── 4. Build the archived filename ───────────────────────────────────────────
BASENAME="${SOURCE_FILE%.csv}"           # grades
ARCHIVED_NAME="${BASENAME}_${TIMESTAMP}.csv"   # grades_20251105-170000.csv
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"

# ── 5. Move (rename + relocate) the file ─────────────────────────────────────
mv "$SOURCE_FILE" "$ARCHIVED_PATH"
echo "Archived: '$SOURCE_FILE'  →  '$ARCHIVED_PATH'"

# ── 6. Create a fresh empty grades.csv ───────────────────────────────────────
touch "$SOURCE_FILE"
echo "Created fresh empty file: '$SOURCE_FILE'"

# ── 7. Append to the log ─────────────────────────────────────────────────────
LOG_ENTRY="[${TIMESTAMP}] Archived '${SOURCE_FILE}' as '${ARCHIVED_PATH}'"
echo "$LOG_ENTRY" >> "$LOG_FILE"
echo "Logged operation to '$LOG_FILE'"
echo ""
echo "Done. Log entry:"
echo "  $LOG_ENTRY"