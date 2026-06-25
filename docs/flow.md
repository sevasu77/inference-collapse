処理の流れ（UI→LLM→Engine→State）

<img width="636" height="658" alt="image" src="https://github.com/user-attachments/assets/f57027f4-8433-4037-9d80-0099041ba0a0" />
🧠 ① LLM層（頭脳）
📦 役割

「推理・判断を作るAI」

該当コード
ask_gemma_reasoning()
中身の意味
入力:
  - sector（BIO / MEC / CYB）
  - evidence（証拠）

出力:
  - report（推理）
  - confidence（確信度）
  - severity（危険度）
  - contradiction（矛盾）
🧩（これは何か）

👉「探偵AI」
<img width="723" height="262" alt="image" src="https://github.com/user-attachments/assets/6b5c0dd6-ac1d-49b1-9342-c42885b35360" />

🧠 ① backend（脳・ルール・AI）
📦 役割

「世界のルール・AI・状態管理」


<img width="597" height="177" alt="image" src="https://github.com/user-attachments/assets/3456ff15-d81e-495b-bd70-f3e35799e8f5" />


        [全体フロー]
               ↓
        [UI (Streamlit)]
               ↓
        POST /inference
               ↓
        [LLM Service]
               ↓
        POST /state update
               ↓
        [State Manager]
               ↓
        POST /simulate
               ↓
        [Game Engine]
               ↓
        frontend描画


| 今のコード                      | 新構造              |
| -------------------------- | ---------------- |
| ask_gemma_reasoning        | backend/services |
| recalculateWorldThreat     | backend/engine   |
| auditStates                | backend/state    |
| collectors / update / draw | frontend/engine  |
| Streamlit + HTML           | ui/app.py        |
