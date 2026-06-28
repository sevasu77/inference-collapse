## What is Inference Collapse?

## Welcome

**Inference Collapse** は、LLM の推論結果を単なるテキスト出力として扱うのではなく、**ゲーム世界を変化させる物理パラメータ**として利用する実験的なシステムです。

一般的な AI アプリケーションでは、

```
LLM → Text Response → User
```

という流れになります。

一方、本プロジェクトでは、

```
LLM → Cognitive State → Physics → Simulation → Player Experience
```

という新しいパイプラインを採用しています。

AI は文章を生成するだけではなく、世界の状態を変化させる認知コンポーネントとして機能します。

---

# Project Goal

本プロジェクトの目的は、ゲームを作ることではありません。

目指しているのは、

**「AI の認知状態がどのようにゲーム世界へ影響を与えるのか」を観測・実験できるシステムを構築すること**

です。

そのため、LLM の推論結果はゲーム難易度へ直接適用されるのではなく、物理パラメータへ変換されます。

例えば、

| AI Output     | World Effect          |
| ------------- | --------------------- |
| Confidence    | Enemy Speed           |
| Severity      | Spatial Distortion    |
| Contradiction | Perception Distortion |

このように、**認知状態を物理法則へ変換する**ことが、本システムの中核となるアイデアです。

---


# Vision

Inference Collapse は、ゲームエンジンでも AI ライブラリでもありません。

**AI の認知状態を物理世界へ変換し、その振る舞いを観測するための実験プラットフォーム**です。

本プロジェクトを通して、AI・ゲーム・シミュレーションを組み合わせた新しいアーキテクチャの可能性を探求していきます。
