# 出典・変更・ライセンスの適用範囲 / Credits, changes and license scopes

## 0.14.0 additions / 追加内容

0.14.0では、DimStorageの36項目、Step Crafterの80項目、Refined Storage - Quartz Arsenalの23項目を追加しています。既存の44対象は保持します。全47対象・3,438項目（翻訳3,419、原文メタデータ18、Apache 4(b)改変通知1）を収録します。ゲーム画面の目視確認は0件です。

Version 0.14.0 adds 36 DimStorage entries, 80 Step Crafter entries and 23 Refined Storage - Quartz Arsenal entries. Earlier language/review files and their individual license scopes are retained. Independent language review, format checks and native resource-loader checks are separate from game-screen visual checks, which remain at 0.

ATM11 Japanese project / **ueda-keisuke** provides this unofficial Japanese language collection for Minecraft 26.1.2 / NeoForge 26.1.2.106. Version 0.14.0 contains 3,438 entries across 47 namespaces: 3,419 translations, 18 preserved original metadata entries and one Apache 4(b) project notice. The original metadata comprises JEI `_comment`, Jade `__comment` / `jade.metadata`, QuarryPlus `_comment`, Nature's Compass `_comment`, and Enchantment Descriptions `_comment`, `__comment_jei` and 11 `__support_*` entries. Changes comprise Japanese names, descriptions, narration and search terms, with the metadata and project-notice exceptions below. Language modification date: **2026-09-20 (UTC)**.

Each `assets/<namespace>/lang/ja_jp.json` is a separate, human-readable, editable language work. The ZIP is a distribution container: the files are not merged into a single language asset or linked program. Individual licenses remain applicable to their respective files, including our Japanese adaptations. No collection-wide MIT grant or additional collection-wide noncommercial restriction is imposed on independently licensed files. Redistributing the complete collection requires compliance with all included works' terms.

This is not an official release or endorsement by the original authors or translators. No MOD JARs, Java code, quests, worlds, images, logos, private logs or backups are included. The parent JAR identities below establish provenance only; they grant no rights to unrelated parent assets.

## ToolBelt — `assets/toolbelt/lang/ja_jp.json`

**Copyright (c) 2024, David Quintana <gigaherz@gmail.com>.** BSD-3-Clause: `LICENSES/ToolBelt-BSD-3-Clause.txt`. The original BSD notice and conditions remain applicable; this project does not relicense ToolBelt as MIT.

Fixed source: https://github.com/gigaherz/ToolBelt/tree/66be987684d5e9dab7825c73d35da3bca3b0b2ea

Upstream language sources: [English](https://raw.githubusercontent.com/gigaherz/ToolBelt/66be987684d5e9dab7825c73d35da3bca3b0b2ea/src/main/resources/assets/toolbelt/lang/en_us.json), [existing Japanese](https://raw.githubusercontent.com/gigaherz/ToolBelt/66be987684d5e9dab7825c73d35da3bca3b0b2ea/src/main/resources/assets/toolbelt/lang/ja_jp.json).

Target: **2.9.5**, 26 keys. The selected English and existing Japanese assets are bound to this fixed source and installed JAR by the fixed source and JAR identities; line endings differ but normalized text matches. Existing upstream Japanese provenance is retained; no named Japanese contributor was recorded in the fixed evidence. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / **ueda-keisuke**. The complete editable modified source is `assets/toolbelt/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository). The original JAR, code and other assets are not included.

## Cucumber — `assets/cucumber/lang/ja_jp.json`

**Copyright (c) 2018 BlakeBr0.** MIT: `LICENSES/Cucumber-MIT.txt`.

Fixed source: https://github.com/BlakeBr0/Cucumber/tree/0716111611f9d334c34043bb391697261383a5c9

Upstream language sources: [English](https://raw.githubusercontent.com/BlakeBr0/Cucumber/0716111611f9d334c34043bb391697261383a5c9/src/main/resources/assets/cucumber/lang/en_us.json), [existing Japanese](https://raw.githubusercontent.com/BlakeBr0/Cucumber/0716111611f9d334c34043bb391697261383a5c9/src/main/resources/assets/cucumber/lang/ja_jp.json).

Target: **26.1.2-9.0.6**, 16 keys. The English and existing Japanese assets match the fixed source and installed JAR byte-for-byte. Existing upstream Japanese provenance is retained; no named Japanese contributor was recorded in the fixed evidence. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / **ueda-keisuke**. The complete editable modified source is `assets/cucumber/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository). No Cucumber JAR, code or other assets are included.

## Iron Jetpacks — `assets/ironjetpacks/lang/ja_jp.json`

**Copyright (c) 2018 BlakeBr0.** MIT: `LICENSES/IronJetpacks-MIT.txt`.

Fixed source: https://github.com/BlakeBr0/IronJetpacks/tree/601f96aaa8b1d389d7b5d587ca68dc6b68fe9a15

Upstream language sources: [English](https://raw.githubusercontent.com/BlakeBr0/IronJetpacks/601f96aaa8b1d389d7b5d587ca68dc6b68fe9a15/src/main/resources/assets/ironjetpacks/lang/en_us.json), [existing Japanese](https://raw.githubusercontent.com/BlakeBr0/IronJetpacks/601f96aaa8b1d389d7b5d587ca68dc6b68fe9a15/src/main/resources/assets/ironjetpacks/lang/ja_jp.json).

Target: **9.0.3**, 41 normal English-corresponding keys. Existing upstream Japanese provenance and the fixed English/Japanese source hashes are retained. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / **ueda-keisuke**. The complete editable modified source is `assets/ironjetpacks/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository).

The separate 14 material-prefix entries are derived from the installed `com/blakebr0/ironjetpacks/registry/Jetpack.class` `getDisplayName`/name contract, not from the 41-key English language JSON. They are bound to the immutable derived contract SHA `c3e51fc6fd9ccbcd23c882ff08062b215bf718796bfc9ab0b885a8271af7da3d` and the fixed class/source hashes in `reviews/ironjetpacks.json`. The original name-generation code is [Jetpack.java](https://github.com/BlakeBr0/IronJetpacks/blob/601f96aaa8b1d389d7b5d587ca68dc6b68fe9a15/src/main/java/com/blakebr0/ironjetpacks/registry/Jetpack.java). The contract supplies the current material names and the original method's fallback/composition behavior; it does not distribute the class or live configuration. The 14 entries are independently reviewed and included in the same editable `assets/ironjetpacks/lang/ja_jp.json` file. No Iron Jetpacks JAR, Java code, class, configuration, image or model is included.

## Functional Storage — `assets/functionalstorage/lang/ja_jp.json`

**Copyright (c) 2021 Buuz135, Rid.** MIT: `LICENSES/FunctionalStorage-MIT.txt`.

Fixed source: https://github.com/Buuz135/FunctionalStorage/tree/9945d211c9bb2f45a8dfb14c2bab28742b02acde

Upstream language sources: [English](https://raw.githubusercontent.com/Buuz135/FunctionalStorage/9945d211c9bb2f45a8dfb14c2bab28742b02acde/src/generated/resources/assets/functionalstorage/lang/en_us.json), [existing Japanese](https://raw.githubusercontent.com/Buuz135/FunctionalStorage/9945d211c9bb2f45a8dfb14c2bab28742b02acde/src/main/resources/assets/functionalstorage/lang/ja_jp.json).

Target: **1.6.1**, 164 current English-corresponding keys. The fixed English asset and 135-key existing Japanese asset match the installed JAR and fixed source; existing Japanese provenance is retained and current values are revised or supplied. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / **ueda-keisuke**. The complete editable modified source is `assets/functionalstorage/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository). No Functional Storage JAR, Java code or other assets are included.

