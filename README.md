# ATM11 日本語改善

ATM11 で使う一部 MOD の日本語を改善する、非公式リソースパックです。**基本パックと Jade 専用パックを別々に配布**します。必要な方だけ、または両方を導入できます。ATM11 全体の翻訳は進行中で、クエストや下表以外の MOD は含みません。

## 0.3.0 の収録内容

| ZIP | 対象 | キー数 | 主なライセンス |
| --- | --- | ---: | --- |
| `ATM11-Japanese-0.3.0.zip` | Transmog 25 / JEI 335 / AppleSkin 22 / Controlling 12 | 394 | MIT、AppleSkin 原作は Unlicense |
| `ATM11-Japanese-Jade-0.3.0.zip` | Jade | 496 | **CC BY-NC-SA 4.0** |

件数は現行英語に対応する **キー・項目数**で、表示文、ナレーション、検索補助語、保持した metadata を含みます。画面数や目視確認済みの文字列数ではありません。JEI の metadata 1 キーと Jade の metadata 2 キーは翻訳件数には数えず、元の値を保持します。Jade の言語機能設定は既存の日本語設定を保持します。

各言語は小さな単位で独立レビューしたデータだけを配布します。開発途中で manifest が `pending` の場合、ビルドは拒否されます。全項目のゲーム画面での目視確認はまだ行っていません。

対応環境は ATM11 **0.8.0-beta** / Minecraft **26.1.2** / NeoForge **26.1.2.106**。対象 MOD は Transmog **1.8.0+26.1**、JEI **29.36.0.96**、AppleSkin **3.0.9**（MC 26.1 用）、Controlling **26.1.2.4**、Jade **26.1.10** です。MOD 本体は別途必要です。他の版は未確認です。

## 導入・解除

1. [リリース](https://github.com/ueda-keisuke/atm11-japanese/releases/latest)から必要な ZIP をダウンロードします。Jade 版は非営利・帰属表示・同条件継承のライセンスです。
2. 使用するインスタンスの `resourcepacks` フォルダへ、解凍せずに置きます。Prism Launcher ではインスタンス内の `minecraft/resourcepacks` です。
3. Minecraft の「設定」→「リソースパック」で有効にし、選択中の一覧の**一番上、特に「MOD のリソース（MOD Resources）」より上**へ移動します。両方使う場合は両方を MOD Resources より上に置きます。2 つの相互の順序は問いません。旧版の同じ日本語改善パックは無効にします。
4. 言語を「日本語」にして読み込みを完了します。

基本パックは、構文エラーのある **低優先の `transmog:lang/ja_jp.json` だけ**を遮断して同梱の日本語を読み込みます。同じファイルを使う低優先パックの差分も遮断されます。JEI・AppleSkin・Controlling と Jade 専用パックは通常のキー上書きで、filter は使いません。英語原文にない既存日本語キーは、基底リソースから残る場合があります。元 MOD の JAR は変更しません。

日本語が反映されないときはパックの並び順を確認してください。解除は設定で無効化し、不要になった ZIP を `resourcepacks` から削除します。

## ソースから ZIP を作る

リポジトリのルートで実行します。Python 3.10 以降の標準ライブラリだけを使います。

```sh
python3 build_pack.py --check
python3 build_pack.py
```

既定では両方を検証・生成します。片方だけなら `--pack base` または `--pack jade` を付けます。訳文・独立レビュー要約・原文の識別情報・完全なキー集合・ライセンスの hash、件数、pack format 84.0 と限定 filter を検証します。選択した入力をすべて検証してから `dist/` に ZIP を生成し、既存版の異なる bytes は上書きしません。同じ入力と圧縮環境ではファイル順と日時が固定された ZIP を再生成できます。

基本パックの記録は `release.json`、Jade は `release-jade.json`、レビューの要約は `reviews/` にあります。各 ZIP 内では対応する記録を `release.json`、出典・変更表示を `NOTICE.md` として同梱します。0.1.0 / 0.2.0 の公開 ZIP とタグは変更しません。

## ライセンスとクレジット

**Jade とその日本語改変は CC BY-NC-SA 4.0 であり、MIT の対象ではありません。** 非営利目的、作者への帰属表示、改変の表示、同じライセンスでの共有が必要です。Jade ZIP の `LICENSES/` に全文を同梱します。

基本パックへの本プロジェクトの追加分とビルドスクリプトは MIT（`LICENSES/Project-MIT.txt`）。元資産のライセンス・クレジットも保持します。

- **Transmog / Hidoni** — MIT。既存日本語の貢献者 **elinka47**。
- **Just Enough Items / mezz** — MIT。既存日本語の貢献者に **Abbage230**。
- **AppleSkin / squeek502** — 原作の **Unlicense** 全文を保持。
- **Controlling / Jaredlll08** — MIT。
- **Jade / Snownee** — **CC BY-NC-SA 4.0**。原作の credits: **TehNut, ProfMobius, kalkafox**。既存日本語: **momo-i, RascalNiki**。

元作者・既存訳者による公式版ではありません。各 ZIP の `NOTICE.md` と `LICENSES/` に出典・改変内容・全文を同梱します。リポジトリでは基本パックが `NOTICE.md`、Jade が `NOTICE-Jade.md` です。

## English

Unofficial Japanese improvements for selected ATM11 MODs. Version 0.3.0 provides two independent ZIPs: **base** (Transmog 25, JEI 335, AppleSkin 22, Controlling 12 keys) and **Jade** (496 keys). Counts include display text, narration, search keywords and preserved metadata; they are not counts of visually tested screens. ATM11 quests and other MODs are outside this release.

Target: Minecraft 26.1.2 / NeoForge 26.1.2.106, with the exact MOD versions above. Download either or both ZIPs from [Releases](https://github.com/ueda-keisuke/atm11-japanese/releases/latest), put them in `resourcepacks` without extracting, enable them **at the top, above MOD Resources**, disable older editions, and select Japanese. Disable/remove the pack to uninstall.

Only the base pack filters the malformed lower-priority `transmog:lang/ja_jp.json`. Other namespaces use normal key overlays. No MOD JAR is modified. All distributed language data must pass independent review; not every game screen has been visually checked.

The base project additions and build script use MIT; the original AppleSkin Unlicense and other original MIT notices remain included. **Jade and its adapted Japanese language asset use CC BY-NC-SA 4.0, not MIT**: noncommercial use, attribution, modification notice and ShareAlike apply. Each ZIP contains the relevant full license text and credits.
