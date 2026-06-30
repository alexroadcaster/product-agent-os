import { expect, test } from "@playwright/test";

import {
  addContactChannel,
  archiveTag,
  archiveTagGroup,
  attachTagToContact,
  bulkTagSuggestions,
  createTag,
  createTagGroup,
  detachTagFromContact,
  generateTagSuggestions,
  getContact,
  getContactChats,
  getContactDossier,
  getContactFacets,
  getContactMessages,
  getContactRelationshipEvidenceSourceContext,
  getContactRelationshipSummary,
  getContacts,
  getMergeCandidates,
  getTaggingEval,
  getTaggingSettings,
  getTagGroups,
  getTagSuggestions,
  getTags,
  mergeContact,
  patchContactLocation,
  patchTag,
  patchTagGroup,
  patchTaggingSettings,
  patchContact,
  patchContactRelationshipState,
  rejectTagSuggestion,
  restoreTag,
  restoreTagGroup,
  unmergeContact,
  type ContactDetail,
  type ContactFacetsResponse,
  type ContactsResponse,
} from "@/features/crm/api";

function jsonFetch(payload: unknown, calls: Array<{ body: string | null; method: string; url: string }> = []): typeof fetch {
  return async (url, init) => {
    calls.push({
      body: typeof init?.body === "string" ? init.body : null,
      method: init?.method ?? "GET",
      url: String(url),
    });

    return new Response(JSON.stringify(payload), {
      headers: { "content-type": "application/json" },
      status: 200,
    });
  };
}

test("builds current contacts list query against local FastAPI", async () => {
  const calls: Array<{ body: string | null; method: string; url: string }> = [];
  const payload: ContactsResponse = {
    items: [],
    limit: 25,
    offset: 50,
    total: 0,
  };

  await getContacts(
    {
      includeMerged: true,
      limit: 25,
      minWeight: 2.5,
      network: "telegram",
      offset: 50,
      query: "ivan petrov",
      relationshipTier: "potential",
      tagId: 7,
    },
    { fetchImpl: jsonFetch(payload, calls) },
  );

  const url = new URL(calls[0].url);
  expect(url.pathname).toBe("/api/contacts");
  expect(url.searchParams.get("q")).toBe("ivan petrov");
  expect(url.searchParams.get("network")).toBe("telegram");
  expect(url.searchParams.get("relationship_tier")).toBe("potential");
  expect(url.searchParams.get("tag_id")).toBe("7");
  expect(url.searchParams.get("min_weight")).toBe("2.5");
  expect(url.searchParams.get("include_merged")).toBe("true");
  expect(url.searchParams.get("limit")).toBe("25");
  expect(url.searchParams.get("offset")).toBe("50");
});

test("builds current contacts facets query against local FastAPI", async () => {
  const calls: Array<{ body: string | null; method: string; url: string }> = [];
  const payload: ContactFacetsResponse = {
    channels: [],
    contract_version: "people-facets-v1",
    locations: { known: 0, manual: 0, unknown: 0, user_verified: 0 },
    networks: [],
    relationship_state_sources: [],
    source_types: [],
    tiers: [{ count: 12, value: "confirmed" }],
    total: 12,
  };

  await getContactFacets(
    {
      includeMerged: true,
      minWeight: 2.5,
      network: "telegram",
      query: "ivan petrov",
      relationshipStateSource: "user",
      relationshipTier: "confirmed",
      tagId: 7,
      userLocked: true,
    },
    { fetchImpl: jsonFetch(payload, calls) },
  );

  const url = new URL(calls[0].url);
  expect(url.pathname).toBe("/api/contacts/facets");
  expect(url.searchParams.get("q")).toBe("ivan petrov");
  expect(url.searchParams.get("network")).toBe("telegram");
  expect(url.searchParams.get("relationship_tier")).toBe("confirmed");
  expect(url.searchParams.get("relationship_state_source")).toBe("user");
  expect(url.searchParams.get("user_locked")).toBe("true");
  expect(url.searchParams.get("tag_id")).toBe("7");
  expect(url.searchParams.get("min_weight")).toBe("2.5");
  expect(url.searchParams.get("include_merged")).toBe("true");
});

