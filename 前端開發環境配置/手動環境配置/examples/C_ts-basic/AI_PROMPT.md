# AI Prompt 參考：TypeScript 專案

## 使用說明

當你手動建立好 TypeScript 環境後，可以使用以下 prompt 讓 AI 幫你寫程式碼。

---

## Prompt 範例 1：基本 TypeScript

```
我已經建立了一個 TypeScript 專案，結構如下：
- src/main.ts（主程式）
- tsconfig.json（已配置）
- package.json（已設定編譯腳本）

請幫我：
1. 建立一個計算機類別（Calculator）
2. 包含加、減、乘、除方法
3. 所有方法都要有型別註解
4. 在 main.ts 中實例化並使用

環境資訊：
- TypeScript 5.0
- 編譯目標：ES2020
- 嚴格模式開啟
```

---

## Prompt 範例 2：介面和型別

```
我有一個 TypeScript 專案，想建立一個使用者管理系統。

請幫我建立：
1. 定義 User 介面（id, name, email, age）
2. 定義 UserService 類別，包含：
   - addUser(user: User): void
   - getUser(id: number): User | undefined
   - getAllUsers(): User[]
3. 在 main.ts 中測試這些功能

要求：
- 所有函數都要有完整的型別註解
- 使用 TypeScript 的嚴格模式
- 加上適當的註解
```

---

## Prompt 範例 3：模組化組織

```
我有一個 TypeScript 專案，想用模組化的方式組織程式碼。

專案結構：
- src/
  - main.ts（主程式）
  - types/（型別定義）
  - services/（服務類別）
  - utils/（工具函數）

請幫我建立一個待辦事項系統：
1. types/todo.ts - 定義 Todo 介面
2. services/todoService.ts - TodoService 類別（CRUD 操作）
3. utils/dateHelper.ts - 日期處理工具函數
4. main.ts - 整合以上模組

要求：
- 所有檔案都要有完整的型別
- 使用 ES Module（import/export）
- 編譯後要能在瀏覽器執行
```

---

## Prompt 範例 4：錯誤處理和型別安全

```
我有一個 TypeScript 專案，想建立一個表單驗證系統。

請幫我建立：
1. types/validation.ts - 定義驗證規則和錯誤型別
2. utils/validator.ts - 驗證函數（email、phone、password 等）
3. main.ts - 使用驗證函數

要求：
- 使用 TypeScript 的型別系統確保型別安全
- 錯誤訊息要有明確的型別
- 使用聯合型別（Union Types）處理不同的驗證結果
- 不使用 any 型別
```

---

## 使用技巧

### 1. 明確說明 TypeScript 版本和配置

```
✅ 好的描述：
「TypeScript 5.0，嚴格模式開啟，編譯目標 ES2020」

❌ 不好的描述：
「用 TypeScript」
```

### 2. 要求完整的型別註解

```
✅ 好的描述：
「所有函數都要有完整的型別註解，包括參數和返回值」

❌ 不好的描述：
「寫一些函數」
```

### 3. 說明編譯環境

```
✅ 好的描述：
「編譯後要能在瀏覽器執行，使用 ES Module」

❌ 不好的描述：
「寫程式碼」
```

### 4. 避免使用 any

```
✅ 好的描述：
「不使用 any 型別，使用明確的型別或 unknown」

❌ 不好的描述：
「隨便用型別」
```

---

## 常見問題

### Q: AI 給的程式碼沒有型別怎麼辦？

**A**: 明確要求：
```
「請為所有變數、函數參數、返回值加上完整的型別註解，
不要使用 any，使用明確的型別」
```

### Q: AI 給的程式碼編譯錯誤怎麼辦？

**A**: 提供錯誤訊息和配置：
```
「編譯時出現錯誤：xxx
我的 tsconfig.json 設定是：xxx
請修正程式碼以符合配置」
```

### Q: AI 使用了不存在的型別怎麼辦？

**A**: 要求檢查：
```
「這個型別不存在，請使用標準的 TypeScript 型別，
或定義這個型別」
```

---

## 進階 Prompt 範例

### 完整專案描述

```
我已經手動建立了一個 TypeScript 專案，環境如下：

專案結構：
- src/
  - main.ts
  - types/
  - services/
  - utils/
- tsconfig.json（已配置）
- package.json（已設定編譯腳本）

TypeScript 配置：
- 版本：5.0
- 嚴格模式：開啟
- 編譯目標：ES2020
- 模組系統：ES2020
- 輸出目錄：dist/

技術限制：
- 不使用框架
- 不使用 npm 套件（除了 TypeScript）
- 編譯後要能在瀏覽器執行
- 使用 ES Module

功能需求：
建立一個簡單的任務管理系統：
1. 定義 Task 介面（id, title, description, completed, dueDate）
2. TaskService 類別（CRUD 操作）
3. 日期處理工具（格式化、比較）
4. 在 main.ts 中整合並測試

要求：
1. 所有程式碼都要有完整的型別
2. 不使用 any 型別
3. 使用介面和型別別名
4. 加上適當的註解
5. 編譯後要能正常執行
```

---

## TypeScript 特定提示詞

### 要求型別推斷

```
「請利用 TypeScript 的型別推斷，在可以推斷的地方省略型別註解」
```

### 要求使用泛型

```
「請使用泛型（Generics）讓這個函數可以處理不同型別的資料」
```

### 要求使用聯合型別

```
「請使用聯合型別（Union Types）處理不同的狀態或結果」
```

### 要求使用介面

```
「請定義介面（Interface）來描述資料結構，而不是使用型別別名」
```

---

## 提示

1. **先配置環境**：確保 tsconfig.json 正確配置
2. **明確型別要求**：告訴 AI 你對型別的要求
3. **檢查編譯**：AI 給的程式碼要檢查是否能編譯
4. **理解型別**：不要只是複製，要理解型別的作用

---

**記住：TypeScript 的價值在於型別安全，要善用型別系統！**
