# ATM11 日本語改善

ATM11 で使う一部 MOD の日本語を改善する、非公式リソースパックです。**0.8.0 は31のMOD・内包ライブラリを対象に、2,321項目を1つのZIPへ収録します。** ATM11 全体の翻訳は進行中で、クエストや下表以外の MOD は含みません。

## 導入・解除

1. [リリース](https://github.com/ueda-keisuke/atm11-japanese/releases/latest)から **`ATM11-Japanese-0.8.0.zip`** をダウンロードします。非営利条件付きの Jade・Better Advancements 素材を含みます。再配布・改変時は下記の個別条件を確認してください。
2. 使用するインスタンスの `resourcepacks` フォルダへ、解凍せずに置きます。Prism Launcher ではインスタンス内の `minecraft/resourcepacks` です。
3. Minecraft の「設定」→「リソースパック」で有効にし、選択中の一覧の**一番上（最高優先度）、特に「MOD のリソース（MOD Resources）」より上**へ移動します。旧版の日本語改善パックを無効にします。0.3.0 を使っていた場合は、基本パックと Jade 専用パックの両方を無効にします。
4. 言語を「日本語」にして読み込みを完了します。

日本語が反映されないときはパックの並び順を確認してください。解除は設定で無効化し、不要になった ZIP を `resourcepacks` から削除します。

## 収録内容

| MOD / namespace | 対象版 | キー数 | 言語資産のライセンス |
| --- | --- | ---: | --- |
| Transmog / `transmog` | 1.8.0+26.1 | 25 | MIT |
| Just Enough Items / `jei` | 29.36.0.96 | 335 | MIT |
| AppleSkin / `appleskin` | 3.0.9（MC 26.1） | 22 | 原作 Unlicense |
| Controlling / `controlling` | 26.1.2.4 | 12 | MIT |
| Jade / `jade` | 26.1.10 | 496 | CC BY-NC-SA 4.0 |
| Searchables / `searchables` | 1.0.2 | 2 | MIT |
| Resourceful Config / `resourcefulconfig` | 4.0.1 | 32 | MIT |
| AE2 Network Analyzer / `ae2netanalyser` | 26.1-1.0.0-neoforge | 38 | LGPL 3.0 |
| Cumulus Menus / `cumulus_menus` | 2.0.15 | 35 | LGPL 3.0 |
| Sodium / `sodium` | 0.9.1 | 105 | PolyForm Shield 1.0.0 |
| Better Advancements / `betteradvancements` | 0.6.0.76 | 3 | Don't Be a Jerk 非営利ライセンス |
| QuarryPlus / `quarryplus` | 26.12.160 | 240 | LGPL 3.0 |
| Code Defined GUI / `codedefinedgui` | 1.12.0 | 63 | CC BY 4.0（言語資産） |
| SathLib / `sathlib` | 1.1.0+26.1.2 | 18 | LGPL 3.0 |
| AE2AddonLib / `ae2addonlib` | 26.1.3-alpha | 11 | GPL 3.0（今回の配布物） |
| AE2WTLib API / `ae2wtlib_api` | 26.1.1-beta | 5 | MIT |
| Kuma API / `kuma_api` | 26.1.2.2 | 4 | MIT |
| Apollib / `apollib` | 1.1.6 | 7 | MIT |
| Ender IO — Modded Conduits / `enderio` | 9.0.5-alpha | **1** | 元metadata CC0／原作 Unlicense |
| Magic Particles Lib / `magicparticleslib` | 1.4.0 | 2 | CC BY 4.0（言語資産） |
| SpectreLib / `spectrelib` | 0.21.0+26.1.2 | 1 | LGPL 2.1-only |
| Advanced AE / `advanced_ae` | 26.1.7 | 245 | LGPL 3.0 |
| ExtendedAE / `extendedae` | 26.1-1.0.4-neoforge | 253 | LGPL 3.0 |
| Comforts / `comforts` | 15.0.0+26.1.2 | 84 | LGPL 3.0-or-later |
| Crafting on a Stick / `crafting_on_a_stick` | 26.1-1.1 | 14 | GPL 3.0 |
| Toast Control / `toastcontrol` | 26.1.2-10.0.0 | 2 | MIT |
| Better Advanced Tooltips / `betteradvancedtooltips` | 2601.1.0-build.9 | 5 | MIT |
| ToolBelt / `toolbelt` | 2.9.5 | 26 | BSD-3-Clause |
| Cucumber / `cucumber` | 26.1.2-9.0.6 | 16 | MIT |
| Iron Jetpacks / `ironjetpacks` | 9.0.3 | 55（素材名14種類を含む） | MIT |
| Functional Storage / `functionalstorage` | 1.6.1 | 164 | MIT |

件数は現行英語に対応する **キー・項目数**で、表示文、ナレーション、検索補助語、保持した metadata を含みます。画面数や目視確認済みの文字列数ではありません。JEI 1・Jade 2・QuarryPlus 1の計4 metadataキーは翻訳件数には数えず、原文または既存日本語の機能設定を保持します。

対応環境は ATM11 **0.8.0-beta** / Minecraft **26.1.2** / NeoForge **26.1.2.106**。対象 MOD 本体は別途必要です。他の版は未確認です。独立レビューで受理された言語データだけを収録し、**本版のゲーム画面による実表示確認は0件**です。言語データのレビューや読み込み検証と、ゲーム画面の目視確認を区別しています。

EnderIOは **Modded Conduits内の `conduit.enderio.rs` 1キーだけ**が対象です。EnderIO全体の日本語化ではありません。API・内包ライブラリは表のnamespaceだけを収録します。

## 対応範囲と制限

構文エラーのある **低優先の `transmog:lang/ja_jp.json` だけ**を遮断して同梱の日本語を読み込みます。同じファイルを使う低優先パックの差分も遮断されます。他の30 namespace は通常のキー上書きで、filter は使いません。Iron Jetpacksのderived14キーは通常41キーとは別source・別reviewです。英語原文にない既存日本語キーは、基底リソースから残る場合があります。元 MOD の JAR は変更しません。ExtendedAE のゲーム内ガイド45ページ、開発中のQuarryPlus補助MOD、画像・モデルは収録しません。FTB UltimineはARR（All Rights Reserved）で公開許諾を確認できないため収録しません。

**QuarryPlusの直書きGUI・診断チャットの一部は未対応です。** 言語JSONを参照しない `Size`、`Top+` / `Bottom+` 系のボタン、`Modules`、プレイサーモード、発電機の通知等は、このパックでは置換できません。表の件数は対象言語JSONのキー数で、MODの全表示文を網羅した件数ではありません。

## ライセンスとクレジット

この ZIP は `assets/<namespace>/lang/ja_jp.json` ごとに独立した言語資産を集めたものです。**パック全体を MIT として配布しているわけではありません。** 個別ファイルを取り出して使う場合も、そのファイルに適用される条件を保持してください。同梱したことを理由に、MIT・Unlicense・CC BY・GPL・LGPL の素材へ別素材の非営利制限を追加しません。

- **Jade とその日本語改変**: CC BY-NC-SA 4.0。非営利目的、帰属・改変表示、同じライセンスでの共有が必要です。
- **AE2 Network Analyzer / Cumulus Menus / QuarryPlus / SathLib / Advanced AE / ExtendedAE とその日本語改変**: LGPL 3.0。GPL・LGPL全文、変更日、元ソース、編集できるJSONを同梱します。
- **AE2AddonLib**: 今回の日本語改変は公式LICENSEのGPL 3.0に従って配布します。元metadataのLGPL表示との差はNOTICEに記録しています。
- **SpectreLib**: LGPL 2.1-only。全文と元のForge／NightConfig通知を保持します。
- **Code Defined GUI / Magic Particles Libの言語資産**: CC BY 4.0。作者への帰属、出典・ライセンス・改変の表示を保持します。コード側のMITとは適用範囲が異なります。
- **Sodium とその日本語改変**: PolyForm Shield 1.0.0。競合用途を除く許容目的など、全文の条件が適用されます。本パックは原版 Sodium を必要とする日本語補助資産です。
- **Better Advancements とその日本語改変**: 原作の Don't Be a Jerk ライセンス。非営利条件などを保持します。
- **MITライセンスの言語資産**: 原作のMIT表示と作者表示を保持します。Toast Control と Better Advanced Tooltips を含みます。
- **Comforts**: LGPL 3.0-or-later。原文のLICENSE、GPLのCOPYING、LGPLのCOPYING.LESSER、SpectreLibの通知を保持します。
- **Crafting on a Stick**: GPL 3.0。原文LICENSEと作者表示を保持します。
- **FTB Ultimine**: ARRのため本版には収録しません。
- **AppleSkin**: 原作のUnlicenseと作者表示を保持します。
- **EnderIOの対象言語資産**: 内包metadataのCC0表示、原作のUnlicense、作者表示を保持します。本プロジェクトの追加分の適用範囲は [NOTICE.md](NOTICE.md) に記載しています。

元作者・既存訳者による公式版ではありません。作者、既存訳者、出典、変更内容、ライセンスの適用範囲は [NOTICE.md](NOTICE.md)、全文は [LICENSES/](LICENSES/) にあります。

## ソースから ZIP を作る

Python 3.10 以降の標準ライブラリだけで実行できます。

```sh
python3 build_pack.py --check
python3 build_pack.py
```

受理済みの訳文・独立レビュー要約・元 JAR と内包 chain の識別情報・複数sourceのidentity・完全なキー集合・ライセンスのhash、件数、pack format 84.0と限定filterを検証し、`dist/ATM11-Japanese-0.8.0.zip`を生成します。レビュー要約は`reviews/`にあります。元MODのJARや外部ライブラリは再ビルドに不要です。

ファイル順と日時を固定し、同じ入力と圧縮環境なら同じ ZIP を再生成できます。異なる bytes の既存 ZIP は上書きしません。以前の公開 ZIP・タグは変更しません。

## English

Unofficial Japanese improvements for **31 language namespaces / 2321 keys**, collected into **one ZIP**. Counts include narration, search terms and preserved metadata, not visually tested screens. ATM11 quests and other MODs are outside this release. Target: Minecraft 26.1.2 / NeoForge 26.1.2.106, with the exact MOD versions above.

Download `ATM11-Japanese-0.8.0.zip` from [Releases](https://github.com/ueda-keisuke/atm11-japanese/releases/latest), place it in `resourcepacks` without extracting, enable it **at the top, above MOD Resources**, disable previous editions, and select Japanese. Disable/remove the pack to uninstall. Only the malformed lower-priority Transmog Japanese file is filtered; no MOD JAR is changed. Iron Jetpacks normal and derived sources are reviewed separately.

Each namespace remains a separate work under its own license. **There is no blanket MIT grant.** The collection contains noncommercial Jade and Better Advancements material; Jade also requires attribution and ShareAlike. GPL/LGPL assets include readable modified JSON and their applicable full license texts; SpectreLib retains LGPL 2.1-only and original notices. Code Defined GUI and Magic Particles language assets use CC BY 4.0. Sodium retains PolyForm Shield conditions. These conditions do not relicense unrelated namespace files. See `NOTICE.md` and `LICENSES/` for the individual scopes, credits and full terms. Only accepted review inputs pass the builder. **Game-screen visual checks for this version: 0.** Review and loader checks are separate from visual QA. ExtendedAE in-game guide pages (45 pages), the experimental QuarryPlus helper MOD, FTB Ultimine (ARR without public redistribution permission), and images/models are excluded. QuarryPlus hardcoded GUI labels and diagnostic messages remain partly untranslated; this language-only pack cannot replace them. EnderIO scope is only `conduit.enderio.rs` from its Modded Conduits child; the rest of EnderIO is outside this release.
