# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Enum__S3_Server__Stack__State
# EC2 lifecycle states for an S3 server node.
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__S3_Server__Stack__State(Enum):
    PENDING     = 'pending'
    READY       = 'ready'
    TERMINATING = 'terminating'
    TERMINATED  = 'terminated'
    FAILED      = 'failed'
    UNKNOWN     = 'unknown'
