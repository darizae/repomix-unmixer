"""Single-export CLI (`unmix-repomix`).

A thin console-script wrapper around :func:`repomix_unmixer.
extractor.main` so installed distributions expose a stable command while the
parsing/extracting logic stays in one auditable module.
"""

from __future__ import annotations

import sys

from repomix_unmixer.extractor import main

if __name__ == "__main__":
    sys.exit(main())
