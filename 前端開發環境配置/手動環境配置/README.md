# 手動配置前端開發環境教學

> **本文不追求「最快做出專案」，而是帶你親手走過前端環境為什麼會變成今天這樣**

---

## 📚 教學定位

這是一份專為**已了解 HTML/JavaScript 基礎**的學生設計的前端環境配置教學。我們不會從零開始教程式語法，而是專注於理解：

- **為什麼**前端開發需要這些工具？
- **每個工具**解決了什麼問題？
- **如何組合**這些工具形成現代前端環境？

---

## 🎯 核心教學主軸

整份教學圍繞著這個核心觀念：

> **前端環境 = 語言 + 編譯 + 模組系統 + 開發工具 + 框架**

只要你能分清楚這五件事，後面不管是 Vite、Webpack、React、Vue，都不會怕。

### 五個層次說明

1. **語言**：JavaScript、TypeScript
2. **編譯**：將 TypeScript/JSX 轉換成瀏覽器能理解的 JavaScript
3. **模組系統**：ES Module、CommonJS、如何管理程式碼組織
4. **開發工具**：Vite、Webpack、開發伺服器、熱更新
5. **框架**：React、Vue、Angular

---

## 📖 學習路徑

### 建議學習順序

```
第 0 章：為什麼需要前端建置環境
    ↓
第 1 章：純 JavaScript 最小環境（建立基準）
    ↓
第 2 章：JavaScript + npm（發現問題）
    ↓
第 3 章：TypeScript 的本質（理解編譯）
    ↓
第 4 章：為什麼需要 Vite（工具整合）
    ↓
第 5 章：React 出現的理由（框架思維）
    ↓
第 6 章：React + JavaScript（框架實作）
    ↓
第 7 章：React + TypeScript（型別安全）
    ↓
第 8 章：完整現代環境（整合所有概念）
```

### 快速導航

- [📘 第 0 章：為什麼需要前端建置環境](./chapters/00_為什麼需要前端建置環境.md)
- [📘 第 1 章：純 JavaScript 最小環境](./chapters/01_純JavaScript最小環境.md)
- [📘 第 2 章：JavaScript 與 npm](./chapters/02_JavaScript與npm.md)
- [📘 第 3 章：TypeScript 的本質](./chapters/03_TypeScript的本質.md)
- [📘 第 4 章：為什麼需要 Vite](./chapters/04_為什麼需要Vite.md)
- [📘 第 5 章：React 出現的理由](./chapters/05_React出現的理由.md)
- [📘 第 6 章：React 與 JavaScript](./chapters/06_React與JavaScript.md)
- [📘 第 7 章：React 與 TypeScript](./chapters/07_React與TypeScript.md)
- [📘 第 8 章：完整現代環境](./chapters/08_完整現代環境.md)

---

## 🎓 各章節摘要

### 第 0 章：為什麼需要前端建置環境
理解「瀏覽器」與「開發環境」是兩個不同世界，建立「開發 → 建置 → 部署」的基本流程概念。

### 第 1 章：純 JavaScript 最小環境
建立「沒有任何工具時」的世界觀，理解現代瀏覽器已內建 ES Module 機制，但仍有其限制。

### 第 2 章：JavaScript 與 npm
理解 npm 的角色是「開發階段的套件管理」，知道為什麼瀏覽器不能直接讀 node_modules。

### 第 3 章：TypeScript 的本質
明確知道 TypeScript 只是 JavaScript 的超集，理解 tsc 的角色是「轉譯器」，TypeScript 永遠不會在瀏覽器執行。

### 第 4 章：為什麼需要 Vite
理解 Vite 解決的是「開發體驗」與「工具整合」問題，分清楚「開發伺服器」與「正式建置」的差異。

### 第 5 章：React 出現的理由
理解 React 解決的是「UI 複雜度」問題，建立 Component 與 State 的核心觀念。

### 第 6 章：React 與 JavaScript
讓學生實際感受「沒有工具時寫 React 的痛點」，理解 JSX 為什麼需要編譯。

### 第 7 章：React 與 TypeScript
理解型別如何幫助元件設計，知道 Props、State 為什麼需要型別。