## Transmog — `assets/transmog/lang/ja_jp.json`

**Copyright (c) 2023 Hidoni.** MIT: `LICENSES/Transmog-MIT.txt`. Existing Japanese contributor: **elinka47**.

Source: https://github.com/Hidoni/Transmog

Target: **1.8.0+26.1**, 25 keys. Japanese values are revised. The only pack filter bypasses the malformed lower-priority `transmog:lang/ja_jp.json`; the original JAR is neither changed nor distributed.

## Just Enough Items — `assets/jei/lang/ja_jp.json`

**Copyright (c) 2014-2015 mezz.** MIT: `LICENSES/JEI-MIT.txt`. Existing Japanese contributors include **Abbage230**, whose 26.1 update was merged in https://github.com/mezz/JustEnoughItems/pull/4300. This is not an exhaustive historical contributor list.

Source: https://github.com/mezz/JustEnoughItems/tree/634d109ddd299a62beb2d9a1b8566da3dfd56bb8

Target: **29.36.0.96**, 335 keys. The language assets match upstream tag `v29.36.0` at this commit. Japanese values and search aliases are revised. `_comment` retains its original English value.

## AppleSkin — `assets/appleskin/lang/ja_jp.json`

**squeek502 (squeek)**. Original **Unlicense**: `LICENSES/AppleSkin-Unlicense.txt`. The original asset is not relabeled as MIT. This project's Japanese additions retain the Project MIT grant stated for the previous release, while the original Unlicense remains included.

Source: https://github.com/squeek502/AppleSkin/tree/09d8ccbcb0241e873a45eb843c1267b52e2c38ce

Target: **3.0.9 for Minecraft 26.1**, 22 current English keys. Japanese values are revised. Older Japanese-only keys may remain in underlying original resources.

## Controlling — `assets/controlling/lang/ja_jp.json`

**Copyright (c) 2021 Jared; author Jaredlll08.** MIT: `LICENSES/Controlling-MIT.txt`.

Source: https://github.com/jaredlll08/Controlling/tree/43851d44a389833f98f4096d3803c15c67276b75

Target: **26.1.2.4**, 12 keys. Japanese values are supplied for the exact current English key set.

## Jade — `assets/jade/lang/ja_jp.json`

**Jade / Snownee**. Original project credits: **TehNut, ProfMobius, kalkafox**. Existing Japanese translators: **momo-i, RascalNiki**.

**The Jade language asset and this Japanese adaptation use CC BY-NC-SA 4.0, not MIT.** Attribution, indication of changes, noncommercial use and ShareAlike apply. No additional restriction or technical protection is imposed by this collection.

License: https://creativecommons.org/licenses/by-nc-sa/4.0/

Full legal text: `LICENSES/Jade-CC-BY-NC-SA-4.0.md`.

Source: https://github.com/Snownee/Jade/tree/5130218d29f8acb7132c91ef27204a4ff1e2e31d

Upstream license: https://github.com/Snownee/Jade/blob/5130218d29f8acb7132c91ef27204a4ff1e2e31d/LICENSE.md

Target: **26.1.10**, 496 current English keys, including narration, search terms and two preserved settings. We revise the original Japanese values and supply missing current keys. Existing translator credits are retained. `jade.metadata` preserves the exact original Japanese runtime language settings; `__comment` retains the English testing-section marker. These two entries are not new translations. Jade uses no filter; Japanese-only upstream keys may remain in underlying resources.

## Searchables — `assets/searchables/lang/ja_jp.json`

**Copyright (c) 2023 Jared; author Jaredlll08.** MIT: `LICENSES/Searchables-MIT.txt`.

Source: https://github.com/jaredlll08/Searchables/tree/18d453f71671829e65c5bff2cf9dc21b83561940

Target: **1.0.2**, 2 keys. Japanese language values are revised/supplied. The original English, Japanese and license bytes match this source.

## Resourceful Config — `assets/resourcefulconfig/lang/ja_jp.json`

**Copyright (c) 2023 Team Resourceful.** MIT: `LICENSES/ResourcefulConfig-MIT.txt`.

Source: https://github.com/Team-Resourceful/Resourceful-Config/tree/b047b620ff8b2f9b61685e79797742a72191a60e

Target: **4.0.1**, 32 keys. New Japanese values are supplied for the original English language asset. The selected copy was inside Lootr's `META-INF/jarjar/resourcefulconfig-neoforge-26.1-4.0.1.jar`. Only the Resourceful Config language asset is included; no Lootr asset, logo or JAR is included or licensed by this notice.

## AE2 Network Analyzer — `assets/ae2netanalyser/lang/ja_jp.json`

**GlodBlock**; original credits: **bdew**. GNU Lesser General Public License **3.0**: `LICENSES/AE2NetworkAnalyzer-LGPL-3.0.txt`. The LGPL incorporates GPLv3 terms; the full GPL is also included in `LICENSES/GPL-3.0.txt`. This Japanese adaptation remains under LGPL 3.0, not MIT.

Target: **26.1-1.0.0-neoforge**, 38 keys. **Modified 2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese names, settings and explanations are revised/supplied. No executable code is changed.

