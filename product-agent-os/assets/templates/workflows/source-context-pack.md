# Source Context Pack

Project: {project_name}
Profile: {profile_name}

## Inputs

- Task:
- Detected stack: {detected_stack_text}
- Source status:
- Freshness requirement:
- Context7 query, if official docs are needed:

## Process

- Collect enough read-only context for the next role.
- Prefer official sources for platform behavior.
- Record source status and freshness for every source-backed claim.
- Note whether Context7 was used and whether the underlying source is official.
- Check whether `docs/sources/registry.md` needs an entry or update.
- Keep unsupported claims separate from verified facts.

## Outputs

- Files read:
- Existing patterns:
- Commands discovered:
- Constraints:
- Official-source registry notes:
- Unsupported claims:
- Unknowns:

## Verification

- Source links or local file paths are recorded.
- Freshness risk is named for current APIs, models, prices, security, and runtime behavior.
- Unsupported claims are not promoted into core guidance.

## Stop Conditions

- Required source cannot be accessed.
- Official source conflicts with local docs.
- Claim cannot be verified within the current scope.
