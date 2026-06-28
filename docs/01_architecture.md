# Architecture

## Overview

Inference Collapse は、「LLM の認知状態がゲーム世界へ影響を与える」ことを目的とした実験的シミュレーションシステムです。

一般的な AI アプリケーションでは、

```text
LLM
   ↓
Text Response
   ↓
User
```

という流れで推論結果をテキストとして返します。

一方、本プロジェクトでは、

```text
LLM
      ↓
Cognitive State
      ↓
Physics Parameters
      ↓
Simulation
      ↓
Player Experience
```

という一方向のパイプラインを採用しています。

LLM は文章生成器ではなく、

**「認知状態（Cognitive State）を生成するコンポーネント」**

として扱われます。

生成された認知状態は、そのままゲームロジックへ渡されるのではなく、物理パラメータへ変換されることでゲーム世界へ影響を与えます。

---

# System Architecture

現在のシステムは、以下の責務ごとにコンポーネントを分離することを目標として設計されています。

```text
Inference Collapse

├── UI Layer
│      ├── Streamlit
│      ├── HTML5 Canvas
│      └── Components
│
├── AI Layer
│      ├── Gemma Client
│      └── Prompts
│
├── Decision Layer
│      ├── Inference Normalizer
│      └── Validator
│
├── Game State
│      ├── Environment State
│      ├── Cognitive State
│      ├── Runtime State
│      └── Telemetry State
│
├── Simulation Engine
│      ├── Threat Engine
│      └── Simulation Engine
│
└── Data Models
       ├── NormalizedInference
       └── PhysicsParameters
```

各コンポーネントは責務ごとに独立しており、一方向のデータフローによって接続されます。

---

# Current Runtime

現在の実装は、コンテスト向けプロトタイプ（Phase 1）として構築されています。

使用技術は以下の通りです。

* UI：Streamlit + HTML5 Canvas
* Backend：Python
* AI：Gemma 4
* Rendering：JavaScript Canvas

現時点では Python Backend が各コンポーネントの仲介役となり、同期的に処理を行っています。

---

# Current Runtime Flow

現在のプロトタイプでは、以下の順序でデータが処理されます。

```text
Streamlit UI
        │
        ▼
Python Backend
        │
        ▼
Gemma 4 API
        │
        ▼
Runtime State
        │
        ▼
Game Engine
        │
        ▼
HTML5 Canvas
```

Gemma の推論結果は Runtime State に保存され、その状態をゲームエンジンが参照してゲーム世界を更新します。

---

# Current Limitations

現在のプロトタイプには、以下の課題があります。

* Streamlit とゲームロジックが密結合している
* Runtime State に責務が集中している
* Decision Layer が未実装である
* LLM の生データを直接利用している
* API 層が分離されていない

これらは、今後のリファクタリング対象です。

---

# Component Responsibilities

## UI Layer

**責務**

* ユーザー入力
* HUD の表示
* Canvas 描画

**担当しないもの**

* AI 推論
* 物理演算
* 状態管理

---

## AI Layer

**責務**

* Gemma API 通信
* プロンプト管理
* 推論結果の生成

AI はゲーム世界を書き換えません。

認知状態を生成することだけを担当します。

---

## Decision Layer

**責務**

LLM の生データを検証し、安全なデータモデルへ変換します。

役割は、

**AI の気まぐれからゲームエンジンを守る防波堤**

です。

---

## Game State

**責務**

ゲーム世界の現在の状態を保持します。

* Environment State
* Cognitive State
* Runtime State
* Telemetry State

Game State はデータのみを保持し、ゲームロジックは持ちません。

---

## Threat Engine

本プロジェクトの中核となるコンポーネントです。

AI の認知状態をゲーム世界の物理法則へ変換します。

| Cognitive State | Physical Effect       |
| --------------- | --------------------- |
| Confidence      | Enemy Speed           |
| Severity        | Spatial Distortion    |
| Contradiction   | Perception Distortion |

AI はゲームを直接制御せず、認知状態だけを提供します。

Threat Engine が認知と物理世界を接続します。

---

## Simulation Engine

**責務**

Threat Engine が生成した物理パラメータを受け取り、

* プレイヤー
* 敵 AI
* 衝突判定
* タイマー
* エフェクト

などを更新します。

Simulation Engine は AI の存在を知りません。

---

# Data Flow

理想的なデータフローは、一方向のみです。

```text
AI Layer
      │
      ▼
Decision Layer
      │
      ▼
NormalizedInference
      │
      ▼
Game State
      │
      ▼
Threat Engine
      │
      ▼
PhysicsParameters
      │
      ▼
Simulation Engine
      │
      ▼
UI Layer
```

各レイヤーは上流の情報のみを受け取り、下流へ渡します。

逆方向の依存は持ちません。

---

# Design Principles

本プロジェクトは、以下の設計原則に基づいています。

## Prototype First

まず動作するプロトタイプを構築し、コアコンセプトの実現可能性を検証する。

---

## Post-Hoc Architecture

動作するプロトタイプから責務を抽出し、段階的にアーキテクチャへ発展させる。

---

## Separation of Responsibilities

AI・状態管理・シミュレーション・UI を独立したコンポーネントとして設計する。

---

## Inference-to-Physics Mapping

LLM の推論結果を直接ゲームへ反映するのではなく、物理パラメータへ変換することで AI とゲームロジックを疎結合に保つ。

---

# Design Goals

本アーキテクチャが目指す最終的な目標は次のとおりです。

* AI・状態管理・シミュレーション・UI の責務分離
* LLM を容易に差し替えられる構造
* バックエンドの独立
* 保守性・拡張性・再利用性の向上
* AI の認知状態を安全かつ制御可能な形で物理世界へ変換するアーキテクチャ