Exact source: https://github.com/GlodBlock/ExtendedAE/tree/4ddb52dfef6c3173b7c99abea1db3644d48fede8

Original English: https://github.com/GlodBlock/ExtendedAE/blob/4ddb52dfef6c3173b7c99abea1db3644d48fede8/src/main/resources/assets/ae2netanalyser/lang/en_us.json

Original Japanese: https://github.com/GlodBlock/ExtendedAE/blob/4ddb52dfef6c3173b7c99abea1db3644d48fede8/src/main/resources/assets/ae2netanalyser/lang/ja_jp.json

The complete modified source is the human-readable `assets/ae2netanalyser/lang/ja_jp.json` in this ZIP (in the repository under `resourcepack/`). It can be extracted, edited, replaced and redistributed under its license; no object-code-only artifact or source download offer is substituted for it. The original JAR's language bytes use CRLF; the official source matches after line-ending normalization. Original and modified hashes are in `reviews/ae2netanalyser.json` and `release.json`.

## Cumulus Menus — `assets/cumulus_menus/lang/ja_jp.json`

**The Aether Team**; authors: **AlphaMode, bconlon, Blodhgarm**. Original credits: **The Aether Team; kingbdogz, for the original Main Menu API that this is inspired by**.

GNU Lesser General Public License **3.0**: `LICENSES/CumulusMenus-LGPL-3.0.txt`; full GPLv3: `LICENSES/GPL-3.0.txt`. This Japanese adaptation remains under LGPL 3.0, not MIT.

Target: **2.0.15**, 35 keys. **Modified 2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese menu values are supplied for all current English keys; upstream Japanese was an empty object. No executable code is changed.

Exact source: https://github.com/The-Aether-Team/Cumulus/tree/0c44de7b060218fad5a21dddbd38141287f50054

Original English: https://github.com/The-Aether-Team/Cumulus/blob/0c44de7b060218fad5a21dddbd38141287f50054/neoforge/src/generated/resources/assets/cumulus_menus/lang/en_us.json

Original Japanese: https://github.com/The-Aether-Team/Cumulus/blob/0c44de7b060218fad5a21dddbd38141287f50054/common/src/main/resources/assets/cumulus_menus/lang/ja_jp.json

The complete modified source is the human-readable `assets/cumulus_menus/lang/ja_jp.json` in this ZIP (in the repository under `resourcepack/`). It can be extracted, edited, replaced and redistributed under its license. Original and modified hashes are in `reviews/cumulus_menus.json` and `release.json`.

The selected copy was inside Aether II's `META-INF/jarjar/cumulus_menus-26.1.2-2.0.15-neoforge.jar`. Cumulus code and assets have their own LGPL scope. No Aether II asset, image, brand or JAR is included or licensed by this notice.

## Sodium — `assets/sodium/lang/ja_jp.json`

**JellySquid (jellysquid3), IMS212**. Original project credits: **bytzo, PepperCode1, FlashyReese, altrisi, Grayray75, Madis0, Johni0702, comp500, coderbot16, Moulberry, MCRcortex, Altirix, embeddedt, pajicadvance, Kroppeb, douira, burgerindividual, TwistedZero, Leo40Git, haykam821, muzikbike**.

**PolyForm Shield 1.0.0**: `LICENSES/Sodium-PolyForm-Shield-1.0.0.md`. This notice does not sublicense the original work as MIT or grant broader rights than the original license. The license's permitted-purpose and noncompeting-use conditions remain applicable.

Exact source: https://github.com/CaffeineMC/sodium/tree/836dacd26604e1466e3c69dfaa1a4b9a2017c191

Upstream license: https://github.com/CaffeineMC/sodium/blob/836dacd26604e1466e3c69dfaa1a4b9a2017c191/LICENSE.md

Target: **0.9.1 for Minecraft 26.1.2**, 105 keys. New Japanese names and explanations are supplied. This is a complementary Japanese resource requiring the original Sodium MOD; it is not a renderer, replacement implementation or competing Sodium product. The selected language asset is inside `META-INF/jarjar/net.caffeinemc.sodium-neoforge-0.9.1+mc26.1.2-mod.jar`. No Sodium Java code or third-party implementation is included.

## Better Advancements — `assets/betteradvancements/lang/ja_jp.json`

**Copyright (c) 2017 way2muchnoise.** Original **Don't Be a Jerk** license: `LICENSES/BetterAdvancements-Dont-Be-a-Jerk.md`. Its noncommercial and other conditions remain applicable to this unofficial Japanese modification; no MIT grant is made for it.

Source: https://github.com/way2muchnoise/BetterAdvancements/tree/1fd067b4de74f82b9767bda7c62ec023e534d550

Target: **0.6.0.76**, 3 keys. Japanese values are revised/supplied. The exact language and license bytes match this official source; this is not a claim that the entire build 76 JAR was built from that commit. This free resource-pack supplement is not an official release and makes no ownership claim over the original work.

## QuarryPlus — `assets/quarryplus/lang/ja_jp.json`

**Copyright (C) 2012, 2013 yogpstop; Copyright (C) 2017–2024 Kotori316.** Author/credits: **Kotori316**. LGPL 3.0: `LICENSES/QuarryPlus-LGPL-3.0.txt`, with `LICENSES/GPL-3.0.txt`. This adaptation is not MIT.

Source: https://github.com/Kotori316/QuarryPlus/tree/a758a34a27438a81b9a35038ccc1c77c586093f0

