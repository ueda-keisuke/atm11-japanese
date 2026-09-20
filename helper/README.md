# ATM11 日本語表示補助 MOD 0.2.0-dev

言語ファイルを参照しない表示を日本語化する、クライアント用の補助MODです。
QuarryPlusの9つの画面ラベルと、Mining Gadgetsの精密モードの「有効／無効」を対象にします。
日本語の訳文は、作成担当とは別の担当が原文と表示処理に照らして確認しています。
ATM11全体の日本語化が完了したものではありません。

**開発版です。ゲーム画面の描画・文字幅・クリック操作は未確認です。**
検証済みの範囲は、このソースと同時に配布する検証記録に示します。
言語リソースパックとは別のMODで、元のMODファイルを変更しません。

## 対応環境と導入

- Minecraft **26.1.2** / NeoForge **26.1.2.106**。
- QuarryPlus **26.12.160**、Mining Gadgets **1.19.3** の固定クラスを対象にします。
  片方だけ導入した環境でも、対応する機能を独立して有効にします。
  対象クラスが異なる版では、そのMOD向けの修正を適用しません。
- 元のMODとゲームは、利用者が別途正規に入手してください。

ゲームを終了し、以前の `atm11-japanese-helper-*.jar` があれば取り除いたうえで、
`atm11-japanese-helper-0.2.0-dev.jar` をインスタンスの `minecraft/mods` へ入れます。
Minecraftの言語を日本語にしてください。通常のリソースパックと併用できます。
本補助MODには、対象11ラベルの日本語と英語の代替表示を含みます。
解除するには、ゲームを終了して本補助MODのJARだけを取り除きます。

サーバーへの導入は不要です。サーバー用MODとして配布するものではありません。

## 対象となる表示

QuarryPlusではChunk Markerのサイズ・上下端ボタン、Module画面の見出し、
Placerの3つの操作ラベルを置き換えます。既存のボタン番号や処理は維持します。
診断チャット、発電機の通知など、ほかの直書き表示は対象外です。

Mining Gadgetsでは、精密モードの現在の状態を「精密モード：有効」または
「精密モード：無効」と表示します。画面を開いた直後と、切り替えた後の両方が対象です。
切り替え処理とサーバーへの通知は元の命令のままです。
通常の86言語項目は、別途公開している日本語改善リソースパックの範囲です。

## ソースから再生成する

Python 3.11以上、JDK 25.0.1、正規に入手した対応版のゲーム・NeoForgeライブラリと
元の2つのMOD JARを用意します。Prism Launcherのライブラリ相対パスと固定ハッシュは
`dependencies.lock.json` に記録しています。スクリプトは外部ファイルをダウンロードしません。

```sh
python3 build.py \
  --prism-root "/path/to/PrismLauncher" \
  --quarry-jar "/path/to/AdditionalEnchantedMiner-26.1.2-neoforge-26.12.160.jar" \
  --mining-jar "/path/to/mininggadgets-1.19.3.jar" \
  --java-home "/path/to/jdk-25.0.1" \
  --verify
```

`--prism-root` は `libraries/` を含むディレクトリです。
出力は `build/atm11-japanese-helper-0.2.0-dev.jar` です。
ビルド時には両方の元MODが必要ですが、ゲームでの使用時には片方だけでも構いません。
固定の依存ファイルと原クラス、独立レビュー、翻訳資産、ソースのハッシュを確認し、
出力が `release-inputs.json` の参照JARと完全に一致した場合だけ成功します。
時刻・ファイル順・属性・無圧縮方式を固定しています。
macOS以外での再生成は未確認です。別OSのJDKは参照JDKと同じバイト列とは扱いません。

## 検証範囲

`--verify` は実際のMixinエンジンと元MODのクラスを使うオフライン検証です。
QuarryPlusの3クラス・12箇所、Mining Gadgetsの1クラス・2箇所を対象に、
表示の呼び出し以外の元の命令が維持されることを調べます。
片方のMODが存在しない場合・クラスが変更されている場合・両方がない場合にも、
無関係な機能を巻き込まずに適用を見送ることを検証します。

Minecraftの実際の言語・Component処理による表示確認と、画面描画は別の検証です。
この版では、ウィンドウの作成、画面全体の初期化、実際のクリック・通信は行いません。
ゲーム起動の失敗やログに記録された変換だけを、画面表示の成功とは扱いません。

## 出典とライセンス

補助MODのJavaソースは LGPL-3.0-only です。LGPL-3.0・GPL-3.0の全文と、
Mining Gadgets由来の2ラベルに適用されるMITの原文を `LICENSES/` に収録しています。
MOD全体を一律にMITとして配布するものではありません。
原作者、固定した出典、変更内容は `NOTICE.md` を参照してください。
バイナリを再配布するときは、この版に対応したソース・ビルド手順・ライセンスも提供してください。
元のゲーム・MOD・依存JAR・変換後の原クラスは配布物に含みません。

`language-contract.json` と `mining-language-contract.json` が、それぞれ9項目と2項目の原文契約です。
`reviews/` は元の提出と独立レビュー、`translation-evidence.json` はそれらと資産の対応です。
記録中の `localization/...` は原記録の識別子で、ビルド時に外部ワークスペースを参照するパスではありません。
`/root/...` はエージェント識別子です。個人のホームディレクトリは含みません。

## English

Client-only development helper for nine QuarryPlus GUI labels and the enabled/disabled
precision-mode captions in Mining Gadgets. Target: Minecraft 26.1.2, NeoForge 26.1.2.106,
QuarryPlus 26.12.160 and Mining Gadgets 1.19.3. Each optional feature has an independent
exact-class hash guard; an absent or different MOD disables only its corresponding feature.
English fallback and eleven independently reviewed Japanese captions are included.

Close the game, remove any older helper JAR, and put `atm11-japanese-helper-0.2.0-dev.jar`
in the client instance's `minecraft/mods` directory. Select Japanese. No server installation
is needed. Remove this JAR while the game is closed to uninstall. The original MOD JARs
are not modified. The ordinary Japanese language resource pack is distributed separately.

Use the command above with your own legitimate MOD JARs, Prism libraries and JDK 25.0.1
to reproduce the fixed artifact. No original binaries are bundled or downloaded.
`--verify` runs real Mixin and native language/component checks without starting the game;
it is not a test of full screen initialization, clicking, packet delivery, rendering or layout.
Game-screen visual verification remains absent in this development release.

Helper source: LGPL-3.0-only, with complete LGPL/GPL texts and corresponding source.
The Mining-derived captions retain their MIT notice. See NOTICE.md for source-specific
credits, terms and modification information. This is not complete ATM11 localization.
