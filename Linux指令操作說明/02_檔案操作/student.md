# 檔案操作練習 – 學生實作手冊

歡迎來到檔案操作實作練習！檔案是 Linux 系統中儲存資訊的基本單位，掌握檔案操作技能是成為 Linux 使用者的重要一步。請在您的 Raspberry Pi（或任何 Linux 終端）上逐一完成以下任務。

---

## 📋 練習前準備

在開始之前，請先建立練習環境：

```sh
# 建立練習目錄
mkdir -p ~/file_practice
cd ~/file_practice

# 確認目前位置
pwd
```

---

## 1️⃣ 基礎檔案建立 – 建立你的第一個檔案

### 任務目標
學會使用 `touch` 和 `echo` 建立檔案並寫入內容。

### 操作步驟
1. 使用 `touch` 建立三個空檔案：
   ```sh
   touch note.txt diary.md todo.log
   ```

2. 使用 `ls -l` 確認檔案已建立

3. 使用 `echo` 向 `note.txt` 寫入內容：
   ```sh
   echo "這是我的第一份 Linux 筆記" > note.txt
   ```

4. 使用 `cat` 檢視檔案內容：
   ```sh
   cat note.txt
   ```

### 預期結果
- 成功建立三個空檔案
- 能夠向檔案寫入文字內容
- 能夠檢視檔案內容

### 自我檢查
- [ ] 我能使用 `touch` 建立空檔案
- [ ] 我能使用 `echo` 寫入內容到檔案
- [ ] 我能使用 `cat` 檢視檔案內容

---

## 2️⃣ 檔案內容追加 – 豐富你的筆記

### 任務目標
學會保留原有內容並追加新內容。

### 操作步驟
1. 檢視目前的 `note.txt` 內容：
   ```sh
   cat note.txt
   ```

2. 使用 `>>` 追加新內容：
   ```sh
   echo "學習日期：$(date)" >> note.txt
   echo "學習內容：檔案操作指令" >> note.txt
   ```

3. 再次檢視檔案內容，確認內容已追加：
   ```sh
   cat note.txt
   ```

4. 使用 `>` 測試覆蓋寫入：
   ```sh
   echo "這會覆蓋原有內容" > note.txt
   cat note.txt
   ```

### 預期結果
- 理解 `>>` 和 `>` 的差異
- 能夠正確地追加內容到檔案
- 了解覆蓋寫入的效果

### 自我檢查
- [ ] 我了解 `>>` 和 `>` 的區別
- [ ] 我能正確地追加內容到檔案
- [ ] 我知道何時使用覆蓋寫入

---

## 3️⃣ 多行內容寫入 – 建立完整的日誌

### 任務目標
學會使用 here-document 一次寫入多行內容。

### 操作步驟
1. 使用 here-document 建立日記檔案：
   ```sh
   cat <<EOF > diary.md
   # 今日學習日誌
   
   ## 日期
   $(date)
   
   ## 學習內容
   - 檔案建立 (touch)
   - 內容寫入 (echo)
   - 內容檢視 (cat)
   
   ## 心得
   檔案操作是 Linux 的基礎技能！
   EOF
   ```

2. 檢視建立的檔案：
   ```sh
   cat diary.md
   ```

3. 使用 `nl` 顯示行號：
   ```sh
   nl -ba diary.md
   ```

### 預期結果
- 能夠使用 here-document 建立多行內容
- 理解 `EOF` 標記的作用
- 能夠使用 `nl` 顯示行號

### 自我檢查
- [ ] 我能使用 here-document 寫入多行內容
- [ ] 我了解 `EOF` 標記的用途
- [ ] 我能使用 `nl` 顯示檔案行號

---

## 4️⃣ 檔案複製與備份 – 保護重要資料

### 任務目標
學會複製檔案和建立備份。

### 操作步驟
1. 建立備份目錄：
   ```sh
   mkdir backup
   ```

2. 複製單一檔案：
   ```sh
   cp note.txt note_backup.txt
   ```

3. 複製多個檔案到備份目錄：
   ```sh
   cp diary.md todo.log backup/
   ```

4. 檢視備份目錄內容：
   ```sh
   ls -l backup/
   ```

5. 遞迴複製整個目錄：
   ```sh
   cp -r backup backup_copy
   tree
   ```

### 預期結果
- 能夠複製單一和多個檔案
- 能夠建立目錄備份
- 理解遞迴複製的概念

### 自我檢查
- [ ] 我能複製單一檔案
- [ ] 我能複製多個檔案到目錄
- [ ] 我能使用 `-r` 參數複製目錄

