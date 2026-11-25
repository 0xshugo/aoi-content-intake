# ドキュメント索引（v0.2）

| 文書 | 読者 | 内容 |
|------|------|------|
| [SPEC.md](SPEC.md) | 全員 | 要件・切替条件 |
| [DESIGN.md](DESIGN.md) | 実装 | 全体アーキテクチャ・フェーズ |
| [SITE-IA.md](SITE-IA.md) | 編集・フロント | `/news` と `/news/context` の情報設計 |
| [INTERFACES.md](INTERFACES.md) | 実装 | パス・ファイル契約・環境変数 |
| [COLLECT.md](COLLECT.md) | dailynews-pipeline | 共有 collect の責務 |
| [NEWS-WORKER.md](NEWS-WORKER.md) | aoi-news-worker | 昼前 Edition 生成 |
| [CONTEXT-STREAM.md](CONTEXT-STREAM.md) | aoi-news-worker / web | FSA 軸 delta → Context |
| [FSA-AXIS-MAP.md](FSA-AXIS-MAP.md) | 編集 | FSA slug と Context の対応 |
| [WRITER-REVIEW.md](WRITER-REVIEW.md) | 編集・LLM | Note / News の分離ゲート |
| [LEDGER-BACKFILL.md](LEDGER-BACKFILL.md) | 運用 | URL 台帳の過去取り込み |
| [ORCA-SCHEDULE.md](ORCA-SCHEDULE.md) | Orca | VPS timer 目標構成 |
| [CUTOVER.md](CUTOVER.md) | オーナー | 旧 Mac 経路からの移行試験 |
| [IMPLEMENTATION-TRACKER.md](IMPLEMENTATION-TRACKER.md) | PM | イシュー・依存・順序 |