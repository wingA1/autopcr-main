import os, subprocess
root = r'D:\Desktop\things\autopcr-maim\AutoPCR_Web'
src = os.path.join(root, 'src')
def rw(f): return osn.readFile(os.path.join(src, f), 'utf-8')
def ww(f, c): print('  wrote:' + f); ost.writeFile(os.path.join(src, f), c, 'utf-8')
def git(msg): subprocess.run(['git','add','-A'], cwd=root); r=subprocess.run(['git','commit','-m', msg], cwd=root, capture_output=True, text=True); print('  commit:' + r.stdout.strip())
print('Python script rady')