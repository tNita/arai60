# 929. Unique Email Addresses

Every valid email consists of a local name and a domain name, separated by the '@' sign. Besides lowercase letters, the email may contain one or more '.' or '+'.

For example, in "alice@leetcode.com", "alice" is the local name, and "leetcode.com" is the domain name.
If you add periods '.' between some characters in the local name part of an email address, mail sent there will be forwarded to the same address without dots in the local name. Note that this rule does not apply to domain names.

For example, "alice.z@leetcode.com" and "alicez@leetcode.com" forward to the same email address.
If you add a plus '+' in the local name, everything after the first plus sign will be ignored. This allows certain emails to be filtered. Note that this rule does not apply to domain names.

For example, "m.y+name@email.com" will be forwarded to "my@email.com".
It is possible to use both of these rules at the same time.

Given an array of strings emails where we send one email to each emails[i], return the number of different addresses that actually receive mails.



Example 1:

Input: emails = ["test.email+alex@leetcode.com","test.e.mail+bob.cathy@leetcode.com","testemail+david@lee.tcode.com"]
Output: 2
Explanation: "testemail@leetcode.com" and "testemail@lee.tcode.com" actually receive mails.
Example 2:

Input: emails = ["a@leetcode.com","b@leetcode.com","c@leetcode.com"]
Output: 3


Constraints:

1 <= emails.length <= 100
1 <= emails[i].length <= 100
emails[i] consist of lowercase English letters, '+', '.' and '@'.
Each emails[i] contains exactly one '@' character.
All local and domain names are non-empty.
Local names do not start with a '+' character.
Domain names end with the ".com" suffix.
Domain names must contain at least one character before ".com" suffix.

## Step1

- ケース
  - メーリングリストに対して送信するケースが背景か？
- 思いついた解法
  - 選択肢1: setを利用
    - 詳細
      - @より前で.を除外、+以降を除外したものを作る
      - これがsetにあれば無視、setになければ追加
      - setにある数をcount
      - pros
        - シンプルに実装可能
      - cons
        - 元のメアド（.や+付き）がわからない
  - 選択肢2: dictを使う（key：domain name、value: local name）
    - 詳細
      - local name, domain nameで分け、domain nameをキー、local nameの集合（set）をキーに
    - pros
      - domainごとに別の処理をしたいなどの要望が出てくる時に、簡単に対応可能
    - cons
      - 元のメアド（.や+付き）がわからない
      - 今回の要件だけ考えると、結局setを持っているので冗長
  - 選択肢3: dictを使う（key: 加工後のメアド、value: 元のメアドのリスト）
    - 選択肢1や2の弱点を補う
      - 加工（.を除外、+以降を除外）後のメアドがキーにあれば、対象のvalueのリストに追加、なければ加工後のメアドをキーに、加工前のメアドが入った要素数1のリストをバリューにdictに追加
    - pros
      - 元のメアド（.や+付き）がわかる（送り先と実際に表示するメアドは変えたいとかの要望があれば簡単に対応できる）
    - cons
      - 今回の要件だけを満たすためだけにしては冗長
- シンプルに実装するため選択肢1で対応
- メアドの加工はforで一文字ずつチェックするか、reを使って行う
  - シンプルさを考え、正規表現を利用する
    - https://docs.python.org/3/library/re.html
    - 正規表現の実装方法を問われそうだが、答えられないので調べる
    - https://swtch.com/~rsc/regexp/regexp1.html
    - まとめ（by GPT）
      - バックトラッキング（Perl系） 
        - マッチ候補の経路を1つずつ試し、失敗したら戻って再探索する（DFS的） 
        - メリット 
          - 実装がシンプル 
          - 後方参照などの強力な機能を扱える 
        - デメリット 
          - 最悪で指数時間（catastrophic backtracking） 
          - ReDoSの原因になる 
      - Thompson NFA 
        - 正規表現をNFAに変換し、現在あり得る状態を集合として同時に追跡 
        - メリット
          - 入力長に対して線形時間 O(n) で動く （Russ Cox） 
          - ReDoS耐性
        - デメリット 
          - 状態集合を持つためメモリ使用量が増える 
          - 後方参照などは扱えない 
      - DFA
        - 正規表現→NFA→DFAに変換し実行
        - メリット
          - 分岐なしで1パスで処理できるため、高速 
          - ReDoS耐性
        - デメリット 
          - DFA構築コストのオーバーヘッド
          - 後方参照などは扱えない
    - PythonのreはPerlと同様（バックトラッキング）なので、最悪計算量が指数関数時間かかることがあるため注意
      - ReDos攻撃というものもあるくらい
      - https://yamory.io/blog/about-redos-attack

