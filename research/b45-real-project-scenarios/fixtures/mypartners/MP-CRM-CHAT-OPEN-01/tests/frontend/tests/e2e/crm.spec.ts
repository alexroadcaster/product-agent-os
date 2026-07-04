import { mkdirSync } from "node:fs";
import path from "node:path";

import { expect, type Locator, type Page, test } from "./e2e-runtime-guard";

const screenshotDir =
  process.env.CODEX_SCREENSHOT_DIR ??
  path.resolve(process.cwd(), "..", ".codex-tmp", "frontend-screenshots");

const SIGNAL_UI_FORBIDDEN_COPY_PATTERN =
  /\/100|0\.\d+|score_value|confidence_score|component_scores|scientific|science|psycholog|diagnos|trustworth|human worth|personality|mood|manipulat/i;

const contactsPayload = {
  items: [
    {
      account_id: "local-telegram",
      beeper_contact_id: "@alice:telegram",
      first_name: "Alice",
      id: 1,
      is_deleted: false,
      last_name: "Stone",
      merged_into_id: null,
      network: "telegram",
      relationship_state_reason: "address_book_contact",
      relationship_state_source: "sync",
      relationship_state_user_locked: false,
      relationship_tier: "confirmed",
      username: "alice",
    },
    {
      account_id: "local-linkedin",
      beeper_contact_id: "@bob:linkedin",
      first_name: "Bob",
      id: 2,
      is_deleted: false,
      last_name: "Vega",
      merged_into_id: null,
      network: "linkedin",
      relationship_state_reason: "single_chat_participant",
      relationship_state_source: "sync",
      relationship_state_user_locked: false,
      relationship_tier: "potential",
      username: "bob",
    },
  ],
  limit: 25,
  offset: 0,
  total: 2,
};

const selfContactsPayload = {
  items: [
    {
      account_id: "local-telegram",
      beeper_contact_id: "@me:telegram",
      first_name: "Local",
      id: 99,
      is_deleted: false,
      last_name: "Operator",
      merged_into_id: null,
      network: "telegram",
      relationship_state_reason: "self_account",
      relationship_state_source: "sync",
      relationship_state_user_locked: false,
      relationship_tier: "self",
      username: "local_operator",
    },
    {
      account_id: "local-linkedin",
      beeper_contact_id: "@me:linkedin",
      first_name: "LinkedIn",
      id: 100,
      is_deleted: false,
      last_name: "Self",
      merged_into_id: null,
      network: "linkedin",
      relationship_state_reason: "self_account",
      relationship_state_source: "sync",
      relationship_state_user_locked: false,
      relationship_tier: "self",
      username: "local_linkedin",
    },
  ],
  limit: 20,
  offset: 0,
  total: 2,
};

const longContactId =
  "@vsev777rom-with-a-very-long-unbroken-beeper-identifier-used-by-real-imports:beeper.com";

const longContactsFirstPage = {
  items: [
    {
      account_id: "local-telegram",
      beeper_contact_id: longContactId,
      first_name: null,
      id: 1,
      is_deleted: false,
      last_name: null,
      merged_into_id: null,
      network: "telegram",
      relationship_state_reason: "address_book_contact",
      relationship_state_source: "sync",
      relationship_state_user_locked: false,
      relationship_tier: "confirmed",
      username: "vsev777rom-with-a-very-long-unbroken-username-for-crm-layout",
    },
    {
      account_id: "local-linkedin",
      beeper_contact_id: "@compact:linkedin",
      first_name: "Compact",
      id: 2,
      is_deleted: false,
      last_name: "Contact",
      merged_into_id: null,
      network: "linkedin",
      relationship_state_reason: "address_book_contact",
      relationship_state_source: "sync",
      relationship_state_user_locked: false,
      relationship_tier: "confirmed",
      username: "compact",
    },
  ],
  limit: 25,
  offset: 0,
  total: 50,
};

const longContactsSecondPage = {
  items: [
    {
      account_id: "local-telegram",
      beeper_contact_id: "@page-two-contact:telegram",
      first_name: "Page",
      id: 26,
      is_deleted: false,
      last_name: "Two",
      merged_into_id: null,
      network: "telegram",
      relationship_state_reason: "address_book_contact",
      relationship_state_source: "sync",
      relationship_state_user_locked: false,
      relationship_tier: "confirmed",
      username: "page-two",
    },
  ],
  limit: 25,
  offset: 25,
  total: 50,
};

const tagsPayload = {
  items: [
    { color: "#ca8a04", contact_count: 1, id: 7, name: "VIP" },
    { color: "#6f7f5b", contact_count: 0, id: 8, name: "Founder" },
  ],
};

const contactDetail = {
  account_id: "local-telegram",
  avatar_url: null,
  beeper_contact_id: "@alice:telegram",
  channels: [
    {
      channel_type: "network",
      is_primary: false,
      label: "Telegram",
      network: "telegram",
      open_target: { method: "unsupported", status: "unsupported", value: null },
    },
    {
      channel_type: "profile",
      is_primary: true,
      label: "Telegram profile",
      network: "telegram",
      open_target: { method: "url", status: "available", value: "https://t.me/alice" },
    },
    {
      channel_type: "profile",
      is_primary: false,
      label: "Linkedin profile",
      network: "linkedin",
      open_target: { method: "url", status: "available", value: "https://linkedin.com/in/alice" },
    },
  ],
  first_name: "Alice",
  id: 1,
  is_merged: false,
  is_self: false,
  last_name: "Stone",
  merged_into_id: null,
  merged_sources: [{ beeper_contact_id: "@alice:linkedin", id: 5, network: "linkedin" }],
  network: "telegram",
  networks: ["telegram", "linkedin"],
  note: { note_text: "Met at SaaStr", updated_at: 1_746_300_000 },
  phone_number: null,
  primary_location: {
    archived: false,
    city: null,
    confidence_score: null,
    country: "Georgia",
    is_manual: true,
    is_primary: true,
    location_id: "manual:1",
    location_label: "Tbilisi",
    open_target: {
      method: "maps_search",
      status: "available",
      value: "https://www.google.com/maps/search/?api=1&query=Tbilisi",
    },
    region: null,
    source: "manual",
    timezone: null,
    user_verified: true,
  },
  relationship_state_reason: "address_book_contact",
  relationship_state_source: "sync",
  relationship_state_user_locked: false,
  relationship_tier: "confirmed",
  tags: [{ color: "#ca8a04", id: 7, name: "VIP" }],
  username: "alice",
  locations: [
    {
      archived: false,
      city: null,
      confidence_score: null,
      country: "Georgia",
      is_manual: true,
      is_primary: true,
      location_id: "manual:1",
      location_label: "Tbilisi",
      open_target: {
        method: "maps_search",
        status: "available",
        value: "https://www.google.com/maps/search/?api=1&query=Tbilisi",
      },
      region: null,
      source: "manual",
      timezone: null,
      user_verified: true,
    },
  ],
};

const graphPayload = {
  communities: [[1, 2]],
  edges: [
    {
      cross_platform: true,
      shared_groups_count: 3,
      shared_topics: ["pricing", "pilot"],
      source: 1,
      target: 2,
      weight: 4.4,
    },
  ],
  nodes: [
    {
      id: 1,
      is_merged: true,
      is_self: false,
      label: "Alice Stone",
      merged_count: 1,
      network: "telegram",
      networks: ["telegram", "linkedin"],
    },
    {
      id: 2,
      is_merged: false,
      is_self: false,
      label: "Bob Vega",
      merged_count: 0,
      network: "linkedin",
      networks: ["linkedin"],
    },
  ],
};

const userContextGoalsPayload = {
  contract_version: "user-context-v1",
  items: [
    {
      archived_at: null,
      completed_at: null,
      contract_version: "user-context-v1",
      created_at: 1_770_086_400,
      created_by: "user",
      description: "private-crm-goal-description-canary",
      goal_id: "goal-crm-e2e",
      horizon: "now",
      id: 17,
      linked_memory_fact_id: null,
      priority: "high",
      profile_row_id: null,
      source_exclusion_active_count: 0,
      source_exclusion_latest_updated_at: null,
      source_exclusion_policy_version: "source-exclusion-v1",
      source_type: "user",
      status: "active",
      title: "Private CRM goal title canary",
      updated_at: 1_770_086_400,
    },
  ],
};

const userContextProfilePayload = {
  accepted_self_memory_count: 2,
  contract_version: "user-context-v1",
  profile: {
    archived_at: null,
    communication_preference: "Concise context before meetings",
    contract_version: "user-context-v1",
    created_at: 1_770_086_400,
    created_by: "user",
    current_focus: "Founder pipeline",
    display_label: "Local Operator",
    headline: "Relationship intelligence workspace",
    id: 9,
    location_label: "Berlin",
    professional_profile_id: "founder_ceo",
    profile_id: "profile-crm-e2e",
    profile_version: 2,
    schema_version: "0026_user_context",
    status: "active",
    timezone: "Europe/Berlin",
    updated_at: 1_770_086_400,
    work_context: "Early-stage GTM",
  },
};

