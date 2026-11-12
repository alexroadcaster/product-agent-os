# Web accessibility, languages and themes

Source status: project-authored / bounded local technical verification; PAOS-0029, 2026-11-12.

In Settings, choose Russian or English and Light, Dark or System, then save. System follows the system color preference. User-authored task and workflow names, paths, identifiers and document content retain their original values. Technical error codes and schema keys may remain in English.

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
