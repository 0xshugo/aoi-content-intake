# Collect 仕様 — 共有一次取得

**実装オーナー:** `0xshugo/dailynews-pipeline`（`collect` パッケージ拡張）  
**契約オーナー:** 本 repo

---

## 1. 責務

1. FreshRSS（GReader）— 既存アダプタを正本化  
2. FSA `GET /v1/research-axes` — スナップショット（slug, id, title, data_class）  
3. （任意）signals JSON — 既存 dailynews signals  
4. 正規化 → `items.jsonl` + 台帳 upsert  
5. **軸マッチ v1** — ルールベース（ [FSA-AXIS-MAP.md](FSA-AXIS-MAP.md)）

**禁止:** Note/News 向け本文生成。スコアは `internal-scores.jsonl` のみ。

---

## 2. 処理順

```
start → snapshot_id 発行
  → FreshRSS fetch (fail: manifest.errors[], partial OK if items>0)
  → FSA axes fetch (fail: fsa-axes.json 空 + error)
  → dedupe URL (canonical)
  → for each item: ledger upsert + axis match
  → write manifest status=complete
```

---

## 3. items.jsonl 行（要約）

`corpus-item.v0` — title, url, published_at, observed_at, source_feed, language_hint。

**時間窓:** 既定 72h JST。manifest に `window_hours: 72` を記録。

---

## 4. FreshRSS 失敗時

DailyNews と同様 **BLOCK** ではなく corpus に error を残す。ただし `items.jsonl` が空なら downstream は **BLOCKED**（Note/News 両方）。

---

## 5. dailynews-pipeline との統合

| 段階 | 挙動 |
|------|------|
| P1 | collect 完了後、従来の FreshRSS 直読みを **corpus 読み** に差し替え |
| P2 | signals / FSA hints は corpus `manifest` から読む |

collect モジュールは **Python パッケージ `aoi_intake.collect`** として切り出し、将来 `aoi-news-worker` からも import（repo 間は git submodule または PyPI  private は後決定）。

---

## 6. 受け入れテスト

- 7 日連続 `manifest.status=complete` かつ `freshrss_item_count>100`
- `fsa_axis_count>=8`
- 台帳 `materials.jsonl` が単調増加（同一 url の used_in マージのみ）