const userContextItemsPayload = {
  contract_version: "user-context-v1",
  items: [
    {
      archived_at: null,
      contract_version: "user-context-v1",
      created_at: 1_770_086_400,
      created_by: "user",
      detail: "Needs founder introductions in climate SaaS",
      goal_row_id: null,
      id: 31,
      item_id: "item-crm-e2e",
      item_type: "need",
      label: "Warm intros",
      linked_memory_fact_id: null,
      priority: "normal",
      source_exclusion_active_count: 0,
      source_exclusion_latest_updated_at: null,
      source_exclusion_policy_version: "source-exclusion-v1",
      source_type: "user",
      status: "active",
      updated_at: 1_770_086_400,
    },
  ],
};

const userContextStatusPayload = {
  accepted_self_memory_count: 2,
  active_goal_count: 1,
  active_item_count: 1,
  advisor_prompt_context: {},
  candidate_self_memory_count: 0,
  contract_version: "self-context-advisor-status-v1",
  degraded: false,
  profile_status: "active",
  profile_version: 2,
  ready: true,
  reason: "ready",
  status: "ready",
};

const tagGroupsPayload = {
  contract_version: "crm-tags-v1",
  items: [
    {
      archived_at: null,
      auto_apply_policy: "review",
      auto_suggest_enabled: true,
      color: "#C7A15A",
      description: "Role tags",
      id: 2,
      name: "Role",
      risk_level: "low",
      slug: "role",
      sort_order: 10,
    },
  ],
};

const taggingSettingsPayload = {
  allowed_group_slugs: ["role"],
  allow_contact_auto_tagging: "review_batches",
  confidence_threshold: 0.85,
  contract_version: "crm-tags-v1",
  max_batch_size: 50,
};

const taggingEvalPayload = {
  auto_apply_mode: "review_batches",
  claim_language_gate: { status: "passed" },
  confidence_band_counts: { high: 1 },
  confidence_threshold: 0.85,
  contains_raw_private_text: false,
  contract_version: "crm-tags-v1",
  max_active_tags_per_contact: 7,
  privacy_surface: "metadata_only",
  reason_code_counts: { role_match: 1 },
  status_counts: { suggested: 1 },
};

const reviewQueuePayload = {
  contract_version: "review-queue-v1",
  counts: {
    by_kind: { self_memory: 0, tag_suggestion: 1, typed_memory: 0 },
    by_status: { suggested: 1 },
    invalidated: 0,
    stale: 0,
    total: 1,
    total_available: 1,
  },
  items: [
    {
      allowed_actions: ["accept", "reject", "undo"],
      blocked_reason: null,
      confidence_band: "high",
      confidence_score: 0.87,
      contract_version: "review-queue-v1",
      evidence_count: 2,
      invalidated: false,
      item_id: "tag-suggestion-41",
      item_kind: "tag_suggestion",
      memory_id: null,
      reason_code: "role_match",
      source_exclusion_active_count: 0,
      source_exclusion_latest_updated_at: null,
      source_exclusion_policy_version: "source-exclusion-v1",
      stale: false,
      status: "suggested",
      subject_label: "Alice Stone",
      suggestion_id: 41,
      summary: "Review VIP tag suggestion",
      target_label: "VIP",
      updated_at: 1_770_086_400,
    },
  ],
};

const contactUsefulnessPayload = {
  contact_id: 1,
  contract_version: "relationship-signals-v1",
  goal_context: {
    degraded_reasons: [],
    goal_horizon: "now",
    goal_id: "goal-crm-e2e",
    goal_priority: "high",
    goal_scope_key: "selected_goal:goal-crm-e2e",
    goal_status: "active",
    lens_id: "selected_goal",
    profile_version: 2,
    source_exclusion_active_count: 0,
    source_exclusion_latest_updated_at: null,
    source_exclusion_policy_version: "source-exclusion-v1",
    status: "ready",
  },
  items: [
    {
      component_scores: { goal_fit: 0.9, warm_access: 0.75 },
      confidence_score: 0.86,
      contact_id: 1,
      degraded_reasons: [],
      display_band: "high",
      goal_id: "goal-crm-e2e",
      goal_scope_key: "selected_goal:goal-crm-e2e",
      last_computed_at: 1_770_086_400,
      lens_id: "selected_goal",
      profile_version: 2,
      reason_codes: ["goal_fit", "warm_access", "existing_crm_context"],
      score_value: 0.93,
      signal_kind: "contact_value",
      signal_version: "contact_value_v1",
      stale: false,
      status: "current",
      subject_type: "contact",
    },
  ],
  limit: 1,
  mutation_performed: false,
  privacy: {
    action_authority: false,
    metadata_only: true,
    production_appdata_write: false,
    raw_messages_included: false,
    worker_called: false,
  },
  production_appdata_mutation_allowed: false,
  signal_version: "contact_value_v1",
  status: "ready",
};

const contactFacetsPayload = {
  channels: [
    { count: 1, value: "telegram" },
    { count: 1, value: "linkedin" },
  ],
  contract_version: "people-facets-v1",
  locations: { known: 1, manual: 1, unknown: 1, user_verified: 1 },
  networks: [
    { count: 1, value: "telegram" },
    { count: 1, value: "linkedin" },
  ],
  relationship_state_sources: [{ count: 2, value: "sync" }],
  source_types: [{ count: 2, value: "contact" }],
  tiers: [
    { count: 1, value: "confirmed" },
    { count: 1, value: "potential" },
  ],
  total: 2,
};

const contactRelationshipSummaryPayload = {
  activity: { chat_count: 1, last_activity_ts: 1_746_300_000, message_count: 80 },
  contact_id: 1,
  contract_version: "person-relationship-summary-v1",
  counts: {
    accepted_memory_facts: 2,
    active_contact_sources: 3,
    chat_memberships: 1,
    memory_evidence_refs: 4,
    visible_messages_from_contact: 80,
  },
  graph_summary: {
    direct_ties: 5,
    full_graph_loaded: false,
    shared_groups_count: 2,
    strongest_tie_label: "Bob Vega",
  },
  memory: {
    accepted_count: 2,
    evidence_ref_count: 4,
    items: [
      {
        accepted_at: 1_746_300_000,
        confidence_band: "high",
        confidence_score: 0.9,
        evidence_ref_count: 1,
        evidence_refs: [
          {
            evidence_type: "supporting_ref",
            rank: 1,
            redaction_state: "metadata_only",
            ref_id: 77,
            source_type: "message",
          },
        ],
        fact_type: "relationship_context",
        memory_id: "mem-alice",
        review_source: "user_created",
        source_category: "message_window",
      },
    ],
  },
  source_state: { source: "sync", stale: false, status: "available" },
  tags: [{ color: "#ca8a04", id: 7, name: "VIP" }],
};

const contactChatsPayload = {
  items: [
    {
      beeper_chat_id: "!chat:telegram",
      id: 11,
      last_activity_ts: 1_746_300_000,
      network: "telegram",
      open_target: {
        method: "beeper_chat",
        status: "available",
        value: "!chat:telegram",
      },
      participants_count: 2,
      title: "Direct: Alice",
      type: "single",
    },
  ],
};

test("crm renders loading and empty contacts states", async ({ page }) => {
  let releaseContacts: () => void = () => {};
  const contactsCanFulfill = new Promise<void>((resolve) => {
    releaseContacts = resolve;
  });

  await page.route("http://127.0.0.1:8000/api/tags", async (route) => {
    await route.fulfill({ contentType: "application/json", json: { items: [] }, status: 200 });
  });
  await page.route("http://127.0.0.1:8000/api/contacts**", async (route) => {
    await contactsCanFulfill;
    await route.fulfill({
      contentType: "application/json",
      json: { items: [], limit: 25, offset: 0, total: 0 },
      status: 200,
    });
  });

  await page.goto("/crm");
  await expect(page.getByText("Loading contacts")).toBeVisible();

  releaseContacts();

  await expect(page.getByText("No contacts match current filters")).toBeVisible();
});

test("crm renders error state when local FastAPI contacts fail", async ({ page }) => {
  await page.route("http://127.0.0.1:8000/api/tags", async (route) => {
    await route.fulfill({ contentType: "application/json", json: { items: [] }, status: 200 });
  });
  await page.route("http://127.0.0.1:8000/api/contacts**", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      json: { detail: "database unavailable" },
      status: 503,
    });
  });

  await page.goto("/crm");

  await expect(page.getByText("Unable to load contacts")).toBeVisible();
});

