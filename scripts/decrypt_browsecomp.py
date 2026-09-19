"""BrowseComp 원본(canary XOR 암호화 CSV) → data/browsecomp/raw.jsonl.

OpenAI simple-evals가 쓰는 방식 그대로다. canary 문자열의 SHA256을 길이에 맞게
반복해 키로 삼고, base64 디코드한 본문과 XOR 한다.
"""

import base64
import csv
import hashlib
import json
import sys
from pathlib import Path

csv.field_size_limit(10**7)


def derive_key(password: str, length: int) -> bytes:
    key = hashlib.sha256(password.encode()).digest()
    return key * (length // len(key)) + key[: length % len(key)]


def decrypt(ciphertext_b64: str, password: str) -> str:
    encrypted = base64.b64decode(ciphertext_b64)
    key = derive_key(password, len(encrypted))
    return bytes(a ^ b for a, b in zip(encrypted, key)).decode()


def main(src: str, dst: str) -> int:
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    out = Path(dst)
    out.parent.mkdir(parents=True, exist_ok=True)

    records, skipped = [], 0
    for index, row in enumerate(rows):
        canary = row["canary"]
        try:
            question = decrypt(row["problem"], canary).strip()
            answer = decrypt(row["answer"], canary).strip()
        except Exception as exc:  # 복호화 실패는 조용히 넘기지 않는다
            print(f"[{index}] 복호화 실패: {exc}", file=sys.stderr)
            skipped += 1
            continue
        if not question or not answer:
            skipped += 1
            continue
        records.append(
            {
                "index": index,
                "question": question,
                "answer": answer,
                "category": (row.get("problem_topic") or "").strip(),
            }
        )

    with out.open("w", encoding="utf-8", newline="\n") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    lengths = sorted(len(r["answer"]) for r in records)
    print(f"{len(records)}행 기록 (건너뜀 {skipped}) → {out}")
    print(f"정답 길이 중앙값 {lengths[len(lengths) // 2]}자 / 최대 {lengths[-1]}자")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
