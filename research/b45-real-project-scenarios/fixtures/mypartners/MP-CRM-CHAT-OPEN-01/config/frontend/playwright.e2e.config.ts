import { defineConfig } from "@playwright/test";
import path from "node:path";

const port = Number(process.env.FRONTEND_E2E_PORT ?? 3100);
const baseURL = process.env.FRONTEND_BASE_URL ?? `http://127.0.0.1:${port}`;
const outputDir =
  process.env.PLAYWRIGHT_OUTPUT_DIR ??
  path.resolve(process.cwd(), "..", ".codex-tmp", "frontend-e2e-results");

export default defineConfig({
  testDir: "./tests/e2e",
  outputDir,
  timeout: 60_000,
  workers: 1,
  reporter: "line",
  use: {
    baseURL,
    trace: "retain-on-failure",
  },
});
