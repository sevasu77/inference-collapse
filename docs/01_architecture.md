# Inference Collapse
# アーキテクチャ仕様書

## 1. 概要

## 2. システムコンセプト

## 3. 現在の動作構成（Live System）

## 4. 現在の実行フロー

## 5. 現状の制約

## 6. 目標アーキテクチャ

## 7. コンポーネント責務

## 8. データフロー

## 9. 設計原則

## 10. 設計目標

## 11. 関連ドキュメント

そして、Future Extensions は削除します。

理由は、

05_future_improvements.md

が存在するからです。

同じ内容を二か所に書くと、
後で100%ズレます。

私ならここも少し変えます

今は

2. Current Runtime

となっていますが、

これは

## 現在の実装（Live System）

の方が自然です。

Current Limitations

↓

現在の構造と課題
Target Architecture

↓

目標アーキテクチャ
Design Goals

↓

この設計で実現したいこと

この方が読み手が頭に入りやすいです。

あと一つだけ追加したい

冒頭にこれを入れます。

## このドキュメントについて

このドキュメントでは、Inference Collapse の現在の実装と、
目指しているアーキテクチャをまとめて説明します。

設計上の考え方や意思決定の理由については
`02_design_decisions.md` を参照してください。

また、プロトタイプから現在の構造へ至るまでの経緯は
`03_history.md` にまとめています。

これがあるだけで、

「ここは設計図なんだ」

ということが一瞬で分かります。

逆に削除していい部分

ここ。

## Future Extensions

FastAPI

Redis

Docker

Kubernetes

・・・

これは完全に

05_future_improvements.md

へ移します。

最終構成はこれが一番きれいです
README.md
    ↓
作品紹介

01_architecture.md
    ↓
現在の構造
理想構造
責務
データフロー
設計原則

02_design_decisions.md
    ↓
なぜこう設計したか

03_history.md
    ↓
どう進化したか

04_lessons_learned.md
    ↓
開発を通じて学んだこと

05_future_improvements.md
    ↓
これから何を作るか

adr/
    ↓
その瞬間その瞬間の意思決定ログ

technical_specs/
    ↓
内部仕様書