test("uses current contact detail, chats, messages, merge, tag, and note endpoints", async () => {
  const calls: Array<{ body: string | null; method: string; url: string }> = [];
  const detail: ContactDetail = {
    account_id: "local-telegram",
    avatar_url: null,
    beeper_contact_id: "@alice:telegram",
    first_name: "Alice",
    id: 42,
    is_deleted: false,
    is_merged: false,
    is_self: false,
    last_name: "Stone",
    merged_into_id: null,
    merged_sources: [],
    network: "telegram",
    networks: ["telegram"],
    note: { note_text: "Investor intro", updated_at: 1_746_300_000 },
    phone_number: null,
    tags: [{ color: "#ca8a04", id: 3, name: "VIP" }],
    username: "alice",
  };

  await getContact(42, { fetchImpl: jsonFetch(detail, calls) });
  await getContactDossier(42, {
    fetchImpl: jsonFetch(
      {
        chats: { items: [] },
        contact: detail,
        relationship_summary: {
          contact_id: 42,
          contract_version: "person-relationship-summary-v1",
          graph_summary: {
            direct_ties: 5,
            full_graph_loaded: false,
            shared_groups_count: 2,
            strongest_tie_contact_id: 8,
          },
        },
      },
      calls,
    ),
  });
  await patchContact(42, { first_name: "Alice", last_name: "Stone", note_text: "Updated note" }, { fetchImpl: jsonFetch({ id: 42, status: "ok" }, calls) });
  await addContactChannel(
    42,
    { network: "telegram", profile_url: "https://t.me/alice" },
    {
      fetchImpl: jsonFetch(
        {
          channel_type: "profile",
          is_primary: false,
          label: "Telegram profile",
          network: "telegram",
          open_target: { method: "url", status: "available", value: "https://t.me/alice" },
        },
        calls,
      ),
    },
  );
  await patchContactLocation(
    42,
    { location_label: "Tbilisi" },
    {
      fetchImpl: jsonFetch(
        {
          archived: false,
          city: null,
          confidence_score: null,
          country: null,
          is_manual: true,
          is_primary: true,
          location_id: "manual:42",
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
        calls,
      ),
    },
  );
  await getContactChats(42, { fetchImpl: jsonFetch({ items: [] }, calls) });
  await getContactRelationshipSummary(
    42,
    {
      fetchImpl: jsonFetch(
        {
          activity: { chat_count: 2, last_activity_ts: 1_746_300_000, message_count: 80 },
          contact_id: 42,
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
            strongest_tie_contact_id: 8,
          },
          source_state: { source: "sync", stale: false, status: "available" },
          tags: [{ color: "#ca8a04", id: 3, name: "VIP" }],
        },
        calls,
      ),
    },
  );
  await getContactRelationshipEvidenceSourceContext(
    42,
    77,
    {
      fetchImpl: jsonFetch(
        {
          contact_id: 42,
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
        calls,
      ),
    },
  );
  await getContactMessages(
    42,
    { chatId: 9, limit: 10, sender: "me", toTs: 1_746_300_000 },
    { fetchImpl: jsonFetch({ items: [], limit: 10, next_cursor: null }, calls) },
  );
  await getMergeCandidates(42, { topK: 3 }, { fetchImpl: jsonFetch({ items: [] }, calls) });
  await patchContactRelationshipState(
    42,
    { reason_code: "user_hidden", relationship_tier: "ignored", user_locked: true },
    {
      fetchImpl: jsonFetch(
        {
          classification_source: "user",
          confidence_band: null,
          confidence_score: null,
          contact_id: 42,
          contract_version: "people-classification-v1",
          created_at: 1_746_300_000,
          reason_code: "user_hidden",
          relationship_tier: "ignored",
          updated_at: 1_746_300_001,
          user_locked: true,
        },
        calls,
      ),
    },
  );
  await mergeContact(99, 42, { fetchImpl: jsonFetch({ canonical_id: 42, merged_id: 99, status: "merged" }, calls) });
  await unmergeContact(99, { fetchImpl: jsonFetch({ id: 99, status: "unmerged" }, calls) });
  await getTags({ fetchImpl: jsonFetch({ items: [] }, calls) });
  await createTag({ color: "#6f7f5b", name: "Founder" }, { fetchImpl: jsonFetch({ color: "#6f7f5b", id: 4, name: "Founder" }, calls) });
  await attachTagToContact(42, 4, { fetchImpl: jsonFetch({ contact_id: 42, status: "attached", tag_id: 4 }, calls) });
  await detachTagFromContact(42, 4, { fetchImpl: jsonFetch(null, calls) });

  expect(calls.map((call) => [new URL(call.url).pathname, call.method])).toEqual([
    ["/api/contacts/42", "GET"],
    ["/api/contacts/42/dossier", "GET"],
    ["/api/contacts/42", "PATCH"],
    ["/api/contacts/42/channels", "POST"],
    ["/api/contacts/42/location", "PATCH"],
    ["/api/contacts/42/chats", "GET"],
    ["/api/contacts/42/relationship-summary", "GET"],
    ["/api/contacts/42/relationship-summary/evidence/77/source-context", "GET"],
    ["/api/contacts/42/messages", "GET"],
    ["/api/contacts/42/merge-candidates", "GET"],
    ["/api/contacts/42/relationship-state", "PATCH"],
    ["/api/contacts/99/merge", "POST"],
    ["/api/contacts/99/unmerge", "POST"],
    ["/api/tags", "GET"],
    ["/api/tags", "POST"],
    ["/api/contacts/42/tags", "POST"],
    ["/api/contacts/42/tags/4", "DELETE"],
  ]);
  const patchContactCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/42" && call.method === "PATCH";
  });
  const channelCreateCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/42/channels" && call.method === "POST";
  });
  const locationPatchCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/42/location" && call.method === "PATCH";
  });
  const messagesCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/42/messages" && call.method === "GET";
  });
  const mergeCandidatesCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/42/merge-candidates" && call.method === "GET";
  });
  const relationshipStatePatchCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/42/relationship-state" && call.method === "PATCH";
  });
  const mergeCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/99/merge" && call.method === "POST";
  });
  const createTagCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/tags" && call.method === "POST";
  });
  const attachTagCall = calls.find((call) => {
    const url = new URL(call.url);
    return url.pathname === "/api/contacts/42/tags" && call.method === "POST";
  });
  expect(JSON.parse(patchContactCall?.body ?? "{}")).toEqual({
    first_name: "Alice",
    last_name: "Stone",
    note_text: "Updated note",
  });
  expect(JSON.parse(channelCreateCall?.body ?? "{}")).toEqual({
    network: "telegram",
    profile_url: "https://t.me/alice",
  });
  expect(JSON.parse(locationPatchCall?.body ?? "{}")).toEqual({ location_label: "Tbilisi" });
  expect(new URL(messagesCall?.url ?? "http://127.0.0.1").searchParams.get("chat_id")).toBe("9");
  expect(new URL(messagesCall?.url ?? "http://127.0.0.1").searchParams.get("sender")).toBe("me");
  expect(new URL(mergeCandidatesCall?.url ?? "http://127.0.0.1").searchParams.get("top_k")).toBe("3");
  expect(JSON.parse(relationshipStatePatchCall?.body ?? "{}")).toEqual({
    reason_code: "user_hidden",
    relationship_tier: "ignored",
    user_locked: true,
  });
  expect(JSON.parse(mergeCall?.body ?? "{}")).toEqual({ into_contact_id: 42 });
  expect(JSON.parse(createTagCall?.body ?? "{}")).toEqual({ color: "#6f7f5b", name: "Founder" });
  expect(JSON.parse(attachTagCall?.body ?? "{}")).toEqual({ tag_id: 4 });
});

