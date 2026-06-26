👉 内容

AIの状態をリアルタイムで物理法則に変換する設計

書いてあること
confidence → enemy speed
severity → glitch
hallucination → FOV
重要ポイント

普通のゲーム：

difficulty = static value

この設計：

difficulty = AI state
一言でいうと

「AIの思考がゲーム世界のルールになる」

----------------------------------------------------------------------------

      confidence
          │
          ▼
 ┌─────────────────┐
 │ Threat System   │
 └───────┬─────────┘
         │
         ▼

speed
FOV
glitch
enemy AI

         │
         ▼

 Game Engine

 Decision

AIの認知状態をゲーム物理へ変換する。

Why

通常ゲームは

Difficulty
    │
    ▼

Enemy Speed

だけである。

本プロジェクトでは

AI Confidence
        │
        ▼

Threat Level
        │
        ▼

Physics

となる。

つまり

AIの認知状態が物理法則になる。

これがこのシステム最大の特徴である。