test("crm table-first initial load uses list-only contact data", async ({ page }) => {
  const calls: Array<{ body: unknown; method: string; path: string }> = [];

  await mockCrmApis(page, calls, { graphMode: "hang", recordGet: true });
  await page.goto("/crm");

  await expect(page.getByRole("table", { name: "People contacts table" })).toBeVisible();
  await expect(page.getByTestId("crm-people-row-1")).toBeVisible();
  await expect(page.getByTestId("crm-people-segments")).toBeVisible();
  const segmentWidth = await page
    .getByTestId("crm-people-segments")
    .evaluate((node) => (node as HTMLElement).getBoundingClientRect().width);
  const viewportWidth = page.viewportSize()?.width ?? 1280;
  expect(segmentWidth).toBeLessThan(viewportWidth * 0.6);
  const segmentBox = await page.getByTestId("crm-people-segments").boundingBox();
  const searchBox = await page.getByTestId("crm-people-filter-search").boundingBox();
  const networkBox = await page.getByTestId("crm-people-filter-network").boundingBox();
  const tagBox = await page.getByTestId("crm-people-filter-tag").boundingBox();
  const weightBox = await page.getByTestId("crm-people-filter-weight").boundingBox();
  expect(segmentBox).not.toBeNull();
  expect(searchBox).not.toBeNull();
  expect(networkBox).not.toBeNull();
  expect(tagBox).not.toBeNull();
  expect(weightBox).not.toBeNull();
  expect(Math.abs(segmentBox!.y - searchBox!.y)).toBeLessThanOrEqual(6);
  expect(Math.abs(segmentBox!.y - networkBox!.y)).toBeLessThanOrEqual(6);
  expect(Math.abs(segmentBox!.y - tagBox!.y)).toBeLessThanOrEqual(6);
  expect(Math.abs(segmentBox!.y - weightBox!.y)).toBeLessThanOrEqual(6);
  expect(networkBox!.x + networkBox!.width).toBeLessThanOrEqual(tagBox!.x);
  await expect(page.getByText("Include merged")).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Open Alice Stone" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Contact Workspace" })).toHaveCount(0);
  await expect(page.getByText("Projection needed").first()).toBeVisible();
  await expect(page.getByText("Synthetic opened message canary")).toBeHidden();

  const initialGetPaths = calls
    .filter((call) => call.method === "GET")
    .map((call) => call.path);
  expect(initialGetPaths).toContain("/api/contacts");
  expect(initialGetPaths).toContain("/api/tags");
  expect(initialGetPaths).not.toContain("/api/graph");
  expect(initialGetPaths.some((item) => /^\/api\/contacts\/\d+/.test(item))).toBe(false);
  expect(initialGetPaths.some((item) => item.includes("/messages"))).toBe(false);
  expect(initialGetPaths.some((item) => item.includes("/relationship-summary"))).toBe(false);
  expect(initialGetPaths.some((item) => item.includes("/merge-candidates"))).toBe(false);
});

test("crm people search debounces list queries without tier-total fanout", async ({ page }) => {
  const calls: Array<{ body: unknown; method: string; path: string; query?: string }> = [];

  await mockCrmApis(page, calls, { graphMode: "hang", recordGet: true, recordQuery: true });
  await page.goto("/crm");

  await expect(page.getByRole("table", { name: "People contacts table" })).toBeVisible();
  await expect
    .poll(() => calls.filter((call) => call.path === "/api/contacts").length)
    .toBeGreaterThanOrEqual(6);

  calls.length = 0;
  const search = page.getByPlaceholder("Name or username");
  await search.fill("A");
  await search.fill("Al");
  await search.fill("Ali");
  await search.fill("Alic");
  await search.fill("Alice");

  await expect
    .poll(() =>
      calls.filter(
        (call) => call.path === "/api/contacts" && call.query?.includes("q=Alice"),
      ).length,
    )
    .toBe(1);

  const contactSearchCalls = calls.filter((call) => call.path === "/api/contacts");
  expect(contactSearchCalls).toHaveLength(1);
  expect(contactSearchCalls[0].query).toContain("relationship_tier=confirmed");
});

test("crm local profile tags and review workspaces load only after explicit selection", async ({
  page,
}) => {
  const calls: Array<{ body: unknown; method: string; path: string; query?: string }> = [];

  await page.setViewportSize({ height: 900, width: 1440 });
  await mockCrmApis(page, calls, { graphMode: "hang", recordGet: true, recordQuery: true });
  await page.goto("/crm");

  await expect(page.getByRole("heading", { name: "People", exact: true })).toBeVisible();
  await expect(page.getByRole("table", { name: "People contacts table" })).toBeVisible();
  await expect(page.getByTestId("crm-local-workspace-actions")).not.toContainText("current");
  expect(calls.map((call) => call.path)).not.toContain("/api/user-context/profile");
  expect(calls.map((call) => call.path)).not.toContain("/api/review-queue/items");
  expect(calls.filter((call) => call.method !== "GET")).toEqual([]);

  await page.getByRole("button", { name: /My Profile/ }).click();
  await expect(page.getByTestId("crm-local-profile-workspace")).toBeVisible();
  await expect(page.getByText("Self Context stays separate")).toHaveCount(0);
  await expect(page.getByLabel("Your name")).toHaveValue("Local Operator");
  await expect(page.getByLabel("Location")).toHaveValue("Berlin");
  await expect(page.getByLabel("Timezone")).toHaveValue("Europe/Berlin");
  await expect(page.getByTestId("crm-profile-network-icon-telegram")).toBeVisible();
  await expect(page.getByTestId("crm-profile-network-icon-linkedin")).toBeVisible();
  await expect(page.getByTestId("crm-profile-location-link")).toHaveAttribute(
    "href",
    /google\.com\/maps\/search/,
  );
  await expect(page.getByText("Private CRM goal title canary")).toBeVisible();
  await expect(page.getByRole("heading", { name: "My groups and chats" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Chats I wrote in" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Read-only groups" })).toBeVisible();
  await expect(
    page.getByTestId("crm-profile-written-chats").getByRole("heading", {
      name: "Local Operator / telegram",
    }),
  ).toBeVisible();
  const savedMessagesLink = page
    .getByTestId("crm-profile-written-chats")
    .getByRole("link", { name: "Saved Messages" });
  await expect(savedMessagesLink).toHaveAttribute("href", /matrix\.to/);
  await expect(
    page.getByTestId("crm-profile-readonly-chats").getByRole("link", {
      name: "Read-only Research Group",
    }),
  ).toHaveAttribute("href", /matrix\.to/);
  expect(calls.map((call) => call.path)).not.toContain("/api/contacts/99/messages");
  await page.getByRole("button", { name: "Show messages" }).click();
  await expect(page.getByText("Self opened message canary")).toBeVisible();
  await expect(page.getByText("Inbound self-profile leak canary")).toHaveCount(0);
  await expect(page.getByTestId("crm-message-reply-context")).toHaveCount(0);
  await page.getByRole("button", { name: "Delete goal Private CRM goal title canary" }).click();
  await expect
    .poll(() =>
      calls.some(
        (call) =>
          call.path === "/api/user-context/goals/goal-crm-e2e/archive" &&
          call.method === "POST",
      ),
    )
    .toBe(true);
  await page.getByRole("button", { name: "Delete context item Warm intros" }).click();
  await expect
    .poll(() =>
      calls.some(
        (call) =>
          call.path === "/api/user-context/items/item-crm-e2e/archive" &&
          call.method === "POST",
      ),
    )
    .toBe(true);
  await page.getByLabel("Your name").fill("Local Operator Updated");
  await page.getByLabel("Location").fill("Tbilisi");
  await page.getByLabel("Timezone").selectOption("Asia/Tbilisi");
  await page.getByRole("button", { name: "Save My Profile" }).click();
  await expect
    .poll(() =>
      calls.some((call) => call.path === "/api/user-context/profile" && call.method === "PATCH"),
    )
    .toBe(true);
  const profilePatch = calls.find(
    (call) => call.path === "/api/user-context/profile" && call.method === "PATCH",
  );
  expect(profilePatch?.body).toMatchObject({
    display_label: "Local Operator Updated",
    location_label: "Tbilisi",
    timezone: "Asia/Tbilisi",
  });

  await page.getByRole("button", { name: /People Tags/ }).click();
  await expect(page.getByTestId("crm-local-tags-workspace")).toBeVisible();
  await expect(page.getByText("CRM taxonomy")).toBeVisible();
  await expect(page.getByTestId("crm-tags-telemetry")).toBeVisible();
  await expect(page.getByTestId("crm-tags-column")).toBeVisible();
  await expect(page.getByTestId("crm-tag-groups-column")).toBeVisible();
  await expect(page.getByTestId("crm-tags-create-form")).toBeVisible();
  await expect(page.getByTestId("crm-tag-groups-form")).toBeVisible();
  await expect(page.getByTestId("crm-tags-list")).toBeVisible();
  await expect(page.getByTestId("crm-tag-groups-list")).toBeVisible();
  const tagsWorkspace = page.getByTestId("crm-local-tags-workspace");
  const telemetryBox = await page.getByTestId("crm-tags-telemetry").boundingBox();
  const tagsColumnBox = await page.getByTestId("crm-tags-column").boundingBox();
  const groupsColumnBox = await page.getByTestId("crm-tag-groups-column").boundingBox();
  const createFormBox = await page.getByTestId("crm-tags-create-form").boundingBox();
  const groupFormBox = await page.getByTestId("crm-tag-groups-form").boundingBox();
  const tagsListBox = await page.getByTestId("crm-tags-list").boundingBox();
  const tagGroupsBox = await page.getByTestId("crm-tag-groups-list").boundingBox();
  expect(telemetryBox).not.toBeNull();
  expect(tagsColumnBox).not.toBeNull();
  expect(groupsColumnBox).not.toBeNull();
  expect(createFormBox).not.toBeNull();
  expect(groupFormBox).not.toBeNull();
  expect(tagsListBox).not.toBeNull();
  expect(tagGroupsBox).not.toBeNull();
  expect(telemetryBox!.height).toBeLessThanOrEqual(58);
  expect(Math.abs(tagsColumnBox!.y - groupsColumnBox!.y)).toBeLessThanOrEqual(6);
  expect(tagsColumnBox!.x + tagsColumnBox!.width).toBeLessThanOrEqual(groupsColumnBox!.x + 1);
  await expectElementInside(page.getByTestId("crm-tags-telemetry"), tagsWorkspace);
  await expectElementInside(page.getByTestId("crm-tags-column"), tagsWorkspace);
  await expectElementInside(page.getByTestId("crm-tag-groups-column"), tagsWorkspace);
  await expectElementInside(page.getByTestId("crm-tags-create-form"), page.getByTestId("crm-tags-column"));
  await expectElementInside(page.getByTestId("crm-tags-list"), page.getByTestId("crm-tags-column"));
  await expectElementInside(page.getByTestId("crm-tag-groups-form"), page.getByTestId("crm-tag-groups-column"));
  await expectElementInside(page.getByTestId("crm-tag-groups-list"), page.getByTestId("crm-tag-groups-column"));
  await expectNoHorizontalOverflow(page);
  await expectNoVerticalPageOverflow(page);
  await page.getByLabel("Tag name").fill("Партнер");
  await page
    .getByTestId("crm-tags-create-form")
    .getByRole("button", { name: "Use color #6F7F5B" })
    .click();
  await page.getByRole("button", { name: "Create tag" }).click();
  await expect
    .poll(() => calls.some((call) => call.path === "/api/tags" && call.method === "POST"))
    .toBe(true);
  const tagPost = calls.find((call) => call.path === "/api/tags" && call.method === "POST");
  expect(tagPost?.body).toMatchObject({
    color: "#6F7F5B",
    name: "Партнер",
  });
  const groupForm = page.getByTestId("crm-tag-groups-form");
  await groupForm.getByLabel("Group name").fill("Партнеры");
  await groupForm.getByRole("button", { name: "Use color #A65F46" }).click();
  await groupForm.getByLabel("Risk").selectOption("medium");
  await groupForm.getByLabel("Policy").selectOption("review");
  await groupForm.getByRole("button", { name: "Create group" }).click();
  await expect
    .poll(() => calls.some((call) => call.path === "/api/tags/groups" && call.method === "POST"))
    .toBe(true);
  const groupPost = calls.find(
    (call) => call.path === "/api/tags/groups" && call.method === "POST",
  );
  expect(groupPost?.body).toMatchObject({
    auto_apply_policy: "review",
    color: "#A65F46",
    name: "Партнеры",
    risk_level: "medium",
  });
  await groupForm.getByLabel("Group action").selectOption("2");
  await groupForm.getByLabel("Group name").fill("Роли");
  await groupForm.getByRole("button", { name: "Save group" }).click();
  await expect
    .poll(() =>
      calls.some((call) => call.path === "/api/tags/groups/2" && call.method === "PATCH"),
    )
    .toBe(true);
  const groupPatch = calls.find(
    (call) => call.path === "/api/tags/groups/2" && call.method === "PATCH",
  );
  expect(groupPatch?.body).toMatchObject({ name: "Роли" });

  await page.getByRole("button", { name: /Review Queue/ }).click();
  await expect(page.getByTestId("crm-local-review-workspace")).toBeVisible();
  await expect(page.getByText("Review VIP tag suggestion")).toBeVisible();
  await page.getByRole("button", { name: "Accept" }).click();
  await expect
    .poll(() =>
      calls.some(
        (call) => call.path === "/api/tags/suggestions/41/accept" && call.method === "POST",
      ),
    )
    .toBe(true);

  const paths = calls.map((call) => call.path);
  expect(paths).toContain("/api/user-context/profile");
  expect(paths).toContain("/api/user-context/goals");
  expect(paths).toContain("/api/user-context/items");
  expect(paths).toContain("/api/user-context/status");
  expect(paths).toContain("/api/contacts");
  expect(paths).toContain("/api/contacts/99/chats");
  expect(paths).toContain("/api/contacts/100/chats");
  expect(paths).toContain("/api/contacts/99/messages");
  const selfMessageCall = calls.find((call) => call.path === "/api/contacts/99/messages");
  expect(selfMessageCall?.query).toContain("sender=me");
  expect(paths).toContain("/api/tags/groups");
  expect(paths).toContain("/api/tags/settings");
  expect(paths).toContain("/api/tags/eval");
  expect(paths).toContain("/api/review-queue/items");
  await expect(page.getByRole("link", { name: "My Profile" })).toHaveCount(0);
  await expect(page.getByRole("link", { name: "People Tags" })).toHaveCount(0);
  await expect(page.getByRole("link", { name: "Review Queue" })).toHaveCount(0);
});

