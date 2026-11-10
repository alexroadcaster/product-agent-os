"""Review/apply a task's documentation packet using existing recovery storage."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from product_agent_os import documentation_sync as sync
from product_agent_os.control_plane_compaction import rollback


def main() -> int:
    """Preview to stdout; only an exact approved proposal can write the workspace."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', type=Path)
    parser.add_argument('action', choices=('assess', 'preview', 'apply', 'rollback'))
    parser.add_argument('packet', help='existing task packet/proposal JSON, or recovery journal for rollback')
    parser.add_argument('--approved-digest')
    parser.add_argument('--abandoned-lock-digest')
    args = parser.parse_args()
    try:
        if args.action == 'rollback':
            result = rollback(args.workspace, args.packet, abandoned_lock_digest=args.abandoned_lock_digest)
        else:
            path = Path(args.packet)
            if path.stat().st_size > 16 * 1024 * 1024:
                raise ValueError('packet size budget exceeded')
            packet = json.loads(path.read_text(encoding='utf-8'))
            if args.action == 'assess':
                result = sync.assess(args.workspace, packet['impact'])
            elif args.action == 'preview':
                result = sync.propose(args.workspace, packet['impact'], packet.get('patches', []), completion=packet.get('completion'))
            else:
                result = sync.apply(args.workspace, packet, approved_digest=args.approved_digest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
