import { expect, test } from "@playwright/test";

test("synthetic home page has keyboard-reachable search", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Synthetic Frontend Fixture" })).toBeVisible();
  await page.keyboard.press("Tab");
  await expect(page.getByLabel("Search")).toBeFocused();
});