test("crm workspace calls notes, tags, merge, unmerge endpoints and hides raw messages first", async ({ page }) => {
  const calls: Array<{ body: unknown; method: string; path: string }> = [];
  const forbiddenSignalRequests = trackForbiddenCrmSignalRequests(page);
  const browserErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") {
      browserErrors.push(message.text());
    }
  });
  page.on("pageerror", (error) => {
    browserErrors.push(error.message);
  });

  await mockCrmApis(page, calls, { recordGet: true });
  await page.goto("/crm");

  await expect(page.getByRole("heading", { name: "People", exact: true })).toBeVisible();
  const peopleTable = page.getByRole("table", { name: "People contacts table" });
  await expect(peopleTable).toBeVisible();
  await expect(peopleTable.locator("th").first()).toHaveAttribute("aria-sort", "ascending");
  await peopleTable.getByRole("button", { name: "Sort by Person" }).click();
  await expect(peopleTable.locator("th").first()).toHaveAttribute("aria-sort", "descending");
  await page.getByText("Columns").click();
  await page.getByRole("checkbox", { name: "Review" }).uncheck();
  await page.getByText("Columns").click();
  await expect(peopleTable.getByRole("button", { name: "Sort by Review" })).toBeHidden();
  await page.getByRole("button", { name: "comfortable" }).click();
  await expect(page.getByRole("button", { name: "comfortable" })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await expect(page.getByRole("button", { name: /Confirmed/ })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await expect(page.getByTestId("crm-people-row-1")).toBeVisible();
  await page.getByTestId("crm-people-row-1").dblclick();

  await expect(page).toHaveURL(/\/crm\/1$/);
  await expect(page.getByRole("heading", { name: "Contact dossier" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible();
  await expect(page.getByText("Channels And Location")).toHaveCount(0);
  const headerActions = page.getByTestId("crm-contact-header-actions");
  await expect(headerActions).toBeVisible();
  await expect(headerActions.getByRole("button", { name: "Open Telegram" })).toHaveAttribute(
    "data-icon-source",
    "icons0.dev",
  );
  await expect(headerActions.getByTestId("crm-contact-location-icon")).toHaveAttribute(
    "data-icon-source",
    "icons0.dev",
  );
  await expect(page.getByTestId("crm-contact-add-channel-network")).toHaveCount(0);
  await expect(page.getByTestId("crm-contact-location-input")).toHaveCount(0);
  await expect(headerActions.getByTestId("crm-contact-add-menu-button")).toBeVisible();
  const profileSummary = page.getByTestId("crm-contact-profile-summary");
  await expect(profileSummary).toBeVisible();
  await expect(profileSummary).toContainText("Direct ties");
  await expect(profileSummary).toContainText("Shared groups");
  await expect(profileSummary).toContainText("Strongest tie");
  const directTiesBox = await page.getByTestId("crm-contact-summary-direct-ties").boundingBox();
  const sharedGroupsBox = await page.getByTestId("crm-contact-summary-shared-groups").boundingBox();
  const strongestTieBox = await page.getByTestId("crm-contact-summary-strongest-tie").boundingBox();
  const whyBox = await page.getByTestId("crm-contact-why-summary").boundingBox();
  expect(directTiesBox).not.toBeNull();
  expect(sharedGroupsBox).not.toBeNull();
  expect(strongestTieBox).not.toBeNull();
  expect(whyBox).not.toBeNull();
  expect(Math.abs(directTiesBox!.y - sharedGroupsBox!.y)).toBeLessThanOrEqual(6);
  expect(Math.abs(directTiesBox!.y - strongestTieBox!.y)).toBeLessThanOrEqual(6);
  expect(Math.abs(directTiesBox!.y - whyBox!.y)).toBeLessThanOrEqual(6);
  await expect(page.getByTestId("crm-person-signal-band")).toHaveText("High goal fit");
  await expect(page.getByTestId("crm-person-signal-status")).toHaveText("Current local signal");
  await expect(page.getByTestId("crm-person-why-this-matters")).toContainText("Goal match");
  await expect(page.getByTestId("crm-person-why-this-matters")).toContainText("Warm path");
  await expect(page.getByTestId("crm-person-why-this-matters")).not.toContainText(
    "Private CRM goal title canary",
  );
  await expect(page.getByTestId("crm-person-why-this-matters")).not.toContainText(
    "private-crm-goal-description-canary",
  );
  await expect(page.getByTestId("crm-person-why-this-matters")).not.toContainText("0.93");
  await expect(page.getByTestId("crm-person-why-this-matters")).not.toContainText("0.86");
  await expect(page.getByTestId("crm-person-why-this-matters")).not.toContainText("/100");
  await expect(page.getByTestId("crm-person-signal-chip").first()).toBeVisible();
  const whyThisMatters = page.getByTestId("crm-person-why-this-matters");
  await expectElementInside(whyThisMatters, profileSummary);
  await expectElementInside(page.getByTestId("crm-person-signal-band"), profileSummary);
  await expectElementInside(page.getByTestId("crm-person-signal-status"), profileSummary);
  await expectElementInside(page.getByTestId("crm-person-signal-chip").first(), whyThisMatters);
  await expectTextNotClipped(page.getByTestId("crm-person-signal-band"));
  await expectTextNotClipped(page.getByTestId("crm-person-signal-status"));
  await expectTextNotClipped(page.getByTestId("crm-person-signal-chip").first());
  const signalPanelText =
    (await page.getByTestId("crm-person-why-this-matters").textContent()) ?? "";
  expect(signalPanelText).not.toMatch(SIGNAL_UI_FORBIDDEN_COPY_PATTERN);
  const signalRenderGetPaths = calls
    .filter((call) => call.method === "GET")
    .map((call) => call.path);
  expect(signalRenderGetPaths).toContain("/api/relationship-signals/contacts/1/usefulness");
  expect(signalRenderGetPaths).not.toContain("/api/relationship-signals/usefulness");
  expect(signalRenderGetPaths).not.toContain("/api/relationship-signals/recompute");
  expect(calls.filter((call) => call.method !== "GET")).toEqual([]);
  expect(forbiddenSignalRequests).toEqual([]);
  await expect(page.getByRole("heading", { name: "People card" })).toBeVisible();
  await expect(page.getByText("address book contact").first()).toBeVisible();
  await expect(page.getByText("5 direct ties")).toBeVisible();
  await expect(page.getByText("2 memory facts")).toBeVisible();
  await expect(page.getByText("4 allowed refs")).toBeVisible();
  await expect(page.getByText("Message bodies load only after an explicit chat open")).toBeVisible();
  await expect(page.getByText("Raw private sentence from Beeper")).toBeHidden();
  await expect(page.getByRole("heading", { name: "People Triage" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Why this matters" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Scoped Graph Summary" })).toHaveCount(0);
  await expectNoVerticalPageOverflow(page);
  await page.getByRole("button", { name: "Source #77" }).click();
  await expect(page.getByRole("dialog", { name: "Evidence source context" })).toContainText(
    "Synthetic People source context.",
  );
  await page.getByRole("button", { name: "Close evidence drawer" }).click();
  await page.getByRole("button", { name: "Show messages" }).click();
  await expect(page.getByText("Synthetic opened message canary")).toBeVisible();
  await expect(page.getByTestId("crm-message-reply-context")).toContainText("Replying to You");
  await expect(page.getByTestId("crm-message-reply-context")).toContainText(
    "Earlier outbound context",
  );
  await expect(page.getByTestId("crm-message-reply-context")).not.toContainText(/<strong|<br/i);
  const messageBody = page.getByTestId("crm-message-body").first();
  await expect(messageBody).toContainText("Synthetic opened message canary");
  await expect(messageBody).toContainText("important context");
  await expect(messageBody).toContainText("bad link");
  await expect(messageBody).not.toContainText(/<strong|<br|<a href|script|alert|onerror|iframe|style/i);
  const safeBriefingLink = page.getByRole("link", { name: "safe briefing" });
  await expect(safeBriefingLink).toHaveAttribute("href", "https://safe.example/brief?x=1&y=2");
  await expect(safeBriefingLink).toHaveAttribute("target", "_blank");
  await expect(safeBriefingLink).toHaveAttribute("rel", /noopener/);
  await expect(safeBriefingLink).toHaveAttribute("rel", /noreferrer/);
  await expect(page.getByRole("link", { name: "bad link" })).toHaveCount(0);
  await expect(page.getByRole("link", { name: /plain\.example/ })).toHaveAttribute(
    "href",
    "https://plain.example/very/long/path?ref=safe",
  );
  expect(await page.evaluate(() => (window as Window & { __crmMessageXss?: boolean }).__crmMessageXss)).toBeFalsy();
  const triageActions = page.getByTestId("crm-contact-triage-actions");
  await expect(triageActions.getByRole("button", { name: /^Hide$/ })).toBeVisible();
  await expect(triageActions.getByRole("button", { name: /Move to potential/ })).toBeVisible();
  await triageActions.getByRole("button", { name: /^Hide$/ }).click();
  await expect(page.getByText("People segment set to Ignored")).toBeVisible();

  await page.getByLabel("Contact note").fill("Updated relationship note");
  await page.getByRole("button", { name: "Save note" }).click();
  await page.getByTestId("crm-contact-add-menu-button").click();
  const addMenuPanelBox = await page.getByTestId("crm-contact-add-menu-panel").boundingBox();
  const viewport = page.viewportSize();
  expect(addMenuPanelBox).not.toBeNull();
  expect(addMenuPanelBox!.x).toBeGreaterThanOrEqual(0);
  expect(addMenuPanelBox!.x + addMenuPanelBox!.width).toBeLessThanOrEqual(
    (viewport?.width ?? 1280) + 1,
  );
  await expect(page.getByTestId("crm-contact-add-menu-whatsapp").locator("img")).toHaveAttribute(
    "data-icon-source",
    "icons0.dev",
  );
  await page.getByTestId("crm-contact-add-menu-whatsapp").click();
  await page.getByTestId("crm-contact-add-channel-url").fill("https://wa.me/15551234567");
  await page.getByTestId("crm-contact-add-channel-submit").click();
  await page.getByTestId("crm-contact-add-menu-location").click();
  await page.getByTestId("crm-contact-location-input").fill("Lisbon");
  await page.getByTestId("crm-contact-location-save").click();
  await page.getByRole("button", { name: "Attach Founder" }).click();
  await page.getByRole("button", { name: "Remove VIP" }).click();
  await page.getByRole("button", { name: "Merge Bob Vega into Alice Stone" }).click();
  await page.getByRole("button", { name: "Unmerge linkedin source 5" }).click();

  expect(calls).toEqual(
    expect.arrayContaining([
      {
        body: { reason_code: "user_hidden", relationship_tier: "ignored", user_locked: true },
        method: "PATCH",
        path: "/api/contacts/1/relationship-state",
      },
      {
        body: { first_name: "Alice", last_name: "Stone", note_text: "Updated relationship note" },
        method: "PATCH",
        path: "/api/contacts/1",
      },
      {
        body: { network: "whatsapp", profile_url: "https://wa.me/15551234567" },
        method: "POST",
        path: "/api/contacts/1/channels",
      },
      {
        body: { location_label: "Lisbon" },
        method: "PATCH",
        path: "/api/contacts/1/location",
      },
      { body: { tag_id: 8 }, method: "POST", path: "/api/contacts/1/tags" },
      { body: null, method: "DELETE", path: "/api/contacts/1/tags/7" },
      { body: { into_contact_id: 1 }, method: "POST", path: "/api/contacts/2/merge" },
      { body: null, method: "POST", path: "/api/contacts/5/unmerge" },
    ]),
  );

  mkdirSync(screenshotDir, { recursive: true });
  await page.screenshot({
    fullPage: true,
    path: path.join(screenshotDir, "crm-workspace-desktop.png"),
  });
  expect(browserErrors).toEqual([]);
});

test("crm workspace stays usable at mobile width", async ({ page }) => {
  const browserErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") {
      browserErrors.push(message.text());
    }
  });
  page.on("pageerror", (error) => {
    browserErrors.push(error.message);
  });

  await page.setViewportSize({ height: 844, width: 390 });
  await mockCrmApis(page, []);
  await page.goto("/crm");
  await page.getByTestId("crm-people-row-1").dblclick();

  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible();
  await expect(page.getByTestId("crm-person-signal-band")).toHaveText("High goal fit");
  await expect(page.getByTestId("crm-person-signal-status")).toHaveText("Current local signal");
  await expect(page.getByTestId("crm-person-why-this-matters")).toContainText("Goal match");
  await expect(page.getByTestId("crm-person-why-this-matters")).not.toContainText("/100");
  await expectNoHorizontalOverflow(page);
  const whyThisMatters = page.getByTestId("crm-person-why-this-matters");
  const profileSummary = page.getByTestId("crm-contact-profile-summary");
  await expectElementInside(whyThisMatters, profileSummary);
  await expectElementInside(page.getByTestId("crm-person-signal-band"), profileSummary);
  await expectElementInside(page.getByTestId("crm-person-signal-status"), profileSummary);
  await expectElementInside(page.getByTestId("crm-person-signal-chip").first(), whyThisMatters);
  await expectTextNotClipped(page.getByTestId("crm-person-signal-band"));
  await expectTextNotClipped(page.getByTestId("crm-person-signal-status"));
  await expectTextNotClipped(page.getByTestId("crm-person-signal-chip").first());
  await expect(page.getByRole("heading", { name: "People card" })).toBeVisible();
  await expect(page.getByText("Message bodies load only after an explicit chat open")).toBeVisible();
  await expect(page.getByText("Raw private sentence from Beeper")).toBeHidden();

  mkdirSync(screenshotDir, { recursive: true });
  await page.screenshot({
    fullPage: true,
    path: path.join(screenshotDir, "crm-workspace-mobile.png"),
  });
  expect(browserErrors).toEqual([]);
});

