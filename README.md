# 🏆 Python 程式自動測試系統

一個功能強大的 Python 程式自動化測試系統，支援檔案監控和美觀的測試結果顯示。**不僅適用於程式競賽，更是日常程式解題、演算法學習、程式練習的絕佳工具！**

## 🎯 適用場景

- 🏆 **程式競賽**: ACM、ICPC、AtCoder、Codeforces 等競賽練習
- 📚 **演算法學習**: 資料結構與演算法課程作業和練習
- 🎯 **程式解題**: LeetCode、HackerRank、CodeWars 等平台練習
- 🔬 **程式開發**: 任何需要快速測試多組輸入輸出的 Python 程式
- 👨‍🎓 **教學輔助**: 教師批改作業、學生自我檢測

## ✨ 功能特色

- 🔍 **智慧檔案監控**: 使用 `watchdog` 監控 Python 檔案變更，支援多檔案同時監控
- 🧪 **自動測試執行**: 檔案儲存時自動執行預定義的測試案例，即時獲得反饋
- 🎨 **美觀的輸出介面**: 使用 `rich` 函式庫提供豐富的終端顯示效果和彩色輸出
- ⚙️ **彈性配置系統**: JSON 配置檔案管理，支援多問題、多測試案例配置
- 📊 **詳細測試報告**: 顯示測試結果、執行時間、錯誤訊息和詳細比對結果
- 🏃‍♂️ **即時反饋機制**: 程式碼修改後立即獲得測試結果，提升開發效率
- 🚦 **錯誤處理**: 完善的超時處理、執行錯誤捕捉和錯誤訊息顯示

## 📋 系統需求

- Python 3.7 或以上版本
- Windows/Linux/macOS 作業系統
- 終端機或命令列環境

## 🚀 快速開始

### 1. 下載專案

```bash
# 如果您有 Git
git clone https://github.com/your-username/python-auto-tester.git
cd python-auto-tester

# 或者直接下載 ZIP 檔案並解壓縮
```

### 2. 安裝相依套件

```bash
pip install -r requirements.txt
```

相依套件說明：
- `watchdog==4.0.0`: 檔案系統監控套件
- `rich==13.7.0`: 美觀終端輸出套件

### 3. 立即開始使用

```bash
python main.py
```

首次執行會自動建立範例配置檔案 `config.json`，您可以參考範例進行修改。

## 🎯 使用說明

### 快速開始

1. **執行程式**
   ```bash
   python main.py
   ```

2. **編輯配置檔案**  
   系統會自動建立 `config.json` 範例檔案，包含詳細的配置說明。

3. **開始編寫程式**  
   在監控目錄中編寫您的 Python 程式，每次儲存時會自動執行測試。

### 配置檔案結構

系統使用 JSON 配置檔案來定義測試案例，預設配置檔案為 `config.json`：

```json
{
  "watch_directory": ".",  // 監控目錄，"." 表示當前目錄
  "problems": {
    "solution.py": {  // 要測試的 Python 檔案名稱
      "name": "兩數之和問題",  // 問題的顯示名稱
      "test_cases": [
        {
          "name": "基本測試",  // 測試案例名稱
          "input": "4\n2 7 11 15\n9",  // 輸入資料
          "expected_output": "0 1"  // 預期輸出
        },
        {
          "name": "邊界測試",
          "input": "2\n3 3\n6",
          "expected_output": "0 1"
        }
      ]
    },
    "algorithm.py": {
      "name": "快速排序演算法",
      "test_cases": [
        {
          "name": "一般陣列",
          "input": "5\n64 34 25 12 22",
          "expected_output": "12 22 25 34 64"
        }
      ]
    }
  }
}
```

### 配置參數詳解

| 參數 | 說明 | 範例 |
|------|------|------|
| `watch_directory` | 監控的目錄路徑 | `"."` (當前目錄) 或 `"problems"` |
| `problems` | 問題配置物件 | 包含所有要測試的檔案配置 |
| `檔案名稱` | Python 檔案名稱 | `"solution.py"`, `"main.py"` |
| `name` | 問題的顯示名稱 | `"兩數之和"`, `"快速排序"` |
| `test_cases` | 測試案例陣列 | 包含多組輸入輸出測試 |
| `input` | 輸入資料 | 支援多行輸入，使用 `\n` 換行 |
| `expected_output` | 預期輸出結果 | 與程式實際輸出進行比對 |

