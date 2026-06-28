# Repository Guide

## はじめに

このリポジトリをご覧いただきありがとうございます。

Inference Collapse は、単にゲームを作ることを目的としたプロジェクトではありません。

**「AI の認知状態をゲーム世界の物理法則へ変換する」**

というアイデアを、実際に動くシステムとして検証するために開発しました。

そのため、このリポジトリにはコードだけでなく、多くの設計資料が含まれています。

最初は「ドキュメントが多すぎる」と感じるかもしれません。

でも安心してください。

このページでは、

**「どこから読めばいいのか」**

をできるだけ分かりやすく説明します。

---

# ソフトウェアはコードだけでは作れません

プログラムを書くことは、家を建てることによく似ています。

家を建てるとき、

* 設計図
* 配線図
* 水道の図面
* 工事の記録

などが必要になります。

ソフトウェアも同じです。

コードだけでは、

* なぜこの設計なのか
* どこを変更してよいのか
* 何を変更してはいけないのか

が分かりません。

そのため、実際の開発ではコードと同じくらい設計資料が重要になります。

---

# 設計書を書く本当の理由

例えば半年後、

> 「敵を少しだけ速くしてください」

と言われたとします。

一見すると簡単そうですが、

実際には

```text
Confidence
    ↓
Decision Layer
    ↓
Game State
    ↓
Threat Engine
    ↓
Simulation Engine
    ↓
Enemy
```

という流れ全体を理解しなければ、安全に修正できません。

設計書は、

**「どう作ったか」**

ではなく、

**「どこを変更すればよいか」**

を教えてくれる地図なのです。

---

# このリポジトリの見方

まずは README を読むことをおすすめします。

その後は次の順番で読むと、全体像を理解しやすくなります。

```text
README
    ↓
01_architecture.md
    ↓
02_design_decisions.md
    ↓
03_history.md
    ↓
04_lessons_learned.md
    ↓
05_future_improvements.md
```

これだけ読めば、

プロジェクト全体の考え方を理解できます。

---

# docs フォルダ

```text
docs/

├── 01_architecture.md
├── 02_design_decisions.md
├── 03_history.md
├── 04_lessons_learned.md
├── 05_future_improvements.md
├── adr/
└── technical_specs/
```

それぞれ役割が異なります。

---

## 01_architecture.md

### 「設計図」

家でいう設計図です。

システム全体が

* どんな部品でできているか
* それぞれ何を担当するか

を説明します。

---

## 02_design_decisions.md

### 「なぜそう作ったの？」

設計には必ず理由があります。

例えば、

* なぜ State を分けたのか
* なぜ LLM を直接ゲームへつながないのか
* なぜ Decision Layer を作ったのか

などを説明しています。

---

## 03_history.md

### 「進化の記録」

最初から今の設計だったわけではありません。

実際には、

```
動くプロトタイプ
        ↓
問題発見
        ↓
設計改善
        ↓
現在
```

という流れで進化しました。

その過程をまとめています。

---

## 04_lessons_learned.md

### 「失敗から学んだこと」

開発中に気付いたことをまとめています。

例えば、

* LLM は必ず検証が必要
* State は肥大化しやすい
* UI は分離した方がよい

などです。

未来の自分や他の開発者へのメモでもあります。

---

## 05_future_improvements.md

### 「これから作るもの」

現在のプロトタイプを、

将来的にどのようなシステムへ発展させる予定なのかを書いています。

例えば、

* FastAPI
* WebSocket
* Multi-Agent
* Telemetry
* Replay

などの拡張予定です。

---

# ADR フォルダ

```text
docs/
└── adr/
```

ADR は

**Architecture Decision Record**

の略です。

簡単にいうと、

**「設計者の日記」**

です。

開発中、

「どちらの設計にするべきだろう？」

という判断を何度も行います。

その瞬間の考え方を記録したものが ADR です。

あとから、

「なぜこの設計になったのか」

を振り返ることができます。

---

# technical_specs フォルダ

ここには、

**実装者向けの詳細仕様**

が入っています。

```text
technical_specs/

flow.md
state.md
api_spec.md
threat.md
```

---

## flow.md

データがシステム内をどのように流れるかを説明します。

```
UI
 ↓
AI
 ↓
Decision Layer
 ↓
Game State
 ↓
Threat Engine
 ↓
Simulation Engine
 ↓
Rendering
```

---

## state.md

Game State の内部構造を説明します。

例えば、

* WorldState
* CognitiveState
* SimulationState
* TelemetryState

などの役割です。

---

## api_spec.md

API の仕様です。

どのデータを受け取り、

どのデータを返すのかを定義します。

---

## threat.md

このプロジェクトで最も特徴的な部分です。

AI の認知状態を、

ゲーム世界の物理法則へどのように変換するかを説明しています。

---

# ソースコード

コードは src フォルダにあります。

```text
src/

├── ai/
├── decision_layer/
├── game_state/
├── simulation_engine/
├── ui/
└── data_models/
```

それぞれが一つの責務だけを担当しています。

---

## ai/

AI と通信する部分です。

Gemma などの LLM を呼び出します。

---

## decision_layer/

AI の出力を安全なデータへ変換します。

ゲームを AI の予測不能な出力から守る「防波堤」です。

---

## game_state/

世界の状態を保存する場所です。

ここではデータだけを管理し、

ゲームロジックは持ちません。

---

## simulation_engine/

ゲーム世界を動かす心臓部です。

Threat Engine が生成した物理パラメータだけを使って、

ゲーム世界を更新します。

---

## ui/

画面を表示する部分です。

プレイヤーからの入力もここで受け取ります。

---

# 実際の開発現場では

このリポジトリには比較的多くの設計資料があります。

しかし、実際の業務ではさらに多くの資料が作成されます。

例えば、

```text
requirements.md
functional_spec.md
non_functional.md

database.md
deployment.md
testing.md
logging.md
security.md
performance.md
error_handling.md
configuration.md
```

さらに大規模なプロジェクトでは、

* データベース設計
* OpenAPI / Swagger
* Docker
* Kubernetes
* CI/CD
* 運用手順書
* 障害対応手順
* 監視設計

なども含まれます。

銀行や官公庁のような大規模案件では、設計資料だけで数百ファイルになることも珍しくありません。

---

# 最後に

このプロジェクトで一番伝えたいことは、

**「動くものを作ること」だけではありません。**

動くプロトタイプを作り、

そこから責務を整理し、

設計を抽出し、

改善していく。

そのプロセスそのものが、このプロジェクトの価値だと考えています。

コードだけでなく、設計資料も合わせて読んでいただくことで、Inference Collapse の設計思想をより深く理解していただければ幸いです。
