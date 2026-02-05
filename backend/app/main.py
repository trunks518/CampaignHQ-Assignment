# from __future__ import annotations

# import csv
# import io
# from datetime import datetime
# from typing import Any, Dict, List, Set, Tuple

# from fastapi import FastAPI, File, HTTPException, UploadFile
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware


# app = FastAPI(title="Exercise API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# ALLOWED_STATUSES = {"success", "fail", "unknown"}


# def _is_iso8601(ts: str) -> bool:
#     s = ts.strip()
#     if not s:
#         return False
#     try:
#         if s.endswith("Z"):
#             s = s[:-1] + "+00:00"
#         datetime.fromisoformat(s)
#         return True
#     except Exception:
#         return False


# @app.post("/api/results/upload")
# async def upload_results(file: UploadFile = File(...)) -> JSONResponse:
#     # Prepare CSV reader with streaming text decode
#     await file.seek(0)
#     text_stream = io.TextIOWrapper(file.file, encoding="utf-8", newline="")
#     reader = csv.DictReader(text_stream)

#     if not reader.fieldnames:
#         raise HTTPException(status_code=400, detail="CSV has no header row")

#     headers = {
#         h.strip().lower() for h in reader.fieldnames if isinstance(h, str)
#     }
#     required = {"id", "status", "ts", "notes"}
#     if not required.issubset(headers):
#         missing = sorted(required - headers)
#         raise HTTPException(
#             status_code=400, detail=f"Missing headers: {', '.join(missing)}"
#         )

#     total_rows = 0
#     valid_rows = 0
#     errors: List[Dict[str, Any]] = []
#     seen: Set[Tuple[str, str]] = set()
#     by_status: Dict[str, int] = {k: 0 for k in ALLOWED_STATUSES}

#     line_number = 1  # header is line 1
#     for raw_row in reader:
#         line_number += 1
#         total_rows += 1

#         # Normalize keys and values
#         row = {
#             (k.strip().lower() if isinstance(k, str) else k): (
#                 v.strip() if isinstance(v, str) else v
#             )
#             for k, v in raw_row.items()
#         }

#         rid = row.get("id", "")
#         status = (row.get("status", "") or "").lower()
#         ts = row.get("ts", "")

#         if not rid:
#             errors.append({"row": line_number, "reason": "missing id"})
#             continue
#         if status not in ALLOWED_STATUSES:
#             errors.append(
#                 {"row": line_number, "reason": f"invalid status '{status}'"}
#             )
#             continue
#         if not _is_iso8601(ts):
#             errors.append({"row": line_number, "reason": "invalid ts"})
#             continue

#         key = (rid, ts)
#         if key in seen:
#             # Duplicate: ignore subsequent occurrences
#             continue
#         seen.add(key)

#         valid_rows += 1
#         by_status[status] += 1

#     payload = {
#         "total_rows": total_rows,
#         "valid_rows": valid_rows,
#         "errors": errors,
#         "by_status": by_status,
#     }
#     return JSONResponse(content=payload)


from __future__ import annotations

import io
from datetime import datetime
import time
from typing import Any, Dict, List, Set, Tuple
import logging
import pandas as pd

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Exercise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

ALLOWED_STATUSES = {"success", "fail", "unknown"}
CHUNK_SIZE:int = 20_000

def _is_iso8601(ts: str) -> bool:
    s = ts.strip()
    if not s:
        return False
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        datetime.fromisoformat(s)
        return True
    except Exception:
        return False


@app.post("/api/results/upload")
async def upload_results(file: UploadFile = File(...)) -> JSONResponse:
    logger.debug(''' starting upload ''')
    start = time.time()
    
    # Prepare CSV reader with streaming text decode
    await file.seek(0)
    text_stream = io.TextIOWrapper(file.file, encoding="utf-8", newline="")

    check_header:bool = True
    headers: Set[str] = []
    total_rows = 0
    valid_rows = 0
    errors: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str]] = set()
    by_status: Dict[str, int] = {k: 0 for k in ALLOWED_STATUSES}
    line_number = 1  # header is line 1
    
    for chunk in pd.read_csv(text_stream, chunksize=10_000, keep_default_na=False):
        # only need to check it once
        if check_header:
            if len(chunk.columns) == 0:
                raise HTTPException(status_code=400, detail="CSV has no header row")

            headers = {
                h.strip().lower() for h in chunk.columns if isinstance(h, str)
            }
            required = {"id", "status", "ts", "notes"}
            if not required.issubset(headers):
                missing = sorted(required - headers)
                raise HTTPException(
                    status_code=400, detail=f"Missing headers: {', '.join(missing)}"
                )
        
        for raw_row in chunk.itertuples(index=False):
            line_number += 1
            total_rows += 1
    
            # Normalize keys and values
            row = raw_row._asdict()
    
            rid = row.get("id", "")
            status = (row.get("status", "") or "").lower()
            ts = row.get("ts", "")


            if not rid:
                errors.append({"row": line_number, "reason": "missing id"})
                continue
            if status not in ALLOWED_STATUSES:
                errors.append(
                    {"row": line_number, "reason": f"invalid status '{status}'"}
                )
                continue
            if not _is_iso8601(ts):
                errors.append({"row": line_number, "reason": "invalid ts"})
                continue
            
            key = (rid, ts)
            if key in seen:
                # Duplicate: ignore subsequent occurrences
                continue
            seen.add(key)
    
            valid_rows += 1
            by_status[status] += 1

    elapsed_seconds: float = time.time() - start
    payload = {
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "errors": errors,
        "by_status": by_status,
        "runtime": f"{elapsed_seconds:.2f}s"
    }
    return JSONResponse(content=payload)