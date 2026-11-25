# News Worker 仕様

**リポジトリ名（確定案）:** `0xshugo/aoi-news-worker`（未作成・本設計の先行）  
**実行ホスト:** Contabo VPS  
**スケジュール:** [ORCA-SCHEDULE.md](ORCA-SCHEDULE.md) — 目標 **10:30 JST** 開始

---

## 1. 入力

| 入力 | 必須 |
|------|------|
| `corpus/{snapshot_id}/items.jsonl` | yes（朝 collect の `snapshot_id` を `builds/{date}/manifest-build.json` に記録） |
| `material-ledger/materials.jsonl` | yes（重複 URL 排除） |
| `reservations/note-urls.json` | no（Note 確定後に生成） |
| 過去 Edition catalog（git または web export） | yes（source_url 重複チェック・ライター参照） |

**Writer 入力から除去:** `_internal` スコア、FreshRSS メタ。

---

## 2. 出力

### 2.1 Edition

- `builds/{date}/edition/review-candidate.json` — 現行 v1 ラッパー
- `builds/{date}/edition/dryrun.json` — `eligible_dry_run` 必須
- `builds/{date}/edition/writer-report.json` — 非公開メモ

### 2.2 Context（任意・0..8 ファイル）

- `builds/{date}/context-deltas/{axis_slug}.proposal.json`

### 2.3 手渡し

- dry-run 成功後のみ inbox へ rsync（ [INTERFACES.md](INTERFACES.md)）
- Context proposal は **inbox とは別** — `aoifuture-web` promoter 入力ディレクトリ（未接続時は review-only 滞留）

---

## 3. パイプライン段

```
select candidates (policy 多様性・件数は LLM 前の機械フィルタ)
  → fetch primary URLs (HTTP 200, 既存 fetch 契約)
  → news-writer (別プロンプト: [WRITER-REVIEW.md](WRITER-REVIEW.md))
  → news-reviewer (事実照合チェックリスト)
  → assemble review-candidate.json
  → dry-run (state-root: .../policy-dryrun.* NOT under grokbot symlink)
  → on success: deploy inbox
```

**edition_id:** `{edition_date}-HHMM` JST、生成完了時刻。

---

## 4. Note との順序

1. 05:30 collect  
2. 06:30–09:00 DailyNews → `note-urls.json` を reservations に出力（実装は dailynews-pipeline）  
3. News worker は reservations を **優先度調整** にのみ使用（主役 URL を Note が取った場合、News では brief/watch に回す）

---

## 5. 障害時（Mac バックアップ）

手順は [CUTOVER.md](CUTOVER.md) §ロールバック。VPS worker が **3 回連続 BLOCKED** のときのみ Mac 手動 Edition を許可。

---

## 6. リポ構成（案）

```
aoi-news-worker/
  README.md
  pyproject.toml
  aoi_news_worker/
    select.py
    fetch.py
    assemble.py
    deploy_inbox.sh
  prompts/
    writer.ja.md
    reviewer.ja.md
  tests/
    fixtures/
```

依存: `aoi-content-intake` schemas（submodule または vendor copy + checksum）。