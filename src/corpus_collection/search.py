"""
Logic για search και filtering papers από το arXiv.
"""
import arxiv
from typing import Iterator
from . import config


# Module-level: ένας client για όλο το module
_client = arxiv.Client(
    page_size=100,
    delay_seconds=3.0,
    num_retries=3,
)

def search_arxiv(query: str, max_results: int):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    return _client.results(search)


def passes_category_filter(result: arxiv.Result) -> bool:
    """
    Ελέγχει αν το paper περνάει το category filter.
    Αν ΕΣΤΩ ΜΙΑ από τις κατηγορίες είναι στο blacklist, πετάμε το paper.
    """
    paper_categories = set(result.categories)
    blacklisted = paper_categories & config.CATEGORY_BLACKLIST
    return len(blacklisted) == 0


def passes_keyword_filter(result: arxiv.Result) -> bool:
    """
    Ελέγχει αν το abstract περιέχει τουλάχιστον μία basketball-specific
    λέξη-κλειδί (case-insensitive).
    """
    abstract_lower = result.summary.lower()
    return any(kw in abstract_lower for kw in config.ABSTRACT_KEYWORDS)


def is_relevant(result: arxiv.Result) -> tuple[bool, str]:
    """
    Συνολικός έλεγχος relevance. Επιστρέφει (passes, reason).
    Αν δεν περνάει, το reason εξηγεί γιατί (για logging/debugging).
    """
    if not passes_category_filter(result):
        blacklisted = set(result.categories) & config.CATEGORY_BLACKLIST
        return False, f"blacklisted category: {blacklisted}"
    
    if not passes_keyword_filter(result):
        return False, "no basketball keyword in abstract"
    
    return True, "ok"


def get_arxiv_id(result: arxiv.Result) -> str:
    """
    Εξάγει το arXiv ID από το entry_id URL.
    π.χ. 'http://arxiv.org/abs/2401.12345v1' -> '2401.12345v1'
    """
    return result.entry_id.split("/")[-1]