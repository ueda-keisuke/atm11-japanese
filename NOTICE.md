# 基本パックの出典・変更 / Base pack credits and changes

This unofficial pack targets Minecraft 26.1.2 / NeoForge 26.1.2.106. Version 0.3.0 covers the exact current English key sets: Transmog 25, JEI 335, AppleSkin 22 and Controlling 12. These are key counts, including search aliases and metadata, not counts of visually checked display strings. The separate Jade asset is not part of this ZIP.

## Transmog

Transmog — Copyright (c) 2023 Hidoni. MIT, retained in `LICENSES/Transmog-MIT.txt`.

Source: https://github.com/Hidoni/Transmog

Target: **1.8.0+26.1**. The original MOD credits **elinka47** for its existing Japanese translation. This pack supplies revised Japanese language values. A narrow filter bypasses only the malformed lower-priority `transmog:lang/ja_jp.json`, without editing or distributing the MOD JAR.

## Just Enough Items

Just Enough Items (JEI) — Copyright (c) 2014-2015 mezz. MIT, retained in `LICENSES/JEI-MIT.txt`.

Source: https://github.com/mezz/JustEnoughItems/tree/634d109ddd299a62beb2d9a1b8566da3dfd56bb8

Target: **29.36.0.96**. The English and Japanese assets match upstream tag `v29.36.0` at the commit above. Existing Japanese contributors include **Abbage230**, whose 26.1 update was merged in https://github.com/mezz/JustEnoughItems/pull/4300. This is not an exhaustive historical contributor list.

This pack revises Japanese language values and search aliases. The `_comment` metadata retains the original English value. JEI uses normal key overlays, with no filter.

## AppleSkin

AppleSkin — **squeek502** (squeek). The original **Unlicense** is retained verbatim in `LICENSES/AppleSkin-Unlicense.txt`; the original asset is not relabeled as MIT.

Source: https://github.com/squeek502/AppleSkin/tree/09d8ccbcb0241e873a45eb843c1267b52e2c38ce

Target: **3.0.9 for Minecraft 26.1**. The exact language bytes match this official `26.1-neoforge` source. This pack revises Japanese values for all 22 current English keys, using normal key overlays. Older Japanese-only keys can remain in the original underlying resources.

## Controlling

Controlling — Copyright (c) 2021 **Jared**; author **Jaredlll08**. MIT, retained in `LICENSES/Controlling-MIT.txt`.

Source: https://github.com/jaredlll08/Controlling/tree/43851d44a389833f98f4096d3803c15c67276b75

Target: **26.1.2.4**. The exact language bytes match this official `26.1.2` source. This pack supplies Japanese values for all 12 current English keys, using normal key overlays.

## License scope and review records

This project's additions to this base pack and the build script are MIT, in `LICENSES/Project-MIT.txt`. The original licenses and credits above remain applicable. **The separately distributed Jade language asset and adaptations are CC BY-NC-SA 4.0 and are excluded from this MIT grant.**

これは元作者・既存訳者の公式版ではありません。本パックは日本語の設定名、説明、検索語などを改変します。MOD 本体・クエスト定義・ワールド・ログ・バックアップを含みません。

`release.json` binds the language bytes and review summaries. `reviews/` identifies exact original source/JAR hashes, accepted keys, reviewer and review/submission hashes. These are provenance records, not digital signatures or proof that every game screen has been visually tested. Only independently accepted language inputs can pass the builder.
