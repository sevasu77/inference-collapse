処理の流れ（UI→LLM→Engine→State）

<img width="597" height="177" alt="image" src="https://github.com/user-attachments/assets/3456ff15-d81e-495b-bd70-f3e35799e8f5" />


全体フロー

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