- いざ正規表現で実装しようと思ったらできない
- 正規表現でエレガントに1行で書けるのかもしれないが、愚直に文字列の加工をする
  - localnameとdomainに分ける
  - localnameを加工（+以降を除く→.を削除）
  - localnameとdomainをくっつけて、setに追加

```Python3
class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            email_splitted = email.split('@')
            localname, domain = email_splitted[0], email_splitted[1]
            localname_plus_removed = localname.split('+')[0]
            original_localname = re.sub(r'\.', '', localname_plus_removed)
            original_email = original_localname + '@' + domain
            if original_email not in unique_emails:
                unique_emails.add(original_email)
        return len(unique_emails)
```

## Step2
### Step1の修正

- 正規表現で書かせてみる（by GPT）
  - leetcode上での実行時間は正規表現の方が5msec程度遅い
  - ちゃんとバリデーションできていないかも

```Python3
import re

class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            normalized = re.sub(r'\.(?=.*@)|\+.*(?=@)', '', email)
            unique_emails.add(normalized)
        return len(unique_emails)
```

### 他の人のコード

- https://github.com/hayashi-ay/leetcode/pull/25
  - 問題文のメアド形式の制約に依存するのではなく、正しい形式のメアドかどうかをちゃんとバリデーションする
    - localnameの`@`は許容
      - local, domain = email.rsplit('@', 1)
      - https://docs.python.org/3/library/stdtypes.html#str.rsplit
      - 第二引数はmaxSplit
- https://github.com/naoto-iwase/leetcode/pull/14
  - https://github.com/naoto-iwase/leetcode/pull/14/changes#diff-3282ee8d1849a45b92b2a4a6e00440ecc86e0ae920337bcef2ea279c2d29b848R76-R94
    - 結局すべてのデータがメモリにロードされるため、遅延評価する必要なく、generatorじゃなくても良さそう
- https://github.com/fuga-98/arai60/pull/15
  - https://github.com/fuga-98/arai60/pull/15/changes#diff-bb50cf953134a4bd3d1f14fd71c15dc42efb1ce2625372e58d6e3b07c0a6fa43R94
  - > →メールアドレスをグループ分けするものだと仮定すると、変なものが混じってても例外を発生させないほうがよさそう。
  - 同意。実際のシステムだと、不適切なものはグループ分けせず無視→無視したものはユーザにわかるように表示すれば良さそう
- https://github.com/tom4649/Coding/pull/21
  - `pattern = re.compile(r"^([a-z0-9.]+)(?:\+[^@]*)?@([a-z0-9.+]+)$")` を読めるようになる
    - `(?: ... )`: 非キャプチャグループ
      - https://docs.python.org/3/library/re.html#:~:text=of%20the%20expression.-,(%3F%3A...),-A%20non%2Dcapturing
    - 一つのメアドに対して左から一文字ずつ解析する場合、どの部分（ローカル、ローカル無視部分、ドメイン）なのかを状態管理する形の実装
- https://github.com/dorxyxki/arai60/pull/14
  - https://github.com/dorxyxki/arai60/pull/14/changes#diff-fc134afe160e17a5286dfa401a60336f71768f3766b27874ad4da654d7e899d8R27-R38
    - 1つのメアドに対して左から一文字ずつ解析する場合、ローカル部分、ドメイン部分で処理を分けて実装（状態管理は不要）
- https://github.com/kitano-kazuki/leetcode/pull/14
  - 丁寧にバリデーション（バリデーションの観点では模範解答か）
  - メアドのバリデーション自前でできますか？というのが今回の題意であるのでライブラリは利用しない方が良さそうだが、実務では特殊な要件ない限り、ライブラリ利用するのが良さそう
  - https://pypi.org/project/email-validator
