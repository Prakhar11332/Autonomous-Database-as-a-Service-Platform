"""
STUB — implement in its own phase per the roadmap.
Keep this router's prefix stable now so main.py and the dashboard
can wire against it before the real logic exists.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/backup", tags=["backup"])


@router.get("/health")
async def health():
    return {"engine": "backup", "status": "not_implemented"}
