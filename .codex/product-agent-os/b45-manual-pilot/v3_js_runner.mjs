import assert from "node:assert/strict";

function result(taskId, cases) {
  return {
    task_id: taskId,
    proof_level: "passed_target_runtime_node_22_18_0",
    status: "passed",
    passed: cases.length,
    total: cases.length,
    cases,
    notes: []
  };
}

function check(name, actual, expected) {
  assert.deepEqual(actual, expected, `${name}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  return { case: name, status: "passed" };
}

function evaluateAccess(request) {
  const audit = [];
  if (!request || !request.actor || !request.resource || !request.action) {
    return { allow: false, reason: "default_deny", audit };
  }
  const { actor, resource, action } = request;
  if (actor.tenantId !== resource.tenantId) {
    const grant = actor.breakGlass;
    if (!grant || !grant.reason || grant.expiresAt <= request.now) {
      return { allow: false, reason: "tenant_mismatch", audit };
    }
    audit.push("break_glass_access");
    return { allow: true, reason: "break_glass", audit };
  }
  if (actor.id === resource.ownerId && action === "read" && resource.sensitivity === "low") {
    return { allow: true, reason: "owner_read", audit };
  }
  if (actor.role === "support" && action === "read" && actor.supportSessionActive) {
    audit.push("support_session");
    return { allow: true, reason: "support_session", audit };
  }
  if (actor.role === "admin") {
    return { allow: true, reason: "tenant_admin", audit };
  }
  return { allow: false, reason: "default_deny", audit };
}

function runAuthPolicy() {
  const base = {
    now: 100,
    actor: { id: "u1", tenantId: "t1", role: "user" },
    resource: { id: "r1", tenantId: "t1", ownerId: "u1", sensitivity: "low" },
    action: "read"
  };
  const cases = [];
  cases.push(check("owner can read own low resource", evaluateAccess(base), { allow: true, reason: "owner_read", audit: [] }));
  cases.push(check(
    "tenant mismatch denies guessed resource id",
    evaluateAccess({ ...base, resource: { ...base.resource, tenantId: "t2" } }),
    { allow: false, reason: "tenant_mismatch", audit: [] }
  ));
  cases.push(check(
    "owner cannot admin by ownership alone",
    evaluateAccess({ ...base, action: "admin" }),
    { allow: false, reason: "default_deny", audit: [] }
  ));
  cases.push(check(
    "support needs active support session",
    evaluateAccess({ ...base, actor: { id: "s1", tenantId: "t1", role: "support", supportSessionActive: true } }),
    { allow: true, reason: "support_session", audit: ["support_session"] }
  ));
  cases.push(check(
    "admin same tenant allowed",
    evaluateAccess({ ...base, actor: { id: "a1", tenantId: "t1", role: "admin" }, action: "delete" }),
    { allow: true, reason: "tenant_admin", audit: [] }
  ));
  cases.push(check(
    "expired break-glass denied",
    evaluateAccess({ ...base, actor: { id: "a1", tenantId: "t1", role: "admin", breakGlass: { reason: "incident", expiresAt: 50 } }, resource: { ...base.resource, tenantId: "t2" } }),
    { allow: false, reason: "tenant_mismatch", audit: [] }
  ));
  cases.push(check(
    "valid break-glass cross-tenant allowed with audit",
    evaluateAccess({ ...base, actor: { id: "a1", tenantId: "t1", role: "admin", breakGlass: { reason: "incident", expiresAt: 150 } }, resource: { ...base.resource, tenantId: "t2" } }),
    { allow: true, reason: "break_glass", audit: ["break_glass_access"] }
  ));
  return result("V3-ENT-JS-01", cases);
}

const sensitiveKeyPattern = /(password|token|authorization|cookie|rawbody|raw_body|body)$/i;
const emailPattern = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i;
const severities = new Set(["DEBUG", "INFO", "WARN", "ERROR"]);
const categories = new Set(["auth", "billing", "data_access", "system"]);

function redact(value) {
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === "object") {
    const output = {};
    for (const [key, inner] of Object.entries(value)) {
      if (sensitiveKeyPattern.test(key)) {
        output[key] = "[REDACTED]";
      } else {
        output[key] = redact(inner);
      }
    }
    return output;
  }
  if (typeof value === "string" && emailPattern.test(value)) return "[REDACTED_EMAIL]";
  return value;
}

function normalizeEvent(event) {
  if (!event || typeof event !== "object") {
    return { accepted: false, error: "invalid_event" };
  }
  if (JSON.stringify(event).length > 2048) {
    return { accepted: false, error: "event_too_large" };
  }
  const severity = String(event.severity || "INFO").toUpperCase();
  const category = String(event.category || "system");
  if (!severities.has(severity) || !categories.has(category)) {
    return { accepted: false, error: "invalid_event_taxonomy" };
  }
  const traceId = typeof event.trace_id === "string" && /^[a-f0-9]{32}$/.test(event.trace_id) ? event.trace_id : undefined;
  return {
    accepted: true,
    severity,
    category,
    trace_id: traceId,
    attributes: redact(event.attributes || {})
  };
}

function runAuditMapper() {
  const cases = [];
  cases.push(check(
    "sensitive top-level fields redacted",
    normalizeEvent({ severity: "info", category: "auth", attributes: { password: "secret", token: "abc" } }).attributes,
    { password: "[REDACTED]", token: "[REDACTED]" }
  ));
  cases.push(check(
    "nested email redacted",
    normalizeEvent({ severity: "warn", category: "billing", attributes: { customer: { email: "alex@example.com", plan: "pro" } } }).attributes,
    { customer: { email: "[REDACTED_EMAIL]", plan: "pro" } }
  ));
  cases.push(check(
    "valid trace id preserved",
    normalizeEvent({ severity: "error", category: "data_access", trace_id: "0123456789abcdef0123456789abcdef", attributes: { resource: "doc-1" } }).trace_id,
    "0123456789abcdef0123456789abcdef"
  ));
  cases.push(check(
    "invalid severity rejected without raw event",
    normalizeEvent({ severity: "panic", category: "system", attributes: { authorization: "Bearer secret" } }),
    { accepted: false, error: "invalid_event_taxonomy" }
  ));
  cases.push(check(
    "oversized event rejected",
    normalizeEvent({ severity: "info", category: "system", attributes: { message: "x".repeat(3000) } }),
    { accepted: false, error: "event_too_large" }
  ));
  cases.push(check(
    "arrays redact mixed private values",
    normalizeEvent({ severity: "info", category: "system", attributes: { reviewers: ["alex@example.com", "team-a"] } }).attributes,
    { reviewers: ["[REDACTED_EMAIL]", "team-a"] }
  ));
  return result("V3-ENT-JS-02", cases);
}

const tasks = {
  "V3-ENT-JS-01": runAuthPolicy,
  "V3-ENT-JS-02": runAuditMapper
};

const task = process.argv[2];
if (!task || !(task in tasks)) {
  console.error(JSON.stringify({ status: "failed", error: "unknown_task", task }));
  process.exit(2);
}

console.log(JSON.stringify(tasks[task](), null, 2));
