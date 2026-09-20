# ATM11 日本語改善

ATM11 で使用する **Transmog と JEI の日本語**を改善する、非公式リソースパックです。設定名、説明、ツールチップなどを対象とします。ATM11 全体の日本語化は進行中で、クエストや他 MOD の翻訳は含まれません。

**0.2.0 は Transmog 25 項目と JEI 334 項目、計359項目の表示文を収録**しています。すべて別担当による意味・自然さのレビューを通した訳文です。JEIの非表示メタデータ1件は原文のまま保持し、表示文の件数には含めていません。

対応環境：ATM11 **0.8.0-beta** / Minecraft **26.1.2** / NeoForge **26.1.2.106** / Transmog **1.8.0+26.1** / JEI **29.36.0.96**。MOD 本体は含まれていないため、対応する環境に別途導入してください。他のバージョンは未確認です。

## 導入

1. [最新版のリリース](https://github.com/ueda-keisuke/atm11-japanese/releases/latest)からリソースパックの ZIP をダウンロードします。0.2.0 以降は `ATM11-Japanese-<version>.zip`、0.1.0 は `ATM11-Japanese-Transmog-0.1.0.zip` です。
2. 使用する Minecraft インスタンスの `resourcepacks` フォルダへ、ZIP を解凍せずに置きます。Prism Launcher では対象インスタンスのフォルダ内にある `minecraft/resourcepacks` です。
3. Minecraft の「設定」→「リソースパック」で有効にし、選択中の一覧で**一番上へ移動**します。特に「MOD のリソース（MOD Resources）」より上に置いてください。旧版の日本語改善パックは無効にします。
4. 言語を「日本語」にして読み込みを完了します。

Transmog 1.8.0 の元の日本語 JSON に構文エラーがあるため、このパックは**低優先の `transmog:lang/ja_jp.json` だけ**を読み飛ばして、同梱の日本語を読み込ませます。同じファイルを使う低優先パックの日本語差分も対象になります。JEI にはこの遮断を適用せず、同梱したキーだけを上書きします。元の MOD JAR は変更しません。

MOD 本体より下に置くと、Transmog の回避処理が働きません。日本語が反映されない場合は、まず上記の並び順を確認してください。全項目のゲーム画面での目視確認はまだ行っていません。

解除するには、リソースパック設定で無効にします。不要になった ZIP は `resourcepacks` から削除できます。

## ソースから ZIP を作る

このリポジトリのルートディレクトリで実行します。Python 3.10 以降の標準ライブラリだけを使用します。

```sh
python3 build_pack.py --check
python3 build_pack.py
```

最初のコマンドは入力の検証だけを行います。2 番目は、受理済み日本語、名前空間、件数、訳文とレビュー要約の SHA-256、限定された filter、両 MOD のライセンスを検証し、`dist/ATM11-Japanese-<version>.zip` を生成します。`release.json` が `pending` の開発途中では両方とも拒否します。ファイル順・タイムスタンプを固定しているため、同じ入力と圧縮環境で再生成できます。既存バージョンの異なる ZIP は上書きしません。

収録件数・ファイルのハッシュは `release.json`、レビューの根拠は `reviews/` に記録します。表示文の件数には非表示の区切りコメントを含めません。

## ライセンスとクレジット

この翻訳パックと作成用スクリプトは MIT ライセンスで配布します。元 MOD の著作権表示・許諾文は各ファイルに保存しています。

- **Transmog / Hidoni**。元 MOD が記載する既存日本語訳の貢献者: **elinka47**。[MIT 全文](LICENSES/Transmog-MIT.txt)
- **Just Enough Items / mezz**。既存日本語の貢献者には **Abbage230** が含まれます。[MIT 全文](LICENSES/JEI-MIT.txt)

これは元作者・既存訳者による公式版ではありません。出典と変更範囲は [NOTICE](NOTICE.md) を参照してください。

## English

An unofficial Japanese resource pack for **Transmog and JEI**, targeting Minecraft 26.1.2, NeoForge 26.1.2.106, Transmog 1.8.0+26.1 and JEI 29.36.0.96. Version 0.2.0 includes 25 Transmog and 334 JEI display strings, independently reviewed in small batches. One non-display JEI metadata entry remains verbatim and is excluded from that count. This project does not translate all of ATM11 or its quests.

Download a ZIP from [Releases](https://github.com/ueda-keisuke/atm11-japanese/releases/latest), put it in your instance's `resourcepacks` folder without extracting it, enable it at the **top of the selected list, above MOD Resources**, disable older versions of this pack, and select Japanese. Disable or remove the pack to uninstall.

A narrow filter excludes lower-priority `transmog:lang/ja_jp.json` resources to bypass the upstream malformed file. JEI uses ordinary key overrides, with no filter. The MOD JARs remain untouched. Not every translated screen has been visually checked. Both upstream MIT licenses and credits are included.
