# Context ストリーム — FSA 軸 delta

**原則:** 新着がある軸だけ、ねつ造しない（SPEC §2.3）。

---

## 1. データフロー

```
corpus item + axis_matches[]
    → ledger: この axis_slug で既に context に載った URL か？
        no → context-delta-proposal.v0
        yes → skip
    → news-writer (context 用短プロンプト)
    → news-reviewer
    → promoter → aoi.news.context.v1 revisions[] 追記
```

---

## 2. context-delta-proposal.v0

スキーマ: `schemas/context-delta-proposal.v0.schema.json`

含むもの:

- `axis_slug`, `axis_id`（FSA）
- `material_url`（一次）
- `proposed_revision`（`change_reason`, `resulting_view` ドラフト、`changed_at` JST）
- `proposed_signal_id`（新規 Signal 草案 id、`sig-{axis}-{date}-{hash8}` 形式）
- `corpus_snapshot_id`

**含まないもの:** FSA provenance 内部フィールド、スコア。

---

## 3. aoifuture-web へのマージ

### 3.1 新規軸（FSA public、Context ファイル無し）

- `initial` context JSON を生成（`title` = Axis title 日本語訳または編集確定、`current_view` = 初回 revision の要約）。
- `publication_status`: 最初は `review-only`、Exact 後 `public`（既存運用踏襲）。

### 3.2 既存ファイルへの update

- 直前ファイルを read → `revisions` 末尾に append → `current_view` / `updated_at` 更新。
- E2 **G4:** promoter は rename による原子更新（設計済み、実装は aoifuture-web / agent-platform PR）。

### 3.3 台帳更新

Context 公開成功後、ledger `used_in` に `{ "product": "context_axis", "artifact_id": revision.id }`。

---

## 4. 軸マッチャ v1（ルール）

1. **タイトル / 要約** に Axis のキーワードセットがヒット（`FSA-AXIS-MAP.md` の `match_terms[]`）。
2. **AND** URL が一次 HTTPS で fetch 検証済み。
3. confidence `high` のみ自動提案。`medium` は reviewer 必須。

---

## 5. 日次 Edition との重複

同一 URL が Edition item と Context revision の両方に出て **よい**。台帳で追跡。

---

## 6. 受け入れ

- 人為的に delta 0 の日: **proposal ファイルゼロ**、promoter 呼び出しゼロ。
- 1 軸 1 日 1 revision 上限（複数 URL ヒット時は **最も新しい 1 件** のみ。残りは翌日コーパスへ）。