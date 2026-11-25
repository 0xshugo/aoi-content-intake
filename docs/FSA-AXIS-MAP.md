# FSA 研究軸マッピング（public）

**スナップショット根拠:** `handoffs/active/20261103-0400-aoifuture-news-fsa-axis-list.md`（2026-11-03 GET 10 軸）

**ルール:** `data_class=public` のみ Context ストリーム対象。`internal`（id 1・2）はマッチしても **提案しない**。

---

## 1. 公開軸一覧

| axis_id | slug | Context パス | 初期状態 |
|---------|------|--------------|----------|
| 3 | `ai-math-proof-verification` | `/news/context/ai-math-proof-verification/` | 新規 JSON |
| 4 | `physical-layer-security-genai-covert` | `/news/context/physical-layer-security-genai-covert/` | 新規 |
| 5 | `ai-agent-economy-trust-tradeoff` | `/news/context/ai-agent-economy-trust-tradeoff/` | 新規（E1 既知軸） |
| 6 | `llm-eval-contamination` | `/news/context/llm-eval-contamination/` | 新規 |
| 7 | `llm-domain-eval-robustness` | `/news/context/llm-domain-eval-robustness/` | 新規 |
| 8 | `genai-provenance-audit` | `/news/context/genai-provenance-audit/` | 新規（E1 既知） |
| 9 | `llm-structural-limits-eval-validity` | `/news/context/llm-structural-limits-eval-validity/` | 新規（E1 既知） |
| 10 | `multimodal-domain-ai-trends` | `/news/context/multimodal-domain-ai-trends/` | 新規 |

**既存 editorial context**（`agent-authority`, `connected-ai-boundaries` 等）は **FSA 軸とは別系列**。将来的に手動で FSA 軸へ統合する場合は slug リダイレクト表を別 Exact。

---

## 2. match_terms v1（機械マッチ用・下書き）

編集レビュー後に確定。過剰マッチを避けるため **軸ごと最低 2 語 AND** 推奨。

| slug | match_terms（例） |
|------|-------------------|
| `llm-eval-contamination` | `contamination`, `benchmark`, `eval` |
| `llm-domain-eval-robustness` | `domain`, `robust`, `evaluation` |
| `genai-provenance-audit` | `provenance`, `audit`, `watermark` |
| `ai-agent-economy-trust-tradeoff` | `agent`, `trust`, `economy` |
| `ai-math-proof-verification` | `proof`, `formal`, `mathematics` |
| `physical-layer-security-genai-covert` | `physical layer`, `covert`, `genai` |
| `llm-structural-limits-eval-validity` | `structural`, `limit`, `validity` |
| `multimodal-domain-ai-trends` | `multimodal`, `speech`, `domain` |

実装は `aoi_intake.axis_matcher` に YAML で外出し: `config/fsa-axis-match-v1.yaml`。

---

## 3. タイトル表示

- ページ `title`: FSA `title` フィールドを基本（日本語が無い場合は編集が `contexts/*.json` で上書き）。
- **FSA API の長文フィールドは保存・表示しない**（E2 P8）。

---

## 4. 更新表示

- 一覧に **最終 revision 日付** のみ。件数バッジは出さない（スコア同様）。