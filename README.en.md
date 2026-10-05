<div align="center">

# FreeCut AI Editing Skill

**Let AI edit with the real FreeCut desktop app and deliver a video plus an editable project.**

[简体中文](README.md) · [English](README.en.md)

[Download the Skill](https://github.com/Watertube-bilibili/shuiguan-cut-skill/releases/tag/v0.6.0) · [FreeCut](https://github.com/Watertube-bilibili/freecut-desktop) · [Star on GitHub](https://github.com/Watertube-bilibili/shuiguan-cut-skill)

</div>

Provide local videos, images, audio and editing instructions. The AI creates a recipe and starts an isolated FreeCut process to import media, save a project and export your video. You receive `project.freecut` and `render.mp4`, so you can continue editing in the app.

**Skill 0.6.0 targets FreeCut 0.6.0. All features are forever free, with no memberships or paid unlocks. No watermark is added by default.** This package contains AI instructions and an automation script. It does not bundle FreeCut, Node.js, Electron, Playwright, FFmpeg or AI models.

## What it supports

| Area | Current recipe bridge |
| --- | --- |
| Editing | Local media import, trimming, sequential concatenation and layered clips |
| Visuals | Text, solid colors, position, uniform scale, rotation and opacity |
| Motion and sound | Transform and volume keyframes, constant speed, fades and basic channel controls |
| Deliverables | Editable `.freecut` project, H.264/AAC MP4, preview image and verification report |
| Export settings | 720 / 1080 / 1440 / 2160 short-edge presets; 24 / 25 / 30 / 50 / 60 fps; the app limits the long edge to 3840 pixels |

FreeCut selects its native FFmpeg composition path or Canvas frame composition, then exports through the product. The Skill does not implement a separate renderer.

The bridge **does not yet automate** masks, color grading, transitions, speed curves, model downloads, speech recognition, text-to-speech or complex timeline interactions. App capabilities and recipe capabilities are different. Unknown recipe fields produce an error rather than being silently ignored.

## Install the Skill

1. Download **[shuiguan-cut.zip](https://github.com/Watertube-bilibili/shuiguan-cut-skill/releases/download/v0.6.0/shuiguan-cut.zip)** from the Release. GitHub's automatically generated source ZIP has a different directory layout.
2. Extract the entire `shuiguan-cut` folder into your Codex `skills` directory: normally `.codex/skills` in your user directory, or `$CODEX_HOME/skills` when `CODEX_HOME` is set.
3. Check that the resulting path is `skills/shuiguan-cut/SKILL.md`, then use `$shuiguan-cut` in a new session.

Back up an existing installation before replacing it. This Windows PowerShell example stops if a Skill with that name already exists:

```powershell
$skillArchive = Join-Path $PWD 'shuiguan-cut.zip' # Set your downloaded archive path
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex/skills' }
$skillTarget = Join-Path $skillRoot 'shuiguan-cut'
if (Test-Path -LiteralPath $skillTarget) { throw 'The Skill already exists. Back up and review the old installation first.' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
Expand-Archive -LiteralPath $skillArchive -DestinationPath $skillRoot
```

The Release includes `SHA256SUMS.txt`. Compare it with `Get-FileHash -Algorithm SHA256 ./shuiguan-cut.zip` on Windows or `shasum -a 256 ./shuiguan-cut.zip` on macOS.

## Prepare the editing environment

Validated platforms are **Windows x64 and macOS on Apple Silicon / Intel**. Install **Node.js 22.12 or newer**, Git, and the FreeCut **0.6.0** source with its dependencies:

```sh
git clone --branch v0.6.0-preview.1 --depth 1 https://github.com/Watertube-bilibili/freecut-desktop.git
cd freecut-desktop
npm ci
npm run prepare:ffmpeg
npm run build
```

`npm ci` installs the lockfile's Electron, Playwright, TypeScript and other dependencies, and may download runtime binaries. If your npm configuration skips binary installation scripts, follow the [main repository's development instructions](https://github.com/Watertube-bilibili/freecut-desktop/blob/v0.6.0-preview.1/README.en.md#development) to install Electron / FFmpeg before preparing and building. The Skill does not download dependencies or models itself.

Replace `<skill-dir>` and `<repo-dir>` with your actual paths:

```sh
node "<skill-dir>/scripts/shuiguan-cut.cjs" doctor --repo "<repo-dir>"
```

`ready: true` confirms that prerequisites and the project model are available; it is not an export test. Source mode runs the real app built from that checkout.

You may add `--exe "<installed FreeCut executable>"` to use the [FreeCut 0.6.0 desktop release](https://github.com/Watertube-bilibili/freecut-desktop/releases/tag/v0.6.0-preview.1). **Installed-app mode still requires a matching source checkout and its `node_modules`** for the project model, TypeScript and Playwright. Use `FreeCut.exe` on Windows or `FreeCut.app/Contents/MacOS/FreeCut` on macOS, not an installer or a self-extracting portable launcher. An actual editing run verifies that app and source versions match.

## Ask your AI to edit

```text
Use $shuiguan-cut to concatenate the videos in my specified folder in natural filename order.
Keep the original audio. Do not add music, captions, watermarks or promotional content.
Use my FreeCut 0.6.0 source checkout and deliver an editable project plus an MP4.
```

The AI should inspect the media and create a UTF-8 JSON recipe using the [recipe reference](shuiguan-cut/references/recipe.md). Direct invocation:

```sh
node "<skill-dir>/scripts/shuiguan-cut.cjs" edit-render --repo "<repo-dir>" --recipe "<recipe.json>" --out-dir "<new-output-dir>" --timeout 1800
```

The output directory **must not exist, and its parent must already exist**. The script refuses to overwrite previous output and starts an isolated app session, without attaching to your open editor. Only report success when `report.json.passed` is `true`; also watch the actual video to check content, ordering and appearance.

| Output | Purpose |
| --- | --- |
| `project.freecut` | Editable project saved by the real app |
| `render.mp4` | Product export, checked by decoding the complete output |
| `preview.png` | Preview inspection image |
| `recipe.json` | Resolved recipe, including absolute local media paths |
| `report.json` | App version, dimensions, duration and success/failure details |

The project references original media paths; it is not a self-contained media archive. Moving it to another computer requires the corresponding legally usable media and relinking. Recipes, projects and diagnostic files may contain local paths, so review them before sharing. The Skill does not upload your footage or exports to this repository. Third-party media and model licenses remain separate.

## Verification and source

The environment check passed against FreeCut 0.6.0. The app's Windows and both Mac architecture CI runs include the real Skill `demo` export; see the [FreeCut 0.6.0 build](https://github.com/Watertube-bilibili/freecut-desktop/actions/runs/37202629502). This package additionally checks Skill structure, script syntax, an explicit packaging allowlist and the downloaded SHA-256. These checks do not guarantee success for every media format or complex project.

**Known product limitation (FreeCut 0.6.0):** `report.json.passed: true` confirms script operations, project/output structure, dimensions, duration and full decoding checks; it does not prove that every frame is visually correct. Independent frame-by-frame comparison of one 24 fps concatenation example found single black frames at some cut times with repeating decimal representations, caused by timing-boundary handling in the app's native export path. This was not observed at every cut and is not a claim about all media. Inspect frames immediately around such cuts rather than accepting decode success alone. This Skill release does not fix the app exporter, and this documentation update does not claim the product issue is resolved. The published ZIP and `v0.6.0` tag remain unchanged; consult this README and the Release body for the latest limitations.

Run a five-second end-to-end example using generated original test media:

```sh
node "<skill-dir>/scripts/shuiguan-cut.cjs" demo --repo "<repo-dir>" --out-dir "<new-demo-dir>"
```

The Skill originates from the [FreeCut repository](https://github.com/Watertube-bilibili/freecut-desktop/tree/v0.6.0-preview.1/skills/shuiguan-cut) and retains **GPL-3.0-or-later**. See [LICENSE](LICENSE) and [source notes](shuiguan-cut/SOURCE.md). FreeCut and its dependencies retain their own licenses and are not bundled or relicensed here.

Created by **我叫水管同学** · [Bilibili](https://space.bilibili.com/390310418). Download, report issues, and support the project with a Star on [this repository](https://github.com/Watertube-bilibili/shuiguan-cut-skill) and [FreeCut](https://github.com/Watertube-bilibili/freecut-desktop).
