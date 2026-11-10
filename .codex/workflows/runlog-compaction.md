# Runlog Compaction

Source status: project-local manual workflow; no fresh-session activation claim.

Use the canonical procedure in `plugins/product-agent-os/assets/templates/workflows/runlog-compaction.md` when a changed active document exceeds 40 000 UTF-8 bytes (warning 32 000), or its stricter project limit.

Detailed task matrices in `docs/planning/` are exempt from the default size trigger and stay intact; this does not exempt index/README/control-plane files, explicit per-file project limits, content checks or link checks. In this repository the owner has deferred the audit-matrix split in `research/`; retain its current layout. Existing split previews are historical proposals, not pending apply permission.

The owner reviews a read-only exact-byte proposal before any apply. Current scope, gates, approvals and next steps stay discoverable; original history moves to indexed owning artifacts. Preserve dirty/untracked bytes, source privacy and rollback journals. Unknown classification or conflicting writers stops apply. Finish only after preservation, links, byte limits and recovery checks; summaries never replace source evidence.

Use `compact_control_plane.py` for reviewed moves and `check_documents.py` for local navigation/provenance checks. The lifecycle marker is not an apply approval. SQL-owned projections/frozen cutover sources are not eligible file targets. This workflow neither starts automation nor permits external project changes.
