import { test } from "node:test";
import assert from "node:assert/strict";
import { createHttpApi } from "../../apps/web/src/api/client.ts";

test('task cycle errors expose only a bounded safe path',async()=>{
 for(const path of [['task-a','task-b','task-a'],['<script>'],Array(257).fill('a')]){
  const api=createHttpApi((async()=>Response.json({error:{code:'DEPENDENCY_CYCLE',details:{cyclePath:path,secret:'not exposed'}}},{status:409})) as typeof fetch);
  await assert.rejects(api.taskManager('p'),(error:any)=>{
   assert.equal(error.code,'DEPENDENCY_CYCLE');assert.deepEqual(error.cyclePath,path.length===3?path:undefined);assert.equal(error.secret,undefined);return true;
  });
 }
});
test("visible message history explicitly requests newest journal pages with scoped offsets and abort signal", async () => {
  let url = "",
    init: RequestInit | undefined;
  const controller = new AbortController(),
    api = createHttpApi((async (input: string, options?: RequestInit) => {
      url = input;
      init = options;
      return Response.json({ items: [], hasMore: false });
    }) as typeof fetch);
  await api.messages("p/one", "s&two", 1050, controller.signal);
  const parsed = new URL(url, "http://synthetic.invalid");
  assert.equal(parsed.pathname, "/api/v1/projects/p%2Fone/entities");
  assert.equal(parsed.searchParams.get("parentId"), "s&two");
  assert.equal(parsed.searchParams.get("kind"), "message");
  assert.equal(parsed.searchParams.get("order"), "newest");
  assert.equal(parsed.searchParams.get("offset"), "1050");
  assert.equal(parsed.searchParams.get("limit"), "50");
  assert.equal(init?.signal, controller.signal);
});
test("backup creation does not rotate; explicit rotation sends only reviewed candidate IDs", async () => {
  const calls: { url: string; body: unknown }[] = [];
  const api = createHttpApi((async (url: string, init?: RequestInit) => {
    calls.push({
      url,
      body: init?.body ? JSON.parse(String(init.body)) : undefined,
    });
    return Response.json(
      url.endsWith("/session")
        ? { csrfToken: "synthetic" }
        : url.endsWith("/rotation")
          ? { rotatedBackupIds: ["managed-1"], retention: "complete" }
          : {
              backupId: "new",
              manifest: {},
              rotationCandidateIds: ["managed-1"],
              retention: "pending",
            },
    );
  }) as typeof fetch);
  await api.pair();
  const backup = await api.backup("p");
  assert.equal(calls.length, 2);
  assert.equal(backup.retention, "pending");
  await api.rotateBackups("p", backup.rotationCandidateIds!);
  assert.equal(calls[2].url, "/api/v1/projects/p/backups/rotation");
  assert.deepEqual(calls[2].body, { candidateIds: ["managed-1"] });
});
test("connection/source/bundle/search operations use only bounded project routes and authenticated bodies", async () => {
  const calls: { url: string; init?: RequestInit }[] = [];
  const api = createHttpApi((async (url: string, init?: RequestInit) => {
    calls.push({ url, init });
    return Response.json(
      url.endsWith("/session")
        ? { csrfToken: "synthetic", instanceId: "instance" }
        : {
            verified: false,
            mode: "legacy_import",
            coverage: "partial",
            status: "rebuilt",
          },
    );
  }) as typeof fetch);
  await api.pair();
  await api.connect({
    connectionId: "synthetic-alias",
    apiKey: "synthetic-not-a-key",
    remember: false,
  });
  await api.disconnect();
  await api.previewImport(
    "p",
    "tasks.json",
    "synthetic",
    "research/tasks.json",
  );
  await api.previewImportBundle("p", [
    {
      role: "records",
      sourceName: "tasks.json",
      sourceRelativePath: "research/tasks.json",
      content: "synthetic",
    },
  ]);
  await api.sourceStatus("p");
  await api.sourceContent("p", "requirements");
  await api.rebuildSearch("p");
  assert.equal(calls[1].url, "/api/v1/connection");
  assert.equal(calls[1].url.includes("synthetic-not-a-key"), false);
  assert.equal(calls[2].init?.method, "DELETE");
  assert.equal(
    JSON.parse(String(calls[3].init?.body)).sourceRelativePath,
    "research/tasks.json",
  );
  assert.equal(calls[5].url, "/api/v1/projects/p/imports/source-status");
  assert.equal(calls[6].url, "/api/v1/projects/p/sources/requirements");
  assert.equal(calls[7].url, "/api/v1/projects/p/search/rebuild");
  assert.equal(calls[7].init?.method, "POST");
});
test("session polling passes abort signals and authenticated Quit carries CSRF", async () => {
  const controller = new AbortController(),
    calls: { url: string; init?: RequestInit }[] = [];
  const api = createHttpApi((async (url: string, init?: RequestInit) => {
    calls.push({ url, init });
    return Response.json(
      url.endsWith("/session")
        ? { csrfToken: "synthetic", instanceId: "instance-valid-format" }
        : url.endsWith("/quit")
          ? { status: "quit_requested" }
          : url.includes("/entities?")
            ? { items: [], hasMore: false }
            : { canSend: false, reason: "unverified", mode: "planning" },
    );
  }) as typeof fetch);
  await api.pair();
  const state = await api.runtimeState("p", "s", controller.signal);
  assert.equal(state.mode, "planning");
  await api.entities("p", "message", "s", 0, controller.signal);
  await api.quit();
  assert.equal(calls[1].init?.signal, controller.signal);
  assert.equal(calls[2].init?.signal, controller.signal);
  assert.equal(calls[3].init?.method, "POST");
  assert.equal(
    (calls[3].init?.headers as Record<string, string>)["X-PAOS-CSRF"],
    "synthetic",
  );
});
test("authenticated commands carry project epoch, revision and CSRF without putting pairing code in URL", async () => {
  const calls: { url: string; init?: RequestInit }[] = [];
  const fetcher = (async (url: string, init?: RequestInit) => {
    calls.push({ url, init });
    return Response.json(
      url.endsWith("/bootstrap/exchange")
        ? { csrfToken: "synthetic-csrf" }
        : url.endsWith("/projects")
          ? { items: [{ id: "p/1", authorityEpoch: 4 }] }
          : { ok: true },
    );
  }) as typeof fetch;
  const api = createHttpApi(fetcher);
  await api.pair("synthetic-code");
  await api.projects();
  await api.command("p/1", [
    {
      expectedRevision: 3,
      entity: { id: "t", projectId: "p/1", kind: "task", revision: 3 },
    },
  ]);
  assert.equal(calls[0].url.includes("synthetic-code"), false);
  assert.equal(calls[2].url, "/api/v1/projects/p%2F1/commands");
  assert.equal(
    (calls[2].init?.headers as Record<string, string>)["X-PAOS-CSRF"],
    "synthetic-csrf",
  );
  assert.equal(
    JSON.parse(String(calls[2].init?.body)).expectedAuthorityEpoch,
    4,
  );
  assert.equal(calls[2].init?.credentials, "same-origin");
});
test("writes fail closed before pairing and before project authority is loaded", async () => {
  let calls = 0;
  const api = createHttpApi((async () => {
    calls++;
    return Response.json({});
  }) as typeof fetch);
  await assert.rejects(
    api.preferences.write({ locale: "en", theme: "dark" }),
    /session/i,
  );
  await assert.rejects(api.command("p", []), /authority/i);
  assert.equal(calls, 0);
});
test("revision conflicts retain the allowlisted service error code for recovery", async () => {
  const api = createHttpApi((async () =>
    Response.json(
      { error: { code: "REVISION_CONFLICT" } },
      { status: 409 },
    )) as typeof fetch);
  await assert.rejects(api.projects(), /HTTP 409: REVISION_CONFLICT/);
});