- https://github.com/X-XsleepZzz/leetcode/pull/15
  - https://github.com/X-XsleepZzz/leetcode/pull/15/changes#r2887203877
  - > 個人的には、正規表現よりも split("+"), replace(".", "") の方が読みやすかったです。
  - 明確なデメリットはどちらの選択肢にもなさそうなので好みの範囲か（でも確かにreplace使った方が素直な感じはする）

### コメント集
https://discord.com/channels/1084280443945353267/1200089668901937312/1209166861821026356
> Domain 名とメールアドレスについての RFC は見たことがありますか?

RFC 1034
https://www.ietf.org/rfc/rfc1034.txt#:~:text=The%20labels%20must%20follow%20the%20rules%20for%20ARPANET%20host%20names.%20%20They%20must%0Astart%20with%20a%20letter%2C%20end%20with%20a%20letter%20or%20digit%2C%20and%20have%20as%20interior%0Acharacters%20only%20letters%2C%20digits%2C%20and%20hyphen.%20%20There%20are%20also%20some%0Arestrictions%20on%20the%20length.%20%20Labels%20must%20be%2063%20characters%20or%20less.
- ドメインの仕様
  - 厳密なルール（構文規則）が定義されている

RFC5322
https://datatracker.ietf.org/doc/html/rfc5322#section-3.4.1
- メアドの仕様

- https://github.com/seal-azarashi/leetcode/pull/14#discussion_r1676988400
  - > あと、ユースケース考えて書いてますか。ユーザーがゴミを1つ突っ込んできたら例外投げて動かないコードでいいんですか。結論がいいならそれはひとつなんですが、私は考慮された形跡がないことを怖がってます。
  - 自分も↑を考慮できていなかったので反省
- https://github.com/SuperHotDogCat/coding-interview/pull/30#discussion_r1646552062
  - > あと、本当はセキュリティー上、メールアドレスはユーザーから渡されるものである可能性が高く、ゴミを渡されたときに落ちるプログラムにしてはいけないですね。
- https://github.com/SuperHotDogCat/coding-interview/pull/30/changes#r1676991757
  - > split("+") が2番目でもいいかも知れませんね。
  - +以降の除外を先にした方が文字数が減る傾向があるからか
- https://github.com/Yoshiki-Iwasa/Arai60/pull/13#discussion_r1649832719
  - > これ、マーケティングのメールを送りたいのか、ある集団のやりとりを整理したいのか。
    つまり、たとえば、誤った入力が一つ入ったときに、全体として、そこそこ動いて欲しいのか、異常だといって止まって欲しいのか。それは何をしたいのかとの兼ね合いになるでしょう。
  - 異常時もユースケースを想定
- https://github.com/plushn/SWE-Arai60/pull/14/changes#r2051710985
  - 文字列の結合は文字列の再構築が走るので一般的には遅い
  - > メールアドレスの長さは最大どれくらいなのか。そのうえで2乗であることは問題なのか。
  - ただ、一般論だけではなく、ユースケースを想定した上でメリデメを考える
- https://github.com/syoshida20/leetcode/pull/20#discussion_r2079714768
  - 落ちて欲しいケース
  - > データサイエンス目的の研究で、バッチで統計処理をしているならば、むしろ落ちて欲しいんですよね
  - データの品質が大事なため

## Step3

- メーリングリストに対して送信するケースを想定（マーケティングが目的）
  - 不適切なメアドがあったとしてもスキップするだけ、適切なメアドには送信してあげた方が良い
```Python3
class Solution:
    LIMITED_TLD = '.com'
    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()
        for email in emails:
            local, domain = email.rsplit('@', 1)
            local = local.split('+', 1)[0]
            local = local.replace('.', '')
            if not self.validation(local, domain):
                continue
            unique_emails.add((local, domain))
        return len(unique_emails)

    def validation(self, local: str, domain: str) -> bool:
        if len(local) == 0:
            return False
        return len(domain) > len(self.LIMITED_TLD) and domain.endswith(self.LIMITED_TLD)
```