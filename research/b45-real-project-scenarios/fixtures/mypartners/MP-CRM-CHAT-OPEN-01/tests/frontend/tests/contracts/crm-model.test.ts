import { expect, test } from "@playwright/test";

import type { GraphPayload } from "@/features/graph/api";
import type { ContactChat, ContactDetail } from "@/features/crm/api";
import {
  buildPeopleCardV2View,
  buildContactListView,
  buildContactRelationshipContext,
  buildPeopleTableRows,
  formatContactDisplayName,
  formatTimestamp,
  type ContactListItem,
} from "@/features/crm/model";

const contacts: ContactListItem[] = [
  {
    account_id: "local-telegram",
    beeper_contact_id: "@alice:telegram",
    first_name: "Alice",
    id: 1,
    is_deleted: false,
    last_name: "Stone",
    merged_into_id: null,
    network: "telegram",
    username: "alice",
  },
  {
    account_id: "local-linkedin",
    beeper_contact_id: "@bob:linkedin",
    first_name: null,
    id: 2,
    is_deleted: false,
    last_name: null,
    merged_into_id: 1,
    network: "linkedin",
    username: "bob_builder",
  },
];

test("builds stable contact display names and list summary", () => {
  expect(formatContactDisplayName(contacts[0])).toBe("Alice Stone");
  expect(formatContactDisplayName(contacts[1])).toBe("bob_builder");
  expect(
    formatContactDisplayName({
      ...contacts[1],
      beeper_contact_id: "",
      id: 9,
      username: null,
    }),
  ).toBe("Contact #9");

  const view = buildContactListView({
    contacts,
    limit: 25,
    offset: 0,
    total: 42,
  });

  expect(view.pageLabel).toBe("1-25 of 42");
  expect(view.networks).toEqual(["linkedin", "telegram"]);
  expect(view.items.map((item) => item.displayName)).toEqual(["Alice Stone", "bob_builder"]);
  expect(view.items[1].mergeLabel).toBe("Merged into #1");
});

test("builds People table rows from current list fields with honest readiness", () => {
  const view = buildContactListView({
    contacts: [
      {
        ...contacts[0],
        channels: [
          {
            channel_type: "profile",
            is_primary: true,
            label: "Telegram",
            network: "telegram",
            open_target: {
              method: "url",
              status: "available",
              value: "https://example.local/alice",
            },
          },
        ],
        primary_location: null,
        relationship_state_reason: "address_book_contact",
        relationship_state_source: "sync",
        relationship_state_user_locked: true,
        relationship_tier: "confirmed",
      },
    ],
    limit: 25,
    offset: 0,
    total: 1,
  });

  const rows = buildPeopleTableRows({
    items: view.items,
    sortDirection: "asc",
    sortKey: "person",
  });

  expect(rows).toHaveLength(1);
  expect(rows[0]).toMatchObject({
    channelLabel: "Telegram",
    channelStateLabel: "open target available",
    dataStateLabel: "user locked",
    lastTouchLabel: "Projection needed",
    locationLabel: "Location unknown",
    nextActionLabel: "Not projected",
    reviewLabel: "Not projected",
    tagSummaryLabel: "Detail only",
  });
  expect(rows[0].readiness).toEqual({
    channels: "current_api_backed",
    dataState: "current_api_backed",
    lastTouch: "projection_needed",
    nextAction: "projection_needed",
    review: "projection_needed",
    tags: "projection_needed",
  });
  expect(JSON.stringify(rows[0])).not.toContain("Raw private");
});

test("sorts People table rows without contact detail, graph, or message inputs", () => {
  const view = buildContactListView({
    contacts: [
      {
        ...contacts[0],
        relationship_state_source: "sync",
        relationship_tier: "confirmed",
      },
      {
        ...contacts[1],
        relationship_state_source: "user",
        relationship_state_user_locked: true,
        relationship_tier: "potential",
      },
    ],
    limit: 25,
    offset: 0,
    total: 2,
  });

  expect(
    buildPeopleTableRows({
      items: view.items,
      sortDirection: "desc",
      sortKey: "person",
    }).map((row) => row.displayName),
  ).toEqual(["bob_builder", "Alice Stone"]);

  expect(
    buildPeopleTableRows({
      items: view.items,
      sortDirection: "asc",
      sortKey: "tier",
    }).map((row) => row.relationshipTier),
  ).toEqual(["confirmed", "potential"]);

  expect(
    buildPeopleTableRows({
      items: view.items,
      sortDirection: "asc",
      sortKey: "data_state",
    }).map((row) => row.dataStateLabel),
  ).toEqual(["merged", "sync managed"]);
});

