<div align="center">

# 水管剪辑 AI 剪辑 Skill

**让 AI 使用真正的水管剪辑 / FreeCut，交付视频和可继续编辑的工程。**

[简体中文](README.md) · [English](README.en.md)

[下载 Skill](https://github.com/Watertube-bilibili/shuiguan-cut-skill/releases/tag/v0.6.0) · [水管剪辑](https://github.com/Watertube-bilibili/freecut-desktop) · [GitHub Star](https://github.com/Watertube-bilibili/shuiguan-cut-skill)

</div>

你提供本地视频、图片、音频和剪辑要求，AI 生成配方，再启动独立的水管剪辑进程完成导入、保存工程与导出。交付 `project.freecut` 和 `render.mp4`；可以回到软件中继续修改。

**Skill 0.6.0 对应 FreeCut 0.6.0。全部功能永久免费，不设会员、不设付费解锁，不默认添加水印。** 这个下载包只有 AI 操作说明和自动化脚本，不包含 FreeCut 应用、Node.js、Electron、Playwright、FFmpeg 或 AI 模型。

## 可以做什么

| 能力 | 当前配方桥接支持 |
| --- | --- |
| 基础剪辑 | 本地素材导入、按入点剪切、顺序拼接、分层叠加 |
| 画面与文字 | 文字、色块、位置、统一缩放、旋转、透明度 |
| 动画与声音 | 上述变换及音量关键帧、固定变速、淡入淡出、左右声道参数 |
| 交付 | 可编辑 `.freecut` 工程、H.264/AAC MP4、预览图和验证报告 |
| 分辨率与帧率 | 720 / 1080 / 1440 / 2160 短边档位，24 / 25 / 30 / 50 / 60 fps；长边受产品 3840 像素限制 |

导出由产品自动选择原生 FFmpeg 合成或 Canvas 逐帧合成，再通过产品导出器完成。这个 Skill 没有复制一套独立渲染器。

**尚未自动操作**蒙版、调色、转场、曲线变速、AI 模型下载、语音识别、语音朗读或复杂时间线交互；应用本身的能力不等于配方桥接全部支持。未知配方字段会报错，不会静默忽略。

## 安装 Skill

1. 下载 Release 中的 **[shuiguan-cut.zip](https://github.com/Watertube-bilibili/shuiguan-cut-skill/releases/download/v0.6.0/shuiguan-cut.zip)**。不要把 GitHub 自动生成的源码 ZIP 当成同样的目录结构。
2. 将压缩包中的整个 `shuiguan-cut` 文件夹放到 Codex 的 `skills` 目录：默认是用户目录下的 `.codex/skills`；设置了 `CODEX_HOME` 时是 `$CODEX_HOME/skills`。
3. 确认最终结构为 `skills/shuiguan-cut/SKILL.md`，再在新会话中使用 `$shuiguan-cut`。

如果已经有同名 Skill，先自行备份旧目录；不要直接覆盖不明修改。下面的 Windows PowerShell 示例在目标已存在时会停止：

```powershell
$skillArchive = Join-Path $PWD 'shuiguan-cut.zip' # 改成下载文件的位置
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex/skills' }
$skillTarget = Join-Path $skillRoot 'shuiguan-cut'
if (Test-Path -LiteralPath $skillTarget) { throw '同名 Skill 已存在，请先备份并处理旧版本。' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
Expand-Archive -LiteralPath $skillArchive -DestinationPath $skillRoot
```

Release 附有 `SHA256SUMS.txt`。Windows 可用 `Get-FileHash -Algorithm SHA256 ./shuiguan-cut.zip`，macOS 可用 `shasum -a 256 ./shuiguan-cut.zip`，与清单核对。

## 准备真实剪辑环境

支持的验证平台为 **Windows x64、macOS Apple Silicon / Intel**。先准备 **Node.js 22.12 或更新版本**、Git，以及 FreeCut **0.6.0** 源码及其依赖：

```sh
git clone --branch v0.6.0-preview.1 --depth 1 https://github.com/Watertube-bilibili/freecut-desktop.git
cd freecut-desktop
npm ci
npm run prepare:ffmpeg
npm run build
```

`npm ci` 安装锁文件中的 Electron、Playwright、TypeScript 等依赖，并可能联网下载应用运行时。若 npm 配置跳过二进制安装脚本，请按 [主仓库开发说明](https://github.com/Watertube-bilibili/freecut-desktop/blob/v0.6.0-preview.1/README.md#开发)补齐 Electron / FFmpeg，再执行准备和构建。Skill 本身不会自动下载这些依赖或模型。

在命令中把 `<skill-dir>` 和 `<repo-dir>` 换成实际路径（路径含空格时保留引号）：

```sh
node "<skill-dir>/scripts/shuiguan-cut.cjs" doctor --repo "<repo-dir>"
```

`ready: true` 表示依赖和工程模型可用；这不等于已完成一次导出。源码模式使用这个仓库构建的真实应用。

也可以追加 `--exe "<已安装的 FreeCut 可执行文件>"` 使用 [FreeCut 0.6.0 安装版](https://github.com/Watertube-bilibili/freecut-desktop/releases/tag/v0.6.0-preview.1)。**即使使用安装版，仍需同版本源码仓库及其 `node_modules`**，用来加载工程模型、TypeScript 和 Playwright。Windows 指向 `FreeCut.exe`，Mac 指向 `FreeCut.app/Contents/MacOS/FreeCut`，不要指向安装器或便携自解压启动器。实际剪辑时会验证应用与源码版本一致。

## 让 AI 开始剪辑

```text
使用 $shuiguan-cut，把指定文件夹里的视频按文件名自然顺序拼接。
保留原声，不加音乐、字幕、水印或宣传内容。
使用我提供的 FreeCut 0.6.0 源码目录，输出可编辑工程和 MP4。
```

AI 应先检查素材，再按 [配方约定](shuiguan-cut/references/recipe.md)生成 UTF-8 JSON。直接调用形式：

```sh
node "<skill-dir>/scripts/shuiguan-cut.cjs" edit-render --repo "<repo-dir>" --recipe "<recipe.json>" --out-dir "<new-output-dir>" --timeout 1800
```

输出目录必须**尚不存在，且父目录已存在**。脚本拒绝覆盖旧目录，不接管你正在编辑的窗口；它只启动独立应用会话，不更改既有工程。`report.json.passed` 必须为 `true` 才能报告成功；还应实际查看成片，核对内容、顺序和画面。

| 输出文件 | 用途 |
| --- | --- |
| `project.freecut` | 产品保存的可继续编辑工程 |
| `render.mp4` | 真实产品导出并完整解码验证的视频 |
| `preview.png` | 预览检查图 |
| `recipe.json` | 解析后的配方，包含本地素材绝对路径 |
| `report.json` | 应用版本、尺寸、时长与成功/失败信息 |

工程引用原素材路径，不是内嵌素材包；搬到另一台电脑需一并提供有权使用的素材并重新链接。配方、工程和诊断文件可能包含本机路径，分享前请检查。Skill 不会上传你的素材或成片到本仓库。第三方素材、模型的许可独立适用。

## 验证与来源

运行环境检查已在 FreeCut 0.6.0 上通过。完整应用的 Windows / Mac 两架构 CI 包含真实 Skill `demo` 导出，见 [FreeCut 0.6.0 构建记录](https://github.com/Watertube-bilibili/freecut-desktop/actions/runs/37202629502)。本包另校验 Skill 格式、脚本语法、打包文件白名单与下载后的 SHA-256；这些检查不保证任意素材或复杂工程都能成功。

**已知产品边界（FreeCut 0.6.0）：** `report.json.passed: true` 只证实脚本操作、工程/输出结构、尺寸、时长与完整解码等检查通过，不证明每一帧画面正确。独立逐帧对照在一个 24 fps 拼接样例的部分循环小数切点发现单帧黑场，来自产品原生导出路径的时间边界处理；并非所有素材或切点都复现。此类切点应额外核查切换前后画面，不能仅靠解码成功验收。当前 Skill 发布包没有修复应用导出器；这条说明仅补充验证范围，不代表产品问题已修复。已发布 ZIP 与 `v0.6.0` 标签保持原样，最新边界说明以本 README 和 Release 正文为准。

可用原创测试素材自行完成 5 秒实际应用导出：

```sh
node "<skill-dir>/scripts/shuiguan-cut.cjs" demo --repo "<repo-dir>" --out-dir "<new-demo-dir>"
```

Skill 源自 [FreeCut 主仓库](https://github.com/Watertube-bilibili/freecut-desktop/tree/v0.6.0-preview.1/skills/shuiguan-cut)，沿用 **GPL-3.0-or-later**，见 [LICENSE](LICENSE) 和 [来源说明](shuiguan-cut/SOURCE.md)。FreeCut 应用及其依赖遵循各自许可；本包没有包含或重许可它们。

作者：**我叫水管同学** · [B站主页](https://space.bilibili.com/390310418)。欢迎下载、反馈问题，或给 [Skill 仓库](https://github.com/Watertube-bilibili/shuiguan-cut-skill) 和 [FreeCut](https://github.com/Watertube-bilibili/freecut-desktop) 点一个 Star。
