# 技術設計 — aoi-content-intake（v0.2）

**SPEC:** [`SPEC.md`](SPEC.md)  
**索引:** [`INDEX.md`](INDEX.md)  
**確定日:** 2026-11-25（v0.2 設計詳細化）

---

## 1. アーキテクチャ概要

```
┌─────────────────────────────────────────────────────────────┐
│ Contabo VPS — collect (Orca timer)                          │
│   FreshRSS GReader │ FSA GET /v1/research-axes │ signals…     │
│        └─► corpus/{snapshot_id}/                            │
│        └─► material-ledger (append + backfill)              │
└─────────────────────────────────────────────────────────────┘
          │                          │
          ▼                          ▼
┌──────────────────┐    ┌──────────────────────────────────┐
│ dailynews-pipeline│    │ news-worker (新設・別リポ)         │
│ 朝: Note bundle   │    │ 昼前: review-candidate.json       │
└──────────────────┘    │      + context-deltas/{axis}/…    │
          │               └──────────────┬───────────────────┘
          │                              ▼
          │               ┌──────────────────────────────────┐
          │               │ Contabo inbox → policy publisher   │
          │               │   --apply (Mac Hermes 不使用)      │
          │               └──────────────────────────────────┘
          ▼
     Note 予約（既存 GB-001/003 経路）

┌─────────────────────────────────────────────────────────────┐
│ Mac mini — 切替後: 原則オフライン                          │
│   例外: 手動 review-candidate + sync（障害バックアップ）       │
└─────────────────────────────────────────────────────────────┘
```

**一本化の原則:** `collect` は **唯一の RSS/FSA 取得入口**。DailyNews と News は **読み取りのみ**。

---

## 2. リポジトリ分担

| リポジトリ | 担当 | 本 repo との関係 |
|------------|------|------------------|
| **`0xshugo/aoi-content-intake`**（本 repo） | 仕様・JSON Schema・運用契約・バックフィル手順 | 正本 |
| `0xshugo/dailynews-pipeline` | collect 実装・Note 生成 | `schemas/*` を参照または submodule |
| `0xshugo/aoi-news-worker`（新規・未作成） | News candidate・context delta 生成 | 同上 |
| `AOI-Future/aoifuture-web` | `/news`・`/news/context/[slug]` レンダリング | promoter／静的 import |
| `0xshugo/agent-platform` | `aoi002_news_policy_publisher.py` | 変更は別 PR |

**新規 repo を分けた理由:** パイプラインは独立デプロイだが、**素材台帳とコーパス世代**は製品横断の契約なので、どちらのパイプラインからも同じスキーマを import できる neutral な正本が必要。

---

## 3. コーパス世代（`corpus/{snapshot_id}/`）

### 3.1 `snapshot_id`

形式: `corpus-{YYYY-MM-DD}T{HHMMSS}+0900`（collect 完了時刻 JST）。

### 3.2 ファイル（v0 案）

| ファイル | 内容 |
|----------|------|
| `manifest.json` | `snapshot_id`, `collect_started_at`, `collect_finished_at`, counts, errors |
| `items.jsonl` | 正規化候補 1 行 1 URL（title, url, published_at, feed_id, raw_ref） |
| `fsa-axes.json` | FSA API の軸スナップショット（id, slug, title, data_class）※本文フィールドは最小 |
| `internal-scores.jsonl` | **任意・非公開** — url, score, reason_codes |

`items.jsonl` から公開製品へは **フィルタ済みビュー** のみ渡す。

---

## 4. 素材台帳（material-ledger）

### 4.1 格納

- **正本:** Contabo `/var/lib/orca-control/work/aoi-content-intake/material-ledger/`（[INTERFACES.md](INTERFACES.md)）。  
- **形式:** `materials.jsonl`（追記）+ `materials-index.sqlite`（任意・高速検索）  
- **Git:** 日次スナップショットを **別ブランチ or 物件ストア** に export 可（サイズ上限に注意）。

### 4.2 レコード例

```json
{
  "url": "https://example.com/path",
  "canonical_host": "example.com",
  "first_seen_at": "2026-11-25T05:31:00+09:00",
  "snapshot_ids": ["corpus-2026-11-25T053000+0900"],
  "axis_matches": [
    { "axis_id": 6, "axis_slug": "llm-eval-contamination", "rule": "keyword-v1", "matched_at": "2026-11-25T05:32:00+09:00" }
  ],
  "used_in": [
    { "product": "dailynews", "date": "2026-11-25", "artifact_id": "note-draft-2026-11-25" },
    { "product": "news_edition", "date": "2026-11-25", "artifact_id": "2026-11-25-1200" }
  ],
  "_internal": { "score": 0.82, "noise": false }
}
```