test("derives selected contact graph context from the global graph payload", () => {
  const graph: GraphPayload = {
    communities: [[1, 2, 3]],
    edges: [
      {
        cross_platform: true,
        shared_groups_count: 2,
        shared_topics: ["pricing", "pilot"],
        source: 1,
        target: 2,
        weight: 4.2,
      },
      {
        cross_platform: false,
        shared_groups_count: 1,
        shared_topics: ["hiring"],
        source: 3,
        target: 1,
        weight: 2,
      },
    ],
    nodes: [
      {
        id: 1,
        is_merged: false,
        is_self: false,
        label: "Alice Stone",
        merged_count: 0,
        network: "telegram",
        networks: ["telegram"],
      },
      {
        id: 2,
        is_merged: false,
        is_self: false,
        label: "Bob",
        merged_count: 0,
        network: "linkedin",
        networks: ["linkedin"],
      },
      {
        id: 3,
        is_merged: false,
        is_self: false,
        label: "Cara",
        merged_count: 0,
        network: "whatsapp",
        networks: ["whatsapp"],
      },
    ],
  };

  const context = buildContactRelationshipContext(graph, 1);

  expect(context).toEqual({
    contactLabel: "Alice Stone",
    degree: 2,
    strongestTieLabel: "Bob",
    strongestTieWeight: 4.2,
    topics: ["pricing", "pilot", "hiring"],
  });
});

test("formats unix timestamps without unstable current-time labels", () => {
  expect(formatTimestamp(null)).toBe("No timestamp");
  expect(formatTimestamp(1_746_300_000)).toMatch(/2025/);
});

test("builds People card v2 metadata without raw evidence text", () => {
  const contact: ContactDetail = {
    account_id: "local-telegram",
    avatar_url: null,
    beeper_contact_id: "@alice:telegram",
    first_name: "Alice",
    id: 1,
    is_deleted: false,
    is_merged: false,
    is_self: false,
    last_name: "Stone",
    merged_into_id: null,
    merged_sources: [],
    network: "telegram",
    networks: ["telegram"],
    note: null,
    phone_number: null,
    relationship_state_reason: "address_book_contact",
    relationship_state_source: "sync",
    relationship_state_user_locked: false,
    relationship_tier: "confirmed",
    tags: [{ color: "#ca8a04", id: 7, name: "VIP" }],
    username: "alice",
  };
  const chats: ContactChat[] = [
    {
      beeper_chat_id: "!chat:telegram",
      id: 11,
      last_activity_ts: 1_746_300_000,
      network: "telegram",
      participants_count: 2,
      title: "Direct: Alice",
      type: "single",
    },
  ];

  const view = buildPeopleCardV2View({
    chats,
    contact,
    summary: {
      activity: { chat_count: 2, last_activity_ts: 1_746_300_000, message_count: 80 },
      contact_id: 1,
      contract_version: "person-relationship-summary-v1",
      counts: {
        accepted_memory_facts: 2,
        active_contact_sources: 3,
        chat_memberships: 2,
        memory_evidence_refs: 4,
        visible_messages_from_contact: 80,
      },
      graph_summary: {
        direct_ties: 5,
        full_graph_loaded: false,
        shared_groups_count: 2,
        strongest_tie_label: "Raw private message from Bob",
      },
      memory: { accepted_count: 2, evidence_ref_count: 4 },
      source_state: { source: "sync", stale: false, status: "available" },
      tags: [{ color: "#ca8a04", id: 7, name: "VIP" }],
    },
    summaryState: "available",
  });

  expect(view.source).toEqual({
    lockLabel: "sync managed",
    sourceLabel: "sync",
    stateLabel: "available",
  });
  expect(view.graph.directTieLabel).toBe("5 direct ties");
  expect(view.graph.strongestTieLabel).toBe("metadata unavailable");
  expect(view.evidence).toEqual({
    allowedEvidenceLabel: "4 allowed refs",
    memoryFactLabel: "2 memory facts",
    sourceRefLabel: "3 source refs",
  });
  expect(view.activity.messageCountLabel).toBe("80 messages");
  expect(JSON.stringify(view)).not.toContain("Raw private message");
});

test("builds People card v2 placeholder from local contact metadata", () => {
  const contact = {
    ...contacts[0],
    avatar_url: null,
    is_merged: false,
    is_self: false,
    merged_sources: [],
    networks: ["telegram"],
    note: null,
    phone_number: null,
    relationship_state_source: "sync",
    relationship_state_user_locked: true,
    relationship_tier: "confirmed",
    tags: [],
  } satisfies ContactDetail;

  const view = buildPeopleCardV2View({
    chats: [],
    contact,
    summary: null,
    summaryState: "placeholder",
  });

  expect(view.state).toBe("placeholder");
  expect(view.source.lockLabel).toBe("user locked");
  expect(view.graph.directTieLabel).toBe("direct ties unavailable");
  expect(view.activity.chatCountLabel).toBe("0 chats");
  expect(view.tags.countLabel).toBe("0 tags");
});