test("crm opened messages render safe rich text without hidden calls or overflow", async ({
  page,
}) => {
  const calls: Array<{ body: unknown; method: string; path: string }> = [];
  const forbiddenRequests = trackForbiddenCrmSignalRequests(page);
  const browserErrors: string[] = [];
  await page.addInitScript(() => {
    (window as Window & { __crmMessageXss?: boolean }).__crmMessageXss = false;
  });
  page.on("console", (message) => {
    if (message.type() === "error") {
      browserErrors.push(message.text());
    }
  });
  page.on("pageerror", (error) => {
    browserErrors.push(error.message);
  });

  await mockCrmApis(page, calls, { graphMode: "hang", recordGet: true });
  await page.setViewportSize({ height: 844, width: 390 });
  await page.goto("/crm/1");

  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible();
  expect(calls.map((call) => call.path)).not.toContain("/api/contacts/1/messages");
  await expect(page.getByText("Synthetic opened message canary")).toBeHidden();
  await expect(page.getByRole("link", { name: "Direct: Alice" })).toHaveAttribute(
    "href",
    /matrix\.to/,
  );

  await page.getByRole("link", { name: "Direct: Alice" }).click();
  await expect
    .poll(() =>
      calls.some(
        (call) =>
          call.method === "POST" && call.path === "/api/contacts/1/chats/11/open",
      ),
    )
    .toBe(true);

  await page.getByRole("button", { name: "Show messages" }).click();
  await expect(page.getByText("Synthetic opened message canary")).toBeVisible();
  await expect(page.getByTestId("crm-chat-messages-scroll")).toBeVisible();
  const body = page.getByTestId("crm-message-body").first();
  await expect(body).toContainText("important context");
  await expect(body).toContainText("bad link");
  await expect(body).not.toContainText(/<strong|<br|<a href|script|alert|onerror|iframe|style/i);
  await expect(page.getByTestId("crm-message-reply-context")).toContainText("Earlier outbound");
  await expect(page.getByRole("link", { name: "safe briefing" })).toHaveAttribute(
    "href",
    "https://safe.example/brief?x=1&y=2",
  );
  await expect(page.getByRole("link", { name: "bad link" })).toHaveCount(0);
  await expect(page.getByRole("link", { name: /plain\.example/ })).toBeVisible();
  await expectNoHorizontalOverflow(page);
  await expectElementInside(body, body.locator("xpath=ancestor::section[1]"));

  const messageCalls = calls.filter((call) => call.path === "/api/contacts/1/messages");
  expect(messageCalls).toHaveLength(1);
  expect(messageCalls[0].method).toBe("GET");
  expect(calls.filter((call) => call.method !== "GET")).toEqual([
    {
      body: null,
      method: "POST",
      path: "/api/contacts/1/chats/11/open",
    },
  ]);
  expect(forbiddenRequests).toEqual([]);
  expect(await page.evaluate(() => (window as Window & { __crmMessageXss?: boolean }).__crmMessageXss)).toBe(
    false,
  );
  expect(browserErrors.filter((error) => !isDevServerResource404(error))).toEqual([]);
});

