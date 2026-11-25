# Orca スケジュール（目標 JST）

**現行維持:** GB-053 publisher `--apply`（01:10 / 07:10 / 13:10 / 19:10）は当面そのまま。**新方式はお昼帯に合わせて 1 tick に寄せる** Exact が必要（下記 ★）。

---

## 日次タイムライン（新方式・確定案）

| 時刻 | ユニット | リポ | 備考 |
|------|----------|------|------|
| 05:30 | `orca-gb001-dailynews-generate`（既存）内で **collect フェーズ** | dailynews-pipeline | FreshRSS+FSA→corpus |
| 05:30–09:00 | GB-001 generate / recovery | dailynews-pipeline | Note READY |
| 09:15 | （新）`orca-gb057-material-ledger-snapshot` | aoi-content-intake script | 任意 compact |
| 10:30 | （新）`orca-gb058-aoi-news-worker` | aoi-news-worker | Edition+delta 提案 |
| 11:00 | （新）`orca-gb058` 内 dry-run | agent-platform | eligible 必須 |
| 11:15 | inbox rsync | shell | Mac sync **廃止後** |
| **12:00 前後** | `orca-gb053-aoifuture-news-policy-publisher` ★ | agent-platform | **`--apply` 1 回/日** へ整理検討 |
| 12:10 | GB-003 Postiz（既存） | — | Note 連動 |

---

## GB 番号

| GB | 名称 | 状態 |
|----|------|------|
| GB-053 | News publisher apply | 稼働中 |
| GB-058 | News worker + context proposals | **設計のみ・未実装** |
| GB-057 | Ledger snapshot | 任意 |

Mac Automation `895531c3`（Writer）は **GB-058 安定後 disabled**。

---

## 依存

- collect が 09:00 前に complete していること  
- Note reservations が 10:00 までにあれば読む（無くても worker 可）