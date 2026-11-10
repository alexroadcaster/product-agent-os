import type { UiLocale } from '../locales/messages.ts';

export type ResolvedUiTheme = 'light' | 'dark';
export type UiTheme = ResolvedUiTheme | 'system';
export type UiPreferences = Readonly<{ locale: UiLocale; theme: UiTheme }>;

/** Backed by the authenticated local service. The payload contains only appearance settings. */
export type UiPreferencesStore = {
  read(): Promise<unknown>;
  write(preferences: UiPreferences): Promise<void>;
};

function isUiLocale(value: unknown): value is UiLocale {
  return value === 'ru' || value === 'en';
}

function isUiTheme(value: unknown): value is UiTheme {
  return value === 'light' || value === 'dark' || value === 'system';
}

/** Missing or older preference records preserve each supported value independently. */
export async function loadUiPreferences(store: Pick<UiPreferencesStore, 'read'>): Promise<UiPreferences> {
  const stored = await store.read();
  const { locale, theme } = typeof stored === 'object' && stored !== null
    ? stored as { locale?: unknown; theme?: unknown }
    : {};
  return { locale: isUiLocale(locale) ? locale : 'ru', theme: isUiTheme(theme) ? theme : 'system' };
}

export async function saveUiPreferences(
  store: Pick<UiPreferencesStore, 'write'>,
  preferences: UiPreferences,
): Promise<void> {
  const { locale, theme } = preferences;
  if (!isUiLocale(locale) || !isUiTheme(theme)) {
    throw new RangeError('Unsupported UI appearance preference.');
  }
  await store.write({ locale, theme });
}

/** Apply to document.documentElement. Pass the current OS preference when it changes. */
export function applyUiPreferences(
  root: { setAttribute(name: string, value: string): void },
  preferences: UiPreferences,
  systemTheme: ResolvedUiTheme,
): void {
  root.setAttribute('lang', preferences.locale);
  root.setAttribute('data-theme', preferences.theme === 'system' ? systemTheme : preferences.theme);
}
