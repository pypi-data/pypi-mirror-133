"""
libqc
~~~~
Statistical tools for genomic library QC.
"""

import gzip
import re
from pathlib import Path
from typing import List

from .counts import Counts
from .library import Brunello, GuideLibrary


def make_counts(
    fastqs: List[Path],
    regex: re.Pattern,
    library: GuideLibrary = Brunello(),
    output_path: Path = None,
) -> Path:
    """Constructs a file enumerating counts for constructs in a chosen library."""

    counts = Counts(library, regex)

    for fastq in fastqs:
        if fastq.suffix == ".gz":
            f = gzip.open(fastq, "rt")
        else:
            f = open(fastq, "r")

        i = 0
        j = 0
        for line in f.readlines():
            if i == 1:
                counts.process(line)
            if i == 3:
                i = 0
                continue
            i += 1
            if j % 1000 == 0:
                print(f"Processed {j} reads.")
            j += 1

    counts.to_csv()
