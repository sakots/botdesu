# ボットデスくん

![私がボットデス](https://github.com/sakots/botdesu/blob/main/ico.png?raw=true)

ポケモンマストドン「[ポケマス](https://pokemon.mastportal.info/)」のさらに一部界隈で有名な、pythonで動くマストドンのマルコフ連鎖botです。  
あとなんか画像を検索したりする。

## 概要

おれはしゅうまい君が作りたかったんだよ…

## 新機能「画像検索して貼る」

ボットデスくんにメンション飛ばして「○○の画像くれ」とか「△△ちょうだい」とか言ってみよう。

## 名言

- 「フナムシゆめおとこ」
- 「おは​​花粉症っぷ？」
- 「キャンドゥーのドレッシング？キャンドゥーのは無理あるじゃろう？おれとしては」
- 「タオルとマステ買ったのにいつも足りない」
- 「今日はエンニュートだ！！！！！！」
- 「大船渡線だよあ」
- 「アブソルアイコンの動画見てるだけか？」
- 「それちんこですよ」

など

## ここがすごいぞボットデス

エラーで止まっても自分でそれを把握して勝手に再起動する

- ホストドン側でエラーが出ることが多いので導入しました

## 使い方（下準備）

- python3
  - まあpythonで動きますし。3.8.5で動いてるけどたぶん3.9.1でも動く。
- MeCab
  - インストール必須。[mecab-ipadic-NEologd](https://qiita.com/ekzemplaro/items/c98c7f6698f130b55d53)あたりの辞書を用意すると良いです。
- botをユーザー登録するためのマストドンアカウント
  - そりゃ必要ですわな。その後アカウント→開発から mastodon-api の `client_id` `access_token` `client_secret` あたりがないと動かないですよ。
- configファイルの設定
  - マストドンでbotを動かすための設定を書くファイルです。プログラム内に直接書くのは気がひけるので分けました。
  - config_sample.pyからconfig.pyにコピー＆リネームして使ってください。
  - .envはめんどいのでやめました。

## 使い方（Python編）

- 以下をpythonで使えるようにpip3とか使ってなんとかする。
  - mecab-python3
  - Mastodon.py
  - requests
  - requests_oauthlib
  - beautifulsoup4
  - apscheduler

まあこんな感じ（コピペ用）

```shell:terminal
  pip3 install mecab-python3 Mastodon.py requests requests_oauthlib beautifulsoup4 apscheduler
```

- 他なにか足りなければ動かしたときに「おいこれがねえぞ」ってエラーが出るのでそれ見て適宜導入してください。

## さあ動かすぞ

基本的にubuntuのpython3.8で動かしてますのでそれ以外の環境はわかりませんが

```shell:terminal
  bash run
```

以上。このrunの中でずっとbotdesu.pyを監視しているので落ちてたら起動するのですな～

## 気になる点

- やっぱなんかソースきれいではない
- きりぼっとが超参考になった

## 更新履歴

### [2020/12/17] v0.13.17

- イライラ度が上がらなさすぎるので調整

### [2020/12/17] v0.13.16

- イライラ度が100%を超えても黙ってるので修正

### [2020/12/17] v0.13.15

- 画像検索でエラーが出たときも返事をしてくれるように改良
- 発言間隔調整

### [2020/12/17] v0.13.14

- 発言間隔調整

### [2020/12/17] v0.13.13

- 拾ってきた画像全部貼り付けようとして怒られていたので修正

### [2020/12/17] v0.13.12

- 画像トゥートできないのが直った気がする

### [2020/12/17] v0.13.11

- そうかglobal変数は外部から変更できないのか

### [2020/12/17] v0.13.10

- いやわからんわ

### [2020/12/17] v0.13.9

- わかったぞ！わかったぞ！わかっ…

### [2020/12/17] v0.13.8

- イライラ定義をconfigから戻した

### [2020/12/17] v0.13.7

- 変数の読み込み方を知らなかった。

### [2020/12/17] v0.13.6

- なんか怒られるので修正

### [2020/12/17] v0.13.5

- イライラ定義をconfigに移した

### [2020/12/16] v0.13.4

- なんか画像がダウンロードできないのを修正したい

### [2020/12/16] v0.13.3

- 発言拾いすぎなのでタイミング調整
- yahooが怒るのでヘッダを偽装

### [2020/12/16] v0.13.2

- なんでVSCodeくんエラー出してくれんのやろ。

### [2020/12/16] v0.13.1

- 未定義の変数使ってたので修正。なんでVSCodeくんエラー出してくれんのやろ。

### [2020/12/16] v0.13.0

- 画像のクロールの方法を変えた。
- googleからyahooに変えた。
- イライラ度管理を見つめ直した。

### [2020/12/15] v0.12.6

- ちょっとわかる

### [2020/12/15] v0.12.5

- いや、わからん

### [2020/12/15] v0.12.4

- 誤字っていた

### [2020/12/15] v0.12.3

- 変数超わかんない。

### [2020/12/15] v0.12.2

- なんか動かない気がしてきたけど頑張る

### [2020/12/15] v0.12.1

シェルスクリプトをミスっていた

### [2020/12/15] v0.12.0

- けっこうすごく作り直した。

### [2020/12/15] v0.11.12

- 止まるって言うか動いてない気がしたので_resをバックグラウンドで実行するようにしてみた。
- 起動中のメッセージの変更

### [2020/12/15] v0.11.11

- なんか止まるのでファイルを分けた

### [2020/12/15] v0.11.10

- ディレクトリ名が間違っていた

### [2020/12/15] v0.11.9

- ファイルを消すタイミングを間違えていたの修正

### [2020/12/15] v0.11.8

- 参考にしていた正規表現のサイトが間違っていた。なんてこった。

### [2020/12/15] v0.11.7

- バグなおれよ！！！

### [2020/12/15] v0.11.6

- 私はアホでした

### [2020/12/15] v0.11.5

- おれは正規表現がわかっていなかった。

### [2020/12/14] v0.11.4

- 二次元配列がわかった気がする。

### [2020/12/14] v0.11.3

- がんばった。
- あと改行コードを変えた

### [2020/12/14] v0.11.2

- 検索もバグってた

### [2020/12/14] v0.11.1

- 配列がバグってた

### [2020/12/14] v0.11.0

- 画像検索機能をつけてみた。

### [2020/12/14] v0.9.26

- ファイルは作成されてたんや…　空っぽの時の例外処理がなかったんや…
- なので分離して追加

### [2020/12/14] v0.9.25

- やっぱりファイルが作成されないので手法を変えた

### [2020/12/14] v0.9.24

- なんでか動かないと思ってたら変数がかぶってたので修正

### [2020/12/14] v0.9.23

- 初回起動時にtoot.txtがないとエラーが出るので修正
- トゥートできなかったときにイライラ度が減ることもあるように修正
- readme整理

### [2020/12/13] v0.9.22

- なんか計算をミスってたので修正

### [2020/12/13] v0.9.21

- ボットデスくんのイライラ度をコンソール見たらわかるようにした
- コード整理

### [2020/12/12] v0.9.20

- bashわからんすぎるのでpythonをがんばるほうにもどした

### [2020/12/12] v0.10.2

- bashまじでわからん

### [2020/12/12] v0.10.1

- bashわからん

### [2020/12/12] v0.10.0

- 思ったように動かないのでファイルを分割してみた

### [2020/12/12] v0.9.18

- 変数が未定義で怒られて止まるので修正
- コンソールにデバック用のいろいろが見えるようにした

### [2020/12/12] v0.9.17

- やっぱり喋らないのでよく見たら変数が変数しすぎてた

### [2020/12/12] v0.9.16

- おいこいつちっとも喋らねえぞの修正

### [2020/12/12] v0.9.15

- scheduleなんていらんかったんや！

### [2020/12/12] v0.9.14

- 発言頻度が高すぎてびびったので修正

### [2020/12/12] v0.9.13

- 不機嫌にした

### [2020/12/07] v0.9.12

- 再起動時に発言するようにした

### [2020/12/07] v0.9.11

- ソースの不要な部分を削除

### [2020/12/07] v0.9.10

- タイミングをミスっていたので修正

### [2020/12/07] v0.9.9

- テキスト全消しのタイミング調整

---

特に指定がない限り、ボットデスくんのすべてのコンテンツは[クリエイティブ・コモンズ 表示 - 継承3.0ライセンス](https://creativecommons.org/licenses/by-sa/3.0/deed.ja) の元で利用可能だと思います。