---

## 5️⃣ 檔案移動與重新命名 – 整理你的檔案

### 任務目標
學會移動檔案和重新命名。

### 操作步驟
1. 重新命名檔案：
   ```sh
   mv todo.log task_list.txt
   ls -l
   ```

2. 移動檔案到備份目錄：
   ```sh
   mv task_list.txt backup/
   ls -l backup/
   ```

3. 同時移動並重新命名：
   ```sh
   mv diary.md backup/diary_$(date +%Y%m%d).md
   ls -l backup/
   ```

4. 建立新目錄並移動檔案：
   ```sh
   mkdir important
   mv backup/diary_*.md important/
   tree
   ```

### 預期結果
- 能夠重新命名檔案
- 能夠移動檔案到不同目錄
- 能夠同時執行移動和重新命名

### 自我檢查
- [ ] 我能重新命名檔案
- [ ] 我能移動檔案到其他目錄
- [ ] 我能同時執行移動和重新命名

---

## 6️⃣ 檔案檢視進階技巧 – 閱讀長文件

### 任務目標
學會使用各種工具檢視檔案內容。

### 操作步驟
1. 建立一個較長的檔案：
   ```sh
   for i in {1..50}; do echo "這是第 $i 行內容"; done > long_file.txt
   ```

2. 使用 `head` 查看前 10 行：
   ```sh
   head -n 10 long_file.txt
   ```

3. 使用 `tail` 查看後 10 行：
   ```sh
   tail -n 10 long_file.txt
   ```

4. 使用 `less` 逐頁檢視：
   ```sh
   less long_file.txt
   # 按空白鍵翻頁，按 q 離開
   ```

5. 使用 `wc` 統計檔案資訊：
   ```sh
   wc -l long_file.txt  # 行數
   wc -w long_file.txt  # 字數
   wc -c long_file.txt  # 字元數
   ```

### 預期結果
- 能夠使用 `head` 和 `tail` 查看檔案部分內容
- 能夠使用 `less` 瀏覽長檔案
- 能夠使用 `wc` 統計檔案資訊

### 自我檢查
- [ ] 我能使用 `head` 查看檔案開頭
- [ ] 我能使用 `tail` 查看檔案結尾
- [ ] 我能使用 `less` 瀏覽長檔案
- [ ] 我能使用 `wc` 統計檔案資訊

---

## 7️⃣ 檔案刪除與安全操作 – 謹慎清理空間

### 任務目標
學會安全地刪除檔案。

### 操作步驟
1. 使用互動模式刪除檔案：
   ```sh
   touch temp1.txt temp2.txt
   rm -i temp1.txt
   # 輸入 y 確認刪除
   ```

2. 刪除多個檔案：
   ```sh
   rm temp2.txt note_backup.txt
   ```

3. 嘗試刪除不存在的檔案：
   ```sh
   rm nonexistent.txt  # 應該會顯示錯誤
   rm -f nonexistent.txt  # 使用 -f 不會顯示錯誤
   ```

4. 清理練習檔案：
   ```sh
   ls
   # 謹慎檢查後刪除不需要的檔案
   rm -i *.txt *.md *.log
   ```

### 預期結果
- 理解 `rm` 指令的危險性
- 能夠使用互動模式安全刪除
- 了解 `-f` 參數的作用

### 自我檢查
- [ ] 我了解 `rm` 指令的危險性
- [ ] 我能使用 `-i` 參數安全刪除
- [ ] 我知道何時使用 `-f` 參數

---

## 8️⃣ 文字編輯器實戰 – 選擇你的工具

### 任務目標
學會使用文字編輯器編輯檔案。

### 操作步驟
1. 使用 nano 建立和編輯檔案：
   ```sh
   nano my_notes.txt
   # 輸入以下內容：
   # Hello from nano!
   # This is a simple text editor.
   # Ctrl+O 儲存，Ctrl+X 離開
   ```

2. 檢視編輯結果：
   ```sh
   cat my_notes.txt
   ```

3. （可選）嘗試 vim 編輯器：
   ```sh
   vim practice.txt
   # 按 i 進入插入模式
   # 輸入內容
   # 按 Esc，然後輸入 :wq 儲存並離開
   ```

4. 如果 vim 太困難，可以執行 `vimtutor` 學習基礎操作：
   ```sh
   vimtutor
   ```

### 預期結果
- 能夠使用 nano 編輯檔案
- 了解 vim 的基本概念
- 知道如何選擇適合的編輯器

