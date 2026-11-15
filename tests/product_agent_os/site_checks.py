"""Explicit built-site checks; not part of runtime unittest discovery."""
from tests.product_agent_os.docs_test_support import *

class ProductAgentOsSiteTest(DocsAssertions, unittest.TestCase):
    def test_batch38_p2_readme_registry_and_control_plane_sync_are_current(self):
        rendered_registry = "\n".join(
            [
                (SITE / "sources" / "registry.html").read_text(encoding="utf-8"),
                (SITE / "en" / "sources" / "registry.html").read_text(encoding="utf-8"),
                (SITE / "search" / "search_index.json").read_text(encoding="utf-8"),
            ]
        )
        for expected in [
            "B38-DOC-M04..M10",
            "final docs verification",
            "generated",
            "refresh decision",
        ]:
            with self.subTest(rendered_site=expected):
                self.assertIn(expected, rendered_registry)

    def test_track10_task26_batch34d_product_docs_qa_and_closure_is_recorded(self):
        for expected in [
            SITE / "index.html",
            SITE / "en" / "index.html",
            SITE / "product-agent-os" / "index.html",
            SITE / "en" / "product-agent-os" / "index.html",
        ]:
            with self.subTest(rendered_site=expected):
                self.assertTrue(expected.exists(), expected)

        rendered_html = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                SITE / "index.html",
                SITE / "en" / "index.html",
                SITE / "product-agent-os" / "index.html",
                SITE / "en" / "product-agent-os" / "index.html",
            ]
        )
        for expected in [
            "md-select",
            'hreflang="ru"',
            'hreflang="en"',
            "/en/",
        ]:
            with self.subTest(static_html_language_switcher_evidence=expected):
                self.assertIn(expected, rendered_html)

    def test_track10_task26_local_file_language_switcher_is_file_safe(self):
        config = MKDOCS.read_text(encoding="utf-8")
        script = LOCAL_FILE_I18N_JS.read_text(encoding="utf-8")

        self.assertIn("assets/javascripts/local-file-i18n.js", config)
        for expected in [
            'window.location.protocol !== "file:"',
            'a[href="/en/"], link[href="/en/"]',
            'a[href="/"], link[href="/"]',
            "assets/javascripts/local-file-i18n.js",
            "en/index.html",
        ]:
            with self.subTest(local_file_i18n_guard=expected):
                self.assertIn(expected, script)

        pages_with_absolute_en = []
        for path in SITE.rglob("*.html"):
            html = path.read_text(encoding="utf-8")
            if 'href="/en/"' in html:
                pages_with_absolute_en.append(path)
                with self.subTest(local_file_guard_loaded=path.relative_to(ROOT).as_posix()):
                    self.assertIn("assets/javascripts/local-file-i18n.js", html)

        self.assertEqual(
            [],
            [path.relative_to(SITE).as_posix() for path in pages_with_absolute_en],
            "full-site i18n parity should not leave RU pages with absolute /en/ fallback links",
        )
        self.assertTrue((SITE / "en" / "index.html").exists())

    def test_track10_task26_batch34e_m46_language_switcher_parity_is_recorded(self):
        source_pages = self._localized_markdown_pages()
        self.assertEqual([], self._missing_localized_en_siblings())

        missing_rendered = []
        pair_failures = []
        file_escape_failures = []
        site_root = SITE.resolve()
        site_pages = self._site_promoted_localized_markdown_pages()
        for source_path in site_pages:
            ru_html = self._rendered_site_path_for_source(source_path)
            en_html = self._rendered_site_path_for_source(source_path, locale="en")
            expected = {
                "ru": ru_html.resolve(),
                "en": en_html.resolve(),
            }

            for rendered in [ru_html, en_html]:
                if not rendered.exists():
                    missing_rendered.append(rendered.relative_to(SITE).as_posix())

            if missing_rendered:
                continue

            pages = {
                "ru": (ru_html, self._language_switcher_hrefs(ru_html.read_text(encoding="utf-8"))),
                "en": (en_html, self._language_switcher_hrefs(en_html.read_text(encoding="utf-8"))),
            }
            for page_locale, (html_path, links) in pages.items():
                for target_locale, expected_path in expected.items():
                    hrefs = links.get(target_locale, [])
                    if not hrefs:
                        pair_failures.append(
                            f"{html_path.relative_to(SITE).as_posix()}: missing {target_locale}"
                        )
                        continue

                    resolved_hrefs = []
                    for href in hrefs:
                        resolved = self._resolve_site_href(html_path, href)
                        if resolved is None:
                            file_escape_failures.append(
                                f"{html_path.relative_to(SITE).as_posix()}: {target_locale} -> {href}"
                            )
                            continue
                        try:
                            resolved.relative_to(site_root)
                        except ValueError:
                            file_escape_failures.append(
                                f"{html_path.relative_to(SITE).as_posix()}: {target_locale} -> {href}"
                            )
                            continue
                        resolved_hrefs.append(resolved)

                    if expected_path not in resolved_hrefs:
                        pair_failures.append(
                            f"{html_path.relative_to(SITE).as_posix()}: "
                            f"{page_locale}->{target_locale} expected "
                            f"{expected_path.relative_to(SITE).as_posix()}"
                        )

        self.assertEqual([], missing_rendered[:20])
        self.assertEqual([], pair_failures[:20])
        self.assertEqual([], file_escape_failures[:20])

    def test_track10_task26_batch34e_m47_search_sitemap_parity_is_recorded(self):
        source_pages = self._localized_markdown_pages()
        self.assertEqual([], self._missing_localized_en_siblings())

        site_pages = self._site_promoted_localized_markdown_pages()
        expected_ru = {
            source_path.relative_to(DOCS).with_suffix(".html").as_posix()
            for source_path in site_pages
        }
        expected_en = {
            "en/" + source_path.relative_to(DOCS).with_suffix(".html").as_posix()
            for source_path in site_pages
        }

        search_index = SITE / "search" / "search_index.json"
        sitemap = SITE / "sitemap.xml"
        self.assertTrue(search_index.exists())
        self.assertTrue(sitemap.exists())

        search_locations = {
            doc.get("location", "").split("#", 1)[0]
            for doc in json.loads(search_index.read_text(encoding="utf-8")).get("docs", [])
        }
        sitemap_locations = set(
            match.split("#", 1)[0]
            for match in re.findall(
                r"<loc>(.*?)</loc>",
                sitemap.read_text(encoding="utf-8"),
            )
        )

        missing_search_ru = sorted(expected_ru - search_locations)
        missing_search_en = sorted(expected_en - search_locations)
        missing_sitemap_ru = sorted(expected_ru - sitemap_locations)
        missing_sitemap_en = sorted(expected_en - sitemap_locations)

        self.assertEqual([], missing_search_ru[:20])
        self.assertEqual([], missing_search_en[:20])
        self.assertEqual([], missing_sitemap_ru[:20])
        self.assertEqual([], missing_sitemap_en[:20])

    def test_track10_task26_batch34e_full_site_parity_red_gate(self):
        ru_pages = self._localized_markdown_pages()
        missing_siblings = [
            path.relative_to(DOCS).as_posix()
            for path in ru_pages
            if not self._en_sibling_for(path).exists()
        ]
        self.assertEqual([], missing_siblings)
        self.assertEqual(
            [],
            [
                self._en_sibling_for(path).relative_to(DOCS).as_posix()
                for path in self._english_original_markdown_pages()
                if self._en_sibling_for(path).exists()
            ],
        )

        cyrillic_en_pages = []
        for path in DOCS.rglob("*.en.md"):
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"[\u0400-\u04FF]", text):
                cyrillic_en_pages.append(path.relative_to(DOCS).as_posix())
        self.assertEqual([], cyrillic_en_pages)

        site_pages = self._site_promoted_localized_markdown_pages()
        missing_rendered_en = []
        for path in site_pages:
            rel = path.relative_to(DOCS).with_suffix(".html")
            rendered = SITE / "en" / rel
            if rel.name == "index.html":
                rendered = SITE / "en" / rel.parent / "index.html"
            if not rendered.exists():
                missing_rendered_en.append(rendered.relative_to(SITE).as_posix())
        self.assertEqual([], missing_rendered_en)

    def test_documentation_refresh_doc_m25_site_freshness_is_recorded(self):
        expected_ru = {
            source_path.relative_to(DOCS).with_suffix(".html").as_posix()
            for source_path in DOC_M25_HISTORICAL_PENDING_SITE_PAGES
        }
        expected_en = {"en/" + path for path in expected_ru}
        search_index = SITE / "search" / "search_index.json"
        sitemap = SITE / "sitemap.xml"
        self.assertTrue(search_index.exists())
        self.assertTrue(sitemap.exists())

        search_locations = {
            doc.get("location", "").split("#", 1)[0]
            for doc in json.loads(search_index.read_text(encoding="utf-8")).get("docs", [])
        }
        sitemap_locations = set(
            match.split("#", 1)[0]
            for match in re.findall(r"<loc>(.*?)</loc>", sitemap.read_text(encoding="utf-8"))
        )
        for source_path in DOC_M25_HISTORICAL_PENDING_SITE_PAGES:
            with self.subTest(rendered=source_path.relative_to(DOCS).as_posix()):
                self.assertTrue(self._rendered_site_path_for_source(source_path).exists())
                self.assertTrue(self._rendered_site_path_for_source(source_path, locale="en").exists())

        self.assertEqual([], sorted(expected_ru - search_locations))
        self.assertEqual([], sorted(expected_en - search_locations))
        self.assertEqual([], sorted(expected_ru - sitemap_locations))
        self.assertEqual([], sorted(expected_en - sitemap_locations))

