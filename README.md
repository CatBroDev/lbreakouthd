# LBreakoutHD browser restoration

[Play online](https://oldgamesarchive.org/games/lbreakouthd) · [中文说明与试玩](https://oldgamesarchive.org/zh-cn/games/lbreakouthd)

LBreakoutHD and LBreakout2 are by **Michael Speck and contributors**. Original
GPL-3.0-or-later licensing and theme/font attribution remain intact. This Fork
preserves midzer's community repository and its history; it is not the author's
official repository and does not claim to be the first browser port.

The preserved root source is 1.1.8. Our browser build uses the author's verified
**1.2.4** source tarball in browser/vendor, including both themes and all supplied
level sets. Browser integration by Old Games Archive / CatBroDev adds safe key
release, host pause, true mute, independent local native saves and shared touch
control integration. Texture resizing now preserves the image's blend mode,
fixing an invisible menu background on the tested browser renderer.

See [browser/BUILD.md](browser/BUILD.md) for reproducible build and muted tests,
[browser/RELEASE-README.md](browser/RELEASE-README.md) for controls, save limitations
and full attribution, and the unchanged [original README](README).

Native Resume Game restarts the saved level with recorded score/lives, not the
exact ball position. Saves are local to a site/browser/device. In-game menus are
English. Full level sets, editor workflows and physical-phone performance are
not certified. The default upstream branch is preserved; this work is on
`codex/browser-restoration`.
