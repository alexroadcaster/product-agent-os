# Local HTML Interaction Boundary

Source status: `project evidence`

Generated HTML may include local tabs, search, filters, diagrams, and disclosure controls. These interactions are allowed only as an offline review surface and are not runtime/browser proof without a separately approved evidence packet.

The default policy is local-only: no external scripts, no provider calls, no telemetry, no target mutation, and no hidden readiness wording.

## Allowed Interactions

| Interaction | Condition |
| --- | --- |
| Tabs and section navigation | Work inside one generated file and do not hide claim ceilings. |
| Search/filter | Search embedded data only, without network requests. |
| Diagram controls | Use local/vendor assets or static fallback. |
| Copy/open helpers | Do not mutate files, start shells, or send data. |
| JS-disabled fallback | Main information remains readable without script execution. |

## Forbidden Interactions

- External fetch, provider/API call, telemetry, or beacon.
- File mutation, cleanup execution, shell command, or target apply.
- Hiding unsupported claims, stale warnings, or approval boundaries.
- Browser-proof wording without approved browser run, screenshots, console/network evidence, and viewport notes.

## Browser-Proof Packet

If the owner approves browser proof, evidence must name URL/path, tool, viewport set, console errors, network requests, screenshots, source-boundary labels, mobile overflow status, JS-disabled fallback, and cleanup. Without that packet, status remains `static_docs_only`.

## Verification

For this docs slice, static docs checks and strict MkDocs smoke are enough. Real browser automation, screenshots, WCAG proof, visual regression, and external network checks remain approval-required.
