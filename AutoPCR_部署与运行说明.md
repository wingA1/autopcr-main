
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


这份文档只解决一件事：

- 如何让 AutoPCR 在阿里云 Ubuntu 服务器上稳定运行

说明范围包括：

- 前端资源如何部署到服务器
- 后端服务如何启动
- `venv` 环境如何维护
- `systemd` 服务如何管理
- 更新版本后应该按什么顺序操作

不重点展开本地开发环境。

本地 Windows 机器只负责：

- 修改源码
- 构建前端
- 预览效果

最终是否成功，以服务器上的运行结果为准。

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


当前服务器上的项目根目录为：

```text
/home/pcr/autopcr-main
```

核心目录用途如下：

| 路径 | 作用 |
| --- | --- |
| `/home/pcr/autopcr-main` | 项目根目录 |
| `/home/pcr/autopcr-main/venv` | Python 虚拟环境 |
| `/home/pcr/autopcr-main/autopcr/http_server/ClientApp` | 前端静态资源目录 |
| `/home/pcr/autopcr-main/cache` | 缓存目录 |
| `/home/pcr/autopcr-main/log` | 日志目录 |
| `/home/pcr/autopcr-main/result` | 运行结果目录 |

当前服务托管方式为：

- `systemd`
- 服务名：`autopcr`

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


前端项目目录：

```text
D:\Desktop\things\autopcr-main\AutoPCR_Web
```

在本地执行：

```bash
npm.cmd run build
```

构建成功后，会生成最新静态资源。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


将构建结果整理为压缩包，例如：

```text
static.zip
```

上传到服务器项目根目录，例如：

```bash
scp "D:\Desktop\static.zip" root@<你的服务器IP>:/home/pcr/autopcr-main/
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


SSH 登录服务器后执行：

```bash
cd /home/pcr/autopcr-main
source venv/bin/activate
python3 _download_web.py ./static.zip
```

这一步会把前端资源释放到：

```text
/home/pcr/autopcr-main/autopcr/http_server/ClientApp
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


执行：

```bash
ls -lah /home/pcr/autopcr-main/autopcr/http_server/ClientApp
find /home/pcr/autopcr-main/autopcr/http_server/ClientApp -maxdepth 2 -type f | head -50
```

正常情况下，应能看到：

- `index.html`
- `assets/...`

如果这里没有内容，说明前端资源还没有真正部署完成。

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


服务器最终运行的不是本地环境，也不是 IDE 里的调试方式，而是服务器上的独立 Web 服务模式。

当前应使用的后端入口为：

```text
_httpserver_test.py
```

不再以 `server.py` 作为服务器主入口。

服务器最终正确启动命令应等价于：

```bash
/home/pcr/autopcr-main/venv/bin/python3 /home/pcr/autopcr-main/_httpserver_test.py
```

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


服务器使用的是：

- `venv`

不是：

- 本地 `conda`

因此判断依赖是否完整，必须以服务器 `venv` 为准。

进入虚拟环境命令：

```bash
cd /home/pcr/autopcr-main
source venv/bin/activate
```

查看当前 Python 路径：

```bash
which python3
python3 -V
pip -V
```

查看已安装依赖：

```bash
pip list
```

如果后续某次更新后出现缺包，补包操作也必须在这个 `venv` 中进行。

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```text
/etc/systemd/system/autopcr.service
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```ini
[Unit]
Description=AutoPCR Web Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pcr/autopcr-main
Environment="PYTHONPATH=/home/pcr/autopcr-main"
ExecStart=/home/pcr/autopcr-main/venv/bin/python3 /home/pcr/autopcr-main/_httpserver_test.py
Restart=always
RestartSec=5
MemoryMax=1G
CPUQuota=50%
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


修改服务文件后执行：

```bash
systemctl daemon-reload
systemctl restart autopcr
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
systemctl status autopcr --no-pager -l
journalctl -u autopcr -n 100 --no-pager
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
journalctl -u autopcr -f
```

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


以后每次更新，建议严格按下面顺序执行。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


本地只负责：

- 修改前端源码
- 构建前端
- 必要时修改后端文件
- 打包准备上传

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


将以下内容上传到服务器：

