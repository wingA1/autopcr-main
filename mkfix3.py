import pathlib

p = pathlib.Path(r"D:\\Desktop\\things\\autopcr-main\\AutoPCR_Web\\src\\components\\Account\\Area.tsx")
c = p.read_text(encoding="utf-8")
c = c.replace("return matchesSearch && matchesFilter;\n    });", "return matchesSearch && matchesFilter;\n    });\n    console.log('[DEBUG] filtered:', filtered.length, 'search:', searchQuery, 'filter:', filter);", 1)
p.write_text(c, encoding="utf-8", newline="")
print("Done")
