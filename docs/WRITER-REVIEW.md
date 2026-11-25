# ライター／レビュー分離

---

## 共通

- 入力: corpus material（スコア除去済み）、一次 URL 本文スナップショット。
- **禁止:** 確認できない事実、内部パス、スコア語彙、pipeline 語彙。
- 品質: 新聞社水準（事実 / 評価分離）。

---

## DailyNote

| 項目 | 値 |
|------|-----|
| オーナー | `dailynews-pipeline` |
| 尺 | 長文 1 本 |
| ゲート | 既存 REVIEW 85 / BLOCK ルール |
| モデル | 既存 `claude -p` + critique ループ |
| 出力 | `draft.json`, Note bundle |

**変更点（新方式）:** 候補 URL のみ corpus 由来。`note-urls.json` を reservations に書く。

---

## AOIFUTURE News Edition

| 項目 | 値 |
|------|-----|
| オーナー | `aoi-news-worker` |
| 尺 | 8–12 items、各 item 短め |
| ゲート | policy dry-run `eligible_dry_run` + reviewer チェックリスト |
| プロンプト | `prompts/news-writer.ja.md`（未作成・v1 は Mac grokbot 契約を移植） |
| 出力 | `review-candidate.json` |

**Reviewer 必須項目（機械 + LLM）:**

1. 各 `source_url` が fetch ログと一致  
2. `source_domain` = URL host  
3. 台帳上未使用または意図的再利用（通常禁止）  
4. edition_date = 当日 JST  
5. 内部語彙スキャン

---

## Context revision（FSA 軸）

| 項目 | 値 |
|------|-----|
| 尺 | `resulting_view` ≤ 2000 文字、`change_reason` ≤ 500 |
| ゲート | `aoi.news.context.v1` schema + 一次 URL |
| 頻度 | delta のみ |

Context 用プロンプトは Edition より **短く・軸文脈固定**。「この軸を追う読者向けの新着 1 件」。

---

## 相互干渉

- Note ライターと News ライターは **別プロセス・別プロンプト**。同一 corpus でも **セッション共有しない**。
- Reviewer が **cross-product URL 予約** を見る（reservations）。