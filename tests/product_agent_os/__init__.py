from pathlib import Path


# unittest discovery with "-s tests" imports this directory as top-level
# product_agent_os, which would otherwise shadow the plugin runtime package.
# Keep the compatibility shim test-only by extending this package search path.
_ROOT = Path(__file__).resolve().parents[2]
_RUNTIME_PACKAGE = _ROOT / "plugins" / "product-agent-os" / "scripts" / "product_agent_os"

if _RUNTIME_PACKAGE.is_dir():
    __path__.append(str(_RUNTIME_PACKAGE))
