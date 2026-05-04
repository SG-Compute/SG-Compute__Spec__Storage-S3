# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Enum__S3_Server__Backend
# Storage backend choices. MEMORY is the Phase 1 default.
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__S3_Server__Backend(str, Enum):
    MEMORY  = 'memory'
    DISK    = 'disk'
    VAULT   = 'vault'
    REAL_S3 = 'real-s3'
