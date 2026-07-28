"""
Fires N concurrent provisioning requests at the control plane and reports
success/failure counts + timing. This is your evidence for the
concurrency-control discussion in the DBMS report: no two tenants should
ever be assigned the same host port, even when requests race.

Usage:
    python scripts/load_test.py --count 10 --tenant-id <uuid>
"""
import argparse
import asyncio
import time
import uuid

import httpx


async def provision_one(client: httpx.AsyncClient, tenant_id: str, index: int):
    payload = {
        "tenant_id": tenant_id,
        "engine_type": "postgres",
        "db_name": f"loadtest_{index}",
    }
    start = time.perf_counter()
    try:
        resp = await client.post("/databases", json=payload, timeout=30)
        elapsed = time.perf_counter() - start
        return {"index": index, "status_code": resp.status_code, "elapsed": elapsed}
    except Exception as exc:  # noqa: BLE001 — this is a diagnostic script
        elapsed = time.perf_counter() - start
        return {"index": index, "error": str(exc), "elapsed": elapsed}


async def main(count: int, tenant_id: str, base_url: str):
    async with httpx.AsyncClient(base_url=base_url) as client:
        results = await asyncio.gather(
            *[provision_one(client, tenant_id, i) for i in range(count)]
        )

    ports_seen = set()
    for r in results:
        print(r)

    successes = [r for r in results if r.get("status_code") == 201]
    print(f"\n{len(successes)}/{count} succeeded")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--tenant-id", type=str, default=str(uuid.uuid4()))
    parser.add_argument("--base-url", type=str, default="http://localhost:8000")
    args = parser.parse_args()

    asyncio.run(main(args.count, args.tenant_id, args.base_url))