`_internal` は派生ワーカーが **削除してから** ライター入力に渡す。

### 4.3 バックフィル

1. `AOI-Future/aoifuture-web` `src/content/news/editions/` から全 `source_url`  
2. DailyNote 公開出典リスト（Drive archive または receipt）  
3. 既存 Mac `used-urls.txt`  
4. `used_in` を埋め、`first_seen_at` は不明なら edition/note 日付で近似（`provenance: backfill`）

---

## 5. FSA 軸 × Context delta

### 5.1 対応

| FSA | Web |
|-----|-----|
| `research_axis.slug` | `/news/context/{slug}`（既存ルート） |

### 5.2 delta パイプライン

1. collect 後、各 `material` に **axis matcher**（v1: ルール／キーワード／タイトル；将来 embedding）  
2. 軸ごとに `last_published_url_at[axis]` を台帳から復元  
3. 新規 URL かつマッチ → `context-deltas/{slug}/{YYYY-MM-DD}.json` を **1 件以上あるときだけ** 生成  
4. promoter が context ページ本文に **append**（ねつ造防止: 入力 URL は `items.jsonl` に存在すること）

### 5.3 日次 Edition との関係

- 日次は **全体スコア上位（内部）・policy 多様性** で構成。  
- 軸は **タグ付け・選定理由の補強** としてもよいが、**別導線が主**。  
- 同一 URL が日次と context の両方に出てよいが、台帳 `used_in` で追跡。

---

## 6. News worker（新規）

### 6.1 入力

- `corpus/{snapshot_id}/items.jsonl`  
- `material-ledger`（重複排除）  
- 朝の Note で `reserved` した URL セット（任意ファイル `note-reservations-{date}.json`）

### 6.2 出力

- `publish/aoifuture-news/{date}/review-candidate.json`  
- Contabo: `~/.hermes/work/aoifuture-news-aoi002/publisher/inbox/review-candidate.json`（**rsync/scp 直書き**、Mac sync 廃止後）

### 6.3 dry-run

- `aoi002_news_policy_publisher.py` **--apply 禁止**  
- `state-root`: `aoifuture-news-aoi002/policy-dryrun.*` 直下（**`grokbot` symlink 配下に置かない**）

### 6.4 ライター／レビュー

- Note: 既存 `claude -p` + critique ループ  
- News: 別プロンプト・別ゲート（文量短い・item 単位）。共有するのは **素材メタのみ**。

---

## 7. 現行パイプライン（レガシー）

| 要素 | 切替まで |
|------|----------|
| Mac Orca / Cursor Writer | 継続 |
| `sync_aoifuture_news_inbox_to_contabo.sh` | 継続 |
| Contabo publisher timer | 継続 |
| Mac `feeds.sh` | 新 collect 合格まで残すが **非正本** |

---

## 8. 実装フェーズ（推奨順）

| Phase | 内容 | 完了条件 |
|-------|------|----------|
| P0 | 本 repo スキーマ + バックフィル script 草案 | ledger に過去 URL >95% |
| P1 | VPS collect のみ（FreshRSS + FSA）→ corpus + ledger | 7 日連続 manifest OK |
| P2 | dailynews が corpus を入力に切替 | Note 品質ゲート維持 |
| P3 | news-worker + Contabo inbox 直書き | dry-run + published_verified |
| P4 | context delta builder | 軸 1 本で手動 readback |
| P5 | Mac/Hermes 切離し | ロールバック手順 1 枚 |

---

## 9. 未決（実装前にイシュー化）

1. ~~material-ledger パス~~ → `/var/lib/orca-control/work/aoi-content-intake/`（v0.2 確定）  
2. context delta の promoter 結線（E2 G4）— v0 は **手動 PR フォールバック** 可（[CONTEXT-STREAM.md](CONTEXT-STREAM.md)）  
3. News publisher **お昼 1 tick** — [ORCA-SCHEDULE.md](ORCA-SCHEDULE.md)、Exact 待ち  
4. ~~news-worker リポ名~~ → `0xshugo/aoi-news-worker`（[NEWS-WORKER.md](NEWS-WORKER.md)）  
5. `aoi_intake` Python パッケージの配置（dailynews-pipeline 内モノレポ vs 別 wheel）  

---

## 10. 関連 Scratch / 設計履歴

- AOIFUTURE News × FSA 案B E2: `project-scratch/handoffs/active/20261103-0410-aoifuture-news-fsa-e2-design-lock.md`  
- dailynews 再構築: `handoffs/active/2026-11-21-dailynews-pipeline-rebuild.md`  
- Mac Orca News cutover: `orca-fleet-migration-work/2026-11-18/aoifuture-news-writer-mac-orca-prompt.md`