- 新的前端压缩包，例如 `static.zip`
- 必要时上传新的后端文件

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
ssh root@<你的服务器IP>
cd /home/pcr/autopcr-main
source venv/bin/activate
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
python3 _download_web.py ./static.zip
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


将新的后端代码同步到：

```text
/home/pcr/autopcr-main
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
find /home/pcr/autopcr-main/ -name "__pycache__" -exec rm -rf {} +
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
systemctl daemon-reload
systemctl restart autopcr
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
systemctl status autopcr --no-pager -l
journalctl -u autopcr -n 100 --no-pager
```

如果服务正常，说明更新闭环完成。

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
systemctl status autopcr --no-pager -l
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
systemctl start autopcr
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
systemctl restart autopcr
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
systemctl stop autopcr
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
journalctl -u autopcr -n 100 --no-pager
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
journalctl -u autopcr -f
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
ss -ltnp | grep 13200
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
ps -ef | grep -i "autopcr\|python" | grep -v grep
```

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


下面这些判断，是当前可以继续复用的。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


关键路径：

```text
/home/pcr/autopcr-main/autopcr/http_server/ClientApp
```

只要这里没有正确落盘，页面就不可能真正更新成功。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


不要再用本地环境去推断服务器依赖。

服务器能不能跑，只看：

- `venv` 里装了什么
- `journalctl` 里报了什么

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


不要只看代码目录是否存在。

最终判断标准是：

- `systemctl status autopcr`
- `journalctl -u autopcr`

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


本地构建成功不等于上线成功。

真正有效的结果永远是：

- 服务器静态资源在
- 服务起来了
- 页面能打开
- API 能响应

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


在之前排障过程中，有些方向是阶段性推演，现在不需要继续当作主线。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


本地只是辅助构建与预览。

这份手册不再围绕本地怎么跑展开。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


中间的分析过程对排障有用，但正式手册只保留：

- 能复用的步骤
- 能落地的命令
- 能直接执行的维护动作

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


如果服务器已经能稳定运行，后续更重要的是：

- 如何复用现有部署方式
- 如何减少下次升级成本
- 如何快速排查下一次报错

而不是继续停留在理论层面拆解每个历史分支。

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


当前 AutoPCR 的最终交付逻辑可以概括为：

1. 本地负责构建前端和准备更新文件。
2. 所有最终结果都要上传并落盘到阿里云 Ubuntu 服务器。
3. 服务器通过 `venv` 提供 Python 运行环境。
4. 服务器通过 `systemd` 托管 `autopcr` 服务。
5. 前端是否生效，看 `ClientApp` 是否更新。
6. 后端是否正常，看 `autopcr.service` 和 `journalctl` 日志。

后续只要按这份手册执行，服务器端的更新、重启和维护就可以形成稳定闭环。

---

#
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


这一章专门记录本次升级过程中已经真实遇到过的问题。

目的不是回顾排障历史，而是为了让后续升级时，能更快定位问题、少走弯路。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


- 本地 `npm.cmd run build` 已成功
- 浏览器打开服务器页面后，还是旧界面
- 或者页面直接 404 / 空白

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


最常见原因不是前端没编译成功，而是：

- 静态资源没有真正落盘到服务器后端期望目录
- 或者上传的是源码，不是构建后的静态产物

服务器最终需要的不是前端源码目录，而是：

```text
/home/pcr/autopcr-main/autopcr/http_server/ClientApp
```

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
cd /home/pcr/autopcr-main
source venv/bin/activate
python3 _download_web.py ./static.zip
ls -lah /home/pcr/autopcr-main/autopcr/http_server/ClientApp
find /home/pcr/autopcr-main/autopcr/http_server/ClientApp -maxdepth 2 -type f | head -50
```

确认目录里至少存在：

- `index.html`
- `assets/...`

如果没有，说明前端资源并未真正部署成功。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


- 服务器 `systemd` 启动失败
- `journalctl -u autopcr` 中出现 `ModuleNotFoundError`
- 本地环境却能正常跑

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


这是服务器升级时最容易遇到的问题之一。

根因通常不是代码本身坏了，而是：

