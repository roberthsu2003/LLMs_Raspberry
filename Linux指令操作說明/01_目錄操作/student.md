# 目錄操作練習 – 學生作業

以下題目請在你的 Raspberry Pi（或任何 Linux 終端）上逐一完成。每完成一題，請在終端機執行 `pwd` 或 `ls -l` 確認結果，並把螢幕輸出（或截圖）保存，作為作業回報的依據。

---

## 1️⃣ 基本定位

1. 打開終端機，使用 `pwd` 確認你目前所在的目錄。  
2. 輸入 `ls -a`，列出當前目錄下所有檔案（包括隱藏檔）。  
3. 複製當前路徑（例如 `~/Desktop`），貼到筆記本中。

---

## 2️⃣ 建立與切換多層目錄

1. 使用 `mkdir -p practice/step1/step2` 一次建立三層目錄。  
2. 用 `cd practice/step1/step2` 進入最底層目錄。  
3. 再次執行 `pwd`，確認你已在 `step2` 目錄。  
4. 使用 `cd ..` 回到 `step1`，檢查 `pwd` 是否正確。  
5. 用 `cd ../../` 回到 `practice` 目錄，最後回到家目錄 `cd ~`。

---

## 3️⃣ 列出特定檔案與目錄

1. 在 `practice` 目錄下，建立以下檔案：  
   ```sh
   touch fileA.txt fileB.log fileC.md
   mkdir dirA dirB
   ```  
2. 用 `ls *.txt` 只顯示 `.txt` 檔案。  
3. 用 `ls -d */` 列出所有子目錄（不顯示子目錄內的內容）。  
4. 用 `ls -l` 確認檔案與目錄的權限與擁有者。

---

## 4️⃣ 移除空目錄與清理

1. 使用 `rmdir dirA` 刪除剛才建立的空目錄 `dirA`。  
2. 嘗試直接 `rmdir practice`（應該會失敗，因為 `practice` 內仍有檔案）。觀察錯誤訊息。  
3. 用 `rm fileA.txt fileB.log fileC.md` 刪除所有檔案。  
4. 再次 `rmdir practice`，確認目錄已成功刪除。

---

## 5️⃣ 進階練習：使用 `tree`（若已安裝）

1. 若系統尚未安裝 `tree`，先執行 `sudo apt update && sudo apt install -y tree`。  
2. 在任意目錄（例如 `$HOME`）執行 `tree -L 2`，觀察兩層深度的樹狀結構。  
3. 嘗試 `tree -d -L 1` 只列出目錄名稱，不顯示檔案。

---

## 6️⃣ 小挑戰（加分題）

1. 建立一個名為 `project` 的目錄，裡面再建立 `src`、`docs`、`tests` 三個子目錄。  
2. 在 `src` 中建立 `main.py`，寫入以下內容：
   ```python
   print("Hello, Linux!")
   ```
3. 用 `chmod +x src/main.py` 讓它變成可執行檔。  
4. 使用 `./src/main.py` 執行，確認螢幕顯示 `Hello, Linux!`。  
5. 用 `tree -L 3 project` 檢查整個專案結構。

---

**作業提交**  
完成上述所有步驟後，請把以下資訊整理成一份報告（文字或 PDF）：

- 每一步的指令與輸出（可以使用終端機的「複製」功能或截圖）。
- 任何錯誤訊息與你是如何解決的（特別是第 4 題的錯誤）。
- 小挑戰的完成結果與感想。

祝你練習順利，期待看到你的作業！