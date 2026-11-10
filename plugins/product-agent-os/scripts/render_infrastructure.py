from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.infrastructure import (  # noqa: E402
    InfrastructureError,
    render_infrastructure_plan,
    stage_infrastructure,
)
from product_agent_os.task_routing import TaskContextError, add_task_intake_arguments, task_context_from_args  # noqa: E402
from product_agent_os.project_formation import form_project, source_inventory  # noqa: E402
from product_agent_os.merge_infrastructure import build_merge_plan, apply_merge_plan, rollback_merge, MergeInfrastructureError  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    """Route one explicit operation; generation never implicitly authorizes apply."""
    parser = argparse.ArgumentParser(description="Render Product-Agent OS infrastructure plan.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without writing staged files.")
    parser.add_argument("--stage", help="Write staged artifacts to this output directory.")
    parser.add_argument("--formation-context", help="JSON formation request v1; replaces separate selection/structure steps.")
    parser.add_argument("--preview-digest", help="Exact formation preview digest required for staging.")
    parser.add_argument("--previous-plan", help="Previous preview JSON for review-only change impact.")
    parser.add_argument("--legacy-catalog", action="store_true", help="Explicit compatibility mode: propose the full catalog.")
    parser.add_argument("--analyze", action="store_true", help="Read-only bounded source inventory.")
    parser.add_argument("--merge-stage", help="Existing stage: prepare its merge plan without target writes.")
    parser.add_argument("--apply", action="store_true", help="Apply --merge-stage using --approval-file.")
    parser.add_argument("--approval-file", help="Existing exact merge approval; never inferred from preview.")
    parser.add_argument("--rollback", help="Existing rollback manifest; restores only unchanged owned results.")
    add_task_intake_arguments(parser)
    args = parser.parse_args(argv)

    if sum(map(bool, [args.dry_run, args.stage, args.analyze, args.merge_stage, args.rollback])) != 1:
        print("error: choose --dry-run or --stage, or one of --analyze, --merge-stage, --rollback", file=sys.stderr)
        return 2

    try:
        task_context = task_context_from_args(args.workspace, args)
        if args.apply and (not args.merge_stage or not args.approval_file):
            raise ValueError('--apply requires --merge-stage and --approval-file')
        if args.approval_file and not args.apply:
            raise ValueError('--approval-file requires --apply')
        if args.legacy_catalog and task_context is not None:
            raise ValueError("legacy catalog and scoped context are mutually exclusive")
        if args.formation_context and (args.legacy_catalog or task_context is not None):
            raise ValueError('formation, scoped intake and legacy catalog are mutually exclusive')
        if (args.preview_digest or args.previous_plan) and not args.formation_context:
            raise ValueError('preview/previous plan requires --formation-context')
        if (args.analyze or args.merge_stage or args.rollback) and (args.formation_context or args.legacy_catalog or task_context):
            raise ValueError('analysis/merge/rollback cannot mix generation input')
        if args.analyze:
            result = {'source_inventory': source_inventory(Path(args.workspace).resolve()), 'authority': 'read_only'}
        elif args.merge_stage:
            result = (apply_merge_plan(args.workspace, args.merge_stage, args.approval_file) if args.apply
                      else build_merge_plan(args.workspace, args.merge_stage))
        elif args.rollback:
            result = rollback_merge(args.workspace, args.rollback)
        elif args.formation_context:
            request = json.loads(Path(args.formation_context).read_text(encoding='utf-8'))
            previous = json.loads(Path(args.previous_plan).read_text(encoding='utf-8')) if args.previous_plan else None
            result = form_project(args.workspace, request, stage=args.stage,
                                  approved_preview_digest=args.preview_digest, previous=previous)
        elif args.dry_run:
            task_options = ({"task_context": task_context} if task_context is not None else {})
            if args.legacy_catalog:
                task_options["legacy_catalog"] = True
            result = render_infrastructure_plan(args.workspace, **task_options)
        else:
            task_options = ({"task_context": task_context} if task_context is not None else {})
            if args.legacy_catalog:
                task_options["legacy_catalog"] = True
            result = stage_infrastructure(args.workspace, args.stage, **task_options)
    except (InfrastructureError, TaskContextError, MergeInfrastructureError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    validation = result.get("rendered_artifacts", {}).get("validation", {})
    if result.get('status') == 'blocked' or result.get('infrastructure_plan', {}).get('blocked'):
        return 1
    return 0 if validation.get("ok", args.analyze or args.merge_stage or args.rollback) else 1


if __name__ == "__main__":
    raise SystemExit(main())