Target: **26.12.160**, 240 current English keys. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese values are revised/supplied; `_comment` preserves `English lang file.` verbatim. Existing upstream Japanese is the source reference, not claimed as new work. The complete editable modified source is `assets/quarryplus/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository). Only this language asset is supplied, not the original JAR or code.

Hardcoded QuarryPlus GUI labels and diagnostic messages remain partly untranslated. This resource pack cannot replace strings that do not consult language keys. The 240-key count does not assert coverage of all QuarryPlus player-facing text.

## Code Defined GUI — `assets/codedefinedgui/lang/ja_jp.json`

**Copyright 2026 klikli-dev; author Kli Kli.** The language asset and this Japanese adaptation use **CC BY 4.0**, full text `LICENSES/CC-BY-4.0.txt`: https://creativecommons.org/licenses/by/4.0/

Source: https://github.com/klikli-dev/code-defined-gui/tree/cdb0b11e1001b742b9333af2d55ea6f636b0d736

Target: **1.12.0**, 63 keys, selected inside Theurgy. Modified **2026-09-20 (UTC)**: Japanese GUI text is supplied; no Japanese asset existed in the selected upstream source. The fixed source's `REUSE.toml` explicitly assigns `src/generated/resources/**`, including this language asset, to CC BY 4.0. This file-specific license governs here; it is not the code's MIT grant. The upstream README's general CC BY-SA wording differs from its linked CC BY text and REUSE; this project follows the explicit file-specific annotation. No attribution or license notice is removed and no extra use restriction is added.

## SathLib — `assets/sathlib/lang/ja_jp.json`

**Satherov / SathLabs.** LGPL 3.0: `LICENSES/SathLib-LGPL-3.0.txt`, with `LICENSES/GPL-3.0.txt`.

Source: https://github.com/SathLabs/SathLib/tree/2afb6bd1ba525e5cbb208e1772a53c1d3777d272

Target: **1.1.0+26.1.2**, 18 keys, selected inside Crystalix. Modified **2026-09-20 (UTC)**: Japanese explanations/settings are supplied; upstream had no Japanese language file. The complete modified, human-readable source is `assets/sathlib/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository), licensed under LGPL 3.0. No Crystalix code, assets or JAR is included.

## AE2AddonLib — `assets/ae2addonlib/lang/ja_jp.json`

**Pedroksl.** This modified Japanese asset is distributed under **GPL 3.0**, full text `LICENSES/GPL-3.0.txt`, following the exact upstream repository LICENSE. It is not MIT.

Source: https://github.com/pedroksl/AE2AddonLib/tree/5b48a86deea7ebf50bf95166f7b74a24057c90ac

Target: **26.1.3-alpha**, 11 keys, selected inside Advanced AE. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: existing upstream Japanese is revised and missing current keys are supplied. The original Japanese source is retained as provenance; it is not all newly authored by this project. The complete editable modified source is `assets/ae2addonlib/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository).

The original JAR metadata/gradle.properties says LGPL-3.0 while the exact official LICENSE contains GPLv3. The original source identity remains unchanged in the review record. This distribution applies GPLv3 to this JSON only, retaining the original metadata discrepancy in this notice. Unrelated namespace assets remain independent works in the collection; no extra restriction is imposed on their licenses.

## AE2WTLib API — `assets/ae2wtlib_api/lang/ja_jp.json`

**Copyright (c) 2021 mari_023**; authors **mari_023, Ridanisaurus**. MIT: `LICENSES/AE2WTLib-API-MIT.txt`.

Source: https://github.com/Mari023/AE2WirelessTerminalLibrary/tree/16c325df8e68447388798beea83444051d4e2de7

Target: **26.1.1-beta**, 5 API keys. Modified **2026-09-20 (UTC)**: Japanese API values are supplied; no Japanese file existed in the selected API source. This scope is the inner API language file only, not the outer `ae2wtlib` namespace, textures or JAR.

## Kuma API — `assets/kuma_api/lang/ja_jp.json`

**Copyright (c) 2024 BlayTheNinth.** MIT: `LICENSES/Kuma-API-MIT.txt`.

Source: https://github.com/TwelveIterations/KumaAPI/tree/ebd356138b2aa8a7f85a0c93c5457ebf64fc16bd

Target: **26.1.2.2**, 4 keys, selected inside Balm. Modified **2026-09-20 (UTC)**: Japanese API values are supplied; upstream had no Japanese language file. Only the API language asset is included, not Balm assets or the parent JAR.

## Apollib — `assets/apollib/lang/ja_jp.json`

**Copyright (c) 2026 Apollo.** MIT: `LICENSES/Apollib-MIT.txt`.

Source: https://github.com/Apollounknowndev/Apollib/tree/cc459eb27192f41749167a3a52bbefa5574ac743

Target: **1.1.6**, 7 keys, selected inside Lithostitched. Modified **2026-09-20 (UTC)**: Japanese settings values are supplied; upstream had no Japanese language file. Local English uses CRLF and official source uses LF, with matching JSON content. Parent Lithostitched assets and JAR are outside this scope.

## Ender IO — Modded Conduits — `assets/enderio/lang/ja_jp.json`

Original authors: **CrazyPants, tterrag, HenryLoenwind, MatthiasM, CyanideX, EpicSquid, Rover656, HypherionSA, liliandev, Ferri_Arnus, dphaldes**.

The selected child metadata declares **CC0**; the official repository LICENSE is **Unlicense**. Both texts are retained as `LICENSES/CC0-1.0.txt` and `LICENSES/EnderIO-Unlicense.txt`. This notice preserves the original declarations and does not replace them with MIT.

Source: https://github.com/Team-EnderIO/EnderIO/tree/d1fb8f797d6b8b421d6b5d45abee49d4822d9046

Target: **9.0.5-alpha**, only **`conduit.enderio.rs` (1 key)** from the inner `com.enderio.enderio-modded-conduits-9.0.5-alpha.jar`. Modified **2026-09-20 (UTC)**: the Japanese value is revised/reviewed against the selected current English and original Japanese. This is not an EnderIO-wide translation. The original child Japanese file has additional keys which may remain in lower-priority resources; they are not added to this overlay. No whole EnderIO asset collection, parent JAR or child JAR is redistributed.

## Magic Particles Lib — `assets/magicparticleslib/lang/ja_jp.json`

**Copyright 2026 klikli-dev; author Kli Kli.** The language asset and its Japanese adaptation use **CC BY 4.0**, full text `LICENSES/CC-BY-4.0.txt`: https://creativecommons.org/licenses/by/4.0/

Source: https://github.com/klikli-dev/magic-particles-lib/tree/ca615520afd23de078c256b3a47a086c22456a4c

Target: **1.4.0**, 2 keys, selected inside Theurgy. Modified **2026-09-20 (UTC)**: Japanese entity names are supplied; no Japanese file existed upstream. `REUSE.toml` assigns this `src/main/resources/**` language asset to CC BY 4.0. Attribution, license and modification notices remain attached; no extra restriction is imposed. `LICENSES/MagicParticlesLib-MIT-Code.txt` retains the upstream MIT code-license text for context, but it does **not** relicense these language assets as MIT. No code or shaders are included.

## SpectreLib — `assets/spectrelib/lang/ja_jp.json`

**Copyright (C) 2022 Illusive Soulworks.** **LGPL-2.1-only**: full text `LICENSES/GNU-LGPL-2.1.txt`. Original copyright/license/third-party notices are preserved verbatim in `LICENSES/SpectreLib-Original-Notice.txt`.

Source: https://github.com/illusivesoulworks/spectrelib/tree/58dc93dfa9bd26f573c02888c9807a679d6b500a

Target: **0.21.0+26.1.2**, 1 key, selected inside Comforts. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: a Japanese networking-error template is supplied while retaining its argument. The complete editable modified source is `assets/spectrelib/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository), under LGPL-2.1-only.

Original notice also credits **Forge Development LLC and contributors** for modified configuration-system portions under LGPL 2.1, and **TheElectronWill** for NightConfig under LGPL 3.0. Those notices are retained; this ZIP contains no Forge/NightConfig implementation or SpectreLib JAR. They do not change this language asset's LGPL-2.1-only scope. The LGPL 2.1 full text is the FSF license text maintained by SPDX, with the canonical license at https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.

## Advanced AE — `assets/advanced_ae/lang/ja_jp.json`

**Pedroksl.** Original project credits: **Ridanisaurus Rid** (texture style), **Jm³** and **Sea_Kerman** (models). Those images and models are not included. **LGPL 3.0**: `LICENSES/AdvancedAE-LGPL-3.0.md`, with `LICENSES/GPL-3.0.txt`.

Source: https://github.com/pedroksl/AdvancedAE/tree/03d04eb70717591c33aeafbdb33656bd24267042

Target: **26.1.7**, 245 keys. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese names, settings, explanations and search terms are revised/supplied. Existing Japanese originates in the same upstream source; it is not claimed as wholly new work. The complete modified, human-readable source is `assets/advanced_ae/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository), under LGPL 3.0. The separately identified AE2AddonLib child has its own GPL scope above. No JAR, Java code, model or texture is included.

## ExtendedAE — `assets/extendedae/lang/ja_jp.json`

**GlodBlock.** Original metadata credits: **Sea_Kerman** (model), **Ridanisaurus** (new texture), **gt147532689** (Chinese Simplified), and **nekitbrush** (Russian). Those image, model and other visual assets are not included. GNU Lesser General Public License **3.0**: `LICENSES/ExtendedAE-LGPL-3.0.txt`; the LGPL incorporates GPLv3 terms, and the full GPL is also included in `LICENSES/GPL-3.0.txt`. This Japanese adaptation remains under LGPL 3.0, not MIT.

Target: **26.1-1.0.4-neoforge**, 253 keys. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese names, settings, explanations and search terms are revised/supplied. No executable code is changed.

Exact source: https://github.com/GlodBlock/ExtendedAE/tree/333be17a2b936c4b20f24edff6fd9fa61743ecc0

Original English: https://github.com/GlodBlock/ExtendedAE/blob/333be17a2b936c4b20f24edff6fd9fa61743ecc0/src/main/resources/assets/extendedae/lang/en_us.json

Original Japanese: https://github.com/GlodBlock/ExtendedAE/blob/333be17a2b936c4b20f24edff6fd9fa61743ecc0/src/main/resources/assets/extendedae/lang/ja_jp.json

The complete modified, human-readable source is `assets/extendedae/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository), under LGPL 3.0. The existing upstream Japanese values are retained where applicable and are not claimed as wholly new work. Original and modified hashes are recorded in `reviews/extendedae.json` and `release.json`. GuideME in-game guide pages (45 pages), hardcoded display text, and image/model assets are outside this 253-key language scope.

## Comforts — `assets/comforts/lang/ja_jp.json`

**Copyright (C) 2017–2022 Illusive Soulworks.** LGPL **3.0-or-later**. The original `LICENSE`, GPL `COPYING`, and LGPL `COPYING.LESSER` are retained as `LICENSES/Comforts-LGPL-3.0-or-later.txt`, `LICENSES/Comforts-COPYING.txt`, and `LICENSES/Comforts-COPYING.LESSER.txt`. The original SpectreLib notice remains separate in `LICENSES/SpectreLib-Original-Notice.txt`.

Source: https://github.com/illusivesoulworks/comforts/tree/eadbf86be195ec384341a8944b8d717164d52805

Target: **15.0.0+26.1.2**, 84 current English keys. The upstream Japanese asset has 83 keys; existing Japanese provenance is retained and current missing keys are supplied. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. Only the editable language asset is included; no Comforts or SpectreLib JAR, code, textures or models are included.

## Crafting on a Stick — `assets/crafting_on_a_stick/lang/ja_jp.json`

**OfekN.** GNU **GPL 3.0**; the original full license is `LICENSES/CraftingOnAStick-GPL-3.0.txt`.

Source: https://github.com/OfekN-mods/crafting-on-a-stick/tree/fa2f0470bbca0528046583fc8d1c58b95f390f5e

Target: **26.1-1.1**, 14 current English keys. Four existing Japanese values from the upstream asset are retained as provenance and reviewed; the remaining current values are supplied or revised. Modified **2026-09-20 (UTC)**. Only the language asset is included; no MOD JAR, code or other assets are included.

## Toast Control — `assets/toastcontrol/lang/ja_jp.json`

**Brennan Ward (Shadows_of_Fire).** MIT: `LICENSES/ToastControl-MIT.txt`.

Source: https://github.com/Shadows-of-Fire/Toast-Control/tree/7ff041c7bb4a5bb113f3bea0568f9e986b800af9

Target: **26.1.2-10.0.0**, 2 keys. No upstream Japanese asset was found; Japanese values are supplied by ATM11 Japanese project / ueda-keisuke, modified **2026-09-20 (UTC)**. Only the language asset is included.

## Better Advanced Tooltips — `assets/betteradvancedtooltips/lang/ja_jp.json`

**Latvian DEV.** MIT: `LICENSES/BetterAdvancedTooltips-MIT.txt`.

Source: https://github.com/latvian-dev/better-advanced-tooltips/tree/feed1c23eba70c56fd5560336b2785cd6ff969f9

Target: **2601.1.0-build.9**, 5 keys. No upstream Japanese asset was found; Japanese values are supplied by ATM11 Japanese project / ueda-keisuke, modified **2026-09-20 (UTC)**. Only the language asset is included; no code or other assets are included.

## Building Gadgets 2 — `assets/buildinggadgets2/lang/ja_jp.json`

**Copyright (c) 2023 Direwolf20-MC.** MIT: the full original notice is preserved in `LICENSES/BuildingGadgets2-MIT.txt`. This language adaptation retains MIT terms.

Source: https://github.com/Direwolf20-MC/BuildingGadgets2/tree/f669d20cebe287202421d2d83ddb9906baafeeab

Target: **1.4.6**, 113 current English language keys. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese item names, action labels and explanations are revised or supplied. The current generated-client English source matches the installed MOD language bytes. The editable modified JSON and accepted review provenance are included; no MOD JAR, Java, images or private configuration is bundled.

Existing Japanese from the same upstream tree is acknowledged and is not claimed as wholly original work. The original Japanese-only legacy key is outside this current English-key scope and may remain inherited from the base MOD.

## Charging Gadgets — `assets/charginggadgets/lang/ja_jp.json`

**Copyright © 2018 Direwolf20.** MIT: the full original notice is preserved in `LICENSES/ChargingGadgets-MIT.txt`. This language adaptation retains MIT terms.

Source: https://github.com/Direwolf20-MC/ChargingGadgets/tree/9e464f1c5fcdb5f02cb8b1020f0fa9c2f5b0e97a

Target: **1.16.1**, 6 current English language keys plus four derived configuration labels/tooltips in this release. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese item names, action labels and explanations are revised or supplied. The current generated-client English source matches the installed MOD language bytes. The editable modified JSON and accepted review provenance are included; no MOD JAR, Java, images or private configuration is bundled.

The four ConfigSpec-derived Charging Gadgets labels/tooltips were added with the 0.11 language scope. Version 0.12 adds Japanese Range labels through the 46-key NeoForge common configuration scope. The hardcoded menu title, the remaining NeoForge language keys and the rest of the configuration screen remain outside scope; this does not claim that the common UI is fully Japanese. The source range display says `> 0`, while the verified implementation accepts zero; this release does not present that display text as a corrected rule.

## Curios — `assets/curios/lang/ja_jp.json`

**C4 / TheIllusiveC4.** LGPL-3.0-or-later: the complete texts are preserved as `LICENSES/Curios-LGPL-3.0-or-later.txt`, `LICENSES/Curios-COPYING.txt`, and `LICENSES/Curios-COPYING.LESSER.txt`.

Source: https://github.com/TheIllusiveC4/Curios/tree/8f2f1321e4c3a005e16067aa4dd1eec200946dba

Target: **15.0.0+26.1.2**, 48 current English-corresponding entries. The fixed English and existing Japanese assets match the installed JAR and official source byte-for-byte; the existing Japanese provenance is retained. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. The editable Japanese JSON and accepted review provenance are included. No Curios JAR, Java code, images or configuration is bundled.

## Nature's Compass — `assets/naturescompass/lang/ja_jp.json`

**ChaosTheDude.** CC BY-NC-SA 4.0: the complete original license is preserved in `LICENSES/NaturesCompass-CC-BY-NC-SA-4.0.md` and its noncommercial, attribution, modification-notice and ShareAlike terms apply.

Source: https://github.com/MattCzyr/NaturesCompass/tree/fdb412eb41e615c7702dcedf8ea422c1aebf4216

Target: **26.1-3.3.0-neoforge**, 44 entries: 43 Japanese language values and one preserved original `_comment` metadata entry (`STRINGS - PRECIPITATION`). The fixed English and existing Japanese assets match the installed JAR and official source byte-for-byte; no individual existing Japanese translator is named in the asset. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. No Nature's Compass JAR, code, images or configuration is bundled.

## Simple Backups — `assets/simplebackups/lang/ja_jp.json`

**MelanX.** Apache-2.0: the complete original license is preserved in `LICENSES/SimpleBackups-Apache-2.0.txt`.

Source: https://github.com/ChaoticTrials/SimpleBackups/tree/e2fa606f297031a50dd569f53c94623a72168fd5

Target: **26.1.5**, 43 entries: 42 Japanese language values and one project notice `_comment`. The notice reads: `Modified by ATM11 Japanese project / ueda-keisuke on 2026-09-20: Japanese language entries revised or supplied. Original project: Simple Backups by MelanX; Apache-2.0. See NOTICE.md and LICENSES/SimpleBackups-Apache-2.0.txt.` It is an Apache 4(b) modification notice, not a translated game string. No upstream NOTICE file was found in the fixed JAR/source context. No Simple Backups JAR, code, saves, images or configuration is bundled.

## ElevatorID — `assets/elevatorid/lang/ja_jp.json`

**VsnGamer / Vasco.** MIT: the complete original license is included as `LICENSES/ElevatorID-MIT.txt`; the original copyright and permission notice must remain attached.

Source: https://github.com/VsnGamer/ElevatorMod/tree/e3938408148658fd9b725cb6d48698fd433e6c91

Target: **26.1-1.16.2**, 29 language entries. The fixed English and existing Japanese assets match the installed JAR and fixed source byte-for-byte. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. This release includes only the editable Japanese language asset; no JAR, Java code, configuration or other assets.

## Mystical Automation — `assets/mysticalautomation/lang/ja_jp.json`

**BlakeBr0.** MIT: the complete original license is included as `LICENSES/MysticalAutomation-MIT.txt`; the original copyright and permission notice must remain attached.

Source: https://github.com/BlakeBr0/MysticalAutomation/tree/d108d5d91e6e620d9dbaff0e197f5b668352fb14

Target: **2.0.6**, 42 language entries. The fixed English and existing Japanese assets match the installed JAR and fixed source byte-for-byte. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. This release includes only the editable Japanese language asset; no JAR, Java code, configuration or other assets.

## NeoForge configuration surface — `assets/neoforge/lang/ja_jp.json`

**The NeoForged Team.** LGPL-2.1-only: the complete text is preserved as `LICENSES/NeoForge-LGPL-2.1.txt`.

Fixed source: https://github.com/NeoForged/NeoForge/tree/dfe28573ea51212ebdc813783f3de80e8a8aa06c

Target: **26.1.2.106**, 46 original NeoForge configuration UI keys. The installed universal JAR is not included. The existing NeoForge Japanese asset is upstream provenance. ATM11 Japanese project / ueda-keisuke revised these 46 entries on **2026-09-20 (UTC)** and provides the editable modified Japanese JSON. The remaining 220 NeoForge language keys, individual MOD-derived configuration strings and hardcoded UI are outside scope.

Public provenance: `reviews/neoforge.json` records the original English language hash, universal-JAR hash, runtime artifact identity, modified Japanese language hash and accepted review references. The official source archive is https://maven.neoforged.net/releases/net/neoforged/neoforge/26.1.2.106/neoforge-26.1.2.106-sources.jar (SHA-256: `b66d4b0f22ff9b4d110c5a0d29a0cd3c496c3445dd2034bed225d4f56eac00af`). This release retains the complete LGPL text and The NeoForged Team attribution.

## More Overlays Updated — `assets/moreoverlays/lang/ja_jp.json`

**feldim2425, RiDGo8.** MIT: the complete original notice is preserved as `LICENSES/MoreOverlays-MIT.txt`.

Fixed source: https://github.com/r8420/MoreOverlays-updated/tree/c8ad202050dc92ff94be1b7fe34903985c883932

Target: **1.24.4**, 40 language keys. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. The editable modified Japanese JSON and accepted review provenance are included; no JAR, Java source, configuration or image is included.

## Interdimensional Wireless Transmitter — `assets/interdimensionalwirelesstransmitter/lang/ja_jp.json`

**Ultramega.** MIT: the complete original notice is preserved as `LICENSES/InterdimensionalWirelessTransmitter-MIT.txt`.

Fixed source: https://github.com/starforcraft/Interdimensional-Wireless-Transmitter/tree/47e96d5f9e2674acefd4a95a14e913363f66ca12

Target: **26.1.2-1.0.1**, 10 language keys. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. The transmitter requires Refined Storage and provides cross-dimensional, unlimited-range network access; no Refined Storage assets, JAR, Java source, logo or textures are included. The editable modified Japanese JSON and accepted review provenance are included.

## Enchantment Descriptions — `assets/enchdesc/lang/ja_jp.json`

**Darkhax.** LGPL-2.1-only: the complete original license is preserved as `LICENSES/EnchantmentDescriptions-LGPL-2.1.txt`. This Japanese language adaptation is provided under the same terms.

Fixed source: https://github.com/Darkhax-Minecraft/Enchantment-Descriptions/tree/20c67ad705944c9721355a2049d11563c61cf208

Target: **26.1.2.6**, 183 current English-corresponding keys: 170 language entries and 13 verbatim original metadata entries. The fixed source English and Japanese assets match the installed JAR as parsed JSON; serialization differs. Existing Japanese from the same project is acknowledged and is not claimed as wholly original work. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. The complete modified, human-readable source is `assets/enchdesc/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository). The original support links and metadata remain unchanged. Third-party integrations named by the descriptions are not bundled. Description availability depends on the actual lookup route and installed integrations; original keys are retained, including the source `enchantment.endlessbiomes.shared_pain` key without a description suffix.

## Extreme Sound Muffler — `assets/extremesoundmuffler/lang/ja_jp.json`

**LeoBeliik.** LGPL-3.0-only: the full original LGPL text is `LICENSES/ExtremeSoundMuffler-LGPL-3.0.txt`, with the incorporated GPLv3 terms in `LICENSES/GPL-3.0.txt`. This Japanese language adaptation is provided under LGPL-3.0-only.

Fixed source: https://github.com/LeoBeliik/ExtremeSoundMuffler/tree/6ec1ead220b7703c2a0f3537e625b4033239f557

Target: **4.03**, 93 current English language keys. The fixed English source and installed JAR asset match byte-for-byte. The upstream Japanese `lang/needUpdate/ja_jp.json` file is legacy context, not a runtime language asset or an extra file in this release. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke. The complete editable modified source is `assets/extremesoundmuffler/lang/ja_jp.json` in this ZIP (`resourcepack/` in the repository). An unresolved volume-slider narration consumer issue is outside this language-only modification.

## Super Factory Manager — `assets/sfm/lang/ja_jp.json`

**TeamDman.** Mozilla Public License **2.0**: the full original license is `LICENSES/SuperFactoryManager-MPL-2.0.txt`. This modified language file is Covered Software supplied in Source Code Form under MPL 2.0. The complete, editable modified source is `assets/sfm/lang/ja_jp.json` in this ZIP and `resourcepack/assets/sfm/lang/ja_jp.json` in the public repository. Recipients may obtain and modify it under the MPL 2.0 terms; no additional restriction applies to this file.

Fixed source: https://github.com/TeamDman/SuperFactoryManager/tree/fe32b29453b13b4f3050ad441677c7eb79e80814 (tag `4.34.0-26.1.2`).

Target: **4.34.0**, 277 current English language keys from the installed JAR. English language generation is defined in upstream Java localization declarations; this release does not claim byte identity with a tracked source English JSON file. The original generated language asset and JAR hashes are pinned in `reviews/sfm.json`. Modified **2026-09-20 (UTC)** by ATM11 Japanese project / ueda-keisuke: Japanese names, action labels, diagnostics and explanations are supplied. For `gui.sfm.item_inspector.copied_to_clipboard`, the original `Copied {} characters to clipboard!` uses a placeholder incompatible with the actual Minecraft translatable-component consumer. The Japanese value uses `%s` for the supplied character-count component; native composition was checked with 0, 1, 127 and 1024 characters. Other identifiers, DSL syntax and argument contracts retain their source meanings. No SFM JAR, Java implementation, DSL program, model, texture or other third-party asset is bundled.

## Project contributions and provenance

`LICENSES/Project-MIT.txt` applies to this project's build script, original project documentation, and its additions to the MIT namespaces (Transmog, JEI, Controlling, Searchables, Resourceful Config, AE2WTLib API, Kuma API, Apollib, Toast Control, Better Advanced Tooltips, Cucumber, Iron Jetpacks, Functional Storage, Building Gadgets 2, Charging Gadgets, ElevatorID, Mystical Automation, More Overlays Updated, Interdimensional Wireless Transmitter), plus the AppleSkin additions as described above. It **does not** apply to ToolBelt, whose BSD-3-Clause notice remains applicable, or to NeoForge, Jade, AE2 Network Analyzer, Cumulus Menus, Sodium, Better Advancements, QuarryPlus, Code Defined GUI, SathLib, AE2AddonLib, EnderIO, Magic Particles Lib, SpectreLib, Advanced AE, ExtendedAE, Comforts, Crafting on a Stick, Curios, Nature's Compass, Simple Backups, Enchantment Descriptions, Extreme Sound Muffler, Super Factory Manager, their adaptations, or quoted/upstream license texts. Original notices remain applicable to original material.

`release.json` binds the language bytes and review summaries. Each `reviews/<namespace>.json` identifies exact original source/JAR hashes, independently accepted keys, reviewer and review/submission hashes. Nested sources also bind the parent JAR, every archive member/hash and catalog source ID. These are provenance records, not digital signatures or proof that every game screen has been visually tested.

## DimStorage — `assets/dimstorage/lang/ja_jp.json`

Original project: **Edivad99**. Upstream credits: **Thegaarnik**. The complete upstream GNU Affero General Public License version 3 is retained at `LICENSES/DimStorage-AGPL-3.0.txt`. This project's modified language file is provided under **AGPL version 3**. This applies to the DimStorage language work; it does not relicense other independently licensed namespace files in this aggregate.

Fixed source: https://github.com/Edivad99/DimStorage/tree/38a8f7bfe2935b68f8ff9eff90f0dd85e97841bc

Upstream language sources: [English](https://github.com/Edivad99/DimStorage/blob/38a8f7bfe2935b68f8ff9eff90f0dd85e97841bc/src/generated/resources/assets/dimstorage/lang/en_us.json), [existing Japanese and its contributors](https://github.com/Edivad99/DimStorage/blob/38a8f7bfe2935b68f8ff9eff90f0dd85e97841bc/src/main/resources/assets/dimstorage/lang/ja_jp.json).

Modified by ATM11 Japanese project / ueda-keisuke on **2026-09-20 (UTC)**: revised or supplied the 36 Japanese language entries against the installed 10.0.1 English source, retaining keys and formatting. The existing Japanese source and its contributors remain credited. The complete modified language source is the readable, editable JSON included in this ZIP and in `resourcepack/assets/dimstorage/lang/ja_jp.json` in this repository; no compiled form of it is substituted. The public builder used to assemble the ZIP is `build_pack.py`. Recipients may modify and redistribute this language work under the included AGPL version 3 terms. No additional restriction is imposed on this work by the collection. This language-only overlay requires the separately installed original MOD; MOD JARs, Java code, textures and models are not included. No warranty is provided, as stated in the included license.

Installed source JAR SHA-256: `e6808c0fe40f671dd0625c9ab612fd75fe5453a528a58580f13c21a0b93c7511`. English entry SHA-256: `4713de32d6f9833840fad59f9f56b0f036715e5846270c5694c49b5f3c057eeb`. Existing Japanese entry SHA-256: `8828e5d62e0561a71e97ca4d065f1705a8092386a77216a8305f0b96ddef3bac`. Both language entries match the fixed source byte-for-byte. Full license SHA-256: `8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef`.

## Step Crafter — `assets/stepcrafter/lang/ja_jp.json`

**Copyright (c) 2025 Starforcraft.** Author: **Ultramega**. MIT: full original text retained at `LICENSES/StepCrafter-MIT.txt`; the Japanese language adaptation retains MIT.

Fixed source: https://github.com/starforcraft/Step-Crafter/tree/99ca4e98b28995060363ed1f4c275c9daab51480

Upstream [English language source](https://github.com/starforcraft/Step-Crafter/blob/99ca4e98b28995060363ed1f4c275c9daab51480/common/src/main/resources/assets/stepcrafter/lang/en_us.json). The installed JAR contains no Japanese language file. Modified by ATM11 Japanese project / ueda-keisuke on **2026-09-20 (UTC)**: supplied 80 Japanese language entries. One speed-multiplier explanation corrects the upstream words “slot upgrade”: the installed implementation counts Refined Storage Speed Upgrades for speed, and counts Slot Upgrades separately for filter rows. The formula identifiers and translation key are retained. This is a wording correction only; no MOD code or behavior is changed.

Installed version: 26.1.2-1.0.3. JAR SHA-256: `78a5392cf562e75bf803937f6f41d28b51aba3c474e1c95f5aab5ec265abee30`. English entry SHA-256: `2184445666a7b0571b923e0f090a8359e9153dfd2408f41c263a8ee71694c293`. Fixed source English SHA-256: `de1facacb33443f6d17ed9c5e3d58ca555e1978726c363715617b981389abe69`; parsed keys and values match, while serialization bytes differ. Full license SHA-256: `976da1a41c4b86061101f101832ac3d904d95c6836554f5a260c202338b5427d`.

Only the editable language overlay is included. Refined Storage parent language assets, JARs, Java code, textures and models are excluded.

## Refined Storage - Quartz Arsenal — `assets/refinedstorage_quartz_arsenal/lang/ja_jp.json`

**Copyright © 2024 - 2026 Refined Mods.** MIT: the full original license is retained at `LICENSES/RefinedStorageQuartzArsenal-MIT.md`; the Japanese language adaptation retains MIT.

Fixed source: https://github.com/refinedmods/refinedstorage-quartz-arsenal/tree/a1bafea4d8eaf38ca791b2454c33d1249442300d

Upstream language sources: [English](https://github.com/refinedmods/refinedstorage-quartz-arsenal/blob/a1bafea4d8eaf38ca791b2454c33d1249442300d/refinedstorage-quartz-arsenal-common/src/main/resources/assets/refinedstorage_quartz_arsenal/lang/en_us.json), [existing Japanese and its contributors](https://github.com/refinedmods/refinedstorage-quartz-arsenal/blob/a1bafea4d8eaf38ca791b2454c33d1249442300d/refinedstorage-quartz-arsenal-common/src/main/resources/assets/refinedstorage_quartz_arsenal/lang/ja_jp.json).

Modified by ATM11 Japanese project / ueda-keisuke on **2026-09-20 (UTC)**: revised or supplied the 23 Japanese language entries, checking capacity and per-operation energy descriptions against their consumers. Existing Japanese language contributors remain credited through the fixed source above. Installed version: 2.0.6. JAR SHA-256: `4e1bd12aa644320195553e76edbdb159150dd51db6268f532544206567ef165a`. English entry SHA-256: `83bb43ab5a611522ace3a4ac70f099a28c82b1a70fea3ab571dfffad84eb5f39`. Existing Japanese entry SHA-256: `32cc7fbb3739ae203fa69ffb034a4d6ea2a0684799c2f7e14cb564b1d2170bf9`. Both language entries match the fixed source byte-for-byte. Full license SHA-256: `4f332ed10b4b214c0397a37b0344aa5fd4517ea5631e580c6b43676f92ad9f4e`.

Only the editable language overlay is included; Refined Storage parent assets, JARs, Java code, textures and models are not distributed. The 23 keys do not claim coverage of every inherited or hardcoded interface.
