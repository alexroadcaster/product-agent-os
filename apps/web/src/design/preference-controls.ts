import { uiLabel, type UiMessage } from "../locales/messages.ts";
import {
  applyUiPreferences,
  loadUiPreferences,
  saveUiPreferences,
  type UiPreferencesStore,
} from "./preferences.ts";

type LabelTarget = { setAttribute(name: string, value: string): void };
type TextTarget = { textContent: string | null };
type PreferenceSelect = EventTarget &
  LabelTarget & {
    value: string;
    options: ArrayLike<TextTarget & { value: string }>;
  };

type PreferenceControls = Readonly<{
  root: LabelTarget;
  form: EventTarget;
  locale: PreferenceSelect;
  theme: PreferenceSelect;
  save: LabelTarget & TextTarget;
  status: LabelTarget & TextTarget;
  systemScheme: EventTarget & { readonly matches: boolean };
  store: UiPreferencesStore;
}>;

/** Mount on a form with explicit option values. The form emits `paos:preferences-applied` on load and save. */
export async function bindUiPreferenceControls({
  root,
  form,
  locale,
  theme,
  save,
  status,
  systemScheme,
  store,
}: PreferenceControls): Promise<() => void> {
  let applied = await loadUiPreferences(store);
  let saving = false;
  let disposed = false;

  const hasDraft = () =>
    locale.value !== applied.locale || theme.value !== applied.theme;
  const updateStatus = (key: UiMessage | null) => {
    status.textContent = key ? uiLabel(applied.locale, key) : "";
  };
  const applyAppearance = () => {
    applyUiPreferences(root, applied, systemScheme.matches ? "dark" : "light");
  };

  /** Relabel the existing nodes while leaving the current selections and focus in place. */
  function renderApplied() {
    applyAppearance();
    locale.setAttribute(
      "aria-label",
      uiLabel(applied.locale, "preferences.language"),
    );
    theme.setAttribute(
      "aria-label",
      uiLabel(applied.locale, "preferences.theme"),
    );
    for (const option of Array.from(locale.options)) {
      if (option.value === "en" || option.value === "ru") {
        option.textContent = uiLabel(applied.locale, `locale.${option.value}`);
      }
    }
    for (const option of Array.from(theme.options)) {
      if (
        option.value === "light" ||
        option.value === "dark" ||
        option.value === "system"
      ) {
        option.textContent = uiLabel(applied.locale, `theme.${option.value}`);
      }
    }
    save.textContent = uiLabel(applied.locale, "preferences.save");
  }

  function publishApplied() {
    form.dispatchEvent(
      new CustomEvent("paos:preferences-applied", {
        detail: { ...applied },
        bubbles: true,
      }),
    );
  }

  function onDraftChange() {
    if (!saving) {
      updateStatus(hasDraft() ? "preferences.unsaved" : null);
    }
  }

  /** Only a successful write advances applied state. Edits during a write remain a draft. */
  async function saveDraft() {
    saving = true;
    save.setAttribute("aria-disabled", "true");
    updateStatus("preferences.saving");
    try {
      applied = await saveUiPreferences(store, {
        locale: locale.value,
        theme: theme.value,
      });
    } catch {
      if (!disposed) {
        updateStatus("preferences.saveError");
      }
      return;
    } finally {
      saving = false;
      if (!disposed) {
        save.setAttribute("aria-disabled", "false");
      }
    }
    if (!disposed) {
      renderApplied();
      updateStatus(hasDraft() ? "preferences.unsaved" : "preferences.saved");
      publishApplied();
    }
  }

  function onSubmit(event: Event) {
    event.preventDefault();
    if (!saving && hasDraft()) {
      void saveDraft();
    }
  }

  function onSystemChange() {
    if (applied.theme === "system") {
      applyAppearance();
    }
  }

  locale.value = applied.locale;
  theme.value = applied.theme;
  status.setAttribute("role", "status");
  save.setAttribute("aria-disabled", "false");
  updateStatus(null);
  renderApplied();
  locale.addEventListener("change", onDraftChange);
  theme.addEventListener("change", onDraftChange);
  form.addEventListener("submit", onSubmit);
  systemScheme.addEventListener("change", onSystemChange);
  publishApplied();

  return () => {
    disposed = true;
    locale.removeEventListener("change", onDraftChange);
    theme.removeEventListener("change", onDraftChange);
    form.removeEventListener("submit", onSubmit);
    systemScheme.removeEventListener("change", onSystemChange);
  };
}
