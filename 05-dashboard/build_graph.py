#!/usr/bin/env python3
"""Agent OS — knowledge graph generator (stdlib only).

02-memory·06-production·루트 마크다운을 스캔해 [[wikilink]]로 그래프를 만든다.
출력 graph.json → hq-dashboard.html 의 Graph 탭이 fetch.

group 규칙: concepts→concept, entities→entity, 06-production→prod,
            index/SCHEMA/log→index, 루트 헌법문서→root, 그 외 02-memory→note.
한계: 파일명(stem)이 같으면(예: 루트 README와 프로젝트 README) 한 노드로 합쳐짐. 대부분 노트는 고유.

usage:
  python3 build_graph.py --root "G:/내 드라이브/Agent OS" --out 05-dashboard/graph.json
"""
import argparse, json, re
from pathlib import Path

LINK_RE = re.compile(r"\[\[([^\]|#]+)")  # [[target]] / [[target|alias]] / [[target#h]]
ROOT_DOCS = {"README","CLAUDE","AGENTS","MY","MY-TELOS","AGENT-OS","OPERATIONS"}

def group_for(rel: str, stem: str) -> str:
    p = rel.replace("\\", "/")
    if "/concepts/" in p: return "concept"
    if "/entities/" in p: return "entity"
    if p.startswith("06-production/"): return "prod"
    if stem in ("index","SCHEMA","log") and "02-memory" in p: return "index"
    if "/" not in p and stem in ROOT_DOCS: return "root"
    if "02-memory" in p: return "note"
    return "note"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="graph.json")
    a = ap.parse_args()
    root = Path(a.root)
    files = []
    for pat in ("02-memory/**/*.md", "06-production/**/*.md", "*.md"):
        files += root.glob(pat)
    nodes, group = {}, {}
    for f in files:
        stem = f.stem
        rel = str(f.relative_to(root)).replace("\\", "/")
        nid = "02-memory/index" if (stem == "index" and "02-memory" in rel) else stem
        nodes[stem] = nid
        group[nid] = group_for(rel, stem)
    links, seen = [], set()
    for f in files:
        src = nodes[f.stem]
        try: text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception: continue
        for m in LINK_RE.findall(text):
            tgt = m.strip().split("/")[-1]
            if tgt in nodes:
                dst = nodes[tgt]
                if dst != src and (src, dst) not in seen and (dst, src) not in seen:
                    seen.add((src, dst)); links.append([src, dst])
    out = {"nodes": [[nid, group[nid]] for nid in sorted(set(group))], "links": links}
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("OK graph.json  nodes=%d  links=%d" % (len(out["nodes"]), len(links)))

if __name__ == "__main__":
    main()
