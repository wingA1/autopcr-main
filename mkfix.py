import pathlib

p = pathlib.Path(r"D:\\Desktop\\things\\autopcr-main\\AutoPCR_Web\\src\\components\\Account\\Area.tsx")
c = p.read_text(encoding="utf-8")
c = c.replace("setConfig(res)", "setConfig(res); console.log('[DEBUG] config:', JSON.stringify(res).substring(0, 2000))", 1)
p.write_text(c, encoding="utf-8", newline="")
print("Done")
