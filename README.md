# Markdown 转 PDF — Windows GUI 版

双击图形界面选择 `.md`，指定输出路径，点击“开始转换”。Markdown 中的 `![说明](./图片.png)` 相对路径以 MD 文件所在目录解析。

## 在 Windows 上生成 EXE

1. 安装 Python 3，勾选“Add Python to PATH”。
2. 解压工具包，在 Windows 上双击 `一键打包EXE.bat`。
3. 编译成功后使用 `dist\Markdown转PDF.exe`。

**说明：** Windows EXE 必须在 Windows 上构建并验证。WeasyPrint 依赖 Pango 等原生库，部分 Windows 环境需按官方文档安装相关运行库：https://doc.courtbouillon.org/weasyprint/stable/first_steps.html 。`--onefile` 不保证原生库全部自动捆绑。目标电脑的中文字体也会影响最终排版。

## 源码运行

```powershell
py -m pip install -r requirements.txt
py gui.py
```

## 其他

支持 A4、页码、标题、表格、代码块、PNG/JPG 相对路径图片。复杂 Mermaid、交互 HTML 不支持。仅转换可信的 Markdown 文件。
