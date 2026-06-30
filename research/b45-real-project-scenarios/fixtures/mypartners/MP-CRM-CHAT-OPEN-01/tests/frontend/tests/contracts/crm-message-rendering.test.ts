import { expect, test } from "@playwright/test";

import { buildSafeMessageParts } from "@/features/crm/message-rendering";

test("builds safe message parts without leaking source markup", () => {
  const parts = buildSafeMessageParts(
    [
      "Hello <strong>important</strong><br>",
      '<a href="https://safe.example/path?x=1&amp;y=2">Open brief</a>',
      ' <a href="javascript:alert(1)">Bad link</a>',
      " <script>alert('owned')</script>",
      " https://plain.example/long/path?q=ok.",
    ].join(""),
  );

  const serialized = JSON.stringify(parts);
  expect(serialized).not.toMatch(/<strong|<br|<a|script|alert|javascript:/i);
  expect(parts).toEqual(
    expect.arrayContaining([
      { kind: "text", text: "important", tone: "strong" },
      { href: "https://safe.example/path?x=1&y=2", kind: "link", text: "Open brief" },
      { href: "https://plain.example/long/path?q=ok", kind: "link", text: "https://plain.example/long/path?q=ok" },
    ]),
  );
  expect(parts.some((part) => part.kind === "text" && part.text.includes("Bad link"))).toBe(true);
});

test("rejects unsafe message links and preserves readable fallback text", () => {
  const parts = buildSafeMessageParts(
    [
      '<a href="data:text/html;base64,PHNjcmlwdA==">Data link</a>',
      '<a href="/relative">Relative</a>',
      '<a href="mailto:person@example.test">Email</a>',
      '<a href="//evil.example/path">Protocol relative</a>',
    ].join(" "),
  );

  expect(parts).toEqual([{ kind: "text", text: "Data link Relative Email Protocol relative" }]);
});

test("keeps multiline and reply text readable after tag cleanup", () => {
  const parts = buildSafeMessageParts("First line<div>Second <em>line</em></div>");

  expect(parts).toEqual([
    { kind: "text", text: "First line\nSecond " },
    { kind: "text", text: "line", tone: "emphasis" },
    { kind: "text", text: "\n" },
  ]);
});

test("removes encoded and malformed active markup without creating executable output", () => {
  const parts = buildSafeMessageParts(
    [
      "&lt;script&gt;alert(1)&lt;/script&gt;",
      '<img src=x onerror="window.__crmMessageXss=true">',
      '<svg onload="window.__crmMessageXss=true"><text>bad</text></svg>',
      "<iframe>bad frame</iframe>",
      "<style>body{display:none}</style>",
      "<strong>unfinished",
      "normal text",
    ].join(" "),
  );

  const serialized = JSON.stringify(parts);
  expect(serialized).not.toMatch(/script|alert|onerror|svg|iframe|style|__crmMessageXss/i);
  expect(parts.some((part) => part.kind === "text" && part.text.includes("unfinished"))).toBe(true);
  expect(parts.some((part) => part.kind === "text" && part.text.includes("normal text"))).toBe(true);
});

test("uses a stable unavailable fallback for empty message text", () => {
  expect(buildSafeMessageParts(null)).toEqual([
    { kind: "text", text: "Message text unavailable" },
  ]);
});

test("keeps ordinary comparison text that only looks like angle punctuation", () => {
  expect(buildSafeMessageParts("2 < 3 > 1")).toEqual([{ kind: "text", text: "2 < 3 > 1" }]);
});
