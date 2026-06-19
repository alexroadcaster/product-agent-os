const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");

const { chromium } = require("playwright");

const workspace = process.argv[2];
const artifactPath = process.argv[3];
const outputDir = process.argv[4];

if (!workspace || !artifactPath || !outputDir) {
  console.error("usage: node m40_playwright_probe.js <workspace> <artifactPath> <outputDir>");
  process.exit(2);
}

fs.mkdirSync(outputDir, { recursive: true });

async function launchBrowser() {
  const attempts = [
    { name: "bundled-chromium", options: { headless: true } },
    { name: "msedge-channel", options: { channel: "msedge", headless: true } },
    { name: "chrome-channel", options: { channel: "chrome", headless: true } },
  ];
  const failures = [];
  for (const attempt of attempts) {
    try {
      const browser = await chromium.launch(attempt.options);
      return { browser, launchMode: attempt.name, failures };
    } catch (error) {
      failures.push({ launchMode: attempt.name, message: String(error.message || error) });
    }
  }
  throw new Error(JSON.stringify({ status: "browser_launch_failed", failures }, null, 2));
}

function rel(filePath) {
  return path.relative(workspace, filePath).replaceAll(path.sep, "/");
}

function extractLocalRequests(requests) {
  return requests.map((request) => ({
    url: request.url().startsWith("file://") ? "file://local-artifact" : request.url(),
    method: request.method(),
    resourceType: request.resourceType(),
  }));
}

