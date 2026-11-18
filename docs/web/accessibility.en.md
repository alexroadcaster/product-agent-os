# Web accessibility, languages and themes

Source status: project-authored / bounded local technical verification; PAOS-0029, 2026-11-12.

Current feature accessibility changes and the status of F24 are tracked in the [FUNC matrix](../planning/functional-remediation-2026-11-15.en.md); the PAOS-0029 results here apply to the date above. Technical checks are separate from F23 human acceptance.

In Settings, choose Russian or English and Light, Dark or System, then save. System follows the system color preference. User-authored task and workflow names, paths, identifiers and document content retain their original values. Technical error codes and schema keys may remain in English.

## FUNC-G07 / F24 — availability beside the action

Source status: implemented local UI, 2026-11-16; focused checks and synthetic browser7/7 on the current build; human acceptance not observed. Runtime, usage, Map, Database/usages, proposals, discovery, history and autonomy show their own scope, limitation reason and next step. The global connection API attests an attached worker only and displays Connected; broker qualification is checked in the selected session snapshot. Neither broker flags from connection metadata nor model access promote the global badge to qualified. Fresh lexical maps remain partial; empty/Python-only indexes never imply full analysis. Metadata and Files remain available independently of the parser. Not-configured/unsupported/unavailable/indexing/partial/stale/failed states are distinct; unknown is never loading. Named `note` regions preserve native keyboard controls. Explanations add no approval and change no authority. F19 integration and the human [F23 protocol](pilot.en.md#func-g07-pilot-protocol) remain separate. [Current receipts/status](../planning/functional-remediation-2026-11-15.en.md#func-g07-results). App-channel guidance is rendered only for the App route; BYOK retains its own credential/model-access hints.

## Keyboard controls

| Action | Control |
| --- | --- |
| Skip navigation | Tab to the skip link, then Enter |
| Open a section or card | Tab / Shift+Tab, then Enter or Space |
| Scroll Kanban | Focus the board region and use arrow keys; a list view is also available |
| Move a task | Open its card and choose a column in the move field. For columns with multiple statuses, choose a status in the dialog. Existing transition guards and confirmation still apply |
| Switch task tabs | Tab to the selected tab, then arrows, Home / End |
| Close the status dialog | Escape restores focus to the move field. Tab / Shift+Tab remain inside the dialog |
| Close mobile navigation | Escape returns focus to Menu; entering content closes navigation |
| Edit a workflow | Tab through inputs, edit values, press Enter on Save to save a draft. Publication and execution remain separate actions |
| Read a long transcript | Focus the message region and use arrows or PageUp / PageDown |

Narrow layouts wrap fields and actions. Boards, graphs and some tables retain their own scrolling for spatial data. The header truncates long project names; their full values remain available in its tooltip and the project selector.

## Verification and limits

`tests/web/accessibility/browser-acceptance.mts` uses the production build and a disposable local service with synthetic data. It maps S01–S26 to existing functional UI states, including editors within Settings, and tests eight task tabs in RU/EN × Light/Dark at 1440 and 320 CSS px. This mapping does not imply 26 separate implemented URLs.

Checks cover Chromium Accessibility Tree names, computed RGB text contrast, input boundaries, focused action visibility and occlusion, reflow, modal behavior and keyboard controls. Separate scenarios exercise empty data, loading / unavailable / recovery, System and forced colors. Source and build hashes are recorded before and after each run; external requests are blocked. Commands, receipts, failures and limits belong to the PAOS-0029 report: `research/product-agent-os-web-m4-0029-execution-2026-11-12.md` (repository-root path).

Text thresholds are 4.5:1 for normal text and 3:1 for large text; active field boundaries use 3:1, based on [WCAG 2.2](https://www.w3.org/TR/WCAG22/). The RGB audit excludes some native widget paint, gradients, placeholder text and assistive technology combinations. Forced-colors testing demonstrates Chromium keyboard focus, not every OS/browser combination. Manual screen-reader acceptance and full WCAG conformance certification are not claimed.

When the service is unavailable, preserve unsaved text before reloading. Use Refresh or revisit the section after recovery. An error never establishes a successful save. Checking appearance does not require enabling a provider or native execution.
