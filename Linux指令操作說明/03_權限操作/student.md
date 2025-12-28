# 權限操作練習 – 學生作業

以下題目請在你的 Linux 終端機（Raspberry Pi、Docker、或任何 Linux 環境）上依序完成。每完成一步，請使用 `ls -l`、`stat` 或將指令輸出截圖保存，作為作業回報的依據。

---

## 1️⃣ 檢視與理解預設權限

1. 建立一個測試檔 `demo.txt`（`touch demo.txt`）。  
2. 用 `ls -l demo.txt` 觀察權限欄位，記錄下顯示的 10 個字元（例：`-rw-r--r--`）。  
3. 用 `stat demo.txt` 取得更詳細資訊（特別是 **Uid**、**Gid**），寫下你的使用者名稱與群組名稱。

---

## 2️⃣ 符號式變更權限

1. 為 `demo.txt` **加入執行權限**（`chmod u+x demo.txt`），再次 `ls -l`，說明變化。  
2. **移除群組的寫入權限**（`chmod g-w demo.txt`），檢查結果。  
3. **給其他人加入執行權限**（`chmod o+x demo.txt`），確認 `ls -l` 中的最後一位是否為 `x`。  
4. 使用 **一次變更多組**：`chmod a+r demo.txt`（所有人都能讀），驗證。

---

## 3️⃣ 使用八進位模式設定常見權限

1. 把 `demo.txt` 的權限改為 **644**（`chmod 644 demo.txt`），說明每個數字代表的權限。  
2. 把 `demo.txt` 改為 **755**（`chmod 755 demo.txt`），觀察 `ls -l` 中的變化。  
3. 為 `demo.txt` 設定 **600**（`chmod 600 demo.txt`），確認只有所有者能讀寫。

---

## 4️⃣ 目錄的執行權限實作

1. 建立目錄 `secret_folder`（`mkdir secret_folder`）。  
2. 先只給所有者 **完全權限**（`chmod 700 secret_folder`），嘗試 `cd secret_folder`，確認可以進入。  
3. 把 **群組的執行權限** 加回（`chmod 750 secret_folder`），再用 `ls -ld secret_folder` 檢查。  
4. 嘗試以 **非擁有者**（如果有其他使用者可用 `su - otheruser`）`cd secret_folder`，觀察是否被拒絕，說明原因。

---

## 5️⃣ 改變擁有者與群組（需 sudo）

> **提示**：若你沒有 sudo 權限，請先向老師申請或在本機模擬使用 `sudo`。

1. 用 `sudo chown $(whoami):$(whoami) demo.txt` 把檔案的擁有者與群組改為自己（即使已是自己的也練習指令）。  
2. 用 `sudo chgrp staff demo.txt`（假設系統有 `staff` 群組），檢查 `ls -l` 中的群組欄位變化。  
3. 若你是管理員，嘗試把檔案的擁有者改成 `root`（`sudo chown root:root demo.txt`），然後以一般使用者執行 `ls -l demo.txt`，觀察權限與所有者的顯示。

---

## 6️⃣ 結合權限與執行腳本

1. 建立簡易腳本 `runme.sh`：

   ```sh
   #!/bin/bash
   echo "執行成功！"
   ```

2. 先 **只給自己執行權限**（`chmod 700 runme.sh`），嘗試 `./runme.sh`，觀察結果。  
3. 改成 **所有人可執行**（`chmod 755 runme.sh`），再次執行，說明差異。  
4. 把腳本的 **寫入權限移除**（`chmod a-w runme.sh`），嘗試編輯（`nano runme.sh`），確認系統阻止。

---

## 7️⃣ 小挑戰（加分題）

1. 在家目錄下建立 `project`，裡面依序建立 `src`、`docs`、`tests` 三個子目錄。  
2. 在 `src` 中建立 `app.py`，內容：

   ```python
   print("Hello, Linux!")
   ```

3. 設定 `app.py` 為 **所有人可讀、所有者可執行**（`chmod 744 app.py`），然後執行 `./src/app.py`（需要 `#!/usr/bin/env python3` 首行，若無則改為 `python3 src/app.py`）。  
4. 把 `src` 目錄的權限改為 **770**（`chmod 770 src`），讓群組成員也能執行腳本，驗證。

---

## 作業提交說明

完成所有練習後，請把以下資訊整理成一份報告（文字檔或 PDF）：

- 每一步的指令與對應輸出（可直接貼上終端機文字或截圖）。  
- 遇到的錯誤訊息與解決方式（特別是第 5 題的 sudo 操作）。  
- 加分挑戰的完成結果與個人感想。  

祝練習順利，期待看到你的作業！