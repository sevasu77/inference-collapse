Markdown
# Inference Collapse: Architecture & Live System Specification

## 1. Overview
Inference Collapse は、「LLMの認知状態がゲーム世界を書き換える」ことを目的とした実験的シミュレーションシステムです。

一般的な **[ LLM ➔ テキスト生成 ➔ UI表示 ]** という一方通行の構造ではなく、以下の変換パイプラインを採用しているのが最大の特徴です。

```text
[ LLM (外部推論) ] ➔ [ Cognitive State (認知状態) ] ➔ [ Physics Parameters (物理定数) ] ➔ [ World (ゲーム世界) ]
LLMを単なる文章生成器ではなく、ゲーム世界を動かすための「認知状態生成器（Cognitive State Generator）」として扱い、その歪みをリアルタイムに物理法則へ変換します。

2. Current Runtime (現在動作しているシステム)
本プロジェクトは「Post-Hoc Architecture（後付けアーキテクチャ）」アプローチを採用しており、現在は以下の技術スタックを用いた統合型のプロトタイプ（Phase 1）として実際に稼働しています。

UI / Frontend: Streamlit + HTML5 Canvas (JavaScript)

Backend / Hub: Python Backend（メモリ上での状態保持、および各レイヤーの仲介）

LLM (AI Engine): Gemma 4

Rendering: Pythonから埋め込まれたJavaScriptによるCanvas描画

3. Current Runtime Flow
現在（プロトタイプ版）のデータおよび実行の制御フローは以下の通りです。Python Backendがすべてのハブとなり、同期的・直線的にデータを処理しています。

Plaintext
[ Streamlit UI ] ➔ (証拠の入力/ゲーム起動) ➔ [ Python Backend ]
                                                   │
  ┌────────────────────────────────────────────────┘
  ▼
[ Gemma 4 API ] ➔ (生JSONレスポンスのデコード) ➔ [ Runtime State (Pythonメモリ) ]
                                                   │
  ┌────────────────────────────────────────────────┘
  ▼
[ Game Engine ] ➔ (Threat Levelに応じた物理更新) ➔ [ HTML5 Canvas (JS描画) ]
4. Current Limitations (現在の限界と課題)
稼働中のプロトタイプはコアコンセプトの検証を最優先したため、以下の技術적負債（リファクタリングの動機）を抱えています。

Streamlitとゲームロジックの密結合: 画面表示系と裏側の演算が分離しきれていない。

Runtime Stateの責務集中: 単一のメモリ空間にすべての状態（監査結果、物理、メタ情報）が混ざっている。

防衛層（Decision Layer）の未実装: LLMの出力（生dict）を直接受け取っているため、確率的な表記ブレに弱い。

API層が未分離: FastAPI化を前提とした非同期・独立駆動な構造になっていない。

5. Target Architecture (理想設計・最終構造)
上記の課題を完全に解決し、案件やOSSとして世界中のエンジニアに5秒で理解してもらえるよう再設計された、本番仕様のリポジトリ構造（Phase 2）です。

Plaintext
inference-collapse (リポジトリルート / mainブランチ)
│
├── README.md                   # ─── 【パンフレット】この作品は何？（特徴・動かし方・スクショ）
│                               #       ★解説として以下を明記：
│                               #       「docs/adr/ は『設計者の日記（ADR）』です。
│                               #        なぜこの設計を選んだのか、その瞬間の決断を記録しています」
│
├── docs/                       # ─── 【初めて読む方へ：5秒で分かる作品の全貌】
│   ├── 01_architecture.md      # [設計図] 中身はこうなっています（LLM➔Decision➔物理➔画面の図）
│   ├── 02_design_decisions.md  # [なぜこの設計？] 設計者の頭の中（Gemma隔離やState純粋化の理由）
│   ├── 03_history.md           # [設計の変化] 混沌のapp.pyからここへ至ったゲームの進化録・失敗談
│   ├── 04_lessons_learned.md   # [学んだこと] 未来の自分へのメモ（LLMの検証必須、UI分離の教訓）
│   ├── 05_future_improvements.md # [次に作るもの] この作品は終わらない（マルチLLM、Redis、Docker対応）
│   │
│   ├── adr/                    # ─── 【技術者向け：詳細な意思決定の日記（ADR）】
│   │   ├── 000-README.md       # ADRの概要とフォーマットガイド
│   │   ├── 001-separation-of-llm.md # LLM依存を排除した技術적決断の記録
│   │   ├── 002-state-isolation.md    # GameStateを純粋集約器に隔離した技術적決断の記録
│   │   └── 003-real-time-simulation.md # 物理定数を分離し、リアルタイム駆動させた技術적決断の記録
│   │
│   └── technical_specs/        # ─── 【技術者向け：専門的な内部仕様資料】
│       ├── flow.md             # データが一本のパイプラインを流れる詳細フロー
│       ├── api_spec.md         # Decision Layer（InferenceNormalizer）のバリデーション・丸めルール
│       ├── state.md            # 4大ドメインStateの内部構造
│       └── threat.md           # ThreatEngineの認知➔物理変換のマッピング数式
│
└── src/                        # ─── 【ソースコード本体】
    │
    ├── data_models/            # ─── データの型定義層（Immutable）
    │   ├── normalized_inference.py # 正規化された型安全な推論オブジェクト
    │   └── physics_parameters.py   # 純粋な物理行列・定数データ
    │
    ├── ai/                     # ─── AI関連（通信・プロンプト）の集約
    │   ├── gemma_client.py     # [Update] Gemma APIとの低レイヤ通信・生デコード担当（将来の複数LLM対応を見据えた命名）
    │   └── prompts.py          # システムプロンプトや、グリッチ発生用のプロンプト管理
    │
    ├── decision_layer/         # ─── 判定・防衛層（防波堤）
    │   ├── inference_normalizer.py # 生dictをバリデーションし、安全なモデルへ変換
    │   └── validator.py        # 範囲外の数値や型エラーをせき止めるカスタムバリデータ
    │
    ├── game_state/             # ─── [Update] ゲームと世界の現在の状態（データ）のみを保存
    │   ├── __init__.py         # 外部へは game.py (GameState) のみをきれいに公開
    │   ├── game.py             # GameState（4つのStateを束ねる、ロジック無しの純粋集約器）
    │   ├── environment.py      # ステージクリア状況、プレイヤー位置、オブジェクトの存在データ
    │   ├── cognition.py        # AIが世界をどう解釈したかのログ、及び現在の不信感（Suspicion）スコア
    │   ├── runtime.py          # 残り時間、現在のフレームレート、実行フラグ等のセッション状態
    │   └── telemetry.py        # [Update] ゲーム中に起きた出来事を記録する、あとから分析・デバッグするためのログ
    │
    ├── simulation_engine/      # ─── 世界を動かす「計算（ロジック）」を駆動
    │   ├── threat_engine.py    # AIの「認知」を燃料に、物理パラメータを計算・生成する翻訳装置
    │   └── simulation_engine.py # [Update] 物理パラメータを受け取り、ゲーム世界を1フレームずつ更新する心臓部
    │
    └── ui/                     # ─── ユーザーインターフェース層（画面表示）
        ├── streamlit_app.py    # メインのエントリーポイント（画面起動ファイル）
        ├── pages.py            # 各画面（タイトル画面、メインゲーム画面、デバッグ監査画面など）
        └── components.py       # ゲージ、ログウィンドウ、グリッチ演出用UIパーツ群
6. Component Responsibilities (コンポーネントの責務定義)
UI Layer (src/ui/)
責務: ユーザー入力の受付、Canvas描画のキック、HUDおよびステータス表示。

禁止事項: AI推論の直接実行、ゲームロジックの演算、状態の直接書き換え。

AI Layer (src/ai/)
責務: Gemma API（将来は複数LLM）との低レイヤ通信、システムプロンプトの管理。

出力: 生の推論JSONデータ。

Decision Layer (src/decision_layer/)
責務: LLMの非決定的な出力をバリデーションし、安全な型（モデル）へ正規化・丸め処理を行う。

役割: AIの気まぐれからゲームエンジンを守る「防波堤」。

Game State (src/game_state/)
責務: ゲームと世界の現在の状態（環境データ、AIの認知ログ、セッション情報、テレメトリ）を純粋なデータとして保持。

禁止事項: 描画ロジックの保有、AI推レベルの自己決定、物理演算の実行。

Simulation Engine (src/simulation_engine/)
責務: Threat Engineで認知を物理パラメータへ翻訳し、その値だけを盲信して世界を1フレームずつ更新する。

駆動: AIの存在を1ミリも知らない、純粋な決定論的演算。

7. Data Flow (理想的な単方向パイプライン)
理想アーキテクチャにおける、データ流通の一方向（Unidirectional）の保証図です。データは決して逆流しません。

Plaintext
[ AI Layer (Gemma) ] ➔ (生 dict) ➔ [ Decision Layer ] ➔ (型安全なオブジェクト化) ➔ [ data_models (NormalizedInference) ] ➔ (世界のデータを記録) ➔ [ Game State ] ➔ (認知を物理へ翻訳) ➔ [ Simulation Engine (Threat Engine) ] ➔ (物理定数を確定) ➔ [ data_models (PhysicsParameters) ] ➔ (1フレーム更新駆動) ➔ [ Simulation Engine (Core) ] ➔ (画面描画) ➔ [ UI Layer (Streamlit) ]
8. Design Principles (設計原則)
Prototype First: まず力技でも動くものを作り、コア体験の価値を検証する。

Post-Hoc Architecture: 最初に机上の空論で設計せず、動く実装から境界線を抽出する。

Loose Coupling（疎結合）: 各レイヤーの依存方向を上から下への一方向に制限する。

Inference-to-Physics Mapping: 意味情報（AIの不信感など）を、必ずゲームの物理法則（速度、空間のガタツキ）へとマッピングする。

9. Design Goals (設計目標)
本システムがリファクタリングによって達成する最終目標です。

完全な責務分離: 画面を書き換えても物理演算は壊れず、AIを書き換えても状態管理は壊れない。

プラグイン可能なコンポーネント:

Replaceable LLM (GemmaからGPT/Claudeへの容易な切り替え)

Replaceable Game Engine (Python演算から外部エンジンへの移行準備)

Backend Migration Ready: 将来的にFastAPI等の本格的なバックエンドへ移行できる疎結合性の確保。

10. Future Extensions (今後の拡張予定)
FastAPI Backend & WebSocket同期: 通信レイヤーの非同期リアルタイム化。

Multi-Agent LLM: 複数のAIが互いに監査し合うマルチエージェント構造。

Redisを用いたステートキャッシュ: 状態の永続化と高速なセッション管理。

Docker / Kubernetes対応: コンテナ化による環境依存の排除とスケーラビリティの確保。

11. Related Documents
より深い設計の背景や、詳細な技術仕様は以下のドキュメントを順に参照してください。

👉 02_design_decisions.md : なぜこの設計なのか（Gemmaの分離やState隔離の技術的理由）

👉 03_history.md : どう進化したのか（1本のapp.pyからここに至るまでの失敗と歴史）

👉 docs/adr/ : 設計者の日記（ADR）（開発の節目ごとに下された具体的な技術決定のリアルな記録）

👉 docs/technical_specs/ : 専門的な内部仕様資料（データ構造や物理変換の数学的数式）
