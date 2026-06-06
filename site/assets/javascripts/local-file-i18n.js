(function () {
  "use strict";

  var scriptSrc = document.currentScript && document.currentScript.src;

  function siteRelativePrefix() {
    if (!scriptSrc || window.location.protocol !== "file:") {
      return null;
    }

    var scriptPath = new URL(scriptSrc).pathname.replace(/\\/g, "/");
    var pagePath = window.location.pathname.replace(/\\/g, "/");
    var marker = "/assets/javascripts/local-file-i18n.js";

    if (!scriptPath.endsWith(marker)) {
      return null;
    }

    var siteRootPath = scriptPath.slice(0, -marker.length);
    var relativePage = pagePath.startsWith(siteRootPath + "/")
      ? pagePath.slice(siteRootPath.length + 1)
      : pagePath.split("/").pop() || "index.html";
    var depth = Math.max(relativePage.split("/").filter(Boolean).length - 1, 0);

    return depth > 0 ? "../".repeat(depth) : "";
  }

  function rewriteLocalFileLanguageLinks() {
    var prefix = siteRelativePrefix();

    if (prefix === null) {
      return;
    }

    document
      .querySelectorAll('a[href="/en/"], link[href="/en/"]')
      .forEach(function (node) {
        node.setAttribute("href", prefix + "en/index.html");
      });

    document
      .querySelectorAll('a[href="/"], link[href="/"]')
      .forEach(function (node) {
        node.setAttribute("href", prefix + "index.html");
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", rewriteLocalFileLanguageLinks);
  } else {
    rewriteLocalFileLanguageLinks();
  }
})();
