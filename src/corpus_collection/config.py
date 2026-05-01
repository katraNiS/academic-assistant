"""
Configuration για το corpus collection.
Όλες οι παράμετροι σε ένα μέρος για εύκολη τροποποίηση και reproducibility.
"""
from pathlib import Path

# ============================================================
# Search queries
# ============================================================
SEARCH_QUERIES = [
    # Core analytics/prediction
    'abs:"basketball analytics"',
    'abs:basketball AND abs:"machine learning"',
    'abs:basketball AND abs:prediction',
    
    # Player & game-specific
    'abs:basketball AND abs:player',
    'abs:basketball AND abs:performance',
    
    # Vision/tracking
    'abs:basketball AND abs:tracking',
    'abs:basketball AND abs:"computer vision"',
    
    # Specific topics
    'abs:basketball AND abs:"shot selection"',
    'abs:NBA AND abs:basketball',
    
    # Strategy/tactics
    'abs:basketball AND abs:strategy',
]

# Πόσα αποτελέσματα ζητάμε ανά query (μέγιστο)
MAX_RESULTS_PER_QUERY = 30

# ============================================================
# Filtering
# ============================================================

# Categories που πετάμε αμέσως
CATEGORY_BLACKLIST = {
    "cs.RO",   # Robotics
    "cs.GR",   # Graphics
    "cs.HC",   # Human-Computer Interaction
    "cs.CY",   # Computers and Society
    "cs.CR",   # Cryptography
}

# Λέξεις-κλειδιά που πρέπει να εμφανίζονται στο abstract
# (έστω και μία από αυτές, case-insensitive)
ABSTRACT_KEYWORDS = [
    "basketball",
    "nba",
    "wnba",
    "ncaa basketball",
    "euroleague",
]

# ============================================================
# Paths
# ============================================================

# Root του project (δύο επίπεδα πάνω από αυτό το αρχείο)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Πού αποθηκεύονται τα PDFs
PDF_DIR = PROJECT_ROOT / "corpus" / "pdfs"

# Πού αποθηκεύεται το metadata
METADATA_FILE = PROJECT_ROOT / "corpus" / "metadata.json"

# ============================================================
# Targets
# ============================================================

# Στόχος papers (η εκφώνηση ζητάει 50+)
TARGET_PAPER_COUNT = 50