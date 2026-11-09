import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from md2pdf import convert

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Markdown 转 PDF')
        self.geometry('660x330')
        self.minsize(560, 300)
        self.md = tk.StringVar()
        self.pdf = tk.StringVar()
        self.status = tk.StringVar(value='请选择 Markdown 文件')
        self.columnconfigure(1, weight=1)
        ttk.Label(self, text='Markdown 转 PDF', font=('Microsoft YaHei UI', 17, 'bold')).grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 18), sticky='w')
        ttk.Label(self, text='Markdown 文件').grid(row=1, column=0, padx=(20, 10), pady=7, sticky='w')
        ttk.Entry(self, textvariable=self.md).grid(row=1, column=1, sticky='ew', pady=7)
        ttk.Button(self, text='选择文件', command=self.choose_md).grid(row=1, column=2, padx=(10, 20), pady=7)
        ttk.Label(self, text='输出 PDF').grid(row=2, column=0, padx=(20, 10), pady=7, sticky='w')
        ttk.Entry(self, textvariable=self.pdf).grid(row=2, column=1, sticky='ew', pady=7)
        ttk.Button(self, text='保存位置', command=self.choose_pdf).grid(row=2, column=2, padx=(10, 20), pady=7)
        self.run = ttk.Button(self, text='开始转换', command=self.start)
        self.run.grid(row=3, column=0, columnspan=3, pady=18)
        ttk.Label(self, textvariable=self.status, wraplength=610).grid(row=4, column=0, columnspan=3, padx=20, sticky='w')
        ttk.Label(self, text='支持：中文 / A4 / 标题 / 表格 / 代码块 / 本地相对路径图片', foreground='#666').grid(row=5, column=0, columnspan=3, padx=20, pady=(20, 0), sticky='w')
        if len(sys.argv) > 1 and Path(sys.argv[1]).is_file():
            self.set_md(sys.argv[1])

    def set_md(self, filename):
        p = Path(filename).resolve()
        self.md.set(str(p))
        self.pdf.set(str(p.with_suffix('.pdf')))
        self.status.set('文件已选择，点击“开始转换”')

    def choose_md(self):
        p = filedialog.askopenfilename(title='选择 Markdown 文件', filetypes=[('Markdown', '*.md *.markdown'), ('所有文件', '*.*')])
        if p:
            self.set_md(p)

    def choose_pdf(self):
        p = filedialog.asksaveasfilename(title='保存 PDF', defaultextension='.pdf', filetypes=[('PDF 文件', '*.pdf')], initialfile=Path(self.pdf.get() or '输出.pdf').name)
        if p:
            self.pdf.set(p)

    def start(self):
        source = Path(self.md.get())
        if not source.is_file():
            messagebox.showerror('文件不存在', '请先选择有效的 Markdown 文件')
            return
        dest = Path(self.pdf.get() or str(source.with_suffix('.pdf')))
        self.run.configure(state='disabled')
        self.status.set('正在转换，请稍候……')
        threading.Thread(target=self.worker, args=(str(source), str(dest)), daemon=True).start()

    def worker(self, source, dest):
        try:
            convert(source, dest)
        except Exception as exc:
            self.after(0, lambda msg=str(exc): self.failed(msg))
        else:
            self.after(0, lambda: self.done(dest))

    def failed(self, msg):
        self.run.configure(state='normal')
        self.status.set('转换失败：' + msg)
        messagebox.showerror('转换失败', msg)

    def done(self, dest):
        self.run.configure(state='normal')
        self.status.set('转换成功：' + dest)
        messagebox.showinfo('转换成功', 'PDF 已生成：\n' + dest)

if __name__ == '__main__':
    App().mainloop()
