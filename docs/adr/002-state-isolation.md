👉 内容

State設計を分割した理由（4層構造）

書いてあること
Stateを1個にすると何が起きるか（God Object問題）
なぜ4つに分けたか

構造👇

WorldState（世界の事実）
AIState（推論）
EngineState（物理）
MetaState（ログ）
一言でいうと

「全部まとめると破綻するから役割分けした」

--------------------------------------------------------

          LLM
           │
           ▼
     ┌──────────┐
     │  STATE   │
     └────┬─────┘
          │
 ┌────────┼────────┐
 ▼        ▼        ▼

World   AI      Engine
State   State   State

Decision

すべての情報は一度Stateへ保存する。

Why

直接Engineを書き換えない。

これにより

デバッグ可能
ログ取得可能
再現性向上

となる。