### 第 8 章：完整現代環境
能清楚說出每一層技術在做什麼，理解現代前端專案的標準組成。

---

## 💻 實際範例專案

我們提供了 6 個實際可執行的範例專案，從最簡單到最複雜：

| 範例 | 技術組合 | 教學重點 | AI Prompt |
|------|---------|---------|----------|
| [A. 純 JavaScript](./examples/A_js-basic/) | 無任何工具 | 瀏覽器原生極限 | [📝](./examples/A_js-basic/AI_PROMPT.md) |
| [B. JavaScript + npm](./examples/B_js-npm/) | npm（不打包） | 套件世界的矛盾 | [📝](./examples/B_js-npm/AI_PROMPT.md) |
| [C. TypeScript 基礎](./examples/C_ts-basic/) | TypeScript（無框架） | 編譯的本質 | [📝](./examples/C_ts-basic/AI_PROMPT.md) |
| [D. TypeScript + Vite](./examples/D_ts-vite/) | TypeScript + Vite | 工具鏈整合 | [📝](./examples/D_ts-vite/AI_PROMPT.md) |
| [E. React + JavaScript](./examples/E_react-js/) | React + JS（最小） | JSX 為何不能直接跑 | [📝](./examples/E_react-js/AI_PROMPT.md) |
| [F. 完整現代環境](./examples/F_react-ts-vite/) | React + TS + Vite | 現代完整環境 | [📝](./examples/F_react-ts-vite/AI_PROMPT.md) |

👉 [查看所有範例專案總覽](./resources/範例專案總覽.md)

### 🤖 使用 AI 協助寫程式碼

**重要**：本教學的重點是「手動建立環境」，程式碼部分可以使用 AI 協助。

每個範例專案都包含 `AI_PROMPT.md` 檔案，提供：
- ✅ 如何向 AI 描述你的環境
- ✅ 如何向 AI 說明你的需求
- ✅ 如何確保 AI 給的程式碼符合你的環境
- ✅ 常見問題和解決方法

**使用流程**：
1. 手動建立環境（按照教學步驟）
2. 參考 `AI_PROMPT.md` 中的 prompt 範例
3. 使用 AI 協助寫程式碼
4. 檢查 AI 給的程式碼是否符合環境要求

---

## 📚 輔助教學資源

- [🎯 教學主軸說明](./resources/教學主軸說明.md) - 深入理解五個層次
- [📊 對照表：沒有 Vite vs 有 Vite](./resources/對照表_沒有Vite與有Vite.md) - 詳細對照分析
- [💡 教學技巧與常見問題](./resources/教學技巧與常見問題.md) - 課堂使用建議
- [📋 範例專案總覽](./resources/範例專案總覽.md) - 所有範例的快速參考

---

## 🎯 學習目標

完成這份教學後，你應該能夠：

- ✅ 清楚說出前端環境的五個層次
- ✅ 理解每個工具解決了什麼問題
- ✅ 知道為什麼需要編譯、打包、開發伺服器
- ✅ 能夠手動配置一個簡單的前端專案
- ✅ 理解現代前端工具鏈的工作原理
- ✅ 判斷何時該用、何時不需要這麼完整的環境

---

## 💡 使用建議

### 給學生

1. **按順序學習**：每章都建立在前一章的基礎上
2. **實際動手**：每個範例都要親自執行一次
3. **思考問題**：每章結尾的「常見迷思」要仔細閱讀
4. **不要跳過**：即使覺得簡單，也要完整走過一遍

### 給老師

1. **每章開頭**：先說明教學目標，告訴學生「這堂課要幹嘛」
2. **中間教學**：按照章節內容詳細講解
3. **結尾討論**：用「常見迷思」當 QA 討論
4. **實際操作**：讓學生跟著範例專案動手做

---

## 🚀 開始學習

準備好了嗎？讓我們從 [第 0 章：為什麼需要前端建置環境](./chapters/00_為什麼需要前端建置環境.md) 開始吧！

---

## 📝 授權與回饋

本教學文件採用 MIT 授權，歡迎自由使用、修改、分享。

如有問題或建議，歡迎提出 Issue 或 Pull Request。

---

**祝學習愉快！Happy Coding! 🚀**
