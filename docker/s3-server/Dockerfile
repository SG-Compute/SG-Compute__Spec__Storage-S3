# ═══════════════════════════════════════════════════════════════════════════════
# SG S3 Server — Docker image stub
# Phase 1: installs sg_s3_server from source (not yet on PyPI).
# TODO: replace COPY . . / pip install . with PyPI install once sg_s3_server is published.
# ═══════════════════════════════════════════════════════════════════════════════

FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO: replace with: RUN pip install sg-s3-server  (once published to PyPI)
COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 9000

CMD ["uvicorn", "sg_s3_server.app.Fast_API__S3_Server:app", "--host", "0.0.0.0", "--port", "9000"]
