# ATM11 日本語表示補助 MOD 0.4.0-dev

言語ファイルを参照しない表示を日本語化し、NeoForgeのチャンク生成進捗エラー表示へ不足していた引数を渡す補助MODです。
QuarryPlusの画面ラベル9項目、Mining Gadgetsの精密モード2項目、Measurementsの色選択35項目を対象にします。
日本語の訳文は、作成担当とは別の担当が原文と表示処理に照らして確認しています。
ATM11全体の日本語化が完了したものではありません。0.4で追加した修正は新しい翻訳キーを追加せず、NeoForgeの既存キー `commands.neoforge.chunkgen.progress_bar_errors` を使います。

**開発版です。ゲーム画面の描画・文字幅・クリック操作は未確認です。**
検証済みの範囲は、このソースと同時に配布する検証記録に示します。
言語リソースパックとは別のMODで、元のMODファイルを変更しません。

## 対応環境と導入

- Minecraft **26.1.2** / NeoForge **26.1.2.106**。
- QuarryPlus **26.12.160**、Mining Gadgets **1.19.3**、Measurements **4.0.0** の固定クラスを対象にします。
  それぞれのMODに対応する機能を独立して有効にします。
  対象クラスが異なる版では、そのMOD向けの修正を適用しません。
- 元のMODとゲームは、利用者が別途正規に入手してください。

ゲームを終了し、以前の `atm11-japanese-helper-*.jar` があれば取り除いたうえで、
`atm11-japanese-helper-0.4.0-dev.jar` をインスタンスの `minecraft/mods` へ入れます。
Minecraftの言語を日本語にしてください。通常のリソースパックと併用できます。
本補助MODには、対象46ラベルの日本語と英語の代替表示を含みます。
解除するには、ゲームを終了して本補助MODのJARだけを取り除きます。

QuarryPlus、Mining Gadgets、Measurementsの3機能はクライアント側の任意機能です。NeoForgeのチャンク生成エラー数修正は、統合サーバーではクライアントに入れた本MODが担当します。専用サーバーでそのコマンド表示を修正するには、専用サーバー側にも本MODを導入してください。クライアントだけに入れても、接続先のリモートサーバーの表示は修正しません。専用サーバーの起動、ワールド、通信、画面描画は確認していません。

## 対象となる表示

QuarryPlusではChunk Markerのサイズ・上下端ボタン、Module画面の見出し、
Placerの3つの操作ラベルを置き換えます。既存のボタン番号や処理は維持します。
診断チャット、発電機の通知など、ほかの直書き表示は対象外です。

Mining Gadgetsでは、精密モードの現在の状態を「精密モード：有効」または
「精密モード：無効」と表示します。画面を開いた直後と、切り替えた後の両方が対象です。
切り替え処理とサーバーへの通知は元の命令のままです。
通常の86言語項目は、別途公開している日本語改善リソースパックの範囲です。

Measurementsでは、線の色17種類と文字の色18種類の選択肢を日本語化します。
設定に保存する識別子や、測定の作成時に選ばれる色は維持します。
対応する翻訳が見つからない場合は、元の識別子を表示します。
NeoForgeの色選択表示に使うAPIと処理も固定クラスのハッシュで確認します。

## ソースから再生成する

Python 3.11以上、JDK 25.0.1、正規に入手した対応版のゲーム・NeoForgeライブラリと
元の3つのMOD JARを用意します。Prism Launcherのライブラリ相対パスと固定ハッシュは
`dependencies.lock.json` に記録しています。スクリプトは外部ファイルをダウンロードしません。

```sh
python3 build.py \
  --prism-root "/path/to/PrismLauncher" \
  --quarry-jar "/path/to/AdditionalEnchantedMiner-26.1.2-neoforge-26.12.160.jar" \
  --mining-jar "/path/to/mininggadgets-1.19.3.jar" \
  --measurements-jar "/path/to/Measurements-neoforge-26.1-4.0.0.jar" \
  --language-pack "/path/to/ATM11-Japanese-0.21.0.zip" \
  --java-home "/path/to/jdk-25.0.1" \
  --verify
```

`--prism-root` は `libraries/` を含むディレクトリです。
`--verify` には別途取得した日本語改善パック0.21.0が必要です。`--language-pack`で指定してください。
このZIPはNeoForgeの修正後の日本語を確認するために使い、補助MODへ同梱・インストールはしません。
出力は `build/atm11-japanese-helper-0.4.0-dev.jar` です。
ビルド時には3つの元MODが必要ですが、ゲームでの使用時はそれぞれ任意です。
固定の依存ファイルと原クラス、独立レビュー、翻訳資産、ソースのハッシュを確認し、
出力が `release-inputs.json` の参照JARと完全に一致した場合だけ成功します。
時刻・ファイル順・属性・無圧縮方式を固定しています。
macOS以外での再生成は未確認です。別OSのJDKは参照JDKと同じバイト列とは扱いません。

## 検証範囲

