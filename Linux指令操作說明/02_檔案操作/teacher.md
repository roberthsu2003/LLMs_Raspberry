# 檔案操作教學 – 老師示範

本文件為教師在課堂上示範「檔案操作」時的完整步驟與說明，涵蓋基礎指令、常用參數、實務範例與進階技巧。請依序在終端機執行以下指令，並逐一解說每一步的目的與結果。

---

## 1. 建立空檔與檢視內容

```sh
# 建立三個空檔
touch note.txt diary.md report.log

# 確認檔案已建立
ls -l note.txt diary.md report.log

# 使用 cat 查看空檔（不會有輸出）
cat note.txt
```

*說明*：`touch` 會建立新檔或更新既有檔的時間戳記。`cat` 用於顯示檔案內容，若檔案為空則無輸出。

---

## 2. 向檔案寫入與追加文字

```sh
# 使用重定向寫入（會覆蓋原有內容）
echo "今天的學習筆記" > note.txt

# 使用追加寫入（保留舊內容，往下加）
echo "第二行內容" >> note.txt

# 同時寫入多行（使用 here‑document）
cat <<EOF > diary.md
# 日誌
2025-12-28 第一次使用 Linux
- 建立檔案
- 練習指令
EOF
```

*說明*：`>` 會覆蓋檔案，`>>` 會在檔案末端追加。`cat <<EOF` 可一次寫入多行文字。

---

## 3. 複製檔案與目錄

```sh
# 複製單一檔案
cp note.txt note_copy.txt

# 複製多個檔案到目錄
mkdir backup
cp note.txt diary.md backup/

# 複製目錄（-r 代表遞迴）
cp -r backup backup_copy
```

*說明*：`cp` 的 `-r`（或 `-R`）選項讓目錄遞迴複製。若目標目錄不存在，`cp` 會自動建立。

---

## 4. 移動與重新命名

```sh
# 重新命名檔案
mv report.log final_report.log

# 移動檔案到另一目錄
mv note.txt backup/

# 同時移動並重新命名
mv diary.md backup/diary_2025.md
```

*說明*：`mv` 同時支援檔案的搬移與重新命名，目標路徑若是目錄則視為搬移。

---

## 5. 刪除檔案與安全刪除

```sh
# 刪除單一檔案（-i 會詢問確認）
rm -i final_report.log

# 刪除多個檔案
rm note_copy.txt backup/*.md

# 強制刪除（不會詢問，請小心使用）
rm -f *.log
```

*說明*：`rm` 的 `-i` 讓系統在刪除前提示確認，`-f` 則會忽略不存在的檔案並不提示。

---

## 6. 檢視檔案內容的進階指令

```sh
# 逐頁檢視（適合長檔案）
less diary.md

# 顯示行號
nl -ba diary.md

# 只顯示前 10 行或後 10 行
head -n 10 diary.md
tail -n 10 diary.md

# 同時查看檔案前後（-f 追蹤新增內容）
tail -f /var/log/syslog
```

*說明*：`less` 支援上下捲動與搜尋；`head`、`tail` 常用於快速檢視檔案首尾；`tail -f` 常用於監看日誌檔。

---

## 7. 使用文字編輯器（nano / vim）進行即時編輯

```sh
# 使用 nano（簡易、直觀）
nano note.txt

# 使用 vim（功能強大，適合進階使用者）
vim diary.md
```

*說明*：`nano` 友好且易上手，`vim` 具備大量快捷鍵與插件，適合長期開發。

---

## 8. 進階範例：結合管道與重定向

```sh
# 取得目前目錄下的 .md 檔，排序後寫入清單
ls *.md | sort > markdown_list.txt

# 用 grep 找出包含「Linux」的行，並寫入新檔
grep -i "linux" diary.md > linux_mentions.txt

# 使用 awk 只保留第一欄（檔名），再寫入檔案
awk '{print $1}' markdown_list.txt > filenames_only.txt
```

*說明*：管道 `|` 讓多個指令串接，`>` 重新導向輸出，`>>` 追加輸出。`grep`、`awk` 常用於文字處理。

---

## 9. 小結

- **`touch` / `echo`**：建立與寫入檔案  
- **`cat` / `less` / `head` / `tail`**：檢視檔案  
- **`cp` / `mv`**：複製與搬移  
- **`rm`**：刪除（建議使用 `-i`）  
- **文字編輯器**：`nano`、`vim`  
- **管道與重定向**：結合指令完成複雜任務  

在示範過程中，請隨時停下來提問「這個指令做了什麼？」、「為什麼要加這個參數？」以加深學生的概念理解。祝教學順利！