test("uses CRM tag settings, taxonomy, generated suggestions, and review routes", async () => {
  const calls: Array<{ body: string | null; method: string; url: string }> = [];

  await getTagGroups({ fetchImpl: jsonFetch({ contract_version: "crm-tags-v1", items: [] }, calls) });
  await createTagGroup(
    { name: "Role", slug: "role" },
    { fetchImpl: jsonFetch({ id: 1, name: "Role", slug: "role" }, calls) },
  );
  await patchTagGroup(1, { auto_apply_policy: "supervised" }, { fetchImpl: jsonFetch({ id: 1 }, calls) });
  await archiveTagGroup(1, { fetchImpl: jsonFetch({ id: 1 }, calls) });
  await restoreTagGroup(1, { fetchImpl: jsonFetch({ id: 1 }, calls) });
  await patchTag(4, { auto_apply_eligible: true }, { fetchImpl: jsonFetch({ id: 4 }, calls) });
  await archiveTag(4, { fetchImpl: jsonFetch({ id: 4 }, calls) });
  await restoreTag(4, { fetchImpl: jsonFetch({ id: 4 }, calls) });
  await getTaggingSettings({
    fetchImpl: jsonFetch(
      {
        allowed_group_slugs: [],
        allow_contact_auto_tagging: "off",
        confidence_threshold: 0.85,
        contract_version: "crm-tags-v1",
        max_batch_size: 50,
      },
      calls,
    ),
  });
  await patchTaggingSettings(
    {
      allowed_group_slugs: ["role"],
      allow_contact_auto_tagging: "review_batches",
      confidence_threshold: 0.8,
      max_batch_size: 25,
    },
    { fetchImpl: jsonFetch({ contract_version: "crm-tags-v1" }, calls) },
  );
  await generateTagSuggestions(
    { contact_ids: [42], mode: "review_batches", relationship_tiers: ["confirmed"] },
    { fetchImpl: jsonFetch({ contract_version: "crm-tags-v1", run_id: "tagrun_1" }, calls) },
  );
  await getTagSuggestions(
    { confidenceBand: "high", contactId: 42, limit: 20, reasonCode: "role_metadata", status: "suggested" },
    { fetchImpl: jsonFetch({ contract_version: "crm-tags-v1", items: [] }, calls) },
  );
  await rejectTagSuggestion(9, { fetchImpl: jsonFetch({ contract_version: "crm-tags-v1", suggestion: { id: 9 } }, calls) });
  await bulkTagSuggestions(
    { action: "reject", suggestion_ids: [9] },
    { fetchImpl: jsonFetch({ contract_version: "crm-tags-v1", error_count: 0, ok_count: 1, results: [] }, calls) },
  );
  await getTaggingEval({ fetchImpl: jsonFetch({ contract_version: "crm-tags-v1" }, calls) });

  expect(calls.map((call) => [new URL(call.url).pathname, call.method])).toEqual([
    ["/api/tags/groups", "GET"],
    ["/api/tags/groups", "POST"],
    ["/api/tags/groups/1", "PATCH"],
    ["/api/tags/groups/1/archive", "POST"],
    ["/api/tags/groups/1/restore", "POST"],
    ["/api/tags/4", "PATCH"],
    ["/api/tags/4/archive", "POST"],
    ["/api/tags/4/restore", "POST"],
    ["/api/tags/settings", "GET"],
    ["/api/tags/settings", "PATCH"],
    ["/api/tags/suggestion-runs/generate", "POST"],
    ["/api/tags/suggestions", "GET"],
    ["/api/tags/suggestions/9/reject", "POST"],
    ["/api/tags/suggestions/bulk", "POST"],
    ["/api/tags/eval", "GET"],
  ]);
  expect(JSON.parse(calls[9].body ?? "{}")).toEqual({
    allowed_group_slugs: ["role"],
    allow_contact_auto_tagging: "review_batches",
    confidence_threshold: 0.8,
    max_batch_size: 25,
  });
  expect(JSON.parse(calls[10].body ?? "{}")).toEqual({
    contact_ids: [42],
    mode: "review_batches",
    relationship_tiers: ["confirmed"],
  });
  const suggestionsUrl = new URL(calls[11].url);
  expect(suggestionsUrl.searchParams.get("confidence_band")).toBe("high");
  expect(suggestionsUrl.searchParams.get("reason_code")).toBe("role_metadata");
  expect(JSON.parse(calls[12].body ?? "{}")).toEqual({ reason_code: "user_rejected" });
  expect(JSON.parse(calls[13].body ?? "{}")).toEqual({
    action: "reject",
    suggestion_ids: [9],
  });
});
