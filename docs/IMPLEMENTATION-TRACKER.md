# 実装トラッカー

更新: 2026-11-25

---

## Phase 0 — 台帳

| ID | タスク | Repo | 状態 |
|----|--------|------|------|
| P0-1 | `backfill_ledger_from_catalog.py` 本番データで実行 | aoi-content-intake | script あり |
| P0-2 | VPS `materials.jsonl` 初回投入 | ops | 未 |
| P0-3 | duplicate gate を writer で参照 | aoi-news-worker | 未 |

---

## Phase 1 — Collect

| ID | タスク | Repo | 状態 |
|----|--------|------|------|
| P1-1 | `collect` を corpus 出力に接続 | dailynews-pipeline | 未 |
| P1-2 | `fsa-axis-match-v1.yaml` | aoi-content-intake | 未 |
| P1-3 | INTERFACES パス作成 on VPS | orca-fleet | 未 |

---

## Phase 2 — DailyNews 入力切替

| ID | タスク | Repo | 状態 |
|----|--------|------|------|
| P2-1 | generate が corpus 読み | dailynews-pipeline | 未 |
| P2-2 | `note-urls.json` 出力 | dailynews-pipeline | 未 |

---

## Phase 3 — News worker

| ID | タスク | Repo | 状態 |
|----|--------|------|------|
| P3-1 | `0xshugo/aoi-news-worker` 作成 | new | 未 |
| P3-2 | fetch + assemble + dry-run | aoi-news-worker | 未 |
| P3-3 | inbox rsync（Mac 置換） | orca-fleet | 未 |
| P3-4 | GB-058 systemd | orca-fleet | 未 |

---

## Phase 4 — Context

| ID | タスク | Repo | 状態 |
|----|--------|------|------|
| P4-1 | 8 軸の空 context JSON（review-only） | aoifuture-web | 未 |
| P4-2 | delta proposal → promoter | agent-platform / web | 未（G4 依存） |

---

## Phase 5 — 切替

| ID | タスク | Repo | 状態 |
|----|--------|------|------|
| P5-1 | S0–S6 試験 | ops | 未 |
| P5-2 | Mac Writer disable | orca-fleet | 未 |
| P5-3 | publisher tick お昼 1 本化 Exact | orca-fleet | 未 |

---

## ブロッカー

| ID | 内容 |
|----|------|
| B1 | promoter context update（E2 G4）未実装時は Context を手動 PR |
| B2 | policy v2 は本 v0 では **触らない**（Edition v1 のまま） |