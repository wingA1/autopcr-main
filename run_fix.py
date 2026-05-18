import os, subprocess

root = r'D:\Desktop\things\autopcr-main\AutoPCR_Web'
src = os.path.join(root, 'src')

def rb(f):
    with open(os.path.join(src, f), 'rb') as fh:
        return fh.read()

def wb(f, c):
    with open(os.path.join(src, f), 'wb') as fh:
        fh.write(c)
    print('  wrote: ' + f)

def git_commit(msg):
    subprocess.run(['git', 'add', '-A'], cwd=root)
    r = subprocess.run(['git', 'commit', '-m', msg], cwd=root, capture_output=True, text=True)
    print('  commit: ' + r.stdout.strip())

def cn(codes):
    return ''.join(chr(c) for c in codes).encode('utf-8')

# Fix 1: Area.tsx - add Text import
data = rb('components/Account/Area.tsx')
data = data.replace(
    b"import { Box, Flex, IconButton, Popover, Stack, useDisclosure } from '@chakra-ui/react';",
    b"import { Box, Flex, IconButton, Popover, Stack, Text, useDisclosure } from '@chakra-ui/react';"
)
wb('components/Account/Area.tsx', data)

# Fix 2: DailyResult.tsx - add Tag import and fix status comparison
data = rb('components/Account/DailyResult.tsx')
data = data.replace(
    b"import {\r\n    Table,\r\n    TableRowProps,\r\n} from '@chakra-ui/react'",
    b"import {\r\n    Table,\r\n    Tag,\r\n    TableRowProps,\r\n} from '@chakra-ui/react'"
)
# Fix status comparison to use string cast
old_status = b"<Tag.Root size=\x22sm\x22 colorPalette={resultData.status === 'success' ? 'green' : resultData.status === 'failed' ? 'red' : 'yellow'}>"
new_status = b"<Tag.Root size=\x22sm\x22 colorPalette={String(resultData.status) === 'success' ? 'green' : String(resultData.status) === 'failed' ? 'red' : 'yellow'}>"
data = data.replace(old_status, new_status)
wb('components/Account/DailyResult.tsx', data)

# Fix 3: SideBar/Index.tsx - fix style attribute (string -> object)
data = rb('components/SideBar/Index.tsx')
old_style = b'style=\x22color:inherit;text-decoration:none;\x22'
new_style = b'style={{color: "inherit", textDecoration: "none"}}'
data = data.replace(old_style, new_style)
wb('components/SideBar/Index.tsx', data)

git_commit('fix: TS errors in Area/Tag import, DailyResult status type, SideBar style prop')
print('All TS fixes applied')