# 菲傭常見問題與應對辦法（經驗整理）

> 香港雇主實戰經驗整理｜第二版｜更新至 2026-09-09

- **在線閱讀**：<https://frankiezeng6-ai.github.io/fdh-employer-guide/>
- **在線編輯**：點任一頁右上角「✏️ 在 GitHub 上編輯此頁」，或[直接打開 SOURCE.md 編輯器](https://github.com/frankiezeng6-ai/fdh-employer-guide/edit/main/SOURCE.md)
- **下載 Word 原件**：`菲佣常见问题与应对办法（经验整理）.docx`

---

## 這份文檔是什麼

從香港雇主微信群「🇭🇰雇主智囊團」共 42,317 條聊天記錄（2026-04-17 至 2026-09-09）中提煉的實操經驗，
共 **33 條**，分四大類：財務（含出糧／匯款／開戶／八達通）、行為與紀律、照顧孩子、僱傭關係與合規。
每條都附群內原話與日期。

## 怎麼在線編輯

本站採用「Markdown 源文件 + GitHub Actions 自動重建」的方式，**不需要安裝任何東西**：

1. 在 GitHub 登入後，點頁面右上角「✏️ 在 GitHub 上編輯此頁」，或點上面的 `edit/main/SOURCE.md` 連結；
2. 改完拉到頁面底部，`Commit changes`（選 `Commit directly to the main branch`）；
3. GitHub Actions（`.github/workflows/build.yml`）會在約 30–60 秒內自動把 `SOURCE.md` 重建成 `index.html` 並推送回 main；
4. 刷新公網頁面即可看到新內容。

語法只需會四種：`# ` 大標題、`## ` 章、`### ` 條、`- ` 項目符號、`**粗體**`、`> ` 引用（群內原話）。

> 若你沒有 GitHub 帳號也可以在 [Issues](https://github.com/frankiezeng6-ai/fdh-employer-guide/issues) 留言，
> 或直接 Fork 後開 Pull Request。

## 文件結構

| 檔案 | 用途 |
| --- | --- |
| `index.html` | GitHub Pages 實際顯示的頁面，**由 Actions 自動生成，人手不要直接改** |
| `SOURCE.md` | 唯一的人手編輯源文件，改這裡就行 |
| `菲佣常见问题与应对办法（经验整理）.docx` | Word 原件，供打印／傳閱 |
| `tools/md2html.py` | Markdown → 單文件 HTML（只用標準庫） |
| `tools/docx2md.py` | Word → Markdown 的一次性轉換腳本（需 python-docx） |
| `.github/workflows/build.yml` | 每次改動 SOURCE.md 自動重建首頁 |

本地預覽：

```bash
python tools/md2html.py SOURCE.md index.html --repo frankiezeng6-ai/fdh-employer-guide
```

## 重要聲明

- 本文整理自群友經驗，**不是法律意見**。涉及金額、天數、法例條文者，以香港勞工處／入境處最新公告及《標準僱傭合約》正本為準。
- 文檔「附三：待核實清單（N/A）」列明 12 項尚未核實的內容（年假機票歸屬、遣散費計算、MPF、薪俸稅、疫苗要求等），使用前請自行核對。
- 引用中的群友稱呼均為微信暱稱。若不希望暱稱出現在公開頁面，可開 Issue 或自行執行 `tools/anonymize.md` 中的步驟把暱稱替換成「群友 A／B」。
