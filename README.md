# ATM11 日本語改善: Transmog

ATM11 で使用する **Transmog の日本語 25 項目**を改善する、非公式リソースパックです。設定名、説明、ツールチップなどを対象とします。ATM11 全体の日本語化は進行中で、この版にクエストや他 MOD の翻訳は含まれません。

対応環境：Minecraft **26.1.2** / NeoForge **26.1.2.106** / Transmog **1.8.0+26.1**。MOD 本体は含まれていないため、対応する環境に別途導入してください。他のバージョンは未確認です。

## 導入

1. [最新版のリリース](https://github.com/ueda-keisuke/atm11-japanese/releases/latest)から `ATM11-Japanese-Transmog-<version>.zip` をダウンロードします。
2. 使用する Minecraft インスタンスの `resourcepacks` フォルダへ、ZIP を解凍せずに置きます。Prism Launcher では対象インスタンスのフォルダ内にある `minecraft/resourcepacks` です。
3. Minecraft の「設定」→「リソースパック」で有効にし、選択中の一覧で**一番上へ移動**します。特に「MOD のリソース（MOD Resources）」より上に置いてください。
4. 言語を「日本語」にして読み込みを完了します。

Transmog 1.8.0 の元の日本語 JSON に構文エラーがあるため、このパックは**低優先の `transmog:lang/ja_jp.json` だけ**を読み飛ばして、同梱の日本語を読み込ませます。同じファイルを使う低優先パックの日本語差分も対象になります。元の MOD JAR は変更しません。

MOD 本体より下に置くと、この回避処理が働きません。日本語が反映されない場合は、まず上記の並び順を確認してください。全項目のゲーム画面での目視確認はまだ行っていません。

解除するには、リソースパック設定で無効にします。不要になった ZIP は `resourcepacks` から削除できます。

## ソースから ZIP を作る

このリポジトリのソースを取得し、ルートディレクトリで実行します。Python 3.10 以降の標準ライブラリだけを使用します。

```sh
python3 build_pack.py
```

承認済み日本語ファイル、25 キー、リリース情報の SHA-256、限定された filter、ライセンスを検証し、`dist/ATM11-Japanese-Transmog-<version>.zip` を生成します。未レビューの開発途中ではビルドを拒否します。ファイル順・タイムスタンプを固定しているため、同じ入力と圧縮環境で再生成できます。

## ライセンスとクレジット

翻訳パックと作成用スクリプトは MIT ライセンスで配布します。

Transmog: **Hidoni**。元 MOD が記載する既存日本語訳の貢献者: **elinka47**。このパックは英語原文から日本語を見直した非公式の改善版で、元作者・既存訳者による公式版ではありません。[MIT ライセンス全文](LICENSES/Transmog-MIT.txt)と [NOTICE](NOTICE.md) を同梱しています。

## English

An unofficial Japanese resource pack covering **25 Transmog strings**, for Minecraft 26.1.2, NeoForge 26.1.2.106 and Transmog 1.8.0+26.1. This release does not translate the entire ATM11 pack or its quests.

Download the ZIP from [Releases](https://github.com/ueda-keisuke/atm11-japanese/releases/latest), put it in your instance's `resourcepacks` folder without extracting it, enable it, move it to the **top of the selected list, above MOD Resources**, and select Japanese. Disable or remove the pack to uninstall. A narrow filter excludes lower-priority `transmog:lang/ja_jp.json` resources to bypass the upstream malformed file; the MOD JAR is untouched. The filter cannot fix a higher-priority MOD resource. Not every translated screen has been visually checked yet.
