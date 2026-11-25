# サイト情報設計 — AOIFUTURE News（新方式）

**関連:** [SPEC.md](SPEC.md) §2、[CONTEXT-STREAM.md](CONTEXT-STREAM.md)

---

## 1. 公開面の二層

| 導線 | URL | 更新頻度 | 読者体験 |
|------|-----|----------|----------|
| **日次 Edition** | `/news/`, `/news/{edition_id}/` | **1 日 1 本**（JST `edition_date`） | その日の一次ソース新着を **淡々と** 列挙。テーマの強制なし。 |
| **追跡テーマ（FSA 軸）** | `/news/context/{slug}/` | **delta があるときだけ** | 追いかけている研究軸の **新着要約が時系列で積まれる**。無更新は前回表示のまま（ねつ造しない）。 |

**表示しないもの:** 内部スコア、FreshRSS 件数、パイプライン名、ランキング順位の数値。

---

## 2. 日次 Edition（変更なし）

- 契約: 現行 `aoi.news.review-candidate.v1` / `aoi.news.edition.v1`（publisher v1）。
- 8〜12 items、role 配分、domain 多様性は standing policy 準拠。
- **FSA 軸は日次の主役にしない。** 軸に効く記事は日次に載ってもよいが、**軸の語りは Context 側**。

---

## 3. Context（FSA 軸）

### 3.1 正本スキーマ

- `AOI-Future/aoifuture-web` の `aoi.news.context.v1`（`schemas/aoi-news-context-v1.schema.json`）。
- ページ: `src/pages/news/context/[slug].astro`。
- 現状の `contexts/agent-authority.json` 等は **編集テーマ v0**。FSA 公開軸は **slug = FSA `research_axis.slug`** で **別ファイル** として増やす（既存 slug と衝突する場合は [FSA-AXIS-MAP.md](FSA-AXIS-MAP.md) でリダイレクト表）。

### 3.2 更新モデル

1. collect が URL を軸にマッチ（`material.axis_matches[]`）。
2. 台帳上、その軸の Context ストリームに **未掲載** の URL のみ **delta 提案**（`context-delta-proposal.v0`）。
3. News 用ライターが **短い revision** 文案を生成（一次 URL 必須）。
4. reviewer が通過 → **context bundle** を promoter が `src/content/news/contexts/{slug}.json` にマージ（`revisions[]` 追記、`current_view` / `updated_at` 更新）。

**沈黙:** 提案 0 件の軸は **ファイル操作なし**（運用ログに `axis_delta=0` のみ）。

### 3.3 Signal との関係

- Edition item は従来どおり **Signal** として import される。
- Context revision は `evidence_signal_ids` で Signal を参照する（E2 設計と同型）。
- v0 新パイプラインでは: 同一 material から **Signal 草案** と **Context revision 草案** を別々に生成し、publisher が Edition を先に出し、Context は **同日または翌 Orchestrator tick** で追記してよい（ [ORCA-SCHEDULE.md](ORCA-SCHEDULE.md)）。

---

## 4. ナビゲーション（案）

- `/news/` トップ: 最新 Edition + **「追跡テーマ」** リンク一覧（FSA public 8 軸。最終更新日のみ表示、スコアなし）。
- 各 Context ページ: 現在の見立て（`current_view`）+ revision 履歴（折りたたみ可、実装は web 側）。

---

## 5. 非目標

- 全軸の毎日更新バッジ
- FSA の `core_question` 全文の公開
- Edition と Context の自動マージ（別成果物のまま）