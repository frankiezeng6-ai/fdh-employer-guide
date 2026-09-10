# 暱稱匿名化（可選）

公開頁面中的「群內原話」保留了微信暱稱（如 `（2026-09-09 HH）`）。若希望替換成匿名代號，按下列步驟操作即可。

## 做法

1. 在 GitHub 上編輯 `SOURCE.md`（或本地編輯後重新執行 `tools/docx2md.py`）。
2. 用編輯器的「搜尋並取代」把暱稱逐個換成 `群友A`、`群友B`…… 建議用帶括號的完整字串，避免誤傷正文：

   ```
   （2026-09-09 HH）      →  （2026-09-09 群友A）
   （2026-09-02 荞伊）    →  （2026-09-02 群友B）
   ```

3. 本地批次處理可用（Git Bash / PowerShell 皆可）：

   ```bash
   # 列出文件中出現過的所有暱稱
   grep -oP '（\d{4}-\d{2}-\d{2} [^）]+）' SOURCE.md | sort -u

   # 逐個替換（把 Nick 換成真實暱稱，群友A 換成目標代號）
   python - <<'PY'
   import re
   s = open('SOURCE.md', encoding='utf-8').read()
   names = sorted({m.group(1).strip() for m in re.finditer(r'（\d{4}-\d{2}-\d{2}\s+([^）]+)）', s)})
   for i, n in enumerate(names, 1):
       s = re.sub(r'（(\d{4}-\d{2}-\d{2})\s+' + re.escape(n) + r'）', r'（\1 群友%d）' % i, s)
   open('SOURCE.md', 'w', encoding='utf-8').write(s)
   print('replaced', len(names), 'nicknames')
   PY
   ```

4. 提交後 Actions 自動重建 `index.html`。

> 注意：改完暱稱後，日後再跑 `tools/docx2md.py` 會從 Word 原件重新生成並覆蓋匿名結果。
> 建議匿名化後以 `SOURCE.md` 為準，別再倒退回 Word 版本。
