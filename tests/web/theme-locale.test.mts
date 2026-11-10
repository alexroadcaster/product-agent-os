import assert from 'node:assert/strict';
import { test } from 'node:test';
import { applyUiPreferences, loadUiPreferences, saveUiPreferences } from '../../apps/web/src/design/preferences.ts';
import { uiLabel } from '../../apps/web/src/locales/messages.ts';

test('restores the chosen language and theme from the local preferences store', async () => {
  let persisted: unknown;
  await saveUiPreferences({ write: async (preferences) => { persisted = preferences; } }, { locale: 'en', theme: 'dark' });

  assert.deepEqual(await loadUiPreferences({ read: async () => persisted }), { locale: 'en', theme: 'dark' });
});

test('applies locale and resolves System from the device without replacing the app root', () => {
  const attributes = new Map([['data-active-view', 'session']]);
  const root = { setAttribute: (name: string, value: string) => attributes.set(name, value) };

  applyUiPreferences(root, { locale: 'ru', theme: 'system' }, 'dark');
  assert.deepEqual(Object.fromEntries(attributes), { 'data-active-view': 'session', lang: 'ru', 'data-theme': 'dark' });

  applyUiPreferences(root, { locale: 'en', theme: 'light' }, 'dark');
  assert.deepEqual(Object.fromEntries(attributes), { 'data-active-view': 'session', lang: 'en', 'data-theme': 'light' });
});

test('localizes the same navigation and approval controls for both supported languages', () => {
  assert.equal(uiLabel('ru', 'nav.projectMap'), 'Карта проекта');
  assert.equal(uiLabel('en', 'nav.projectMap'), 'Project map');
  assert.equal(uiLabel('ru', 'state.approvalRequired'), 'Требуется разрешение');
  assert.equal(uiLabel('en', 'state.approvalRequired'), 'Approval required');
});
