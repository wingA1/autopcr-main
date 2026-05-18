import os, subprocess

src = r'D:\Desktop\things\autopcr-main\AutoPCR_Web\src'

def rw(f):
    with open(os.path.join(src, f), 'r', encoding='utf-8') as fh:
        return fh.read()

def ww(f, c):
    with open(os.path.join(src, f), 'w', encoding='utf-8') as fh:
        fh.write(c)
    print('  wrote ' + f)

def git(msg):
    d = r'D:\Desktop\things\autopcr-main\AutoPCR_Web'
    subprocess.run(['git','add','-A'], cwd=d)
    r = subprocess.run(['git','commit','-m', msg], cwd=d, capture_output=True, text=True)
    print('  ' + r.stdout.strip())
    if r.returncode != 0 and 'nothing to commit' in r.stdout:
        print('  (no changes)')
    elif r.returncode != 0:
        print('  ERR: ' + r.stderr.strip())

# ============ P0 ============
print('=== P0 ===')

# P0-1: Login page
c = rw('components/Login/LoginWithPasswordComponent.tsx')
c = c.replace('label="QQ"', 'label="\u8d26\u53f7"')
c = c.replace("placeholder='5\u4f4d\u4ee5\u4e0a'", "placeholder='\u8bf7\u8f93\u5165\u8d26\u53f7ID\uff08\u6570\u5b57\uff09'")
c = c.replace("placeholder='8\u4f4d\u4ee5\u4e0a,\u975eQQ\u5bc6\u7801'", "placeholder='\u8bf7\u8f93\u5165\u5bc6\u7801\uff08\u81f3\u5c118\u4f4d\uff09'")
c = c.replace('\u7cfb\u7edf\u7ef4\u62a4\u4eba\u5458\u3002', '\u7ba1\u7406\u5458\u3002')
c = c.replace('>\u6ce8\u518c</Button>', 'variant="outline"\n                            loading={isSubmitting}\n                            onClick={handleSubmit(handleRegister)}\n                        >\n                            \u6ce8\u518c\u65b0\u8d26\u53f7\n                        </Button>')
ww('components/Login/LoginWithPasswordComponent.tsx', c)

# P0-2: APIUtils.ts - 429 retry
api = rw('api/APIUtils.ts')
old_module = "declare module 'axios' {\n    export interface AxiosRequestConfig {\n        /** \u662f\u5426\u8df3\u8fc7\u5168\u5c40\u9519\u8bef\u63d0\u793a */\n        skipErrorHandler?: boolean;\n        /** \u662f\u5426\u8df3\u8fc7 401 \u81ea\u52a8\u8df3\u8f6c */\n        skipAuthRedirect?: boolean;\n    }\n}"
new_module = "declare module 'axios' {\n    export interface AxiosRequestConfig {\n        skipErrorHandler?: boolean;\n        skipAuthRedirect?: boolean;\n        _retryCount?: number;\n    }\n}"
api = api.replace(old_module, new_module)

old_handler = "const errorHandler = (error: AxiosError) => {\n    // \u5982\u679c\u914d\u7f6e\u4e86 skipErrorHandler\uff0c\u5219\u4e0d\u8fdb\u884c\u5168\u5c40 toast \u63d0\u793a\n    if (!error.config?.skipErrorHandler) {\n        const message = getErrorMessage(error);\n        toaster.create({\n            title: \"\u64cd\u4f5c\u5931\u8d25\",\n            description: message,\n            type: \"error\",\n            duration: 4000,\n        });\n    }\n\n    // \u5904\u7406 401 \u672a\u6388\u6743\u60c5\u51b5\n    if (error.response?.status === 401 && !error.config?.skipAuthRedirect) {\n        if (window.location.pathname !== LoginRoute.to) {\n             window.location.href = LoginRoute.to;\n        }\n    }\n\n    return Promise.reject(error);\n};"

new_handler = "const MAX_429_RETRY = 2;\nconst RETRY_DELAY_MS = 1500;\n\nconst errorHandler = (error: AxiosError) => {\n    const status = error.response?.status;\n\n    if (status === 429) {\n        const retryCount = error.config?._retryCount ?? 0;\n        if (retryCount < MAX_429_RETRY) {\n            error.config!._retryCount = retryCount + 1;\n            toaster.create({\n                title: '\u64cd\u4f5c\u8fc7\u4e8e\u9891\u7e41',\n                description: '\u7cfb\u7edf\u7e41\u5fd9\uff0c' + (RETRY_DELAY_MS / 1000) + '\u79d2\u540e\u81ea\u52a8\u91cd\u8bd5 (' + (retryCount + 1) + '/' + MAX_429_RETRY + ')',\n                type: 'warning',\n                duration: 2000,\n            });\n            return new Promise((resolve) => {\n                setTimeout(() => {\n                    resolve(API.request(error.config!));\n                }, RETRY_DELAY_MS * (retryCount + 1));\n            });\n        }\n        if (!error.config?.skipErrorHandler) {\n            toaster.create({\n                title: '\u64cd\u4f5c\u8fc7\u4e8e\u9891\u7e41',\n                description: '\u8bf7\u6c42\u8fc7\u4e8e\u9891\u7e41\uff0c\u8bf7\u7a0d\u540e\u518d\u8bd5',\n                type: 'error',\n                duration: 4000,\n            });\n        }\n        return Promise.reject(error);\n    }\n\n    if (!error.config?.skipErrorHandler) {\n        const message = getErrorMessage(error);\n        toaster.create({\n            title: '\u64cd\u4f5c\u5931\u8d25',\n            description: message,\n            type: 'error',\n            duration: 4000,\n        });\n    }\n\n    if (status === 401 && !error.config?.skipAuthRedirect) {\n        if (window.location.pathname !== LoginRoute.to) {\n             window.location.href = LoginRoute.to;\n        }\n    }\n\n    return Promise.reject(error);\n};"

api = api.replace(old_handler, new_handler)

# Fix garbled Chinese text in getErrorMessage
api = api.replace('\u670d\u52a1\u5668\u65e0\u54cd\u5e94\uff0c\u8bf7\u68c0\u6d4b\u60a8\u7684\u7f51\u7edc\u8fde\u63a5', '\u670d\u52a1\u5668\u65e0\u54cd\u5e94\uff0c\u8bf7\u68c0\u67e5\u7f51\u7edc\u8fde\u63a5')

ww('api/APIUtils.ts', api)
git('P0: login labels fix, 429 retry with backoff, Chinese text cleanup')
print('=== P0 done ===')