## 📁 專案結構

```
python-auto-tester/
├── main.py              # 主程式檔案
├── requirements.txt     # Python 相依套件清單
├── config.json         # 測試配置檔案（自動建立）
├── README.md           # 說明文件
├── LICENSE             # 授權條款
└── your-solutions/     # 您的程式解題目錄（可選）
    ├── problem1.py
    ├── problem2.py
    └── ...
```

### 檔案說明

- **main.py**: 核心程式，包含檔案監控、測試執行和結果顯示功能
- **requirements.txt**: 相依套件清單，使用 `pip install -r requirements.txt` 安裝
- **config.json**: 測試配置檔案，定義要監控的檔案和測試案例
- **LICENSE**: MIT 授權條款

## 💡 使用範例

### 範例 1：LeetCode 兩數之和問題

1. **建立程式檔案 `two_sum.py`：**
```python
def two_sum(nums, target):
    num_dict = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_dict:
            return [num_dict[complement], i]
        num_dict[num] = i
    return []

# 讀取輸入
n = int(input())
nums = list(map(int, input().split()))
target = int(input())

# 執行並輸出結果
result = two_sum(nums, target)
print(' '.join(map(str, result)))
```

2. **修改 `config.json`：**
```json
{
  "watch_directory": ".",
  "problems": {
    "two_sum.py": {
      "name": "LeetCode - 兩數之和",
      "test_cases": [
        {
          "name": "範例測試 1",
          "input": "4\n2 7 11 15\n9",
          "expected_output": "0 1"
        },
        {
          "name": "範例測試 2", 
          "input": "3\n3 2 4\n6",
          "expected_output": "1 2"
        }
      ]
    }
  }
}
```

3. **執行測試系統：**
```bash
python main.py
```

現在每次您儲存 `two_sum.py` 檔案時，系統會自動執行測試並顯示結果！

### 範例 2：競賽程式設計

適用於 ACM、ICPC、AtCoder 等競賽平台的練習：

```json
{
  "watch_directory": "contest",
  "problems": {
    "a.py": {
      "name": "Problem A - 簡單加法",
      "test_cases": [
        {"name": "測試 1", "input": "1 2", "expected_output": "3"},
        {"name": "測試 2", "input": "10 20", "expected_output": "30"}
      ]
    },
    "b.py": {
      "name": "Problem B - 字串處理", 
      "test_cases": [
        {"name": "測試 1", "input": "hello", "expected_output": "HELLO"},
        {"name": "測試 2", "input": "world", "expected_output": "WORLD"}
      ]
    }
  }
}
```

## 🔧 系統核心功能

### 主要元件

1. **MultiFileTestRunner 類別**
   - 載入和管理 JSON 配置檔案
   - 執行測試案例並捕捉程式輸出
   - 比對實際輸出與預期輸出
   - 生成美觀的測試報告

2. **MultiFileCodeMonitor 類別** 
   - 繼承自 watchdog 的 FileSystemEventHandler
   - 監控 Python 檔案的變更事件
   - 自動觸發測試執行
   - 防止重複觸發機制

3. **智慧配置管理**
   - 自動載入 JSON 配置檔案
   - 支援多問題、多測試案例配置
   - 自動建立範例配置檔案
   - 即時重新載入配置變更

### 測試執行流程

1. 📁 監控指定目錄的 Python 檔案變更
2. 🔍 檢測到檔案儲存事件後觸發測試
3. 📋 載入該檔案對應的測試配置
4. ⚡ 執行 Python 程式並傳入測試輸入
5. 📊 比對實際輸出與預期輸出
6. 🎨 生成美觀的測試結果報告
7. ⏱️ 記錄執行時間和錯誤訊息

## 🎨 介面效果展示

系統提供豐富的視覺化輸出效果：

- 📋 **啟動橫幅**: 顯示系統資訊和功能介紹
- 📊 **問題列表表格**: 顯示所有監控的問題及測試案例數量
- 🧪 **測試結果面板**: 美觀的測試執行結果展示
- ⏱️ **執行時間統計**: 每個測試案例的詳細執行時間
- ✅/❌ **狀態指示器**: 清晰的通過/失敗狀態顯示
- 🔄 **即時監控狀態**: 動態的監控進度指示器
- 🎯 **錯誤詳情**: 完整的錯誤訊息和比對結果

