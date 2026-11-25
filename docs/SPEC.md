# 要件仕様 — aoi-content-intake（v0.1）

**確定日:** 2026-11-25（オーナー合意）  
**ステータス:** design lock（実装前）

---

## 1. 目的

1. FreshRSS・FSA・その他一次ソースから **1 日 1 回以上の共有コーパス** を構築する。  
2. **素材台帳**（URL・履歴・製品での使用）を正本とし、DailyNews と AOIFUTURE News の **二重収集をやめる**。  
3. **FSA 軸**は `/news/context/{slug}` で追う **テーマ別新着** のみに使う（delta があるときだけ）。  
4. **公開面にスコアを出さない**（内部メタのみ）。

---

## 2. プロダクトと体験

### 2.1 日次 Edition（既存 News）

- **役割:** その日の新着を **淡々と** 掲載（8〜12 item 等は現行 standing policy に準拠）。  
- **品質:** 新聞社水準の文体・事実分離（`source_fact` / `aoi_note` / `caveat`）。  
- **目標公開時刻:** **お昼前後（JST）**（例: 12:00 公開）。  
- **入力:** 朝に構築した **同じコーパス／素材台帳**（Note 生成後の追加入力は最小）。

### 2.2 DailyNote

- **役割:** 1 日 1 本の長文記事。  
- **目標:** **朝**（コーパス確定後に生成）。  
- **ライター／レビュー:** News とは **別プロセス**（文量・ゲートが異なる）。品質バーは同等。  
- **入力:** 共有コーパス＋素材台帳（News より先に走る）。

### 2.3 FSA 軸 — Context ストリーム

- **導線:** **`/news/context/…`**（サイト既存 context 導線と整合）。  
- **内容:** 追っている **FSA 研究軸（Research Axis）** ごとに、**その軸に効く新着がある日だけ** 短い要約を **時系列で積む**。  
- **禁止:** 更新が無いのに埋め草・総括の **ねつ造**。軸ごと **沈黙** が正常。  
- **表現:** 「このテーマの新着」として文脈に沿った紹介（一次 URL 必須）。

### 2.4 スコア

- 収集・選定用スコアは **パイプライン内部のみ**。  
- 公開 JSON・Web・Note 本文に **スコア順・点数・FreshRSS 件数** 等を載せない。

---

## 3. スケジュール（目標 JST）

| 時刻（目安） | 処理 |
|--------------|------|
| 05:30 前後 | `collect` — FreshRSS・FSA snapshot・signals → コーパス世代 |
| 06:30〜09:00 | DailyNews 生成・レビュー → Note READY |
| 10:00 前後 | News worker — `review-candidate.json` + context delta 素材 |
| 11:00 前後 | policy dry-run 合格 |
| 12:00 前後 | Contabo publisher 公開（現行 timer と整合させる） |

取得タイミングが違えば見出しが変わることは許容する。**`snapshot_id`** で世代を説明する。

---

## 4. インフラ方針

| 項目 | 決定 |
|------|------|
| 正本ホスト | **Contabo VPS**（収集・台帳・派生生成・Contabo inbox 手渡し） |
| Mac mini | 新方式安定後 **パイプラインから外れてよい**。障害時 **最低限の手動編成バックアップ** のみ |
| Hermes cron | News 系から **外してよい**（679f / bed6ee 再開禁止は切替期も維持） |
| リポジトリ | **パイプラインは別リポ**。本 repo は **共有素材・スキーマ・契約** の正本 |

---

## 5. 素材台帳（必須）

### 5.1 要件

- **全製品共通**の URL 正本（DailyNews・News・Context）。  
- **過去分をバックフィル**（既公開 Edition・Note 出典から `used_in` を埋める）。  
- 新規採用時は **台帳と突合** し、同一 `source_url` の重複掲載を防ぐ。  
- スコアは台帳に **任意の内部フィールド** としてよいが、派生成果物へは出さない。

### 5.2 最小フィールド（v0）

`material` 1 件:

- `url`（HTTPS、正規化済み）  
- `first_seen_at`（JST ISO）  
- `snapshot_ids[]`（登場したコーパス世代）  
- `axis_ids[]`（マッチした FSA 軸、空可）  
- `used_in[]`: `{ product, date, artifact_id }`（`dailynews` / `news_edition` / `context_axis`）

詳細スキーマは [`DESIGN.md`](DESIGN.md) §素材台帳。

---

## 6. FSA 軸

- **ソース:** FSA Research Axis API（DailyNews intake と **同じ read 経路**）。  
- **公開軸:** `data_class=public` のみ Context ストリーム対象（現行 8 軸想定）。  
- **delta 条件:** コーパス内の URL が軸スコープに入り、**その軸のストリームに未掲載** のときだけ追加。  
- **軸ニュース＝FSA ニュース:** 軸の更新は FSA 軸定義と API スナップショットに従い、別系統の「軸一覧」を手で二重管理しない。

---

## 7. 品質・ゲート

| 出力 | ゲート（別プロセス） |
|------|----------------------|
| Note | dailynews-pipeline 既存レビュー・BLOCK 条件 |
| News Edition | `aoi002_news_policy_publisher` dry-run → `eligible_dry_run` |
| Context delta | schema + 一次 URL 検証 + **delta ゼロなら出力ファイル無し** |

ライター／レビューアーは製品ごとに分離。upstream（collect）は共有。

---

## 8. 切替

1. **現行維持:** Mac Writer + inbox sync + Contabo `--apply`（2026-11-25 時点で稼働中）。  
2. **並行構築:** VPS collect・素材台帳・News worker・context builder。  
3. **合格条件（案・数値は実装フェーズで確定）:**  
   - N 日連続: コーパス ready → News `published_verified`（お昼帯）  
   - context delta 誤掲載 0（手動サンプル監査）  
   - Mac 無しで再現可能  
4. **切替:** inbox 経路を VPS 直書きに変更。Mac Writer を primary から外す。  
5. **ロールバック:** 1 日分、Mac 手動 candidate + sync を手順書化（バックアップ用途）。

---

## 9. 非目標（v0）

- Grok / Mac `feeds.sh` の恒久維持  
- スコアの読者向け開示  
- 全軸の毎日更新強制  
- policy v2 / context v2 の同時リリース（必要なら別 Exact。v1 Edition は継続可）

---

## 10. 参照（Scratch）

- 横断決定: `0xshugo/project-scratch` → `context/decisions.md`（2026-11-25 項）  
- Handoff: `handoffs/active/2026-11-25-aoi-content-intake-design-lock.md`