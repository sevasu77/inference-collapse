# 🏛️ システム基本設計（Architecture）

本システムは**「AIが物理法則（ゲーム難易度や世界線）を書き換えるゲームエンジン」**を具現化するための実験的アーキテクチャである。

## 🗺️ 全体構造図（依存関係の理想）

現状の「全員が直接世界に触っている状態」から、APIレイヤーを中核に据えた境界の明確な分離を目指す。

```text
        ┌──────────────┐
        │   LLM        │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   API Layer   │
        │ /inference    │
        │ /simulate     │
        │ /state        │
        └──────┬───────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  STATE   │ │   GAME   │ │    UI    │
└──────────┘ └──────────┘ └──────────┘

### 🧠 ① LLM層（頭脳）

* **役割：** 「推理・判断を作るAI」 ➔ **👉「探偵AI」**
* **該当コード：** `ask_gemma_reasoning()`
* **データ構造：**
  * **入力 (Input):**
    * `sector` (BIO / MEC / CYB)
    * `evidence` (証拠)
  * **出力 (Output):**
    * `report` (推理)
    * `confidence` (確信度)
    * `severity` (危険度)
    * `contradiction` (矛盾)

---

### 💾 ② State Manager（記録係）

* **役割：** 「世界の状態を覚える」 ➔ **👉「ゲームのセーブデータ」**
* **該当コード：** `auditStates`, `node_truths`, `gemma_reasonings`
* **データ構造：**
  ```python
  state = {
      "BIO": {"cleared": bool, "fakeMarked": bool},
      "MEC": {"cleared": bool, "fakeMarked": bool},
      "CYB": {"cleared": bool, "fakeMarked": bool}
  }

### 🎮 ③ Game Engine（物理世界）
* **役割：** 「動き・敵・視界・時間」 ➔ **👉「ゲームの物理エンジン」**
* **該当コード：** `update()`, `draw()`, `collectors` (敵AI), `bats` (環境ノイズ)
* **世界のルール：** プレイヤーの移動、敵の追跡（FOV/視界判定）、速度、時間制限。

### ⚠️ ④ Threat System（怖さの正体）
* **役割：** 「AIの確信度がゲーム難易度を変える」 ➔ **👉「AIが世界の物理法則を変える機構」**
* **該当コード：** `recalculateWorldThreat()`
* **動的変化アルゴリズム：**
  * `confidence` (確信度) ⬆️ ➔ 敵の移動スピードUP
  * `severity` (危険度) ⬆️ ➔ 画面にグリッチエフェクト発生
  * `hallucination` (幻覚度) ⬆️ ➔ プレイヤーの視界（FOV）縮小

### 🖥️ ⑤ UI層（見た目）
* **役割：** 「プレイヤーが触る画面」 ➔ **👉「操作パネル」**
* **該当技術：** Streamlit, HTML overlay, HTML5 Canvas, Interaction Buttons
* **画面構造：** 施設画面（audit UI） / ゲーム画面（Canvas） / ステータスインジケータ / 操作系

---

## 2. `docs/flow.md`
> **役割：処理の流れ（UI ➔ LLM ➔ Engine ➔ State）** > ユーザーの1回の操作に対して、データがどのようにシステムを循環するかを書く場所。

# 🔄 処理フロー（Data Flow）

システムにおけるメインループおよびAI推論時のシーケンスフロー。

## 🌊 コアデータフロー

```text
       [UI (Streamlit)]
              │
              ▼ (ユーザー操作 / 証拠提出)
       POST /inference
              │
              ▼
       [LLM Service (Gemma)] ── 🧠 推理・確信度の算出
              │
              ▼
       POST /state update
              │
              ▼
       [State Manager] ─────── 💾 セーブデータの更新
              │
              ▼
       POST /simulate
              │
              ▼
       [Game Engine] ───────── ⚠️ 脅威度計算・物理法則の書き換え
              │
              ▼
       [Frontend / Canvas] ─── 🎨 グリッチ・描画反映

## 🎯 現状の課題と目指す姿

### ❗ 現在の結合度（密結合）
```text
LLM ─┐
      ├── state
UI  ──┤
      ├── game engine
JS  ──┘

# 📝 設計思考メモ（Design Notes）

本プロジェクトの設計に関する意思決定や、アーキテクチャの変遷の記録。

## 💡 本質的なシステム定義
このシステムは、単なるゲームのバグ修正を行っているのではない。
**「システムに適切な『名前』を与え、境界線を引く作業（これはAI、これは状態、これは物理、これはUI）」**を行っている。

「AIがゲーム世界を直接いじっている実験装置」としての面白さを担保しつつ、拡張可能な設計に昇華させるためのメモ。

---

## 📂 構造分離の意思決定（ADRアプローチ）

### 1. なぜ `services` と `engine` を分けたのか
* **理由：** AIの推論ロジック（不確実で時間がかかる処理）と、ゲームの物理演算（確実でリアルタイム性が求められる処理）が混ざると、フレームレートの低下や同期ズレを引き起こすため。

### 2. なぜ `state` を中央管理にするのか
* **理由：** LLMの出力結果（`confidence`等）がダイレクトにJS Canvas（`engine`）に干渉するとデバッグが不可能になる。一度「世界のセーブデータ（`state`）」に状態を安全に書き込み、それをエンジンが読みに行く構造がもっとも堅牢であるため。

### 3. 今後の課題（Streamlit直結の脱却）
* 現状はStreamlitとHTML/JSが密結合しているが、将来的にバックエンド（Python/FastAPI等）とフロントエンド（ピュアなJS/Canvas）を完全にクリーンなWeb APIで結合する設計案を検討中。

---

# 🔌 API仕様書（API Specification）

各コンポーネント間、およびフロント/バックエンド間でやり取りされるインターフェースの定義。

## 🧠 1. 推論エンドポイント

### `POST /inference`
UIから証拠を受け取り、LLMによる解析を実行する。

* **Request Body:**
  ```json
  {
    "sector": "CYB",
    "evidence": "文字列としての証拠テキストデータ"
  }

* **Response Body:**
  ```json
  {
    "report": "AIが生成した詳細な推理テキスト...",
    "confidence": 0.85,
    "severity": 0.70,
    "contradiction": false
  }

## ⚙️ 2. シミュレーション・状態更新

### `POST /state/update`
LLMの推論結果を元に、現在の世界の状態（セーブデータ）を更新する。

### `POST /simulate`
現在の `state` と `threat` レベルをGame Engineに流し込み、次フレームの物理法則（敵の速度、視界等）を計算させる。
