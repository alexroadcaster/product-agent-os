"""Read-only document navigation and provenance checks for a supplied manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from product_agent_os.document_navigation import (
    check_local_links, check_reference, documentation_inventory, duplicate_blocks,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', type=Path)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        packet = json.loads(args.manifest.read_text(encoding='utf-8'))
        paths = packet.get('paths', [])
        if not isinstance(paths, list) or not isinstance(packet.get('references', []), list):
            raise ValueError('invalid document manifest')
        refs = [check_reference(args.workspace, item) for item in packet.get('references', [])]
        links = check_local_links(args.workspace, paths)
        result = {'navigation': documentation_inventory(args.workspace, signals=packet.get('signals', {})),
                  'duplicates': duplicate_blocks(args.workspace, paths), 'links': links, 'references': refs,
                  'write_policy': 'read_only'}
        result['ok'] = not links and all(item['status'] in {'verified', 'unavailable_optional'} for item in refs)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['ok'] else 1
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(json.dumps({'ok': False, 'error_type': type(exc).__name__}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