(async () => {
  const startedAt = new Date().toISOString();
  const url = pathToFileURL(path.resolve(artifactPath)).href;
  const { browser, launchMode, failures } = await launchBrowser();
  const context = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const page = await context.newPage();
  const consoleMessages = [];
  const pageErrors = [];
  const requests = [];
  const failedRequests = [];

  page.on("console", (message) => {
    consoleMessages.push({ type: message.type(), text: message.text().slice(0, 300) });
  });
  page.on("pageerror", (error) => pageErrors.push(String(error.message || error).slice(0, 500)));
  page.on("request", (request) => requests.push(request));
  page.on("requestfailed", (request) => {
    failedRequests.push({
      url: request.url().startsWith("file://") ? "file://local-artifact" : request.url(),
      method: request.method(),
      resourceType: request.resourceType(),
      failure: request.failure() ? request.failure().errorText : "unknown",
    });
  });

  await page.goto(url, { waitUntil: "load" });
  await page.screenshot({ path: path.join(outputDir, "desktop-overview.png"), fullPage: true });

  await page.locator("#cockpit-search").fill("runtime");
  await page.locator("#section-status-filter").selectOption("approval_required");
  await page.locator("a[href='#page-project-map']").click();
  await page.locator("#cockpit-diagnostics details").first().evaluate((element) => {
    element.open = true;
  });
  await page.screenshot({ path: path.join(outputDir, "desktop-interaction.png"), fullPage: true });

  await page.setViewportSize({ width: 390, height: 844 });
  await page.locator("a[href='#page-docs-sources']").click();
  await page.screenshot({ path: path.join(outputDir, "mobile-source-map.png"), fullPage: true });

  const runtime = await page.evaluate(() => {
    const allControls = [...document.querySelectorAll("input, select, button, a, summary")];
    const namedControls = allControls.filter((element) => {
      const id = element.getAttribute("id");
      const label = id ? document.querySelector(`label[for="${CSS.escape(id)}"]`) : null;
      return Boolean(
        label ||
          element.getAttribute("aria-label") ||
          element.textContent.trim() ||
          element.getAttribute("title"),
      );
    });
    const headings = [...document.querySelectorAll("h1,h2,h3,h4")].map((element) => ({
      tag: element.tagName.toLowerCase(),
      text: element.textContent.trim().slice(0, 80),
    }));
    const graphSurface = document.querySelector("[data-graph-kind='source-file-graph']");
    const codeGraphSurface = document.querySelector("[data-graph-kind='code-graph']");
    const canvas = document.querySelector("canvas");
    let webglAvailable = false;
    if (canvas) {
      webglAvailable = Boolean(canvas.getContext("webgl2") || canvas.getContext("webgl"));
    }
    return {
      title: document.title,
      lang: document.documentElement.lang,
      bodyTextLength: document.body.innerText.length,
      h1: document.querySelector("h1")?.textContent.trim() || "",
      mainPresent: Boolean(document.querySelector("main#main-content")),
      generatedViewOnlyLabelPresent: document.body.innerText.toLowerCase().includes("generated-view-only"),
      navLinkCount: document.querySelectorAll(".cockpit-nav a").length,
      searchValue: document.querySelector("#cockpit-search")?.value || "",
      selectedSectionStatus: document.querySelector("#section-status-filter")?.value || "",
      diagnosticDetailsOpen: Boolean(document.querySelector("#cockpit-diagnostics details")?.open),
      sourceGraphSvgPresent: Boolean(document.querySelector("#source-file-graph-canvas svg, svg#source-file-graph-canvas")),
      codeGraphEmptyStatePresent: Boolean(document.querySelector("#code-graph-canvas.empty-graph")),
      sourceGraphAdapterStatus: graphSurface?.getAttribute("data-adapter-status") || "",
      codeGraphAdapterStatus: codeGraphSurface?.getAttribute("data-adapter-status") || "",
      scriptCount: document.scripts.length,
      externalLinkCount: [...document.querySelectorAll("a[href^='http://'],a[href^='https://']")].length,
      imageCount: document.images.length,
      canvasCount: document.querySelectorAll("canvas").length,
      svgCount: document.querySelectorAll("svg").length,
      webglCanvasAvailable: webglAvailable,
      controlsTotal: allControls.length,
      controlsWithAccessibleName: namedControls.length,
      missingAccessibleNameCount: allControls.length - namedControls.length,
      ariaLabelCount: document.querySelectorAll("[aria-label]").length,
      labelsForControls: document.querySelectorAll("label[for]").length,
      skipLinkPresent: Boolean(document.querySelector("a.skip-link[href='#main-content']")),
      headings,
      currentHash: window.location.hash,
    };
  });

  await browser.close();

  const finishedAt = new Date().toISOString();
  const result = {
    schema_version: "batch41_s7_m40_playwright_probe_v1",
    status: "completed",
    started_at: startedAt,
    finished_at: finishedAt,
    launch_mode: launchMode,
    launch_failures_before_success: failures,
    artifact: rel(path.resolve(artifactPath)),
    screenshots: [
      rel(path.join(outputDir, "desktop-overview.png")),
      rel(path.join(outputDir, "desktop-interaction.png")),
      rel(path.join(outputDir, "mobile-source-map.png")),
    ],
    runtime_interaction: {
      status: "passed_static_runtime_interaction",
      search_value: runtime.searchValue,
      selected_section_status: runtime.selectedSectionStatus,
      diagnostic_details_open: runtime.diagnosticDetailsOpen,
      current_hash: runtime.currentHash,
    },
    browser_visual_proof: {
      status: "passed_screenshots_captured",
      desktop_full_page: true,
      mobile_full_page: true,
    },
    console_network: {
      status: consoleMessages.length === 0 && pageErrors.length === 0 && failedRequests.length === 0 ? "passed_clean" : "needs_review",
      console_messages: consoleMessages,
      page_errors: pageErrors,
      request_count: requests.length,
      requests: extractLocalRequests(requests),
      failed_requests: failedRequests,
    },
    wcag_oriented_checks: {
      status: runtime.missingAccessibleNameCount === 0 && runtime.lang && runtime.mainPresent ? "passed_static_browser_checks" : "needs_review",
      lang: runtime.lang,
      main_present: runtime.mainPresent,
      skip_link_present: runtime.skipLinkPresent,
      controls_total: runtime.controlsTotal,
      controls_with_accessible_name: runtime.controlsWithAccessibleName,
      missing_accessible_name_count: runtime.missingAccessibleNameCount,
      aria_label_count: runtime.ariaLabelCount,
      labels_for_controls: runtime.labelsForControls,
      heading_count: runtime.headings.length,
      headings: runtime.headings,
      certification_claim: "not_claimed",
    },
    cosmos_gl_runtime_webgl: {
      status: runtime.canvasCount > 0 && runtime.webglCanvasAvailable ? "passed_webgl_canvas_available" : "blocked_static_fallback_no_vendored_runtime",
      context7_basis: "Cosmos.gl runtime proof expects Graph(container), Float32Array point/link data, render(), graph.ready/isReady, and a WebGL/canvas outcome.",
      source_graph_adapter_status: runtime.sourceGraphAdapterStatus,
      code_graph_adapter_status: runtime.codeGraphAdapterStatus,
      canvas_count: runtime.canvasCount,
      svg_count: runtime.svgCount,
      webgl_canvas_available: runtime.webglCanvasAvailable,
      static_svg_fallback_present: runtime.sourceGraphSvgPresent,
      code_graph_empty_state_present: runtime.codeGraphEmptyStatePresent,
    },
    offline_privacy: {
      script_count: runtime.scriptCount,
      external_link_count: runtime.externalLinkCount,
      image_count: runtime.imageCount,
      generated_view_only_label_present: runtime.generatedViewOnlyLabelPresent,
    },
  };

  fs.writeFileSync(path.join(outputDir, "playwright-runtime-proof.json"), JSON.stringify(result, null, 2) + "\n", "utf8");
  console.log(JSON.stringify(result, null, 2));
})().catch((error) => {
  const failure = {
    schema_version: "batch41_s7_m40_playwright_probe_v1",
    status: "blocked",
    error: String(error.message || error),
  };
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(path.join(outputDir, "playwright-runtime-proof.json"), JSON.stringify(failure, null, 2) + "\n", "utf8");
  console.error(JSON.stringify(failure, null, 2));
  process.exit(1);
});
