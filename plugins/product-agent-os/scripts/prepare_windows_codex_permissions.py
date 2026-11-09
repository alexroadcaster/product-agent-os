from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.windows_codex_permissions import (  # noqa: E402
    apply_permissions,
    build_repair_plan,
    restore_permissions,
    check_permissions,
    dumps_json,
)


def main(argv: list[str] | None = None) -> int:
    """Default to diagnostics; repair modes require explicit scope and pinned evidence."""
    parser = argparse.ArgumentParser(
        description="Read-only Windows permissions diagnostics; exact repair is a separate owner-approved operation."
    )
    parser.add_argument("workspace", help="Target project workspace.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Repair one reviewed target/SID with a fresh plan digest and backup.")
    mode.add_argument("--preview-repair", action="store_true", help="Read-only exact target/SID plan; no ACL writes.")
    mode.add_argument("--restore", action="store_true", help="Restore an owner-approved, digest-pinned snapshot.")
    parser.add_argument("--target")
    parser.add_argument("--sid")
    parser.add_argument("--plan-digest")
    parser.add_argument("--backup")
    parser.add_argument("--backup-sha256")
    args = parser.parse_args(argv)

    if args.preview_repair or args.restore:
        if not args.target or (args.preview_repair and not args.sid) or (args.restore and not (args.backup and args.backup_sha256)):
            parser.error("exact target and mode-specific SID or snapshot/digest are required")
    try:
        if args.apply:
            result = apply_permissions(args.workspace, target=args.target, sid=args.sid,
                plan_digest=args.plan_digest, backup=args.backup)
        elif args.preview_repair:
            result = {**build_repair_plan(args.workspace, args.target, args.sid), "status": "preview"}
        elif args.restore:
            result = restore_permissions(args.workspace, args.target, args.backup, args.backup_sha256)
        else:
            result = check_permissions(args.workspace)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        result = {"status": "blocked", "errors": [str(exc)]}
    print(dumps_json(result))
    return 0 if result["status"] in {"checked", "applied", "preview", "restored"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
