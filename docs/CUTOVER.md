# 切替と試験計画

**前提:** 現行 Mac Writer + sync は **本計画完了まで primary**。

---

## 1. 試験段階

| Stage | 内容 | 合格 |
|-------|------|------|
| S0 | 台帳バックフィル + spot check | 95% URL |
| S1 | collect のみ 7 日 | manifest complete |
| S2 | dry-run のみ（VPS生成 candidate、**inbox に置かない**） | 7 日 eligible |
| S3 | shadow inbox（Contabo 別パス `inbox-shadow/`） | publisher dry-run on shadow |
| S4 | 本番 inbox 1 日 | published_verified + site 200 |
| S5 | 7 日連続 Mac 無し | 欠日 0 |
| S6 | Context delta 1 軸 E2E | revision 公開 readback |

---

## 2. GO / NO-GO

**GO（primary 切替）:** S5 完了 + S6 1 本成功 + オーナー GO。

**NO-GO 即停止:**

- `publication_failed` + rollback 不整合  
- 台帳なしで duplicate `source_url` 公開  
- Context ねつ造疑い 1 件

---

## 3. ロールバック（1 日）

1. GB-058 timer disable  
2. Mac Orca Writer 再有効（手順書のみ保管、Hermes 679f は **使わない**）  
3. inbox 退避 → 手動 candidate  
4. sync スクリプト 1 回

---

## 4. Hermes / Mac

- 切替後: News 系 Hermes job **削除または永久 pause**（Exact）  
- Mac mini: **パイプライン cron から除外**；バックアップ手順のみ README 参照

---

## 5. 観測

| シグナル | 所在 |
|----------|------|
| corpus ready | `manifest.json` |
| edition queued | Contabo inbox + build manifest |
| published | `published_verified` receipt Contabo |
| axis delta | `context-deltas/*.proposal.json` 件数 |