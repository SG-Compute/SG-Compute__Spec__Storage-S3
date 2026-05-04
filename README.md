# SG-Compute — Spec: Storage S3

![version](https://img.shields.io/badge/version-v0.1.0-blue)

S3-compatible storage node spec and server for the SG/Compute platform.

## Overview

Two-layer architecture:

- **`sg_compute_specs/s3_server/`** — spec layer: manifest, schemas, service helpers for provisioning EC2 nodes
- **`sg_s3_server/`** — server layer: FastAPI S3-compatible API running inside the node container

## CI

| Branch | Version bump |
|--------|-------------|
| `dev`  | patch (X.Y.Z → X.Y.Z+1) |
| `main` | minor (X.Y.Z → X.Y+1.0) |
