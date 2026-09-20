# ATM11 日本語改善

ATM11 で使う一部 MOD の日本語を改善する、非公式リソースパックです。**0.4.0 は 11 MOD・1105 キーを1つの ZIP にまとめます。** ATM11 全体の翻訳は進行中で、クエストや下表以外の MOD は含みません。

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

件数は現行英語に対応する **キー・項目数**で、表示文、ナレーション、検索補助語、保持した metadata を含みます。画面数や目視確認済みの文字列数ではありません。JEI の metadata 1 キーと Jade の metadata 2 キーは翻訳件数には数えず、原文または既存日本語の機能設定を保持します。

対応環境は ATM11 **0.8.0-beta** / Minecraft **26.1.2** / NeoForge **26.1.2.106**。対象 MOD 本体は別途必要です。他の版は未確認です。独立レビューで受理された言語データだけを収録し、全項目のゲーム画面での目視確認はまだ行っていません。

## 導入・解除

1. [リリース](https://github.com/ueda-keisuke/atm11-japanese/releases/latest)から **`ATM11-Japanese-0.4.0.zip`** をダウンロードします。非営利条件付きの Jade・Better Advancements 素材を含みます。再配布・改変時は下記の個別条件を確認してください。
2. 使用するインスタンスの `resourcepacks` フォルダへ、解凍せずに置きます。Prism Launcher ではインスタンス内の `minecraft/resourcepacks` です。
3. Minecraft の「設定」→「リソースパック」で有効にし、選択中の一覧の**一番上、特に「MOD のリソース（MOD Resources）」より上**へ移動します。旧版の日本語改善パックを無効にします。0.3.0 を使っていた場合は、基本パックと Jade 専用パックの両方を無効にします。
4. 言語を「日本語」にして読み込みを完了します。

構文エラーのある **低優先の `transmog:lang/ja_jp.json` だけ**を遮断して同梱の日本語を読み込みます。同じファイルを使う低優先パックの差分も遮断されます。他の10 namespace は通常のキー上書きで、filter は使いません。英語原文にない既存日本語キーは、基底リソースから残る場合があります。元 MOD の JAR は変更しません。

日本語が反映されないときはパックの並び順を確認してください。解除は設定で無効化し、不要になった ZIP を `resourcepacks` から削除します。

## ライセンスとクレジット

この ZIP は `assets/<namespace>/lang/ja_jp.json` ごとに独立した言語資産を集めたものです。**パック全体を MIT として配布しているわけではありません。** 個別ファイルを取り出して使う場合も、そのファイルに適用される条件を保持してください。同梱したことを理由に、MIT・Unlicense・LGPL の素材へ別素材の非営利制限を追加しません。

- **Jade とその日本語改変**: CC BY-NC-SA 4.0。非営利目的、帰属・改変表示、同じライセンスでの共有が必要です。
- **AE2 Network Analyzer / Cumulus Menus とその日本語改変**: LGPL 3.0。GPL・LGPL 全文、変更日、元ソース、編集できる JSON を同梱します。
- **Sodium とその日本語改変**: PolyForm Shield 1.0.0。競合用途を除く許容目的など、全文の条件が適用されます。本パックは原版 Sodium を必要とする日本語補助資産です。
- **Better Advancements とその日本語改変**: 原作の Don't Be a Jerk ライセンス。非営利条件などを保持します。
- **MIT / AppleSkin**: 原作の MIT・Unlicense と作者表示を保持します。本プロジェクトの追加分の適用範囲は [NOTICE.md](NOTICE.md) に記載しています。

元作者・既存訳者による公式版ではありません。作者、既存訳者、出典、変更内容、ライセンスの適用範囲は [NOTICE.md](NOTICE.md)、全文は [LICENSES/](LICENSES/) にあります。

## ソースから ZIP を作る

Python 3.10 以降の標準ライブラリだけで実行できます。

```sh
python3 build_pack.py --check
python3 build_pack.py
```

`release.json` が `pending` の間はビルドを拒否します。訳文・独立レビュー要約・元 JAR と内包 chain の識別情報・完全なキー集合・ライセンスの hash、件数、pack format 84.0 と限定 filter を検証し、`dist/ATM11-Japanese-0.4.0.zip` を生成します。レビュー要約は `reviews/` にあります。元 MOD の JAR や外部ライブラリは再ビルドに不要です。

ファイル順と日時を固定し、同じ入力と圧縮環境なら同じ ZIP を再生成できます。異なる bytes の既存 ZIP は上書きしません。以前の公開 ZIP・タグは変更しません。

## English

Unofficial Japanese improvements for **11 ATM11 MODs / 1105 keys**, collected into **one ZIP**. Counts include narration, search terms and preserved metadata, not visually tested screens. ATM11 quests and other MODs are outside this release. Target: Minecraft 26.1.2 / NeoForge 26.1.2.106, with the exact MOD versions above.

Download `ATM11-Japanese-0.4.0.zip` from [Releases](https://github.com/ueda-keisuke/atm11-japanese/releases/latest), place it in `resourcepacks` without extracting, enable it **at the top, above MOD Resources**, disable previous editions (including both 0.3.0 packs), and select Japanese. Disable/remove the pack to uninstall. Only the malformed lower-priority Transmog Japanese file is filtered; no MOD JAR is changed.

Each namespace remains a separate work under its own license. **There is no blanket MIT grant.** The collection contains noncommercial Jade and Better Advancements material; Jade also requires attribution and ShareAlike. LGPL assets include readable modified JSON and both GNU license texts. Sodium retains PolyForm Shield conditions. These conditions do not relicense unrelated namespace files. See `NOTICE.md` and `LICENSES/` for the individual scopes, credits and full terms. Only accepted review inputs pass the builder; not every game screen has been visually checked.
