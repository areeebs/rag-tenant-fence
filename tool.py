from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def audit(document: dict[str, Any]) -> dict[str, Any]:
    docs = document.get("documents")
    queries = document.get("queries")
    if not isinstance(docs, list) or not isinstance(queries, list):
        raise ValueError("Input must contain documents and queries lists.")
    by_id = {item.get("id"): item for item in docs if isinstance(item, dict) and item.get("id")}
    findings: list[dict[str, str]] = []
    checked = 0
    for index, query in enumerate(queries):
        if not isinstance(query, dict):
            findings.append({"severity": "error", "code": "invalid_query", "subject": str(index)})
            continue
        qid = str(query.get("id", index))
        tenant = query.get("tenant_id")
        if not isinstance(tenant, str) or not tenant:
            findings.append({"severity": "error", "code": "missing_query_tenant", "subject": qid})
            continue
        for doc_id in query.get("retrieved_ids", []):
            checked += 1
            doc = by_id.get(doc_id)
            if doc is None:
                findings.append({"severity": "high", "code": "unknown_document", "subject": f"{qid}:{doc_id}"})
                continue
            if not isinstance(doc.get("tenant_id"), str):
                findings.append({"severity": "high", "code": "missing_document_tenant", "subject": f"{qid}:{doc_id}"})
            elif doc["tenant_id"] != tenant:
                findings.append({"severity": "critical", "code": "cross_tenant_result", "subject": f"{qid}:{doc_id}"})
            if not doc.get("source"):
                findings.append({"severity": "medium", "code": "missing_source_provenance", "subject": f"{qid}:{doc_id}"})
    return {"retrieved_documents_checked": checked, "findings": findings,
            "pass": not any(x["severity"] in {"critical", "high", "error"} for x in findings)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit recorded RAG retrieval boundaries; no model or vector store is used.")
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.trace.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Trace must be a JSON object.")
        report = audit(data)
        print(json.dumps(report, indent=2))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
