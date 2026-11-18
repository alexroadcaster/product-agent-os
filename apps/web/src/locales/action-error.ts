import type {UiLocale} from './messages.ts';

export const actionFailedText = ['Действие не выполнено', 'Action failed'] as const;

export function actionErrorText(
  locale: UiLocale,
  error: unknown,
  hints?: Readonly<Record<string, readonly [string, string]>>,
): string {
  const value = String(error);
  const code = (error as {code?: string})?.code ?? value.match(/\b[A-Z][A-Z_]{4,}\b/)?.[0];
  const hint = hints && code && Object.hasOwn(hints, code) ? hints[code] : undefined;
  const path = (error as {cyclePath?: readonly string[]})?.cyclePath;
  const language = locale === 'ru' ? 0 : 1;
  const prefix = actionFailedText[language];
  const detail = hint?.[language] ?? value;
  return `${prefix}: ${detail}${code ? ` (${code})` : ''}${path?.length ? ` · ${path.join(' → ')}` : ''}`;
}
