import statistics
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.audit import AuditLogger
from core.models import AuditRecord


def main() -> None:
    logger = AuditLogger()
    costs = []
    for i in range(200):
        start = time.perf_counter()
        logger.write(AuditRecord(event="bench", query=f"q{i}", purity_score=0.9))
        costs.append((time.perf_counter() - start) * 1000)
    costs.sort()
    print({
        "p50_ms": statistics.median(costs),
        "p95_ms": costs[int(len(costs) * 0.95)],
        "p99_ms": costs[int(len(costs) * 0.99) - 1],
    })


if __name__ == "__main__":
    main()
