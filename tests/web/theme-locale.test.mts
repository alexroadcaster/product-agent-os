import assert from 'node:assert/strict';
import { test } from 'node:test';
import { applyUiPreferences, loadUiPreferences, saveUiPreferences } from '../../apps/web/src/design/preferences.ts';
import { bindUiPreferenceControls } from '../../apps/web/src/design/preference-controls.ts';
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

function createPreferenceControls() {
  function element() {
    const attributes = new Map<string, string>();
    return Object.assign(new EventTarget(), {
      attributes,
      textContent: '',
      setAttribute: (name: string, value: string) => { attributes.set(name, value); },
    });
  }
  function select(values: readonly string[]) {
    return Object.assign(element(), {
      value: '', options: values.map((value) => ({ value, textContent: '' })),
    });
  }
  return {
    root: element(), form: new EventTarget(), locale: select(['ru', 'en']), theme: select(['light', 'dark', 'system']),
    save: element(), status: element(), systemScheme: Object.assign(new EventTarget(), { matches: false }),
  };
}

test('restores native appearance controls and applies the new locale and theme after saving', async () => {
  const controls = createPreferenceControls();
  let stored = { locale: 'en', theme: 'dark' };
  const applied: string[] = [];
  controls.form.addEventListener('paos:preferences-applied', (event) => applied.push((event as CustomEvent).detail.locale));
  const dispose = await bindUiPreferenceControls({
    ...controls,
    store: { read: async () => stored, write: async (preferences) => { stored = preferences; } },
  });

  assert.deepEqual([controls.locale.value, controls.theme.value], ['en', 'dark']);
  assert.equal(controls.root.attributes.get('lang'), 'en');
  assert.equal(controls.root.attributes.get('data-theme'), 'dark');
  assert.equal(controls.locale.attributes.get('aria-label'), 'Language');
  assert.equal(controls.theme.attributes.get('aria-label'), 'Theme');
  assert.equal(controls.status.attributes.get('role'), 'status');
  assert.deepEqual(controls.theme.options.map((option) => option.textContent), ['Light', 'Dark', 'System']);

  controls.locale.value = 'ru';
  controls.theme.value = 'system';
  controls.locale.dispatchEvent(new Event('change'));
  assert.equal(controls.status.textContent, 'Unsaved changes');
  assert.equal(controls.root.attributes.get('lang'), 'en');
  const submit = new Event('submit', { cancelable: true });
  controls.form.dispatchEvent(submit);
  await new Promise<void>((resolve) => setImmediate(resolve));

  assert.equal(submit.defaultPrevented, true);
  assert.deepEqual(stored, { locale: 'ru', theme: 'system' });
  assert.equal(controls.root.attributes.get('lang'), 'ru');
  assert.equal(controls.root.attributes.get('data-theme'), 'light');
  assert.equal(controls.locale.attributes.get('aria-label'), 'Язык');
  assert.equal(controls.save.textContent, 'Сохранить настройки');
  assert.equal(controls.status.textContent, 'Настройки сохранены');
  assert.deepEqual(applied, ['en', 'ru']);
  dispose();
});

test('keeps the draft on a failed write and allows retry without a duplicate in-flight write', async () => {
  const controls = createPreferenceControls();
  const pending = Promise.withResolvers<void>();
  const writes: unknown[] = [];
  const dispose = await bindUiPreferenceControls({
    ...controls,
    store: {
      read: async () => ({ locale: 'en', theme: 'dark' }),
      write: async (preferences) => {
        writes.push(preferences);
        if (writes.length === 1) {
          await pending.promise;
        }
      },
    },
  });

  const submit = () => controls.form.dispatchEvent(new Event('submit', { cancelable: true }));
  controls.theme.value = 'light';
  submit();
  submit();
  assert.deepEqual(writes, [{ locale: 'en', theme: 'light' }]);
  assert.equal(controls.save.attributes.get('aria-disabled'), 'true');
  assert.equal(controls.root.attributes.get('data-theme'), 'dark');

  controls.theme.value = 'system';
  controls.theme.dispatchEvent(new Event('change'));
  pending.reject(new Error('Synthetic write failure'));
  await new Promise<void>((resolve) => setImmediate(resolve));

  assert.equal(controls.status.textContent, 'Could not save preferences');
  assert.equal(controls.theme.value, 'system');
  assert.equal(controls.root.attributes.get('data-theme'), 'dark');
  assert.equal(controls.save.attributes.get('aria-disabled'), 'false');

  submit();
  await new Promise<void>((resolve) => setImmediate(resolve));
  assert.deepEqual(writes, [{ locale: 'en', theme: 'light' }, { locale: 'en', theme: 'system' }]);
  assert.equal(controls.root.attributes.get('data-theme'), 'light');
  assert.equal(controls.status.textContent, 'Preferences saved');
  dispose();
});

test('follows the system theme while mounted and detaches from device changes after disposal', async () => {
  const controls = createPreferenceControls();
  const dispose = await bindUiPreferenceControls({
    ...controls,
    store: { read: async () => ({ locale: 'ru', theme: 'system' }), write: async () => {} },
  });

  assert.equal(controls.root.attributes.get('data-theme'), 'light');
  controls.systemScheme.matches = true;
  controls.systemScheme.dispatchEvent(new Event('change'));
  assert.equal(controls.root.attributes.get('data-theme'), 'dark');

  dispose();
  controls.systemScheme.matches = false;
  controls.systemScheme.dispatchEvent(new Event('change'));
  assert.equal(controls.root.attributes.get('data-theme'), 'dark');
});
