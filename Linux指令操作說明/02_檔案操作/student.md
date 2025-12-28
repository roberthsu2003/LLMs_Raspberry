# 檔案操作練習 – 學生作業

以下題目請在你的 Linux 終端機（Raspberry Pi、Docker、或任意 Linux 環境）上依序完成。每完成一步，請使用 `pwd`、`ls -l` 或將指令輸出截圖保存，作為作業回報的依據。

---

## 1️⃣ 建立與寫入檔案

1. 使用 `touch` 建立三個空檔案：`note.txt`、`todo.md`、`log.txt`。  
2. 用 `echo` 將文字 **「今天的學習筆記」** 寫入 `note.txt`（覆寫）。  
3. 用 `echo` 將 **「完成作業」** 追加寫入 `todo.md`（保留舊內容）。  
4. 使用 **here‑document** 建立 `report.md`，內容如下：

   ```text
   # 每日報告
   日期：2025-12-28
   - 完成檔案建立
   - 練習指令
   ```

   *提示*：`cat <<EOF > report.md` … `EOF`

---

## 2️⃣ 檔案內容檢視

1. 用 `cat note.txt` 觀察剛才寫入的文字。  
2. 用 `nl -ba todo.md` 顯示行號。  
3. 用 `head -n 3 report.md` 顯示前 3 行。  
4. 用 `tail -n 2 report.md` 顯示最後 2 行。  

---

## 3️⃣ 複製與搬移

1. 複製 `note.txt` 為 `note_backup.txt`。  
2. 建立資料夾 `archive`，將 `todo.md` 與 `report.md` 移入該資料夾。  
3. 使用 `cp -r archive archive_copy` 複製整個目錄。  
4. 檢查 `archive_copy` 內的檔案是否完整（`ls -l archive_copy`）。

---

## 4️⃣ 刪除與安全刪除

1. 用 `rm -i note_backup.txt` 刪除備份檔，觀察系統的確認訊息。  
2. 用 `rm -f *.log` 強制刪除所有 `.log` 檔案（如果有的話）。  
3. 嘗試直接 `rmdir archive`（會失敗），說明原因。  
4. 在 `archive` 內使用 `rm -r *` 清空目錄，然後 `rmdir archive` 成功刪除。

---

## 5️⃣ 文字搜尋與管道練習

1. 用 `grep -i "學習" *.md` 找出所有 `.md` 檔中包含「學習」的行。  
2. 把 `report.md` 中所有大寫字母轉成小寫，結果寫入 `report_lower.txt`（`tr` 與管道）。  
   ```sh
   cat report.md | tr 'A-Z' 'a-z' > report_lower.txt
   ```  
3. 使用 `ls -l *.md | sort -k9`（依檔名排序）結果寫入 `sorted_list.txt`。  
4. 以 `awk '{print $9}' sorted_list.txt | wc -l` 計算 `.md` 檔的數量。

---

## 6️⃣ 使用文字編輯器

1. 用 `nano note.txt` 開啟並在檔案最後加入一行 **「結束練習」**，保存離開。  
2. 用 `vim todo.md` 在第一行前插入 `# TODO List`，保存離開。  
   - **提示**：在 `vim` 中按 `i` 進入插入模式，完成後 `Esc` → `:wq`。

---

## 7️⃣ 進階挑戰（加分題）

1. 建立一個專案目錄 `project`，裡面依序建立 `src`、`docs`、`tests` 三個子目錄。  
2. 在 `src` 中建立 `main.sh`，內容：

   ```sh
   #!/bin/bash
   echo "Hello, Linux!"
   ```

3. 給予執行權限：`chmod +x src/main.sh`。  
4. 從 `project` 目錄執行 `./src/main.sh`，確認螢幕顯示 **Hello, Linux!**。  
5. 用 `tree -L 3 project`（若未安裝 `tree`，先 `sudo apt install -y tree`）檢查目錄結構。  

---

## 作業提交說明

完成所有練習後，請把以下資訊整理成一份報告（文字檔或 PDF）：

- 每一步的指令與對應輸出（可直接貼上終端機文字或截圖）。  
- 遇到的錯誤訊息與解決方式（特別是第 4 題的刪除失敗）。  
- 加分挑戰的完成結果與個人感想。  

祝練習順利，期待看到你的作業！