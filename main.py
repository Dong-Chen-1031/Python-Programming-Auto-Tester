import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
from datetime import datetime

# Rich imports for beautiful output
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.align import Align
from rich import box

# 初始化 rich console
# console = Console(markup=False)
console = Console()

CONFIG = r"E:\Dong\YTP\2023-1\config.json"

class MultiFileTestRunner:
    def __init__(self, config_file=CONFIG):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """載入配置檔案"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                
                problem_count = len(self.config.get('problems', {}))
                watch_dir = self.config.get('watch_directory', '.')
                
                console.print(f"✓ [green]載入配置檔案[/green]: [cyan]{problem_count}[/cyan] 個問題")
                console.print(f"📁 [blue]監控目錄[/blue]: [yellow]{watch_dir}[/yellow]")
                
                # 顯示問題列表
                if problem_count > 0:
                    problems_table = Table(title="📋 監控的問題列表", show_header=True, header_style="bold magenta")
                    problems_table.add_column("檔案名稱", style="cyan")
                    problems_table.add_column("問題名稱", style="green") 
                    problems_table.add_column("測試案例數", style="yellow")
                    
                    for filename, problem_config in self.config['problems'].items():
                        test_count = len(problem_config.get('test_cases', []))
                        problems_table.add_row(
                            filename,
                            problem_config.get('name', '未命名'),
                            str(test_count)
                        )
                    
                    console.print(problems_table)
                
            else:
                console.print("[yellow]⚠[/yellow] 配置檔案不存在，將建立範例配置")
                self.create_sample_config()
                
        except Exception as e:
            console.print(f"[red]✗[/red] 載入配置檔案失敗: {e}")
            self.config = {}
    
    def create_sample_config(self):
        """建立範例配置檔案"""
        sample_config = {
            "watch_directory": ".",
            "problems": {
                "solution.py": {
                    "name": "第K大元素問題",
                    "test_cases": [
                        {
                            "name": "基本測試",
                            "input": "5 3\n1 2 3 4 5",
                            "expected_output": "3"
                        },
                        {
                            "name": "相同數字",
                            "input": "3 2\n10 20 30", 
                            "expected_output": "20"
                        }
                    ]
                },
                "problem2.py": {
                    "name": "兩數之和問題",
                    "test_cases": [
                        {
                            "name": "基本測試",
                            "input": "4\n2 7 11 15\n9",
                            "expected_output": "0 1"
                        }
                    ]
                }
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, ensure_ascii=False, indent=2)
        
        self.config = sample_config
        console.print(f"✓ [green]建立範例配置檔案[/green]: {self.config_file}")
    
    def get_test_cases_for_file(self, file_path):
        """獲取指定檔案的測試案例"""
        filename = os.path.basename(file_path)
        problems = self.config.get('problems', {})
        
        if filename in problems:
            return problems[filename]
        else:
            console.print(f"[yellow]⚠[/yellow] 找不到 [bold]{filename}[/bold] 的測試案例配置")
            return None
    
    def get_watch_directory(self):
        """獲取監控目錄"""
        return self.config.get('watch_directory', '.')
    
    def run_tests(self, python_file):
        """執行指定檔案的測試案例"""
        if not os.path.exists(python_file):
            console.print(f"[red]✗[/red] 檔案不存在: {python_file}")
            return False
        
        # 獲取該檔案的測試配置
        problem_config = self.get_test_cases_for_file(python_file)
        if not problem_config:
            return False
        
        test_cases = problem_config.get('test_cases', [])
        problem_name = problem_config.get('name', '未命名問題')
        
        if not test_cases:
            console.print(f"[yellow]⚠[/yellow] {os.path.basename(python_file)} 沒有測試案例")
            return False
        
        # 建立測試標題面板
        title = Panel(
            Align.center(
                f"🧪 [bold blue]{problem_name}[/bold blue]\n"
                f"📄 檔案: [cyan]{os.path.basename(python_file)}[/cyan]\n"
                f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ),
            title="自動測試系統",
            border_style="blue",
            box=box.ROUNDED
        )
        console.print(title)
        
        # 建立測試結果表格
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("測試案例", style="cyan", width=20)
        table.add_column("狀態", width=10)
        table.add_column("執行時間", width=10)
        table.add_column("詳細資訊", style="dim")        
        passed = 0
        total = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            start_time = time.time()
            test_name = f"{i}/{total}: {test_case['name']}"
            
            try:
                # 執行 Python 程式 - 修正路徑和工作目錄問題
                # 確保使用絕對路徑執行檔案
                abs_python_file = os.path.abspath(python_file)
                
                # 修正工作目錄問題：
                # 1. 如果 watch_directory 不是當前目錄，使用項目根目錄作為工作目錄
                # 2. 否則使用檔案所在目錄作為工作目錄
                watch_dir = self.get_watch_directory()
                if watch_dir != '.':
                    # 監控的是子目錄，工作目錄應該是項目根目錄
                    working_dir = os.getcwd()
                else:
                    # 監控的是當前目錄，工作目錄使用檔案所在目錄
                    working_dir = os.path.dirname(abs_python_file) if os.path.dirname(abs_python_file) else os.getcwd()
                
                result = subprocess.run(
                    [sys.executable, abs_python_file],
                    input=test_case['input'],
                    capture_output=True,
                    text=True,
                    timeout=5,  # 5秒超時
                    cwd=working_dir
                )
                
                execution_time = f"{(time.time() - start_time)*1000:.1f}ms"
                
                if result.returncode != 0:
                    # 顯示完整錯誤訊息，延長長度限制
                    error_msg = result.stderr.strip()
                    # 如果錯誤訊息過長，保留更多內容但限制最大長度
                    if len(error_msg) > 800:
                        error_msg = error_msg[:800] + "\n... (錯誤訊息過長，已截斷)"
                    table.add_row(
                        test_name,
                        "[red]✗ 錯誤[/red]",
                        execution_time,
                        f"[red]程式執行錯誤:\n{error_msg}[/red]"
                    )
                    continue
                
                # 比較輸出
                actual_output = result.stdout.strip()
                expected_output = test_case['expected_output'].strip()
                
                if actual_output == expected_output:
                    table.add_row(
                        test_name,
                        "[green]✓ 通過[/green]",
                        execution_time,
                        "[green]輸出正確[/green]"
                    )
                    passed += 1
                else:
                    table.add_row(
                        test_name,
                        "[red]✗ 失敗[/red]",
                        execution_time,
                        f"[yellow]預期: {repr(expected_output)}\n實際: {repr(actual_output)}[/yellow]"
                    )
                    
            except subprocess.TimeoutExpired:
                execution_time = f"{(time.time() - start_time)*1000:.1f}ms"
                table.add_row(
                    test_name,
                    "[red]✗ 超時[/red]",
                    execution_time,
                    "[red]執行超過5秒[/red]"
                )
            except Exception as e:
                execution_time = f"{(time.time() - start_time)*1000:.1f}ms"
                # 顯示完整異常訊息，延長長度限制
                error_msg = str(e)
                if len(error_msg) > 300:
                    error_msg = error_msg[:300] + "\n... (錯誤訊息過長，已截斷)"
                table.add_row(
                    test_name,
                    "[red]✗ 錯誤[/red]",
                    execution_time,
                    f"[red]執行錯誤:\n{error_msg}[/red]"
                )
        
        console.print(table)
        
        # 顯示總結
        if passed == total:
            success_panel = Panel(
                f"🎉 [bold green]恭喜！所有測試都通過了！[/bold green]\n"
                f"✅ 通過: [green]{passed}[/green] / [blue]{total}[/blue] 個測試",
                title=f"[bold green]{problem_name} - 測試成功[/bold green]",
                border_style="green"
            )
            console.print(success_panel)
        else:
            failure_panel = Panel(
                f"❌ [bold red]部分測試失敗[/bold red]\n"
                f"✅ 通過: [green]{passed}[/green] / [blue]{total}[/blue] 個測試\n"
                f"❌ 失敗: [red]{total - passed}[/red] 個測試",
                title=f"[bold red]{problem_name} - 測試結果[/bold red]",
                border_style="red"
            )
            console.print(failure_panel)
        
        return passed == total

class MultiFileCodeMonitor(FileSystemEventHandler):
    def __init__(self):
        self.test_runner = MultiFileTestRunner()
        self.last_modified = {}
        self.watch_directory = self.test_runner.get_watch_directory()
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        
        # 如果是配置檔案被修改，重新載入
        if file_path.endswith(CONFIG):
            console.print("\n📋 [blue]檢測到配置檔案變更，重新載入...[/blue]")
            self.test_runner.load_config()
            self.watch_directory = self.test_runner.get_watch_directory()
            return
        
        # 只監控 Python 檔案，且排除系統檔案
        if (file_path.endswith('.py') and 
            not file_path.endswith('auto.py') and
            not file_path.endswith('auto_multi.py') and
            not file_path.endswith('auto_multi_fixed.py')):
            
            # 檢查檔案是否在監控目錄中
            abs_watch_dir = os.path.abspath(self.watch_directory)
            abs_file_path = os.path.abspath(file_path)
            
            # 判斷檔案是否在監控目錄下
            try:
                relative_path = os.path.relpath(abs_file_path, abs_watch_dir)
                if relative_path.startswith('..'):
                    return  # 檔案不在監控目錄中
            except ValueError:
                return  # 不同的磁碟機，跳過
            
            # 檢查是否有對應的測試配置
            filename = os.path.basename(file_path)
            if filename not in self.test_runner.config.get('problems', {}):
                return  # 沒有配置的檔案不進行測試
            
            # 避免重複觸發
            current_time = time.time()
            if file_path in self.last_modified:
                if current_time - self.last_modified[file_path] < 1:  # 1秒內不重複觸發
                    return
            
            self.last_modified[file_path] = current_time
            
            console.print(f"\n📝 [blue]檢測到檔案變更:[/blue] [bold]{filename}[/bold]")
            time.sleep(0.5)  # 等待檔案寫入完成
            
            # 執行測試
            self.test_runner.run_tests(file_path)

def main():
    # 顯示啟動橫幅
    startup_panel = Panel(
        Align.center(
            "[bold blue]🚀 多檔案程式解題自動測試系統[/bold blue]\n"
            "[dim]支援多檔案監控與個別測試配置[/dim]\n"
        ),
        border_style="cyan",
        box=box.DOUBLE
    )
    console.print(startup_panel)
    
    # 建立監控器
    event_handler = MultiFileCodeMonitor()    
    # 顯示系統資訊
    info_table = Table(show_header=False, box=box.SIMPLE)
    info_table.add_column("", style="cyan", width=15)
    info_table.add_column("", style="green")
    
    info_table.add_row("📁 監控目錄:", f"根目錄 + {event_handler.watch_directory}" if event_handler.watch_directory != "." else "根目錄（遞迴）")
    info_table.add_row("📄 監控檔案:", f"{CONFIG} + 配置的 Python 檔案")
    info_table.add_row("🐢 測試設定:", f"編輯 {CONFIG} 來修改問題配置")
    info_table.add_row("🛑 停止監控:", "按 Ctrl+C")
    
    console.print(info_table)
    console.print()
      # 設置文件監控 - 同時監控根目錄和指定目錄
    observer = Observer()
    
    # 監控根目錄（為了 config.json）
    observer.schedule(event_handler, path=".", recursive=False)
    
    # 如果指定的監控目錄不是根目錄，也監控該目錄
    if event_handler.watch_directory != ".":
        observer.schedule(event_handler, path=event_handler.watch_directory, recursive=True)
        console.print(f"[green]✓[/green] 同時監控根目錄和 [yellow]{event_handler.watch_directory}[/yellow] 目錄")
    else:
        console.print(f"[green]✓[/green] 監控根目錄 [yellow].[/yellow]（遞迴）")
    
    # 開始監控
    observer.start()
    
    try:
        with console.status("[bold green]🔍 監控中...", spinner="dots") as status:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️ 停止監控...[/yellow]")
        observer.stop()
    
    observer.join()
    
    # 顯示結束訊息
    goodbye_panel = Panel(
        Align.center("[bold green]👋 程式已結束，感謝使用！[/bold green]"),
        border_style="green"
    )
    console.print(goodbye_panel)

if __name__ == "__main__":
    main()
