# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Enum__S3__Handler
# How each request was handled — carried in every call-log entry.
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__S3__Handler(str, Enum):
    LOCAL    = 'local'
    PROXY    = 'proxy'
    NOT_IMPL = 'not-impl'
