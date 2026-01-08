# AI Prompt 參考：React + TypeScript + Vite 專案

## 使用說明

當你手動建立好完整的 React + TypeScript + Vite 環境後，可以使用以下 prompt 讓 AI 幫你寫程式碼。

---

## Prompt 範例 1：基本 React + TypeScript 元件

```
我已經建立了一個 React + TypeScript + Vite 專案，結構如下：
- index.html（入口檔案）
- src/main.tsx（主程式）
- src/App.tsx（主應用元件）
- vite.config.ts（已配置 React 插件）
- tsconfig.json（已配置）

請幫我：
1. 建立一個計數器元件（Counter）
2. 使用 TypeScript 定義 Props 和 State 的型別
3. 使用 useState Hook
4. 有增加和減少按鈕

環境資訊：
- React 18
- TypeScript 5.0
- Vite 5.0
- 嚴格模式開啟
```

---

## Prompt 範例 2：型別安全的元件

```
我有一個 React + TypeScript + Vite 專案，想建立型別安全的元件。

專案結構：
- src/
  - components/（元件資料夾）
    - Button.tsx
    - Card.tsx

請幫我建立：
1. Button 元件
   - Props 介面：{ text: string; onClick: () => void; variant?: 'primary' | 'secondary' }
   - 使用 TypeScript 確保型別安全
2. Card 元件
   - Props 介面：{ title: string; content: string; onClose?: () => void }
   - 使用 TypeScript 確保型別安全

要求：
- 所有 Props 都要有明確的介面定義
- 使用 TypeScript 的型別系統
- 不使用 any 型別
- 可選屬性使用 ? 標記
```

---

## Prompt 範例 3：完整的應用

```
我有一個 React + TypeScript + Vite 專案，想建立一個待辦事項應用。

請幫我建立：
1. types/todo.ts - 定義 Todo 介面
2. components/TodoList.tsx - 待辦事項列表元件
3. components/TodoItem.tsx - 單個待辦事項元件
4. components/AddTodo.tsx - 新增待辦事項表單
5. App.tsx - 整合所有元件

功能需求：
- 可以新增待辦事項
- 可以標記為完成/未完成
- 可以刪除待辦事項
- 可以編輯待辦事項
- 狀態持久化（localStorage）

要求：
- 所有資料結構都要有 TypeScript 介面
- 所有元件 Props 都要有型別
- 使用 useState 和 useEffect Hooks
- 型別安全，不使用 any
```

---

## Prompt 範例 4：表單處理和驗證

```
我有一個 React + TypeScript + Vite 專案，想建立一個表單處理系統。

請幫我建立：
1. types/form.ts - 定義表單資料和驗證錯誤的型別
2. components/ContactForm.tsx - 聯絡表單元件
3. utils/validation.ts - 驗證函數（型別安全）

表單欄位：
- 姓名（必填，至少 2 個字）
- 電子郵件（必填，格式驗證）
- 訊息（必填，至少 10 個字）

要求：
- 使用 TypeScript 確保表單資料型別安全
- 驗證錯誤要有明確的型別
- 使用受控元件
- 即時驗證和提交前驗證
```

---

## 使用技巧

### 1. 明確說明技術棧

```
✅ 好的描述：
「React 18 + TypeScript 5.0 + Vite 5.0，
使用函數元件和 Hooks，嚴格模式開啟」

❌ 不好的描述：
「用 React」
```

### 2. 要求完整的型別

```
✅ 好的描述：
「所有 Props、State、函數參數和返回值都要有完整的 TypeScript 型別，
不使用 any 型別」

❌ 不好的描述：
「寫元件」
```

### 3. 說明元件結構

```
✅ 好的描述：
「使用函數元件（Function Component），
使用 Hooks（useState, useEffect），
每個元件放在獨立的 .tsx 檔案中」

❌ 不好的描述：
「寫 React 元件」
```

### 4. 說明型別要求

```
✅ 好的描述：
「使用介面（Interface）定義 Props，
使用型別別名（Type Alias）定義複雜型別，
可選屬性使用 ? 標記」

❌ 不好的描述：
「加型別」
```

---

## 常見問題

### Q: AI 給的程式碼沒有型別怎麼辦？

