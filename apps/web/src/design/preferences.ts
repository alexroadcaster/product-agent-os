import type { ResolvedUiTheme, UiPreferences } from "../../../../packages/contracts/ui/preferences.ts";
export { loadUiPreferences, saveUiPreferences } from "../../../../packages/contracts/ui/preferences.ts";
export type { UiLocale, ResolvedUiTheme, UiTheme, UiPreferences, UiPreferencesStore } from "../../../../packages/contracts/ui/preferences.ts";

/** Apply to document.documentElement. Pass the current OS preference when it changes. */
export function applyUiPreferences(
  root: { setAttribute(name: string, value: string): void },
  preferences: UiPreferences,
  systemTheme: ResolvedUiTheme,
): void {
  root.setAttribute("lang", preferences.locale);
  root.setAttribute(
    "data-theme",
    preferences.theme === "system" ? systemTheme : preferences.theme,
  );
}