- 本地环境比服务器环境更完整
- 本地是历史累积环境
- 服务器是新建 `venv`
- 因此本地“顺带有”的包，在服务器里并不存在

判断依赖是否齐全，必须只看服务器 `venv`，不能看本地 `conda`。

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


```bash
cd /home/pcr/autopcr-main
source venv/bin/activate
python3 -V
pip list
journalctl -u autopcr -n 100 --no-pager
```

缺什么补什么，并始终在服务器 `venv` 中执行安装。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


- 服务能启动一点，但很快因为导入或上下文问题崩溃
- 或者报一串与入口方式相关的错误

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


这次升级中，一个核心教训就是：

- 服务器最终应跑独立 Web 服务入口
- 不应继续把 `server.py` 当成服务器主入口

当前服务器最终正确入口应为：

```text
_httpserver_test.py
```

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


检查 `/etc/systemd/system/autopcr.service` 中的 `ExecStart` 是否为：

```ini
ExecStart=/home/pcr/autopcr-main/venv/bin/python3 /home/pcr/autopcr-main/_httpserver_test.py
```

如果不是，优先修正服务脚本，再重载重启。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


日志中出现类似：

```text
ModuleNotFoundError: No module named 'cv2'
```

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


新版功能链路引入了图像识别能力，而服务器又是无桌面环境，因此默认不会自带 OpenCV。

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


在服务器 `venv` 中安装轻量无桌面版本：

```bash
source /home/pcr/autopcr-main/venv/bin/activate
pip install opencv-python-headless
```

后续如果再升级环境，只要再次出现 `cv2` 缺失，优先按这个方案补齐。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


可能出现：

- Pillow 相关报错
- 字体渲染异常
- 图像扩展加载异常

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


这类问题一般不是业务逻辑问题，而是：

- 系统底层库没装全
- Pillow 在旧环境里编译结果不完整
- 更新系统库后，需要重新安装 Pillow

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


先补系统依赖，再在 `venv` 中强制重装 Pillow。

系统依赖示例：

```bash
apt update
apt install -y libfreetype6 libfreetype6-dev zlib1g-dev libjpeg-dev
```

重装 Pillow：

```bash
source /home/pcr/autopcr-main/venv/bin/activate
pip uninstall -y pillow
pip install --no-cache-dir --force-reinstall pillow
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


- 文件明明已经替换
- 服务也重启了
- 但表现仍像旧版本

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


常见原因有两个：

- `__pycache__` 残留
- 实际重启的不是你当前这份工作目录对应的服务

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


先清理缓存：

```bash
find /home/pcr/autopcr-main/ -name "__pycache__" -exec rm -rf {} +
```

再确认服务配置：

```bash
systemctl cat autopcr
systemctl status autopcr --no-pager -l
```

确认 `WorkingDirectory` 和 `ExecStart` 都指向：

```text
/home/pcr/autopcr-main
```

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


升级后整体异常，但一时无法判断是：

- 前端没更新
- 后端没启动
- 接口没通
- 服务没重载

###
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


按下面顺序排查，不要跳步：

```bash

## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)

ls -lah /home/pcr/autopcr-main/autopcr/http_server/ClientApp


## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)

systemctl status autopcr --no-pager -l


## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)

journalctl -u autopcr -n 100 --no-pager


## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)

ss -ltnp | grep 13200


## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)

ps -ef | grep -i "autopcr\|python" | grep -v grep
```

后续维护时，建议严格遵守这个顺序，而不是一上来就反复改代码。

##
## GitHub 仓库地址

- 后端仓库：[wingA1/autopcr-main](https://github.com/wingA1/autopcr-main)
- 前端仓库：[wingA1/AutoPCR_Web](https://github.com/wingA1/AutoPCR_Web)


下面这些内容在排障阶段讨论过，但后续维护时不必再当成主线：

- 不必再围绕本地怎么跑展开讨论
- 不必再把所有历史推演重新走一遍
- 不必把每次异常都先归因到源码结构

后续运维的核心原则应保持简单：

1. 先看前端资源是否落盘
2. 再看 `venv` 依赖是否齐全
3. 再看 `systemd` 服务是否正常
4. 最后看日志报错具体指向什么

只要这四层按顺序排，升级维护就会清晰很多。


