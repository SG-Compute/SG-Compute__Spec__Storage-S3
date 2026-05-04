# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Enum__S3_Server__Mode
# Four operation modes — Phase 1 ships FULL_PROXY only.
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__S3_Server__Mode(str, Enum):
    FULL_LOCAL = 'full-local'
    FULL_PROXY = 'full-proxy'
    HYBRID     = 'hybrid'
    SELECTIVE  = 'selective'