test("session-required errors are typed and invalidate paired write authority", async () => {
  const calls: string[] = [];
  const api = createHttpApi((async (url: string) => {
    calls.push(url);
    return url.endsWith('/session')
      ? Response.json({csrfToken:'synthetic'})
      : url.endsWith('/projects') ? Response.json({items:[{id:'p',authorityEpoch:4}]})
      : Response.json({error:{code:'SESSION_REQUIRED'}},{status:401});
  }) as typeof fetch);
  await api.pair();
  await api.projects();
  await assert.rejects(api.connection(), (error: any) => error.status===401&&error.code==='SESSION_REQUIRED');
  await assert.rejects(api.quit(), /Paired session required/);
  await api.pair();
  await assert.rejects(api.command('p', []), /authority/i);
  assert.deepEqual(calls,['/api/v1/session','/api/v1/projects','/api/v1/connection','/api/v1/session']);
});
test("import confirmation preserves stage identity and authority, restore stays in a separate destination", async () => {
  const calls: { url: string; body: Record<string, unknown> }[] = [];
  const api = createHttpApi((async (url: string, init?: RequestInit) => {
    calls.push({ url, body: JSON.parse(String(init?.body ?? "{}")) });
    return Response.json(
      url.endsWith("/session")
        ? { csrfToken: "synthetic" }
        : url.endsWith("/projects")
          ? { items: [{ id: "p", authorityEpoch: 7 }] }
          : url.endsWith("/restores")
            ? {
                restoreId: "restore-1",
                requiresRestart: true,
                activeProfileChanged: false,
              }
            : { mappingCount: 2, backupId: "backup-1", receipt: {} },
    );
  }) as typeof fetch);
  await api.pair();
  await api.projects();
  await api.commitImport("p", {
    stageId: "stage-1",
    currentSource: "synthetic source",
    sourceDigest: "digest",
    idempotencyKey: "same-retry",
  });
  assert.equal(calls[2].url, "/api/v1/projects/p/imports/commit");
  assert.equal(calls[2].body.expectedAuthorityEpoch, 7);
  assert.equal(calls[2].body.idempotencyKey, "same-retry");
  const restored = await api.restore("p", "backup-1");
  assert.equal(restored.activeProfileChanged, false);
  assert.equal(restored.requiresRestart, true);
  assert.deepEqual(calls[3].body, { backupId: "backup-1" });
  await api.exportTasks("p");
  assert.equal(calls[4].url, "/api/v1/projects/p/imports/export");
});
