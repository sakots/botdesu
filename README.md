# ボットデスくん

![私がボットデス](https://github.com/sakots/botdesu/blob/main/ico.png?raw=true)

ポケモンマストドン「[ポケマス](https://pokemon.mastportal.info/)」のさらに一部界隈で有名な、pythonで動くマストドンのマルコフ連鎖botです。

## 概要

おれはしゅうまい君が作りたかったんだよ…

## 名言

- 「ゆめおとこ」
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

- MeCab
  - インストール必須。mecab-ipadic-NEologdあたりの辞書を用意すると良いです。
- botをユーザー登録するためのマストドンアカウント
  - そりゃ必要ですわな。その後アカウント→開発から mastodon-api の `client_id` `access_token` `client_secret` あたりがないと動かないですよ。
- .envファイルの設定
  - マストドンでbotを動かすための設定を書いてあるファイルです。プログラム内に直接書くのは気がひけるので分けました。

## 使い方（Python編）

- 以下をpythonで使えるようにpipとか使ってなんとかする。
  - MeCab
  - Mastodon
  - load_dotenv
- 他なにか足りなければ動かしたときに「おいこれがねえぞ」ってエラーが出るのでそれ見て適宜導入してください。

## さあ動かすぞ

基本的にubuntuのpython3.8で動かしてますのでそれ以外の環境はわかりませんが

```shell:terminal
  bash run
```

以上。このrunの中でずっとbotdesu.pyを監視しているので落ちてたら起動するのですな～

## 気になる点

- やっぱなんかソースきれいではない

## 更新履歴

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
