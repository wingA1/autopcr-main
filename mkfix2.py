import pathlib

p = pathlib.Path(r"D:\\Desktop\\things\\autopcr-main\\AutoPCR_Web\\src\\components\\Account\\Area.tsx")
c = p.read_text(encoding="utf-8")
c = c.replace("const enabledCount = config.order.filter((k) => !!config.config[k]).length;", "const enabledCount = config.order.filter((k) => !!config.config[k]).length;\n    console.log('[DEBUG] order:', config.order.length, 'enabled:', enabledCount, 'config:', JSON.stringify(config.config).substring(0, 500));", 1)
p.write_text(c, encoding="utf-8", newline="")
print("Done")
