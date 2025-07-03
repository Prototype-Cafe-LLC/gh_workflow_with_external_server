# gh_workflow_with_external_server
GitHub workflowから外部のサーバにjobを出し、結果を取得するテストプロジェクト

リポジトリのコード
- app
  - 10秒に一回 外部サーバに statusの問い合わせを polling する スクリプト watch.py
  - watch.py は、一度 in-progressを受け取った後、pass または fail を受け取るまで watchを続ける
  - pass または failを受け取ったら終了する。

- 外部サーバの代わりに ここでは action内に http://localhost:3000/ で listenするサーバをセットアップする
   - GET /status で {"status": "<status>"} を返す。　 status は "none"（初期値), "in-progress", "pass", "fail" のいずれか
　 - POST /start (data = {})  で 1分間のjobをスタートする。この時　statusを in-progressに変える
   - job スタート後、 2分したら sttus を pass に変える。以降 再度 /start されるまで statusは変わらない
   - python http.server ベースのサーバとする

 - インストーラは uv
 - python 3.12

- .github/ci.yml
  - PRブランチへのpushが行われたら watch.pyを起動する

トリガー: main branch へのPRブランチ への push
挙動: pushが行われたら、rip
