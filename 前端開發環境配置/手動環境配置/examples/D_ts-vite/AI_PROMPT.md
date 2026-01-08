# AI Prompt 參考：TypeScript + Vite 專案

## 使用說明

當你手動建立好 TypeScript + Vite 環境後，可以使用以下 prompt 讓 AI 幫你寫程式碼。

---

## Prompt 範例 1：基本 Vite + TypeScript

```
我已經建立了一個 TypeScript + Vite 專案，結構如下：
- index.html（入口檔案）
- src/main.ts（主程式）
- vite.config.ts（已配置）
- tsconfig.json（已配置）

請幫我：
1. 在 main.ts 中建立一個簡單的計數器
2. 使用 TypeScript 的型別
3. DOM 操作和事件處理
4. 確保可以在 Vite 開發伺服器中正常執行

環境資訊：
- Vite 5.0
- TypeScript 5.0
- 開發伺服器：http://localhost:5173
```

---

## Prompt 範例 2：模組化組織

```
我有一個 TypeScript + Vite 專案，想用模組化的方式組織程式碼。

專案結構：
- src/
  - main.ts（主程式）
  - components/（元件）
  - utils/（工具函數）
  - types/（型別定義）

請幫我建立一個待辦事項應用：
1. types/todo.ts - 定義 Todo 介面
2. utils/todoStorage.ts - 本地儲存相關函數
3. components/todoList.ts - 待辦事項列表元件
4. main.ts - 整合所有模組

要求：
- 使用 TypeScript 完整型別
- 使用 ES Module
- 可以在 Vite 開發伺服器中即時預覽
- 修改程式碼後自動重新載入
```

---

## Prompt 範例 3：使用 Vite 的特性

```
我有一個 TypeScript + Vite 專案，想利用 Vite 的特性。

請幫我建立：
1. 一個簡單的圖片輪播功能
2. 使用 Vite 的靜態資源處理（圖片放在 public/ 或使用 import）
3. 使用 TypeScript 確保型別安全
4. 利用 Vite 的熱更新功能

環境資訊：
- Vite 5.0
- 開發模式：npm run dev
- 圖片資源：public/images/
```

---

## Prompt 範例 4：表單處理

```
我有一個 TypeScript + Vite 專案，想建立一個表單處理系統。

請幫我建立：
1. 一個聯絡表單（姓名、電子郵件、訊息）
2. 表單驗證（使用 TypeScript 型別確保資料正確）
3. 表單提交處理
4. 錯誤訊息顯示

要求：
- 使用 TypeScript 的型別系統
- 表單資料要有明確的介面定義
- 驗證邏輯要型別安全
- 可以在 Vite 開發伺服器中測試
```

---

## 使用技巧

### 1. 明確說明 Vite 環境

```
✅ 好的描述：
「我使用 Vite 5.0 作為開發工具，開發伺服器在 localhost:5173，
支援熱更新（HMR）」

❌ 不好的描述：
「用 Vite」
```

### 2. 說明檔案結構

```
✅ 好的描述：
「專案結構：
- index.html（入口，引用 /src/main.ts）
- src/main.ts（主程式）
- vite.config.ts（已配置）」

❌ 不好的描述：
「幫我寫程式碼」
```

### 3. 利用 Vite 的特性

```
✅ 好的描述：
「請使用 Vite 的靜態資源處理方式引入圖片，
可以利用 import 或放在 public/ 資料夾」

❌ 不好的描述：
「放圖片」
```

### 4. 說明開發流程

```
✅ 好的描述：
「使用 npm run dev 啟動開發伺服器，
修改程式碼後會自動重新載入」

❌ 不好的描述：
「寫程式碼」
```

---

## 常見問題

### Q: AI 給的程式碼無法在 Vite 中執行怎麼辦？

**A**: 明確說明 Vite 環境：
```
「這個專案使用 Vite，請確保：
1. 使用 ES Module（import/export）
2. 檔案路徑使用絕對路徑（/src/...）或相對路徑
3. 不要使用 require 或 CommonJS 語法」
```

### Q: AI 給的程式碼沒有利用 Vite 的特性怎麼辦？

**A**: 要求使用 Vite 特性：
```
「請利用 Vite 的特性：
1. 直接引用 TypeScript 檔案（不需要先編譯）
2. 使用 Vite 的靜態資源處理
3. 確保支援熱更新（HMR）」
```

### Q: 如何讓 AI 知道這是開發環境？

**A**: 明確說明：
```
「這是開發環境，使用 Vite 開發伺服器，
不需要考慮打包和優化，專注於開發體驗」
```

---

## 進階 Prompt 範例

### 完整專案描述

```
我已經手動建立了一個 TypeScript + Vite 專案，環境如下：

專案結構：
- index.html（入口檔案，引用 /src/main.ts）
- src/
  - main.ts（主程式）
  - components/（元件資料夾）
  - utils/（工具函數）
  - types/（型別定義）
- vite.config.ts（已配置）
- tsconfig.json（已配置）
- package.json（已設定腳本）

Vite 配置：
- 版本：5.0
- 開發伺服器：localhost:5173
- 支援熱更新（HMR）
- 支援 TypeScript 和 ES Module

TypeScript 配置：
- 版本：5.0
- 嚴格模式：開啟
- 編譯目標：ES2020

技術限制：
- 使用 TypeScript（完整型別）
- 使用 ES Module
- 不使用 React 或其他框架
- 純 TypeScript + DOM 操作

功能需求：
建立一個簡單的筆記應用：
1. 可以新增、編輯、刪除筆記
2. 筆記資料儲存在 localStorage
3. 可以搜尋筆記
4. 使用模組化方式組織程式碼

要求：
1. 所有程式碼都要有完整的 TypeScript 型別
2. 使用介面定義資料結構
3. 模組化組織（分成多個檔案）
4. 可以在 Vite 開發伺服器中正常執行
5. 修改程式碼後自動重新載入
```

---

## Vite 特定提示詞

### 利用熱更新

```
「請確保程式碼結構支援 Vite 的熱更新（HMR），
修改檔案後可以自動重新載入而不會丟失狀態」
```

### 使用靜態資源

```
「請使用 Vite 的方式引入靜態資源（圖片、CSS），
可以使用 import 或放在 public/ 資料夾」
```

### 開發 vs 建置

```
「這是開發環境，請專注於開發體驗，
不需要考慮打包和優化（建置時 Vite 會自動處理）」
```

---

## 提示

1. **先啟動開發伺服器**：使用 `npm run dev` 啟動後再請 AI 寫程式碼
2. **利用熱更新**：修改程式碼後觀察自動重新載入
3. **檢查型別**：確保 TypeScript 型別正確
4. **測試功能**：在瀏覽器中測試 AI 給的程式碼

---

**記住：Vite 提供優秀的開發體驗，要善用這些特性！**
