import { useEffect, useState } from "react";
import type { M1Api, StoredEntity } from "../api/client.ts";
import type { AppLabel } from "../locales/app.ts";
export function TaskRelations({
  api,
  entity,
  t,
  onSave,
}: {
  api: M1Api;
  entity: StoredEntity;
  t: (key: AppLabel) => string;
  onSave: (entity: StoredEntity) => Promise<void>;
}) {
  const [tasks, setTasks] = useState<StoredEntity[]>([]),
    [offset, setOffset] = useState(0),
    [more, setMore] = useState(false),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const links = Array.isArray(entity.data?.links)
    ? (entity.data.links as {
        relation: string;
        taskId: string;
        projectId: string;
      }[])
    : [];
  async function load(append = false) {
    setBusy(true);
    try {
      const page = await api.entities(
        entity.projectId,
        "task",
        undefined,
        append ? offset : 0,
      );
      setTasks((previous) =>
        append ? [...previous, ...page.items] : page.items,
      );
      setOffset((append ? offset : 0) + page.items.length);
      setMore(page.hasMore);
    } catch (cause) {
      setError(String(cause));
    } finally {
      setBusy(false);
    }
  }
  useEffect(() => {
    void load();
  }, [entity.projectId]);
  return (
    <section className="task-relations">
      <h3>{t("relations")}</h3>
      <ul>
        {links.map((link, index) => (
          <li key={`${link.relation}:${link.taskId}`}>
            <span className="mono">
              {link.relation} ·{" "}
              {tasks.find((task) => task.id === link.taskId)?.publicKey ??
                link.taskId}
            </span>
            <button
              disabled={busy}
              onClick={async () => {
                setBusy(true);
                try {
                  await onSave({
                    ...entity,
                    data: {
                      ...entity.data,
                      links: links.filter((_, own) => index !== own),
                    },
                  });
                } catch (cause) {
                  setError(String(cause));
                } finally {
                  setBusy(false);
                }
              }}
            >
              {t("remove")}
            </button>
          </li>
        ))}
      </ul>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const data = new FormData(e.currentTarget),
            taskId = String(data.get("taskId")),
            relation = String(data.get("relation"));
          if (
            !tasks.some(
              (task) => task.id === taskId && task.id !== entity.id,
            ) ||
            links.some(
              (link) => link.taskId === taskId && link.relation === relation,
            )
          )
            return;
          setBusy(true);
          try {
            await onSave({
              ...entity,
              data: {
                ...entity.data,
                links: [
                  ...links,
                  { taskId, projectId: entity.projectId, relation },
                ],
              },
            });
          } catch (cause) {
            setError(String(cause));
          } finally {
            setBusy(false);
          }
        }}
      >
        <label>
          {t("relation")}
          <select name="relation">
            {["related", "blocks", "blocked_by"].map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label>
          {t("details")}
          <select name="taskId" required>
            {tasks
              .filter((task) => task.id !== entity.id)
              .map((task) => (
                <option key={task.id} value={task.id}>
                  {task.publicKey ?? task.id}: {task.title}
                </option>
              ))}
          </select>
        </label>
        <button disabled={busy || !tasks.some((task) => task.id !== entity.id)}>
          {t("addRelation")}
        </button>
        {more && (
          <button type="button" disabled={busy} onClick={() => void load(true)}>
            {t("more")}
          </button>
        )}
        <p role="alert">{error}</p>
      </form>
    </section>
  );
}
