import argparse
from pathlib import Path
import markdown
from weasyprint import HTML

CSS = '''
@page { size: A4; margin: 20mm 18mm; @bottom-center { content: counter(page); font-size: 9pt; color: #777; } }
body { font-family: "Noto Sans CJK SC", "Microsoft YaHei", "SimHei", sans-serif; font-size: 11pt; line-height: 1.75; color: #222; overflow-wrap: anywhere; }
h1,h2,h3 { color: #17365d; break-after: avoid; }
h1 { font-size: 22pt; border-bottom: 2px solid #17365d; padding-bottom: 8px; }
h2 { font-size: 16pt; margin-top: 22px; } h3 { font-size: 13pt; }
img { max-width: 100%; height: auto; display: block; margin: 12px auto; }
pre { background: #f3f5f7; padding: 12px; font-size: 9pt; white-space: pre-wrap; overflow-wrap: anywhere; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; }
th,td { border: 1px solid #bbb; padding: 7px; overflow-wrap: anywhere; }
th { background: #eaf0f6; } tr { break-inside: avoid; }
blockquote { border-left: 4px solid #999; padding-left: 12px; color: #555; }
'''

def convert(input_file, output_file=None):
    source = Path(input_file).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f'文件不存在: {source}')
    output = Path(output_file).expanduser().resolve() if output_file else source.with_suffix('.pdf')
    body = markdown.markdown(source.read_text(encoding='utf-8-sig'), extensions=['extra','tables','fenced_code','sane_lists','toc'])
    html = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=source.parent.as_uri() + '/').write_pdf(str(output))
    print(f'转换完成: {output}')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Markdown 转 PDF（支持中文、本地图片、表格）')
    p.add_argument('input', help='输入 Markdown 文件')
    p.add_argument('-o','--output', help='输出 PDF 路径')
    args = p.parse_args()
    try:
        convert(args.input,args.output)
    except Exception as exc:
        p.exit(1, f'转换失败: {exc}\n')
