# インターフェース契約（v0.2）

**正本パス（Contabo VPS 確定案）**

```
/var/lib/orca-control/work/aoi-content-intake/
  material-ledger/
    materials.jsonl          # append-only、台帳正本
    materials.snapshot.json  # 日次 compact（任意）
  corpus/
    {snapshot_id}/
      manifest.json
      items.jsonl
      fsa-axes.json
      internal-scores.jsonl  # mode 600
  builds/{edition_date}/
    manifest-build.json
    edition/
      review-candidate.json
      dryrun.json
      writer-report.json
    context-deltas/
      {axis_slug}.proposal.json   # 0 or 1 file per axis per day
    reservations/
      note-urls.json              # Note が確定した URL（任意）
```

**DailyNews 読み取り**

```
/var/lib/orca-control/work/dailynews-pipeline/state/{date}/
  ← corpus symlink or copy: 最新 snapshot_id を manifest で参照
```

**News 公開手渡し（切替後）**

```
/home/shugo/.hermes/work/aoifuture-news-aoi002/publisher/inbox/review-candidate.json
  ← scp/rsync from builds/{date}/edition/  (Mac sync 廃止後)
```

---

## 環境変数（collect / worker）

| 変数 | 用途 |
|------|------|
| `AOI_CORPUS_ROOT` | 上記 `corpus/` |
| `AOI_LEDGER_ROOT` | `material-ledger/` |
| `FSA_READ_TOKEN_FILE` | 既定 `~/.config/future-search/reader-token` |
| `FSA_API_BASE` | DailyNews と同じ tailscale URL |
| `FRESHRSS_GREADER_*` | dailynews-pipeline 既存 |
| `AOI_NEWS_POLICY` | `aoi002-news-standing-policy.v1.json` path |
| `AOI_NEWS_POLICY_SHA256` | 5bcbc0d4d069f4c8dd59e50d2e83ed872f03c1e42cfbd3017c1d8960041d5e04 |

---

## スキーマ参照

| ファイル | 用途 |
|----------|------|
| `schemas/material.v0.schema.json` | 台帳 1 行 |
| `schemas/corpus-manifest.v0.schema.json` | collect 完了 |
| `schemas/corpus-item.v0.schema.json` | `items.jsonl` 1 行 |
| `schemas/context-delta-proposal.v0.schema.json` | Context 追記提案 |

---

## 冪等性

- `snapshot_id` は collect 開始時に固定。再実行は **同一日の上書き禁止**（`manifest.status=complete` なら exit 0 skip）。
- 台帳: 同一 `url` は **マージ**（`used_in` 追記、`snapshot_ids` union）。
- `review-candidate.json` 配置: inbox へは **candidate_sha256 変化時のみ** push（sync fail-closed 互換）。