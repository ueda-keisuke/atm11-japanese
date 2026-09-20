# ATM11 Japanese Helper 0.4.0-dev — notices and source scope

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

All four features are independently guarded by exact upstream class
hashes. A missing or changed target disables only that feature. The original MOD JARs
are neither modified nor included. English fallback and forty-six independently
reviewed Japanese labels are included; `translation-evidence.json` binds the three
separate source contracts and reviews in the corresponding source package.

Build-time/runtime dependencies are referenced, not bundled: Minecraft/NeoForge,
Sponge Mixin (MIT), ASM (BSD-3-Clause), and their installed dependencies.
No original game/MOD classes, textures, models, test fixtures, test code, logs or
transformed upstream classes are included in the helper JAR. Verification records
distinguish offline transformation/component checks from a full client launch and
visual checks. This development version has no verified game-screen rendering.
