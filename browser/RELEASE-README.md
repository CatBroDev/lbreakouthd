# LBreakoutHD 1.2.4 — browser source build

Play: https://oldgamesarchive.org/games/lbreakouthd
中文：https://oldgamesarchive.org/zh-cn/games/lbreakouthd

LBreakoutHD is Michael Speck's widescreen remake of LBreakout2, retaining its C game engine. Original copyright 2018–2026 Michael Speck and contributors, GNU GPL-3.0-or-later. This is a modern source build, not a DOS executable or the first browser port. The existing midzer browser project supplied the initial investigation; this release builds the author's newer 1.2.4 source.

## Source and licenses

Author: https://lgames.sourceforge.io/LBreakoutHD/

Original release: https://sourceforge.net/projects/lgames/files/lbreakouthd/lbreakouthd-1.2.4.tar.gz/download

Identical source mirror: https://deb.debian.org/debian/pool/main/l/lbreakouthd/lbreakouthd_1.2.4.orig.tar.gz

SHA-256: `4732c3852ba0030fecca65689591ac582c86af46b1a21b274640ffc6cd8fc826`

Original source, artwork and notices are preserved in source.zip. Standard theme credits include Rawpixel, PublicDomainPictures, GameProgrammingSlave/OpenGameArt and clker; Source Sans Pro uses the SIL Open Font License. Theme credit files and font licenses accompany the release. Dependency notices are included. Browser glue by Old Games Archive / CatBroDev is GPL-3.0-or-later; it does not change upstream licenses.

## Browser changes

Asyncify yields the native loops. Host pause freezes both SDL millisecond and high-resolution clocks; releasing controls clears held keys. The mixer output is gated for genuine mute without changing the player's native volume. Native files are stored under `/persistent_data/.lbreakouthd` in the isolated IndexedDB database `oldgames-lbreakouthd-v1`. Checkpoints and normal shutdown serialize writes; quitting closes the audio context. The shared website controller is populated from documented controls, without a new per-game touch layout.

Texture scaling preserves the source blend mode, fixing the missing menu background after scaling an opaque image. The startup package retains both shipped themes and all shipped level sets. Development Makefiles and SVG source assets are excluded from the runtime but retained in corresponding source.

## Playing and saving

Choose New Game, then Start Original Levels. Left/Right moves the paddle; Space or V releases balls and fires available weapons. Up/Down and Enter operate menus. P pauses. Esc, then Y leaves the game and writes a resumable native save. Resume Game restores the saved level, score and lives; the level restarts, so this is not an exact-position snapshot. X accelerates the paddle; C speeds up balls; Backspace recalls an idle ball when allowed; W skips ahead only when the game permits it. Help about extras and bricks is available from the native main menu. English in-game menus are preserved.

Settings, scores and resume files stay in this browser on this site. Clearing browser data or ending a private session can remove them. There is no cloud save. Tests cover initial gameplay and lifecycle, not every level, editor operation or physical phone model.

## Reproducible build

Install Python 3, Node.js and Emscripten **4.0.23**. Set `LBREAKOUT_EMSDK` to the SDK folder containing `.emscripten` and `upstream/emscripten`:

```powershell
$env:LBREAKOUT_EMSDK = 'C:\tools\emsdk'
python -X utf8 build-browser.py release-local
python -X utf8 package-release.py release-local
```

The build reads the preserved `author-source/lbreakouthd-1.2.4` tree. New output directories are required. SDL2, SDL2_image with PNG/JPEG, SDL2_mixer and SDL2_ttf are supplied by Emscripten ports. `--state` enables diagnostic exports for development only; omit it for release. Packaging rejects diagnostic builds and includes original sources, patches, build instructions and dependency notices. Serve the output over HTTP, with `.wasm.bin` as `application/wasm`. It works standalone and supports the optional origin-checked Old Games Archive protocol v1.