### 自我檢查
- [ ] 我能使用 nano 編輯檔案
- [ ] 我了解 vim 的基本操作
- [ ] 我知道如何選擇適合的編輯器

---

## 9️⃣ 進階挑戰 – 綜合應用

### 任務目標
綜合運用所學技能完成實際任務。

### 操作步驟
1. 建立專案結構：
   ```sh
   mkdir -p my_project/{docs,src,data}
   ```

2. 建立 README 檔案：
   ```sh
   cat <<EOF > my_project/README.md
   # My Project
   
   ## 簡介
   這是一個練習檔案操作的專案。
   
   ## 檔案結構
   - docs/ : 文件目錄
   - src/  : 原始碼目錄
   - data/ : 資料目錄
   
   ## 作者
   $(whoami)
   EOF
   ```

3. 建立設定檔：
   ```sh
   echo "PROJECT_NAME=File Practice" > my_project/config.env
   echo "VERSION=1.0" >> my_project/config.env
   echo "AUTHOR=$(whoami)" >> my_project/config.env
   ```

4. 建立資料檔案：
   ```sh
   echo "data1,value1" > my_project/data/sample.csv
   echo "data2,value2" >> my_project/data/sample.csv
   echo "data3,value3" >> my_project/data/sample.csv
   ```

5. 檢視專案結構：
   ```sh
   tree my_project/
   ```

6. 使用管道和重定向建立檔案清單：
   ```sh
   find my_project -type f > my_project/file_list.txt
   cat my_project/file_list.txt
   ```

### 預期結果
- 能夠建立完整的專案結構
- 能夠使用各種檔案操作指令
- 能夠組合多個指令完成複雜任務

### 自我檢查
- [ ] 我能建立完整的專案結構
- [ ] 我能使用管道和重定向
- [ ] 我能組合多個指令完成任務

---

## 🔟 綜合挑戰 – 檔案管理大師

### 任務目標
完成一個完整的檔案管理任務。

### 挑戰任務
1. 建立一個名為 `challenge` 的目錄
2. 在該目錄中建立 10 個測試檔案（test1.txt 到 test10.txt）
3. 建立一個 `summary.txt`，包含所有檔案的清單
4. 建立 `backup` 目錄，複製所有 .txt 檔案到備份目錄
5. 刪除原始目錄中編號為偶數的檔案
6. 將備份目錄重新命名為 `archives`
7. 建立一個 `report.txt`，記錄所有操作的指令和結果

### 提示
- 使用迴圈建立多個檔案
- 使用 `ls` 和重定向建立清單
- 使用萬用字元篩選檔案
- 記錄每個步驟的指令

### 自我檢查
- [ ] 我能使用迴圈建立多個檔案
- [ ] 我能使用萬用字元篩選檔案
- [ ] 我能記錄操作過程
- [ ] 我能完成複雜的檔案管理任務

---

## 📝 作業提交要求

完成所有練習後，請整理一份學習報告：

### 1. 操作記錄
- 每個任務的主要指令和輸出
- 使用截圖或文字複製方式記錄

### 2. 問題與解決
- 遇到的錯誤訊息
- 解決問題的方法
- 學到的經驗教訓

### 3. 學習心得
- 最困難的部分是什麼？
- 最實用的指令是什麼？
- 有什麼新的發現或技巧？

### 4. 挑戰任務成果
- 綜合挑戰的完整過程
- 最終的目錄結構
- `report.txt` 的內容

---

## 💡 學習提示

1. **安全第一**：使用 `rm -i` 或先備份再刪除
2. **多做實驗**：嘗試不同的參數組合
3. **善用幫助**：`man <指令>` 查閱手冊
4. **記錄筆記**：保存有用的指令和技巧
5. **舉一反三**：思考指令的其他應用場景

---

## 🎯 學習目標檢核

完成所有練習後，您應該能夠：

- [ ] 使用 `touch` 建立空檔案
- [ ] 使用 `echo` 寫入檔案內容
- [ ] 使用 `cat` 檢視檔案內容
- [ ] 使用 `cp` 複製檔案和目錄
- [ ] 使用 `mv` 移動和重新命名檔案
- [ ] 使用 `rm` 刪除檔案（安全地）
- [ ] 使用 `head`、`tail`、`less` 檢視檔案
- [ ] 使用 `nano` 編輯檔案
- [ ] 使用重定向和管道
- [ ] 建立和管理專案檔案結構

祝您練習順利！期待看到您的學習成果！