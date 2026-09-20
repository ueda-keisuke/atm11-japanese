# ATM11 Japanese Helper 0.2.0-dev — notices and source scope

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

Both features are client-only and independently check exact upstream class
hashes. A missing or changed target disables that feature. The original MOD JARs
are neither modified nor included. English fallback and eleven independently
reviewed Japanese labels are included; `translation-evidence.json` binds the two
separate source contracts and reviews in the corresponding source package.

Build-time/runtime dependencies are referenced, not bundled: Minecraft/NeoForge,
Sponge Mixin (MIT), ASM (BSD-3-Clause), and their installed dependencies.
No original game/MOD classes, textures, models, test fixtures, test code, logs or
transformed upstream classes are included in the helper JAR. Verification records
distinguish offline transformation/component checks from a full client launch and
visual checks. This development version has no verified game-screen rendering.
