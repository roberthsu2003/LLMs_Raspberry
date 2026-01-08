# AI Prompt 參考：React + JavaScript 專案

## 使用說明

當你手動建立好 React + Vite 環境後，可以使用以下 prompt 讓 AI 幫你寫程式碼。

---

## Prompt 範例 1：基本 React 元件

```
我已經建立了一個 React + Vite 專案，結構如下：
- index.html（入口檔案）
- src/main.jsx（主程式）
- vite.config.js（已配置 React 插件）

請幫我：
1. 建立一個簡單的計數器元件
2. 使用 useState 管理狀態
3. 有增加和減少按鈕
4. 顯示當前計數

環境資訊：
- React 18
- Vite 5.0
- 使用 JSX（不是 TypeScript）
- 開發伺服器：npm run dev
```

---

## Prompt 範例 2：多個元件

```
我有一個 React + Vite 專案，想建立多個元件。

專案結構：
- src/
  - main.jsx（主程式）
  - components/（元件資料夾）
    - Button.jsx
    - Card.jsx

請幫我建立：
1. Button 元件（可接收 text 和 onClick props）
2. Card 元件（可接收 title 和 content props）
3. 在 main.jsx 中使用這些元件

要求：
- 使用函數元件（Function Component）
- 使用 JSX 語法
- 元件要可重複使用
```

---

## Prompt 範例 3：狀態管理

```
我有一個 React + Vite 專案，想建立一個待辦事項應用。

請幫我建立：
1. TodoList 元件（顯示待辦事項列表）
2. TodoItem 元件（單個待辦事項）
3. AddTodo 元件（新增待辦事項的表單）
4. 使用 useState 管理待辦事項狀態

功能需求：
- 可以新增待辦事項
- 可以標記為完成/未完成
- 可以刪除待辦事項
- 狀態要持久化（使用 localStorage）

環境：
- React 18
- Vite 5.0
- 純 JavaScript（不使用 TypeScript）
```

---

## Prompt 範例 4：事件處理

```
我有一個 React + Vite 專案，想建立一個表單處理功能。

請幫我建立：
1. 一個聯絡表單元件
2. 表單欄位：姓名、電子郵件、訊息
3. 表單驗證
4. 提交處理

要求：
- 使用受控元件（Controlled Components）
- 使用 useState 管理表單狀態
- 提交時顯示成功訊息
- 表單驗證錯誤要顯示

環境：
- React 18
- Vite 5.0
- 純 JavaScript
```

---

## 使用技巧

### 1. 明確說明 React 版本

```
✅ 好的描述：
「React 18，使用函數元件和 Hooks」

❌ 不好的描述：
「用 React」
```

### 2. 說明是否使用 TypeScript

```
✅ 好的描述：
「純 JavaScript，不使用 TypeScript，檔案副檔名是 .jsx」

❌ 不好的描述：
「寫 React 元件」
```

### 3. 說明元件結構

```
✅ 好的描述：
「使用函數元件（Function Component），使用 Hooks（useState）」

❌ 不好的描述：
「寫元件」
```

### 4. 說明 Vite 環境

```
✅ 好的描述：
「使用 Vite 5.0，開發伺服器支援熱更新，
可以直接寫 JSX，Vite 會自動轉換」

❌ 不好的描述：
「用 Vite」
```

---

## 常見問題

### Q: AI 給的程式碼使用了 TypeScript 怎麼辦？

**A**: 明確要求：
```
「這個專案不使用 TypeScript，請使用純 JavaScript，
檔案副檔名是 .jsx，不要使用型別註解」
```

### Q: AI 給的程式碼無法在 Vite 中執行怎麼辦？

**A**: 檢查配置：
```
「請確保：
1. 使用 ES Module（import/export）
2. 使用 JSX 語法（Vite 會自動處理）
3. 檔案路徑正確（/src/...）」
```

### Q: AI 使用了類別元件怎麼辦？

**A**: 要求使用函數元件：
```
「請使用函數元件（Function Component）和 Hooks，
不要使用類別元件（Class Component）」
```

---

## 進階 Prompt 範例

### 完整專案描述

```
我已經手動建立了一個 React + Vite 專案，環境如下：

專案結構：
- index.html（入口檔案，引用 /src/main.jsx）
- src/
  - main.jsx（主程式）
  - components/（元件資料夾）
- vite.config.js（已配置 React 插件）
- package.json（已安裝 React 和 Vite）

環境資訊：
- React 18.2
- Vite 5.0
- 純 JavaScript（不使用 TypeScript）
- 檔案副檔名：.jsx
- 開發伺服器：npm run dev（localhost:5173）

技術限制：
- 使用函數元件（Function Component）
- 使用 Hooks（useState, useEffect 等）
- 不使用類別元件
- 不使用 TypeScript
- 使用 JSX 語法

功能需求：
建立一個簡單的部落格文章列表：
1. 從資料陣列讀取文章
2. 顯示文章標題、作者、日期、摘要
3. 點擊文章可以展開顯示完整內容
4. 可以搜尋文章（標題或內容）
5. 可以按作者篩選

要求：
1. 使用模組化方式組織元件
2. 每個元件放在獨立的檔案中
3. 使用 useState 管理狀態
4. 使用適當的 Hooks
5. 加上適當的註解
6. 可以在 Vite 開發伺服器中正常執行
```

---

## React 特定提示詞

### 使用 Hooks

```
「請使用 React Hooks（useState, useEffect）管理狀態和副作用，
不要使用類別元件」
```

### 元件化

```
「請將功能拆分成多個可重複使用的元件，
每個元件放在獨立的檔案中」
```

### 狀態提升

```
「請使用狀態提升（Lifting State Up）讓多個元件共享狀態」
```

### 受控元件

```
「請使用受控元件（Controlled Components）處理表單輸入」
```

---

## 提示

1. **先啟動開發伺服器**：使用 `npm run dev` 啟動
2. **利用熱更新**：修改 JSX 後觀察自動重新載入
3. **檢查 JSX 語法**：確保 JSX 語法正確
4. **測試元件**：在瀏覽器中測試元件功能

---

**記住：React 的核心是元件化，要善用元件和 Hooks！**
