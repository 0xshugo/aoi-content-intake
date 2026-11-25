# aoi-content-intake

AOI Future の **共有コンテンツ取得プレーン**（素材台帳・コーパス・FSA 軸 delta）の仕様とスキーマの正本。

DailyNews（Note）と [AOIFUTURE News](https://www.aoifuture.com/news/) は **別パイプライン・別ライター／レビュー** だが、ここで定義する **素材** を入力として使う。

## 状態

| 項目 | 値 |
|------|-----|
| 段階 | 設計 v0.2（2026-11-25）／P0 スクリプトあり |
| 本番 News | 現行 Mac Writer → Contabo publisher 継続（切替前） |
| ドキュメント | [`docs/INDEX.md`](docs/INDEX.md) から辿る |
| 次リポ | `0xshugo/aoi-news-worker`（未作成） |

## 関連リポジトリ（参照のみ・本 repo はコードを持たない v0）

| リポ | 役割 |
|------|------|
| `0xshugo/dailynews-pipeline` | Note 生成（朝） |
| `AOI-Future/aoifuture-web` | News / Context 公開面 |
| `0xshugo/agent-platform` | policy publisher（Contabo） |
| `0xshugo/future-search-agent` | FSA 軸 API |

## 切替ゲート（要約）

新方式が **テスト合格・安定稼働** するまで現行パイプラインを維持。詳細は `docs/SPEC.md` §切替。