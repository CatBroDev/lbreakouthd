# Building the browser version

This Fork preserves midzer/lbreakouthd at `3cd2a6160941557f48c49b184f0ad47ddd882c23`.
The root source is the historical 1.1.8 snapshot. **The browser build uses Michael
Speck's 1.2.4 release**, bundled unchanged in `vendor/` with SHA-256 verification.
The original tarball remains reproducible and includes all original credits,
licenses, themes and levels. Build-time patches are visible in build-browser.py.

Use Python 3.12+, Node.js and Emscripten **4.0.23**. Set LBREAKOUT_EMSDK to the SDK
root (containing .emscripten and upstream/emscripten). SDL2, SDL2_image PNG/JPEG,
SDL2_mixer and SDL2_ttf are downloaded by the pinned SDK on the first build.

```sh
python -X utf8 browser/build-browser.py release-local
python -X utf8 browser/package-release.py release-local
cd browser
npm install
node accept-release.mjs release-local check-01
```

The acceptance command currently uses the installed Google Chrome channel;
install Chrome or change its `channel` option to use Playwright Chromium.
It always launches with --mute-audio and closes its browser and HTTP server.
It verifies gameplay, PCM sound/mute, pause, full-browser-restart persistence
and native Quit. It does not certify a full playthrough or physical phones.

Output directories must be new. Omit --state for release builds. The packager
rejects diagnostic exports and produces corresponding source and notices.
Serve browser/build/release-local over HTTP; .wasm.bin uses application/wasm.
The standalone Start page supports keyboard/mouse. The live site's shared
configurable touch controller uses the origin-checked protocol v1 in bridge.js.
No account credentials or site backend are required for a standalone build.