test("crm contact detail uses scoped summary without full graph context request", async ({ page }) => {
  await mockCrmApis(page, [], { graphMode: "hang" });
  await page.goto("/crm");

  await page.getByTestId("crm-people-row-1").dblclick();

  await expect(page).toHaveURL(/\/crm\/1$/);
  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible({
    timeout: 12_000,
  });
  await expect(page.getByTestId("crm-contact-profile-summary")).toContainText("Direct ties", {
    timeout: 12_000,
  });
  await expect(page.getByText("Raw private sentence from Beeper")).toBeHidden();
});

test("crm contact route opens a dossier without list, graph, or message fanout", async ({
  page,
}) => {
  const calls: Array<{ body: unknown; method: string; path: string }> = [];

  await mockCrmApis(page, calls, { graphMode: "hang", recordGet: true });
  await page.goto("/crm/1");

  await expect(page.getByRole("heading", { name: "Contact dossier" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible();
  await expect(page.getByTestId("crm-person-signal-band")).toHaveText("High goal fit");
  await expect(page.getByRole("button", { name: "People table" })).toBeVisible();
  await expect(page.getByRole("table", { name: "People contacts table" })).toBeHidden();
  await expect(page.getByText("Message bodies load only after an explicit chat open")).toBeVisible();
  await expect(page.getByText("Raw private sentence from Beeper")).toBeHidden();

  const detailGetPaths = calls
    .filter((call) => call.method === "GET")
    .map((call) => call.path);
  expect(detailGetPaths).toContain("/api/contacts/1/dossier");
  expect(detailGetPaths).toContain("/api/contacts/1/merge-candidates");
  expect(detailGetPaths).toContain("/api/user-context/goals");
  expect(detailGetPaths).toContain("/api/relationship-signals/contacts/1/usefulness");
  expect(detailGetPaths).not.toContain("/api/contacts");
  expect(detailGetPaths).not.toContain("/api/contacts/1");
  expect(detailGetPaths).not.toContain("/api/contacts/1/chats");
  expect(detailGetPaths).not.toContain("/api/contacts/1/relationship-summary");
  expect(detailGetPaths).not.toContain("/api/contacts/1/messages");
  expect(detailGetPaths).not.toContain("/api/graph");
  expect(detailGetPaths).not.toContain("/api/relationship-signals/usefulness");
  expect(detailGetPaths).not.toContain("/api/relationship-signals/recompute");
  expect(detailGetPaths.some((item) => item.startsWith("/api/contacts/2"))).toBe(false);
});

test("crm row open uses canonical contact route with browser back and forward", async ({
  page,
}) => {
  await mockCrmApis(page, []);
  await page.goto("/crm");

  await expect(page.getByRole("table", { name: "People contacts table" })).toBeVisible();
  await page.getByTestId("crm-people-row-1").dblclick();

  await expect(page).toHaveURL(/\/crm\/1$/);
  await expect(page.getByRole("heading", { name: "Contact dossier" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible();

  await page.goBack();
  await expect(page).toHaveURL(/\/crm$/);
  await expect(page.getByRole("heading", { name: "People", exact: true })).toBeVisible();
  await expect(page.getByRole("table", { name: "People contacts table" })).toBeVisible();

  await page.goForward();
  await expect(page).toHaveURL(/\/crm\/1$/);
  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible();
  await expect(page.getByText("Raw private sentence from Beeper")).toBeHidden();
});

test("crm contactId query opens compatible dossier without contact-detail fanout", async ({
  page,
}) => {
  const calls: Array<{ body: unknown; method: string; path: string }> = [];

  await mockCrmApis(page, calls, { recordGet: true });
  await page.goto("/crm?contactId=1");

  await expect(page.getByRole("table", { name: "People contacts table" })).toBeHidden();
  await expect(page.getByRole("heading", { name: "People table" })).toHaveCount(0);
  await expect(page.getByRole("button", { name: "People table" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Alice Stone" })).toBeVisible();
  await expect(page.getByText("Raw private sentence from Beeper")).toBeHidden();

  const detailGetPaths = calls
    .filter((call) => call.method === "GET")
    .map((call) => call.path);
  expect(detailGetPaths).toContain("/api/contacts/1/dossier");
  expect(detailGetPaths).toContain("/api/user-context/goals");
  expect(detailGetPaths).toContain("/api/relationship-signals/contacts/1/usefulness");
  expect(detailGetPaths).not.toContain("/api/contacts/1");
  expect(detailGetPaths).not.toContain("/api/contacts/1/chats");
  expect(detailGetPaths).not.toContain("/api/contacts/1/relationship-summary");
  expect(detailGetPaths).not.toContain("/api/contacts/1/messages");
  expect(detailGetPaths).not.toContain("/api/graph");
  expect(detailGetPaths).not.toContain("/api/relationship-signals/usefulness");
  expect(detailGetPaths).not.toContain("/api/relationship-signals/recompute");
  expect(detailGetPaths.some((item) => item.startsWith("/api/contacts/2"))).toBe(false);
});

test("crm constrains long contact identifiers and requests the next contacts page", async ({ page }) => {
  const contactOffsets: number[] = [];
  const browserErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") {
      browserErrors.push(message.text());
    }
  });
  page.on("pageerror", (error) => {
    browserErrors.push(error.message);
  });

  await page.setViewportSize({ height: 900, width: 1180 });
  await mockCrmPaginationApis(page, contactOffsets);
  await page.goto("/crm");

  const peopleTable = page.getByRole("table", { name: "People contacts table" });
  const longContactRow = page.getByTestId("crm-people-row-1");
  const longContactCell = longContactRow.locator("td").first();

  await expect(longContactRow).toBeVisible();
  await expect(longContactCell).toContainText(
    "vsev777rom-with-a-very-long-unbroken-username-for-crm-layout",
  );
  await expectNoHorizontalOverflow(page);
  await expectElementInside(longContactCell, peopleTable);

  await page.getByRole("button", { name: "Next contacts page" }).click();

  await expect.poll(() => contactOffsets).toContain(25);
  await expect(page.getByText("26-50 of 50")).toBeVisible();
  await expectNoHorizontalOverflow(page);
  expect(browserErrors).toEqual([]);
});

async function mockCrmApis(
  page: Page,
  calls: Array<{ body: unknown; method: string; path: string; query?: string }>,
  options: { graphMode?: "hang" | "success"; recordGet?: boolean; recordQuery?: boolean } = {},
) {
  await page.route("http://127.0.0.1:8000/api/**", async (route) => {
    const request = route.request();
    const url = new URL(request.url());
    const pathName = url.pathname;
    const bodyText = request.postData();
    const body = bodyText ? JSON.parse(bodyText) : null;

    if (options.recordGet || request.method() !== "GET") {
      calls.push({
        body,
        method: request.method(),
        path: pathName,
        ...(options.recordQuery ? { query: url.search } : {}),
      });
    }

    if (pathName === "/api/contacts" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json:
          url.searchParams.get("relationship_tier") === "self"
            ? selfContactsPayload
            : contactsPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/facets" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: contactFacetsPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/tags" && request.method() === "GET") {
      await route.fulfill({ contentType: "application/json", json: tagsPayload, status: 200 });
      return;
    }
    if (pathName === "/api/tags" && request.method() === "POST") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          auto_apply_eligible: false,
          auto_suggest_enabled: true,
          color: body?.color ?? "#C7A15A",
          contact_count: 0,
          group_id: 2,
          id: 41,
          name: body?.name ?? "Partner",
          risk_level: "low",
          slug: "tag_6e3818da",
        },
        status: 201,
      });
      return;
    }
    if (pathName === "/api/tags/groups" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: tagGroupsPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/tags/groups" && request.method() === "POST") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          archived_at: null,
          auto_apply_policy: body?.auto_apply_policy ?? "review",
          auto_suggest_enabled: true,
          color: body?.color ?? "#C7A15A",
          description: body?.description ?? null,
          id: 42,
          name: body?.name ?? "Partners",
          risk_level: body?.risk_level ?? "low",
          slug: "group_6e3818da",
          sort_order: body?.sort_order ?? 0,
        },
        status: 201,
      });
      return;
    }
    if (pathName === "/api/tags/groups/2" && request.method() === "PATCH") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          archived_at: null,
          auto_apply_policy: body?.auto_apply_policy ?? "review",
          auto_suggest_enabled: true,
          color: body?.color ?? "#C7A15A",
          description: body?.description ?? null,
          id: 2,
          name: body?.name ?? "Role",
          risk_level: body?.risk_level ?? "low",
          slug: "role",
          sort_order: body?.sort_order ?? 10,
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/tags/settings" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: taggingSettingsPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/tags/eval" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: taggingEvalPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/tags/suggestions/41/accept" && request.method() === "POST") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          contract_version: "crm-tags-v1",
          suggestion: {
            confidence_band: "high",
            confidence_score: 0.87,
            contact_id: 1,
            evidence_count: 2,
            id: 41,
            policy_result: {},
            proposed_group_slug: "role",
            proposed_tag_name: "VIP",
            proposed_tag_slug: "vip",
            reason_code: "role_match",
            run_id: 4,
            source_exclusion_active_count: 0,
            source_exclusion_latest_updated_at: null,
            source_exclusion_policy_version: "source-exclusion-v1",
            status: "applied",
            tag_id: 7,
          },
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/settings" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: { theme: "noir-gold" },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/user-context/profile" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: userContextProfilePayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/user-context/profile" && request.method() === "PATCH") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          contract_version: "user-context-v1",
          profile: {
            ...userContextProfilePayload.profile,
            display_label: body?.display_label ?? "Local Operator Updated",
            profile_version: 3,
          },
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/user-context/goals" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: userContextGoalsPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/user-context/goals" && request.method() === "POST") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          contract_version: "user-context-v1",
          goal: {
            ...userContextGoalsPayload.items[0],
            goal_id: "goal-created-e2e",
            title: body?.title ?? "New CRM goal",
          },
        },
        status: 200,
      });
      return;
    }
    if (
      pathName === "/api/user-context/goals/goal-crm-e2e/archive" &&
      request.method() === "POST"
    ) {
      await route.fulfill({
        contentType: "application/json",
        json: {
          contract_version: "user-context-v1",
          goal: {
            ...userContextGoalsPayload.items[0],
            archived_at: 1_770_086_500,
            status: "archived",
          },
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/user-context/items" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: userContextItemsPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/user-context/items" && request.method() === "POST") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          contract_version: "user-context-v1",
          item: {
            ...userContextItemsPayload.items[0],
            item_id: "item-created-e2e",
            item_type: body?.item_type ?? "need",
            label: body?.label ?? "New CRM item",
          },
        },
        status: 200,
      });
      return;
    }
    if (
      pathName === "/api/user-context/items/item-crm-e2e/archive" &&
      request.method() === "POST"
    ) {
      await route.fulfill({
        contentType: "application/json",
        json: {
          contract_version: "user-context-v1",
          item: {
            ...userContextItemsPayload.items[0],
            archived_at: 1_770_086_500,
            status: "archived",
          },
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/user-context/status" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: userContextStatusPayload,
        status: 200,
      });
      return;
    }
    if (
      (pathName === "/api/review-queue/items" || pathName === "/api/review-queue") &&
      request.method() === "GET"
    ) {
      await route.fulfill({
        contentType: "application/json",
        json: reviewQueuePayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/relationship-signals/contacts/1/usefulness") {
      await route.fulfill({
        contentType: "application/json",
        json: contactUsefulnessPayload,
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1" && request.method() === "GET") {
      await route.fulfill({ contentType: "application/json", json: contactDetail, status: 200 });
      return;
    }
    if (pathName === "/api/contacts/1/dossier" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          chats: contactChatsPayload,
          contact: contactDetail,
          relationship_summary: contactRelationshipSummaryPayload,
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/channels" && request.method() === "POST") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          channel_type: "profile",
          is_primary: false,
          label: `${body?.network ?? "Messenger"} profile`,
          network: body?.network ?? "telegram",
          open_target: {
            method: "url",
            status: "available",
            value: body?.profile_url ?? "https://t.me/alice",
          },
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/location" && request.method() === "PATCH") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          archived: false,
          city: null,
          confidence_score: null,
          country: null,
          is_manual: true,
          is_primary: true,
          location_id: "manual:2",
          location_label: body?.location_label ?? "Lisbon",
          open_target: {
            method: "maps_search",
            status: "available",
            value: `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
              body?.location_label ?? "Lisbon",
            )}`,
          },
          region: null,
          source: "manual",
          timezone: null,
          user_verified: true,
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/relationship-summary") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          activity: { chat_count: 1, last_activity_ts: 1_746_300_000, message_count: 80 },
          contact_id: 1,
          contract_version: "person-relationship-summary-v1",
          counts: {
            accepted_memory_facts: 2,
            active_contact_sources: 3,
            chat_memberships: 1,
            memory_evidence_refs: 4,
            visible_messages_from_contact: 80,
          },
          graph_summary: {
            direct_ties: 5,
            full_graph_loaded: false,
            shared_groups_count: 2,
            strongest_tie_label: "Bob Vega",
          },
          memory: {
            accepted_count: 2,
            evidence_ref_count: 4,
            items: [
              {
                accepted_at: 1_746_300_000,
                confidence_band: "high",
                confidence_score: 0.9,
                evidence_ref_count: 1,
                evidence_refs: [
                  {
                    evidence_type: "supporting_ref",
                    rank: 1,
                    redaction_state: "metadata_only",
                    ref_id: 77,
                    source_type: "message",
                  },
                ],
                fact_type: "relationship_context",
                memory_id: "mem-alice",
                review_source: "user_created",
                source_category: "message_window",
              },
            ],
          },
          source_state: { source: "sync", stale: false, status: "available" },
          tags: [{ color: "#ca8a04", id: 7, name: "VIP" }],
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/relationship-summary/evidence/77/source-context") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          contact_id: 1,
          contract_version: "person-summary-evidence-source-context-v1",
          count: 1,
          evidence_ref_id: 77,
          items: [
            {
              evidence_ref_id: 77,
              message_count: 1,
              message_ids: [101],
              rag_card_id: null,
              rank: 1,
              redaction_state: "metadata_only",
              restore_status: "restored",
              source_text: "Synthetic People source context.",
              source_type: "message_window",
            },
          ],
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/chats") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          items: [
            {
              beeper_chat_id: "!chat:telegram",
              id: 11,
              last_activity_ts: 1_746_300_000,
              network: "telegram",
              open_target: {
                method: "beeper_chat",
                status: "available",
                value: "!chat:telegram",
              },
              participants_count: 2,
              title: "Direct: Alice",
              type: "single",
            },
          ],
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/chats/11/open" && request.method() === "POST") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          chat_id: 11,
          contact_id: 1,
          method: "beeper_focus",
          status: "opened",
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/messages") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          items: [
            {
              chat_id: 11,
              id: 101,
              is_sender: false,
              network: "telegram",
              reply_to_message: {
                chat_id: 11,
                id: 100,
                is_sender: true,
                network: "telegram",
                sender_beeper_id: "@me:telegram",
                sender_name: "Me",
              text: "Earlier <strong>outbound</strong><br>context",
                timestamp: 1_746_299_900,
              },
              reply_to_message_id: 100,
              reply_to_missing: false,
              sender_beeper_id: "@alice:telegram",
              sender_name: "Alice",
              text: [
                "Synthetic opened message canary <strong>important context</strong><br>",
                '<a href="https://safe.example/brief?x=1&amp;y=2">safe briefing</a> ',
                '<a href="javascript:alert(1)">bad link</a> ',
                '<img src=x onerror="window.__crmMessageXss=true"> ',
                '<script>window.__crmMessageXss=true</script> ',
                '<iframe>unsafe frame</iframe> ',
                '<style>body{display:none}</style> ',
                "https://plain.example/very/long/path?ref=safe",
              ].join(""),
              timestamp: 1_746_300_000,
            },
          ],
          limit: 5,
          next_cursor: 1_746_300_000,
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/99/chats") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          items: [
            {
              beeper_chat_id: "!self:telegram",
              has_local_user_messages: true,
              id: 991,
              last_activity_ts: 1_746_300_100,
              local_user_message_count: 1,
              network: "telegram",
              open_target: {
                method: "beeper_chat",
                status: "available",
                value: "!self:telegram",
              },
              participants_count: 1,
              title: "Saved Messages",
              type: "single",
            },
            {
              beeper_chat_id: "!readonly:telegram",
              has_local_user_messages: false,
              id: 992,
              last_activity_ts: 1_746_300_080,
              local_user_message_count: 0,
              network: "telegram",
              open_target: {
                method: "beeper_chat",
                status: "available",
                value: "!readonly:telegram",
              },
              participants_count: 12,
              title: "Read-only Research Group",
              type: "group",
            },
          ],
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/100/chats") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          items: [
            {
              beeper_chat_id: "!linkedin-readonly:linkedin",
              has_local_user_messages: false,
              id: 1001,
              last_activity_ts: 1_746_300_040,
              local_user_message_count: 0,
              network: "linkedin",
              open_target: {
                method: "beeper_chat",
                status: "available",
                value: "!linkedin-readonly:linkedin",
              },
              participants_count: 32,
              title: "LinkedIn Market Watch",
              type: "group",
            },
          ],
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/99/messages") {
      const selfMessages = [
        {
          chat_id: 991,
          id: 9910,
          is_sender: false,
          network: "telegram",
          reply_to_message: null,
          reply_to_message_id: null,
          reply_to_missing: false,
          sender_beeper_id: "@contact:telegram",
          sender_name: "Contact",
          text: "Inbound self-profile leak canary",
          timestamp: 1_746_300_090,
        },
        {
          chat_id: 991,
          id: 9911,
          is_sender: true,
          network: "telegram",
          reply_to_message: {
            chat_id: 991,
            id: 9910,
            is_sender: false,
            network: "telegram",
            sender_beeper_id: "@contact:telegram",
            sender_name: "Contact",
            text: "Inbound self-profile leak canary",
            timestamp: 1_746_300_090,
          },
          reply_to_message_id: 9910,
          reply_to_missing: false,
          sender_beeper_id: "@me:telegram",
          sender_name: "Me",
          text: "Self opened message canary",
          timestamp: 1_746_300_100,
        },
      ];
      await route.fulfill({
        contentType: "application/json",
        json: {
          items:
            url.searchParams.get("sender") === "me"
              ? selfMessages.filter((message) => message.is_sender)
              : selfMessages,
          limit: 5,
          next_cursor: null,
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/merge-candidates") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          items: [
            {
              avatar_url: null,
              contact_id: 2,
              first_name: "Bob",
              last_name: "Vega",
              network: "linkedin",
              reason: "name_similarity",
              score: 0.82,
              username: "bob",
            },
          ],
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/contacts/1/relationship-state" && request.method() === "PATCH") {
      await route.fulfill({
        contentType: "application/json",
        json: {
          classification_source: "user",
          confidence_band: null,
          confidence_score: null,
          contact_id: 1,
          contract_version: "people-classification-v1",
          created_at: 1_746_300_000,
          reason_code: "user_hidden",
          relationship_tier: "ignored",
          updated_at: 1_746_300_010,
          user_locked: true,
        },
        status: 200,
      });
      return;
    }
    if (pathName === "/api/graph") {
      if (options.graphMode === "hang") {
        await delay(10_000);
        try {
          await route.fulfill({ contentType: "application/json", json: graphPayload, status: 200 });
        } catch {
          // The browser is expected to abort this delayed response after its local timeout.
        }
        return;
      }
      await route.fulfill({ contentType: "application/json", json: graphPayload, status: 200 });
      return;
    }
    if (request.method() !== "GET") {
      if (pathName.includes("/tags/") && request.method() === "DELETE") {
        await route.fulfill({ status: 204 });
        return;
      }
      await route.fulfill({
        contentType: "application/json",
        json: { ok: true },
        status: 200,
      });
      return;
    }

    await route.fulfill({ contentType: "application/json", json: {}, status: 404 });
  });
}