**A**: 明確要求：
```
「請為所有變數、函數參數、返回值、Props、State 加上完整的 TypeScript 型別，
不使用 any，使用明確的型別或 unknown」
```

### Q: AI 使用了 any 型別怎麼辦？

**A**: 要求避免 any：
```
「請避免使用 any 型別，使用明確的型別、unknown 或泛型」
```

### Q: AI 給的程式碼編譯錯誤怎麼辦？

**A**: 提供錯誤訊息：
```
「TypeScript 編譯錯誤：xxx
請修正程式碼，確保型別正確」
```

### Q: AI 沒有使用 React Hooks 的正確型別怎麼辦？

**A**: 要求正確的型別：
```
「請使用 React 的型別定義，
例如：useState<number>(0) 而不是 useState(0)，
確保型別推斷正確」
```

---

## 進階 Prompt 範例

### 完整專案描述

```
我已經手動建立了一個完整的 React + TypeScript + Vite 專案，環境如下：

專案結構：
- index.html（入口檔案，引用 /src/main.tsx）
- src/
  - main.tsx（主程式）
  - App.tsx（主應用元件）
  - components/（元件資料夾）
  - types/（型別定義）
  - utils/（工具函數）
- vite.config.ts（已配置 React 插件）
- tsconfig.json（已配置）
- package.json（已安裝所有依賴）

環境資訊：
- React 18.2
- TypeScript 5.0
- Vite 5.0
- 嚴格模式：開啟
- 開發伺服器：npm run dev（localhost:3000）

技術限制：
- 使用函數元件（Function Component）
- 使用 Hooks（useState, useEffect 等）
- 不使用類別元件
- 完整的 TypeScript 型別
- 不使用 any 型別

功能需求：
建立一個完整的部落格管理系統：
1. 文章列表頁面
   - 顯示所有文章（標題、作者、日期、摘要）
   - 可以搜尋文章（標題或內容）
   - 可以按作者或分類篩選
2. 文章詳情頁面
   - 顯示完整文章內容
   - 可以編輯文章
   - 可以刪除文章
3. 新增/編輯文章表單
   - 標題、作者、分類、內容
   - 表單驗證
   - 儲存到 localStorage

資料結構：
- Article 介面：id, title, author, category, content, createdAt, updatedAt
- Category 型別：'tech' | 'life' | 'travel' | 'food'

要求：
1. 所有資料結構都要有 TypeScript 介面定義
2. 所有元件 Props 都要有明確的介面
3. 使用 useState 和 useEffect 管理狀態
4. 表單驗證要有型別安全的錯誤處理
5. 使用模組化方式組織程式碼
6. 加上適當的註解
7. 可以在 Vite 開發伺服器中正常執行
8. 修改程式碼後自動重新載入
```

---

## React + TypeScript 特定提示詞

### Props 型別

```
「請為所有元件的 Props 定義介面（Interface），
可選屬性使用 ? 標記，使用聯合型別處理不同的變體」
```

### State 型別

```
「請為 useState 明確指定型別，
例如：useState<number>(0) 或 useState<Todo[]>([])」
```

### 事件處理

```
「請為事件處理函數使用正確的型別，
例如：React.ChangeEvent<HTMLInputElement>」
```

### 泛型元件

```
「請使用泛型（Generics）讓這個元件可以處理不同型別的資料」
```

### 自訂 Hooks

```
「請建立一個自訂 Hook，並為它定義明確的返回型別」
```

---

## 提示

1. **先啟動開發伺服器**：使用 `npm run dev` 啟動
2. **檢查型別**：確保所有型別都正確
3. **利用 IDE**：使用 IDE 的型別提示和自動完成
4. **測試功能**：在瀏覽器中測試元件功能
5. **理解型別**：不要只是複製，要理解型別的作用

---

## 型別檢查清單

在請 AI 寫程式碼前，確認：

- [ ] 所有 Props 都有介面定義
- [ ] 所有 State 都有明確型別
- [ ] 所有函數參數和返回值都有型別
- [ ] 沒有使用 any 型別
- [ ] 事件處理函數有正確的型別
- [ ] 可選屬性使用 ? 標記
- [ ] 使用聯合型別處理不同的變體

---

**記住：React + TypeScript 的價值在於型別安全的元件開發，要善用型別系統！**