### 支援的測試狀態

- ✅ **通過**: 輸出完全匹配預期結果
- ❌ **失敗**: 輸出與預期不符，顯示差異比對
- 🚫 **錯誤**: 程式執行時發生異常或語法錯誤
- ⏰ **超時**: 程式執行超過 5 秒鐘限制

## 🚀 進階使用技巧

### 多檔案同時監控

您可以在配置檔案中設定多個檔案同時監控：

```json
{
  "watch_directory": "solutions",
  "problems": {
    "easy_problem.py": { "name": "簡單題目", "test_cases": [...] },
    "medium_problem.py": { "name": "中等題目", "test_cases": [...] },
    "hard_problem.py": { "name": "困難題目", "test_cases": [...] }
  }
}
```

### 複雜輸入輸出處理

支援多行輸入和複雜的資料格式：

```json
{
  "test_cases": [
    {
      "name": "矩陣輸入測試",
      "input": "3 3\n1 2 3\n4 5 6\n7 8 9",
      "expected_output": "1 4 7\n2 5 8\n3 6 9"
    }
  ]
}
```

### 效能測試

系統會自動記錄每個測試案例的執行時間，幫助您優化程式效能。

### 錯誤除錯

當程式發生錯誤時，系統會顯示：
- 完整的錯誤訊息
- 錯誤發生的行號
- 執行時間統計
- 輸入輸出比對結果

## 🔧 故障排除

### 常見問題

**Q: 為什麼程式沒有自動執行測試？**
A: 請檢查：
- 檔案名稱是否與 config.json 中的配置一致
- 檔案是否保存在正確的監控目錄中
- 配置檔案格式是否正確

**Q: 測試一直顯示失敗怎麼辦？**
A: 請檢查：
- 輸出格式是否完全匹配（包括空白字元）
- 程式是否正確讀取輸入
- 是否有多餘的除錯輸出

**Q: 如何處理程式執行超時？**
A: 目前超時限制為 5 秒，您可以：
- 優化演算法複雜度
- 檢查是否有無限迴圈
- 確認輸入格式正確

## 🤝 參與貢獻

我們歡迎所有形式的貢獻！無論您是：

- 🐛 **回報 Bug**: 發現問題請建立 Issue
- 💡 **功能建議**: 有新想法歡迎分享
- 📝 **文件改進**: 幫助完善說明文件
- 🔧 **程式碼貢獻**: 提交 Pull Request

### 貢獻步驟

1. Fork 此專案到您的 GitHub 帳號
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的變更 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

## 📄 授權條款

此專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🙏 致謝

感謝以下優秀的開源專案讓本系統得以實現：

- [watchdog](https://github.com/gorakhargosh/watchdog) - 強大的檔案系統監控套件
- [rich](https://github.com/Textualize/rich) - 美觀的終端輸出和格式化套件

## 📞 聯絡與支援

如果您在使用過程中遇到任何問題，或有功能建議，歡迎透過以下方式聯絡：

- 📋 **GitHub Issues**: [建立新的 Issue](https://github.com/Dong-Chen-1031/Python-Programming-Auto-Tester/issues)

## 🌟 專案特色總結

✨ **為什麼選擇這個自動測試系統？**

1. **🎯 多用途**: 不只是競賽工具，更是日常程式練習的好幫手
2. **🚀 效率提升**: 自動化測試讓您專注於演算法邏輯，不用手動複製貼上測試資料
3. **🎨 用戶體驗**: Rich 套件提供的美觀介面讓測試過程更加愉悅
4. **🔧 易於配置**: JSON 配置檔案簡單易懂，快速上手
5. **⚡ 即時反饋**: 程式碼修改後立即獲得測試結果
6. **🛡️ 錯誤處理**: 完善的異常處理和錯誤訊息顯示

---

⭐ **如果這個專案對您有幫助，請給我們一顆星星！您的支持是我們持續改進的動力！**

🚀 **立即開始您的程式解題之旅吧！**
