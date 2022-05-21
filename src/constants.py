import re
from multiprocessing import cpu_count
from pathlib import Path

EMAIL_REGEX_STR: str = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
EMAIL_REGEX = re.compile(EMAIL_REGEX_STR)
AVAILABLE_CPUS: int = cpu_count()-1
OUT_DIR = Path('../output')
