処理の流れ（UI→LLM→Engine→State）

<img width="597" height="177" alt="image" src="https://github.com/user-attachments/assets/3456ff15-d81e-495b-bd70-f3e35799e8f5" />



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