// Capture requested offsets while stubbing the CRM list endpoints used by the pagination scenario.
async function mockCrmPaginationApis(page: Page, contactOffsets: number[]) {
  await page.route("http://127.0.0.1:8000/api/**", async (route) => {
    const request = route.request();
    const url = new URL(request.url());
    const pathName = url.pathname;

    if (pathName === "/api/contacts" && request.method() === "GET") {
      const offset = Number(url.searchParams.get("offset") ?? "0");
      contactOffsets.push(offset);
      await route.fulfill({
        contentType: "application/json",
        json: offset === 25 ? longContactsSecondPage : longContactsFirstPage,
        status: 200,
      });
      return;
    }

    if (pathName === "/api/tags" && request.method() === "GET") {
      await route.fulfill({ contentType: "application/json", json: { items: [] }, status: 200 });
      return;
    }

    if (pathName === "/api/settings" && request.method() === "GET") {
      await route.fulfill({
        contentType: "application/json",
        json: { theme: "noir-gold" },
        status: 200,
      });
      return;
    }

    await route.fulfill({ contentType: "application/json", json: {}, status: 404 });
  });
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function trackForbiddenCrmSignalRequests(page: Page) {
  const requests: string[] = [];
  page.on("request", (request) => {
    const url = request.url();
    if (
      /workers\.dev|cloudflare|api\.openai\.com|\/v1\/advisor\/infer|\/api\/insights|\/v1\/insights|gateway\/logs|telemetry|\/api\/relationship-signals\/recompute|\/api\/graph\/recompute|\/api\/advisor\/run|\/api\/advisor\/findings\/.+\/actions|\/api\/tags\/suggestions\/.+\/(?:accept|reject|undo)|\/api\/tags\/suggestions\/bulk|\/api\/contacts\/\d+\/tags|\/api\/contacts\/\d+\/relationship-state/i.test(
        url,
      )
    ) {
      requests.push(`${request.method()} ${url}`);
    }
  });
  return requests;
}

function isDevServerResource404(error: string): boolean {
  return /Failed to load resource: the server responded with a status of 404/i.test(error);
}

async function expectNoHorizontalOverflow(page: Page) {
  const overflow = await page.evaluate(() => ({
    bodyWidth: document.body.scrollWidth,
    documentWidth: document.documentElement.scrollWidth,
    viewportWidth: document.documentElement.clientWidth,
  }));

  expect(overflow.documentWidth).toBeLessThanOrEqual(overflow.viewportWidth + 1);
  expect(overflow.bodyWidth).toBeLessThanOrEqual(overflow.viewportWidth + 1);
}

async function expectNoVerticalPageOverflow(page: Page) {
  const overflow = await page.evaluate(() => ({
    bodyHeight: document.body.scrollHeight,
    documentHeight: document.documentElement.scrollHeight,
    viewportHeight: document.documentElement.clientHeight,
  }));

  expect(overflow.documentHeight).toBeLessThanOrEqual(overflow.viewportHeight + 16);
  expect(overflow.bodyHeight).toBeLessThanOrEqual(overflow.viewportHeight + 16);
}

async function expectElementInside(element: Locator, container: Locator) {
  const elementBox = await element.first().boundingBox();
  const containerBox = await container.first().boundingBox();

  expect(elementBox).not.toBeNull();
  expect(containerBox).not.toBeNull();
  expect(elementBox!.x).toBeGreaterThanOrEqual(containerBox!.x - 1);
  expect(elementBox!.y).toBeGreaterThanOrEqual(containerBox!.y - 1);
  expect(elementBox!.x + elementBox!.width).toBeLessThanOrEqual(
    containerBox!.x + containerBox!.width + 1,
  );
  expect(elementBox!.y + elementBox!.height).toBeLessThanOrEqual(
    containerBox!.y + containerBox!.height + 1,
  );
}

async function expectTextNotClipped(element: Locator) {
  const metrics = await element.first().evaluate((node) => {
    const target = node as HTMLElement;
    return {
      clientHeight: target.clientHeight,
      clientWidth: target.clientWidth,
      scrollHeight: target.scrollHeight,
      scrollWidth: target.scrollWidth,
    };
  });

  expect(metrics.scrollWidth).toBeLessThanOrEqual(metrics.clientWidth + 1);
  expect(metrics.scrollHeight).toBeLessThanOrEqual(metrics.clientHeight + 1);
}