`--verify` は実際のMixinエンジンと元MODのクラスを使うオフライン検証です。
QuarryPlusの3クラス・12箇所、Mining Gadgetsの1クラス・2箇所を対象に、
表示の呼び出し以外の元の命令が維持されることを調べます。
Measurementsでは2つの色の型に表示名を追加し、元のメソッドと選択肢の順序が維持されることを確認します。
NeoForgeの実際の表示処理で35項目の訳文と代替表示を検証し、同じ表示部品が言語の変更に追従するかを調べます。
設定変更のコールバックとメモリ上のTOML変換も確認します。
`OptionInstance.set` 自体には起動中のゲームが必要なため、この検証では値の設定と実コールバックの呼び出しを分けています。
対象MODが存在しない場合・クラスが変更されている場合・すべてがない場合にも、
無関係な機能を巻き込まずに適用を見送ることを検証します。

NeoForgeのチャンク生成進捗エラー修正では、固定した `GenerationBar` と `CommandUtils` の呼出し形を確認し、既存キーへエラー数を渡します。新しい翻訳キー、元のNeoForgeクラス、バイナリは追加・同梱しません。
CLIENT・SERVERの実Mixin変換と元の進捗表示処理を使い、エラー数0・1・11、進捗率と文字色、英語・日本語への切り替えを確認します。
対象クラスがない場合・変更された場合・対象の呼び出しが変更された場合と、クライアント用の3つのMODを含めないSERVER側の適用も確認します。
実行時のガードは対象クラスと呼び出し形を確認します。英語原文のキーと引数書式は、これとは別にビルド時に確認します。

Minecraftの実際の言語・Component処理による表示確認と、画面描画は別の検証です。
この版では、ウィンドウの作成、画面全体の初期化、実際のクリック・通信は行いません。
ゲーム起動の失敗やログに記録された変換だけを、画面表示の成功とは扱いません。

## 出典とライセンス

補助MODのJavaソースは LGPL-3.0-only です。LGPL-3.0・GPL-3.0の全文と、
Mining Gadgets由来の2ラベルとMeasurements由来の35ラベルに適用されるMITの原文を `LICENSES/` に収録しています。
MOD全体を一律にMITとして配布するものではありません。
原作者、固定した出典、変更内容は `NOTICE.md` を参照してください。
バイナリを再配布するときは、この版に対応したソース・ビルド手順・ライセンスも提供してください。
元のゲーム・MOD・依存JAR・変換後の原クラスは配布物に含みません。

`language-contract.json` と `mining-language-contract.json` が、それぞれ9項目と2項目の原文契約です。
`measurements-language-contract.json` が色選択35項目の原文契約です。
`reviews/` は元の提出と独立レビュー、`translation-evidence.json` はそれらと資産の対応です。
記録中の `localization/...` は原記録の識別子で、ビルド時に外部ワークスペースを参照するパスではありません。
`/root/...` はエージェント識別子です。個人のホームディレクトリは含みません。

## English

Development helper for nine QuarryPlus GUI labels, the enabled/disabled
precision-mode captions in Mining Gadgets, plus 35 Measurements color-selector captions. Target: Minecraft 26.1.2, NeoForge 26.1.2.106,
QuarryPlus 26.12.160, Mining Gadgets 1.19.3 and Measurements 4.0.0. Each optional feature has an independent
exact-class hash guard; an absent or different MOD disables only its corresponding feature. It also repairs the
missing error-count argument in NeoForge's existing chunk-generation progress message on the server that runs the command.
That repair adds no translation key. English fallback and forty-six independently reviewed Japanese captions are included.

Close the game, remove any older helper JAR, and put `atm11-japanese-helper-0.4.0-dev.jar`
in the client instance's `minecraft/mods` directory. Select Japanese. The three client display features do not require server installation.
The NeoForge error-count repair must be installed on a dedicated server to affect that server's command output; a client-only installation
cannot repair a remote server. Remove this JAR while the game is closed to uninstall. The original MOD JARs
are not modified. The ordinary Japanese language resource pack is distributed separately.

Use the command above with your own legitimate MOD JARs, Prism libraries and JDK 25.0.1
to reproduce the fixed artifact. For `--verify`, also obtain the published ATM11-Japanese-0.21.0.zip separately
and supply it through `--language-pack`; it is used only as an accepted Japanese test fixture and is not bundled or installed.
No original binaries are bundled or downloaded.
`--verify` runs real Mixin and native language/component checks without starting the game;
it is not a test of full screen initialization, clicking, packet delivery, rendering or layout.
Game-screen visual verification remains absent in this development release.
The Measurements checks use NeoForge's actual caption formatter and update callback,
with in-memory TOML round trips. They set the option's value field directly; they do not
execute `OptionInstance.set`, the MeasurementBox constructor, or live GUI interaction.

Helper source: LGPL-3.0-only, with complete LGPL/GPL texts and corresponding source. The NeoForge-derived repair references
NeoForge 26.1.2.106 and its LGPL-2.1 license text is included in `LICENSES/NeoForge-LGPL-2.1.txt`; NeoForged contributors
retain credit. The helper's patch code and the upstream NeoForge implementation are distinguished, and no NeoForge
original classes or binaries are bundled.
The Mining- and Measurements-derived captions retain their respective MIT notices. See NOTICE.md for source-specific
credits, terms and modification information. This is not complete ATM11 localization.
