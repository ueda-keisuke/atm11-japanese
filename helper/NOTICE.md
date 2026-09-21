# ATM11 Japanese Helper 0.6.0-dev — notices and source scope

Modified by ATM11 Japanese project / ueda-keisuke, 2026-09-20 (UTC).
New helper Java source is provided under LGPL-3.0-only. Complete LGPL-3.0 and
GPL-3.0 texts are in `LICENSES/`. Corresponding editable source, fixed dependency
identities and build instructions accompany this development artifact.

The QuarryPlus contribution connects nine GUI labels to language keys.
Source: QuarryPlus 26.12.160, commit `a758a34a27438a81b9a35038ccc1c77c586093f0`,
https://github.com/Kotori316/QuarryPlus/tree/a758a34a27438a81b9a35038ccc1c77c586093f0
by Kotori316. Upstream credits: Copyright (C) 2012, 2013 yogpstop;
2017-2024 Kotori316. The original nine accepted Japanese labels are retained.
The three QuarryPlus target classes and their twelve label injection sites remain
separate from the Mining Gadgets feature. QuarryPlus-derived material retains its
LGPL/GPL notices and applicable terms.

The Mining Gadgets contribution replaces Boolean precision-mode captions with
translatable enabled/disabled captions in initial button construction and after
a toggle. It preserves Boolean updates, packet sending and all other original
instructions. Source: Mining Gadgets 1.19.3, commit
`e36293a76d26f2bf5bf535e8483b8e505a890f59`,
https://github.com/Direwolf20-MC/MiningGadgets/tree/e36293a76d26f2bf5bf535e8483b8e505a890f59
Original copyright: Copyright © 2019 Direwolf20. JAR authors: Direwolf20,
ErrorMikey. Upstream credits: Direwolf20, ErrorMikey, CPW and the entire neoforge
team. Its two derived language captions retain the MIT terms and original notice
in `LICENSES/MiningGadgets-MIT.txt`; no blanket MIT grant applies to this helper.

The Measurements contribution provides translated names for the 17 LineColor and
18 TextColor enum choices through the existing NeoForge TranslatableEnum API.
It adds no new enum constants and preserves serialization, random selection and
axis-based color behavior. Measurements 4.0.0, by Mrbysco, fixed source commit
`72406856f7e26e83e38f220def86a7d3a69246b0`:
https://github.com/Mrbysco/Measurements/tree/72406856f7e26e83e38f220def86a7d3a69246b0
Copyright (c) 2021 Mrbysco. The derived captions retain the complete MIT notice
in `LICENSES/Measurements-MIT.txt`. The helper Java remains LGPL-3.0-only.
NeoForge's API and configuration consumer are runtime dependencies; their original
source and class bytes are not included. This feature is separate from the
Measurements primary language overlay and ConfigSpec tooltips.

The NeoForge GenerationBar repair adds no language key. It supplies the missing error-count argument to the existing
`commands.neoforge.chunkgen.progress_bar_errors` message for fixed NeoForge 26.1.2.106. It is a common-side runtime
repair for the server that runs the chunk-generation command: an integrated server can use the client installation, while
a dedicated server requires this helper on the dedicated server. A client-only installation cannot change a remote server.
The target `GenerationBar` and `CommandUtils` class hashes, fixed source commit, and callsite contract are recorded in
`neoforge-repair-contract.json`. The helper patch is our LGPL-3.0-only source; the upstream NeoForge implementation is
not bundled. NeoForged contributors retain their LGPL-2.1 credit and the complete text is in
`LICENSES/NeoForge-LGPL-2.1.txt`.

## AE2 Fluix repair

The Fluix repair is source-scoped to Applied Energistics 2 commit `3a051bb473de0b8fd329b39db4262f731d17e7e5`, version 26.1.10-beta, with Minecraft 26.1.2 / NeoForge 26.1.2.106. The helper source is LGPL-3.0-only. It changes only the material `Component` argument supplied by `appeng.items.tools.fluix.FluixSmithingTemplateItem` to the fixed `SmithingTemplateItem` constructor, replacing it with the existing `block.ae2.fluix_block` key in vanilla blue style. The item-name key remains `item.ae2.fluix_upgrade_smithing_template`.

The fixed AE2 source JAR SHA-256 is `8412a2208e56989b90e783e0a594c91a955ab8785d7d020fa4d8f342346110f2`. The guarded AE2 target class SHA-256 is `8dc05256c85429b1e4df18e36e5c8bdb93fc4171056cd1eb21a55461ad2b7e1c`; the guarded Minecraft superclass SHA-256 is `bd22e7bf41ed0f44b61808bb350489be81b463b68de429fc806ae9811d646b83`. The five fixed Fluix tool recipes use `ae2:fluix_block` as their addition. AE2 source, JAR, classes, recipes and assets are not distributed.

The separate ATM11-Japanese 0.27.0 language pack supplies the referenced existing CC0 key (`block.ae2.fluix_block`) and has SHA-256 `c978599b81ba24a8a04ae0d085e6fce7271af734e786608931cf776dca7350fb`. That language permission does not grant permission to redistribute AE2 code or assets.

The helper's runtime guard disables only Fluix when AE2 or the target classes are missing or mismatched. If the pre-apply constructor shape differs, the guard reports an `InvalidMixinException`; this is a verification/startup failure for the incompatible transformation, not a claim that the old shape remains safe. Execution results are supplied separately in the release asset `VERIFICATION-helper-0.6.0-dev.json`.

The formal 0.6 source package file set is fixed by SOURCE_PACKAGE_FILES.json and release-inputs.json. AE2 and JEI are separate build/verification inputs; neither original JAR is distributed. The public27 language overlay used for verification is pinned to SHA-256 `c978599b81ba24a8a04ae0d085e6fce7271af734e786608931cf776dca7350fb`.

The AE2 Charger repair reuses the existing `ae2.rei_jei_integration.charger_required_power` key for the literal output of the fixed `ChargerCategory$1.createWidgets` call. It does not add a translation key or change the turns/AE values. The client-side feature requires AE2 and JEI; absent dependencies, SERVER, or any of the seven guarded class hashes being missing or mismatched disables only this repair. A changed pre-apply shape raises `InvalidMixinException` and may abort loading. The actual CLIENT fixture uses null font/drawable and does not perform GUI rendering; no dedicated server is launched.

The Charger guard uses seven runtime class hashes. Whole AE2/JEI JAR hashes are build-time input checks only. The formal verification runner covers the 35 retained legacy cases, 9 Fluix cases and 25 Charger cases (69 total). Execution results are supplied separately in VERIFICATION-helper-0.6.0-dev.json; the source package alone is not evidence that those checks ran.

All six features are independently guarded by exact upstream class
hashes. A missing or hash-mismatched raw target disables only that feature. Changes detected immediately before transformation can instead reject loading with an error. The original MOD JARs
are neither modified nor included. English fallback and forty-six independently
reviewed Japanese labels are included; no new language key is added for Charger; `translation-evidence.json` binds the three
separate source contracts and reviews in the corresponding source package.

Build-time/runtime dependencies are referenced, not bundled: Minecraft/NeoForge,
Sponge Mixin (MIT), ASM (BSD-3-Clause), and their installed dependencies.
No original game/MOD classes, textures, models, test fixtures, test code, logs or
transformed upstream classes are included in the helper JAR. Verification records
distinguish offline transformation/component checks from a full client launch and
visual checks. This development version has no verified game-screen rendering.
