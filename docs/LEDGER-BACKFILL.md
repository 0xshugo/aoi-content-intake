# 素材台帳 — バックフィル手順（P0）

---

## 1. ソース（優先順）

| # | ソース | 方法 |
|---|--------|------|
| 1 | `aoifuture-web` `src/content/news/editions/` | git clone → 各 edition の items `source_url` |
| 2 | Mac `used-urls.txt` | 1 行 1 URL、`used_in` なしで first_seen 不明 |
| 3 | grokbot catalog | `~/.hermes/work/.../grokbot/*/catalog/editions/*.json` |
| 4 | DailyNews Drive archive | 将来: 出典行パース（別 script） |

---

## 2. 出力

`material-ledger/materials.jsonl` — 既存行がある場合は **マージ**（`backfill_ledger_from_catalog.py`）。

各レコード:

- `provenance: backfill`
- `used_in[]`: `{ product: news_edition, date: edition_date, artifact_id: edition_id }`

---

## 3. ローカル実行（設計検証）

```bash
cd aoi-content-intake
python3 scripts/backfill_ledger_from_catalog.py \
  --editions-dir /path/to/catalog/editions \
  --used-urls /Users/shugo/.hermes/work/aoifuture-news-aoi002/grokbot/2026-11-19/used-urls.txt \
  --out /tmp/materials-backfill.jsonl
```

成功基準: **>95%** の公開 edition item URL が台帳に存在（手動 spot check 20 件）。

---

## 4. VPS への初回投入

1. backfill jsonl を Contabo に scp  
2. `materials.jsonl` と `cat` マージ（url キーで python マージ）  
3. checksum を `manifest-backfill.json` に記録

**本番 writer はバックフィル完了まで `duplicate_url` gate を厳格運用。**

---

## 5. スクリプト

`scripts/backfill_ledger_from_catalog.py` — 本 repo 同梱（読み取り専用入力）。