"""Share the unchanged packaged-fixture baseline within one unittest process.

Mutation/error tests call isolated runners directly and never populate this cache.
"""

_results = None


def evaluate_all_cached(runner):
    """Evaluate the packaged baseline once across its contract test modules."""
    global _results
    if _results is None:
        _results = runner.evaluate_all()
    return _results
