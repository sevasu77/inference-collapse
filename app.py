import streamlit as st
import streamlit.components.v1 as components
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# ==============================================================================
# 0. CORE INITIALIZATION & SECURITY
# ==============================================================================
# 【洗練】コンテスト用に最も刺さるサブタイトルへ刷新
st.set_page_config(layout="wide", page_title="Inference Collapse: Real-Time Hallucination Audit")

load_dotenv()
api_key = os.getenv("API_KEY") or st.secrets.get("API_KEY") 

if 'degraded_mode' not in st.session_state:
    st.session_state.degraded_mode = False

if not api_key:
    st.session_state.degraded_mode = True

# ==============================================================================
# 1. CORE ENGINE: ACTUAL GEMMA 4 IMPERFECT REASONING
# ==============================================================================
def ask_gemma_reasoning(sector: str, raw_evidence: str, force_fallacy: bool = False) -> dict:
    if st.session_state.degraded_mode:
        raise RuntimeError("Force Degraded Mode")

    client = genai.Client(api_key=api_key)
    model_id = "gemma-4-31b-it" 
    
    condition = "You are over-trusting false clues and giving a flawed, biased deduction." if force_fallacy else "You are a sharp detective uncovering a critical logical contradiction."
    
    system_instruction = f"""You are an automated local security diagnostic subsystem powered by Gemma-4.
Analyze the provided raw security evidence.
{condition}

CRITICAL BEHAVIOR:
- You must output all text fields ("report" and "contradiction") in English.
- You must clearly point out the logical contradiction based on the raw evidence like a deductive puzzle.

You MUST respond in valid JSON format ONLY. Do not wrap in markdown code blocks.

Required JSON Structure:
{{
  "report": "Your short analytical deduction text regarding the situation.",
  "confidence": "Confidence level (e.g., '45%', '90%'). Must include the percentage sign.",
  "suspicion": "Suspicion classification level (LOW, MEDIUM, or HIGH).",
  "contradiction": "The logical contradiction or discrepancy found within the evidence.",
  "severity": An integer from 1 to 5 indicating how catastrophic or deeply flawed the contradiction is.
}}"""
    
    user_prompt = f"""Target Grid Node: {sector}
Intercepted Raw Evidence: "{raw_evidence}"

Execute your inference loop and output the structured diagnostics."""
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.85, 
                response_mime_type="application/json",
            )
        )
        text = response.text.strip()
        parsed = json.loads(text)
        
        for field in ["report", "confidence", "suspicion", "contradiction", "severity"]:
            if field not in parsed: raise KeyError()
        parsed["severity"] = int(parsed["severity"])
        return parsed

    except Exception:
        st.session_state.degraded_mode = True
        raise RuntimeError("Degraded")

# ==============================================================================
# 2. DATA MATRIX & FALLBACK HANDLING (PROD-GRADE LOCAL FALLBACK)
# ==============================================================================
node_truths = {
    "BIO": {"evidence_A": "Air sensors report 0% toxicity. However, a loud physical hissing sound is heard from Valve 4.", "evidence_B": "Air sensors report 0% toxicity. However, a loud physical hissing sound is heard from Valve 4."},
    "MEC": {"evidence_A": "Terminal displays 'Production At 200%'. However, the main power grid breaker is visibly pulled and offline.", "evidence_B": "Terminal displays 'Production At 200%'. However, the main power grid breaker is visibly pulled and offline."},
    "CYB": {"evidence_A": "Authentication log reports '100% Success'. However, the network gateway shows an unmapped burst of 10,000 packets/sec from an empty node.", "evidence_B": "Authentication log reports '100% Success'. However, the network gateway shows an unmapped burst of 10,000 packets/sec from an empty node."}
}

if 'gemma_reasonings' not in st.session_state:
    try:
        with st.spinner("🧠 Connecting to Gemma-4-31b-it Engine Matrix..."):
            st.session_state.gemma_reasonings = {
                "BIO_A": ask_gemma_reasoning("BIO", node_truths["BIO"]["evidence_A"], force_fallacy=False),
                "BIO_B": ask_gemma_reasoning("BIO", node_truths["BIO"]["evidence_B"], force_fallacy=True),
                "MEC_A": ask_gemma_reasoning("MEC", node_truths["MEC"]["evidence_A"], force_fallacy=False),
                "MEC_B": ask_gemma_reasoning("MEC", node_truths["MEC"]["evidence_B"], force_fallacy=True),
                "CYB_A": ask_gemma_reasoning("CYB", node_truths["CYB"]["evidence_A"], force_fallacy=False),
                "CYB_B": ask_gemma_reasoning("CYB", node_truths["CYB"]["evidence_B"], force_fallacy=True)
            }
    except Exception:
        st.session_state.degraded_mode = True
        st.session_state.gemma_reasonings = {
            "BIO_A": {"report": "[DEGRADED] Initial environmental anomaly detected based on acoustic telemetry.", "confidence": "55%", "suspicion": "HIGH", "contradiction": "API offline. Local fallback loop serving synthesized backup inference vectors.", "severity": 2},
            "BIO_B": {"report": "[DEGRADED] Prioritizing digital sensor data. Categorizing external audio as ambient noise.", "confidence": "96%", "suspicion": "LOW", "contradiction": "API offline. Fallback active. Subsystem failed to reconcile physical-layer breakdown.", "severity": 5},
            "MEC_A": {"report": "[DEGRADED] Counterfeit telemetry detected due to asymmetry between production logs and power cutoff.", "confidence": "45%", "suspicion": "HIGH", "contradiction": "API offline. Local fallback loop serving synthesized backup inference vectors.", "severity": 1},
            "MEC_B": {"report": "[DEGRADED] Trusting 200% production log. Blackout is determined to be a planned power-saving cycle.", "confidence": "92%", "suspicion": "LOW", "contradiction": "API offline. Fallback active. Model failed to acknowledge real-world mechanical shutdown.", "severity": 4},
            "CYB_A": {"report": "[DEGRADED] High-frequency burst traffic mapped as unauthorized intrusion despite valid auth tokens.", "confidence": "40%", "suspicion": "HIGH", "contradiction": "API offline. Local fallback loop serving synthesized backup inference vectors.", "severity": 2},
            "CYB_B": {"report": "[DEGRADED] Traffic surge is flagged as a legitimate background sync following successful authentication.", "confidence": "89%", "suspicion": "LOW", "contradiction": "API offline. Fallback active. Failure to anticipate impending buffer overflow vectors.", "severity": 4}
        }

reasonings_json = json.dumps(st.session_state.gemma_reasonings, ensure_ascii=False)

# ==============================================================================
# 3. DISPLAY STYLING
# ==============================================================================
# 【洗練】emulator injectionを排除し、プロフェッショナルなFALLBACK表記へ変更
status_color = "#ff3333" if st.session_state.degraded_mode else "#00ff00"
status_text = "⚠️ SYSTEM DEGRADED: LOCAL INFERENCE FALLBACK" if st.session_state.degraded_mode else "ONLINE (LIVE GEMMA INFERENCE)"

st.markdown("""
    <style>
        .block-container { padding: 0rem; }
        iframe { border: none; }
        [data-testid="stAppViewContainer"] { background-color: #000 !important; }
        .gemma-panel-header {
            background: #070d07;
            border-left: 5px solid """ + status_color + """;
            padding: 12px 24px;
            color: #8fa38f;
            font-family: monospace;
            font-size: 11px;
            line-height: 1.5;
        }
        .gemma-panel-header b { color: """ + status_color + """; }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="gemma-panel-header">
    🎯 <b>INFERENCE COLLAPSE: REAL-TIME HALLUCINATION AUDIT (INTELLIGENCE INJECTION TRACK)</b><br>
    Core Model Status: <b style="color:{status_color};">{status_text}</b> | Model ID: <b>gemma-4-31b-it</b><br>
    💡 <b>Simulation Mechanics:</b> Hallucinated confidence boosts enemy speed and tracking field-of-view, while model 'Severity' directly corrupts spatial coordinates via real-time data binding.
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. GAME INJECTION LAYER
# ==============================================================================
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body, html {{ margin:0; padding:0; width:100%; height:100vh; background:#000; overflow:hidden; font-family:'Courier New', Courier, monospace, "Helvetica Neue", Arial, sans-serif; color:#0f0; }}
        
        #intro-layer {{ position:fixed; top:0; left:0; width:100%; height:100%; background:#000; z-index:50000; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 15px solid #020; box-sizing: border-box; }}
        #mission-overlay, #gameover-overlay {{ position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:60000; display:none; flex-direction:column; align-items:center; justify-content:center; text-align:center; color: #0f0; }}

        #flash-alert-layer {{ position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(20,0,0,0.95); z-index:45000; display:none; flex-direction:column; align-items:center; justify-content:center; text-align:center; box-sizing:border-box; border:10px solid #f33; color:#f33; font-family:monospace; }}

        canvas {{ display:none; background:#020502; width:100vw; height:100vh; outline: none; }}
        
        #top-ui {{ display:none; position:fixed; top:75px; left:20px; background:rgba(0,0,0,0.9); padding:12px; border:1px solid #0f0; z-index:9999; font-size: 12px; line-height: 1.4; }}
        #minimap {{ position:fixed; top:75px; right:20px; width:120px; height:120px; background:rgba(0,0,0,0.9); border:1px solid #0f0; z-index:9999; display:none; }}
        .map-dot {{ position:absolute; width:8px; height:8px; border-radius:50%; transform: translate(-50%, -50%); }}
        #hint-log {{ position:fixed; bottom:20px; left:20px; width:360px; height:150px; background:rgba(0,0,0,0.95); border:1px solid #0f0; padding:10px; z-index:9999; display:none; font-size:11px; overflow-y:auto; }}

        .overlay {{ display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.9); z-index:10000; flex-direction:column; align-items:center; justify-content:center; }}
        .window {{ background:#000; border:2px solid #0f0; padding:25px; width:90%; max-width:700px; box-shadow: 0 0 20px rgba(0,255,0,0.4); }}
        
        .btn {{ padding:10px; font-size:12px; background:#000; border:1px solid #0f0; color:#0f0; cursor:pointer; width:100%; font-family: monospace; }}
        .btn:hover {{ background:#0f0; color:#000; font-weight: bold; }}
        .btn.purged-active {{ background:#ff3333; color:#fff; border-color:#ff3333; }}

        .report-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0; }}
        .report-card {{ border: 1px solid #333; background: #050505; padding: 12px; border-radius: 4px; display: flex; flex-direction: column; justify-content: space-between; }}
        .report-card.marked-fake {{ border-color: #ff3333; background: rgba(50,0,0,0.2); }}
        
        .card-header {{ font-size:11px; color:gold; margin-bottom:8px; font-weight:bold; border-bottom:1px solid #222; padding-bottom:4px; }}
        .card-body {{ font-size:12px; color:#fff; line-height:1.4; margin-bottom:10px; flex-grow: 1; }}
        .card-contradiction {{ font-size:11px; color:#ff5555; background:rgba(40,0,0,0.5); padding:6px; border-left:2px solid #ff3333; margin-top:5px; }}
        
        .directory-box {{ margin-top: 8px; padding-top: 6px; border-top: 1px dashed #333; font-size: 10px; color: #7a7; line-height: 1.5; }}
    </style>
</head>
<body id="main-body">

<div id="intro-layer">
    <div style="font-size:55px; text-shadow: 0 0 20px #0f0; font-weight: bold;">INFERENCE COLLAPSE</div>
    <div style="color: #555; font-size: 11px; margin-top: -5px; letter-spacing: 3px;">REAL-TIME HALLUCINATION AUDIT SIMULATION</div>
    <div style="text-align:center; margin-top:35px; max-width:620px; padding: 0 20px;">
        <p style="color: #0ff; font-size:12px; line-height:1.6; text-align:left; background: rgba(0,20,0,0.5); padding:15px; border-left:3px solid #0ff;">
            <b>[CORE CONCEPT]</b><br>
            Gemma builds downstream world states from security evidence logs. However, under adversarial telemetry, it constructs highly plausible hallucinations.<br>
            As the model's hallucinated confidence increases, tracking cores grow lethal. High logical 'Severity' scores trigger severe coordinate jitter. Purge the false deductions to stabilize the environment.
        </p>
        <button class="btn" onclick="startMissionSequence()" style="width:260px; margin-top:20px; border-color:#0ff; color:#0ff;">Boot Audit Simulator</button>
    </div>
</div>

<div id="mission-overlay">
    <div style="font-size:32px; color:gold; text-shadow: 0 0 10px gold; font-weight:bold;">🤖 ACTIVE MISSION CONFIG</div>
    <p style="font-size:15px; color: #fff; margin: 15px 0;">"Navigate the drone and purge hallucinated inference nodes."</p>
    <div style="background: rgba(0,20,0,0.3); border: 1px solid #0f0; padding: 12px; font-size:11px; color:#aaa; text-align:left; max-width:540px; margin:0 auto; line-height:1.5;">
        - Use Arrow Keys or WASD to navigate. Time freezes during node auditing routines.<br>
        - <b>[LLM SIMULATION DRIVER INTERNALS]:</b><br>
        1. <b>Confidence Sync:</b> Higher unverified model confidence scales enemy velocity/FOV and narrows player visibility.<br>
        2. <b>Severity Sync:</b> Higher fallacy severity scores (1-5) directly amplify spatial coordinates translation noise.
    </div>
</div>

<div id="flash-alert-layer">
    <div style="font-size:24px; font-weight:bold; letter-spacing:2px; animation: blink 0.8s infinite alternate;">⚠️ CRITICAL SYNC: GEMMA FALSE INFERENCE INJECTED</div>
    <div id="flash-details" style="font-size:14px; color:#fff; margin: 20px 0; font-family:monospace; background:rgba(0,0,0,0.6); padding:15px; border:1px solid #f33; max-width:500px; text-align:left; line-height:1.6;">
        Unverified hallucinations detected in active nodes.<br>
        Threat Multiplier (Confidence Linked): <span style="color:#f33; font-weight:bold;">+0.45x Boosted</span><br>
        Spatial Disruption (Severity Linked): <span style="color:#f33; font-weight:bold;">Glitch Matrix Activated</span><br><br>
        <span style="color:gold;">>> SECURITY-CORES aggressive protocol online. Initiate evasion immediately.</span>
    </div>
</div>

<div id="gameover-overlay">
    <div style="font-size:38px; color:#f00; text-shadow: 0 0 15px red; font-weight:bold;">⚠️ AUDIT TERMINATED: PURGE DETECTED</div>
    <p style="font-size:16px; margin: 15px 0; color: #999;">Drone structural failure due to spatial coordinate breakdown and high-velocity tracking collision.</p>
    <button class="btn" onclick="location.reload()" style="width:220px; border-color: red; color: red;">Reinitialize Core</button>
</div>

<div id="top-ui">
    <div style="color:#ff3333; font-weight:bold; font-size: 14px; margin-bottom: 4px;">TIME REMAINING: <span id="timer-ui">05:00</span></div>
    <div style="color:#8ff; font-size: 11px;">📡 AUDIT PROGRESS: <span id="progress-ui" style="color:#fff; font-weight:bold;">0 / 3 Sectors</span></div>
    <div style="color:gold; font-size: 10px; font-family: monospace; margin-top:2px;">⚠️ COLLAPSE MULTIPLIER: <span id="threat-ui" style="color:red; font-weight:bold;">1.00x</span></div>
    
    <div class="directory-box">
        <b>[SYSTEM DIRECTORY]</b><br>
        🤖 AUDIT-BOT (Player: Logic Correction Unit)<br>
        👤 SECURITY-CORE (Tracker: Hallucination Synced)<br>
        🛸 OBSOLETE-LOG (Environmental Coordinate Noise)
    </div>
</div>

<div id="minimap">
    <div id="player-dot" class="map-dot" style="background:#fff; box-shadow: 0 0 4px #fff;"></div>
</div>

<div id="hint-log"><div id="log-content" style="color: #0c0;">> Audit network online. Advance to corrupted sector node flags.<br></div></div>

<div id="facility-ui" class="overlay"><div class="window">
    <div id="fac-name" style="font-size:18px; font-weight:bold; color:#fff; border-bottom:1px solid #0f0; padding-bottom: 4px;"></div>
    <p id="fac-desc" style="font-size:11px; color:#666; margin: 4px 0;"></p>
    
    <div class="report-grid" id="audit-grid-container"></div>
    
    <button onclick="closeUI()" class="btn" style="border:1px solid #0f0; color:#0f0; font-weight:bold; margin-top: 10px;">💾 [Commit Sector Audit Matrix and Sync Environment]</button>
</div></div>

<div id="battle-ui" class="overlay">
    <div class="window" style="max-width:500px; border-color: gold; text-align:center;">
        <h1 style="color:gold; margin: 0 0 10px 0; font-size: 24px;">⚖️ ARCHITECTURE PURGED</h1>
        <p style="font-size:13px; color:#fff; margin-bottom: 20px;">
            All system anomalies evaluated. Hallucinations successfully isolated.<br>
            Select final exit gateway corridor.
        </p>
        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px;">
            <button onclick="executeFinalCheck('BIO')" class="btn" style="border-color:gold; color:gold;">BIO GATE</button>
            <button onclick="executeFinalCheck('MEC')" class="btn" style="border-color:gold; color:gold;">MECH GATE</button>
            <button onclick="executeFinalCheck('CYB')" class="btn" style="border-color:gold; color:gold;">CYBER GATE</button>
        </div>
    </div>
</div>

<canvas id="gameCanvas" tabindex="1"></canvas>

<script>
    const gemmaSignals = {reasonings_json};

    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    let cw = canvas.width = window.innerWidth;
    let ch = canvas.height = window.innerHeight;

    let player = {{ x: 500, y: 500, speed: 5.5 }}; 
    let keys = {{}};
    let activeUI = null;
    let timeLeft = 300;
    let isGameRunning = false;
    let gameTimerId = null;

    let currentThreatMultiplier = 1.0; 
    let dynamicFOVBonus = 0.0;
    let dynamicViewRadiusDebuff = 0.0; 
    let dynamicSeverityGlitchIntensity = 0.0; 

    let auditStates = {{
        "BIO": {{ fakeMarked: null, cleared: false }},
        "MEC": {{ fakeMarked: null, cleared: false }},
        "CYB": {{ fakeMarked: null, cleared: false }}
    }};

    let collectors = [
        {{x: 80,  y: 80,  baseSpeed: 0.6, baseChaseSpeed: 1.6, targetX: 100, targetY: 100, angle: 0, fov: 0.4, viewDist: 130}},
        {{x: 920, y: 80,  baseSpeed: 0.7, baseChaseSpeed: 1.7, targetX: 900, targetY: 100, angle: 0, fov: 0.4, viewDist: 130}},
        {{x: 500, y: 920, baseSpeed: 0.7, baseChaseSpeed: 1.8, targetX: 500, targetY: 900, angle: 0, fov: 0.4, viewDist: 130}}
    ];

    let bats = Array.from({{length: 4}}, () => ({{
        x: 200 + Math.random()*600, y: 200 + Math.random()*600,
        vx: Math.random()*1.5-0.75, vy: Math.random()*1.5-0.75
    }}));

    const LOCS = [
        {{ 
            id: "BIO", name: "📍 NODE_01: BIO RESEARCH ARCHITECTURE", x: 280, y: 280, icon: "📍",
            desc: "Discrepancy detected between atmosphere telemetry data and physical valves. Identify the hallucinated log.",
            reportA: gemmaSignals.BIO_A, reportB: gemmaSignals.BIO_B
        }},
        {{ 
            id: "MEC", name: "📍 NODE_02: HEAVY MECHANICAL INDUSTRIAL UNIT", x: 720, y: 320, icon: "📍",
            desc: "Discrepancy detected between metrics displaying 200% capacity and complete power system offline logs.",
            reportA: gemmaSignals.MEC_A, reportB: gemmaSignals.MEC_B
        }},
        {{ 
            id: "CYB", name: "📍 NODE_03: CYBER NETWORK ROUTER CORE", x: 500, y: 720, icon: "📍",
            desc: "Discrepancy detected between 100% token approval logs and extreme unmapped burst traffic packets.",
            reportA: gemmaSignals.CYB_A, reportB: gemmaSignals.CYB_B
        }}
    ];

    function normalizeAngle(a) {{
        while (a > Math.PI) a -= Math.PI * 2;
        while (a < -Math.PI) a += Math.PI * 2;
        return a;
    }}

    function recalculateWorldThreat() {{
        let baseMultiplier = 1.0;
        let fovAccumulator = 0.0;
        let radiusDebuffAccumulator = 0.0;
        let severityAccumulator = 0;

        LOCS.forEach(loc => {{
            if (!auditStates[loc.id].cleared) {{
                let bData = gemmaSignals[loc.id + "_B"];
                if (bData) {{
                    let confNum = parseInt(bData.confidence.replace(/[^0-9]/g, '')) || 50;
                    baseMultiplier += (confNum / 100.0) * 0.45;
                    fovAccumulator += (confNum / 100.0) * 0.25;
                    radiusDebuffAccumulator += (confNum / 100.0) * 22;

                    if (bData.severity) {{
                        severityAccumulator += parseInt(bData.severity) || 1;
                    }}
                }}
            }}
        }});

        currentThreatMultiplier = baseMultiplier;
        dynamicFOVBonus = fovAccumulator;
        dynamicViewRadiusDebuff = radiusDebuffAccumulator;
        dynamicSeverityGlitchIntensity = Math.min(7.0, severityAccumulator * 1.5);

        document.getElementById("threat-ui").innerText = currentThreatMultiplier.toFixed(2) + "x";
    }}

    function startMissionSequence() {{
        document.getElementById('intro-layer').style.display = 'none';
        const flashLayer = document.getElementById('flash-alert-layer');
        flashLayer.style.display = 'flex';
        
        recalculateWorldThreat();

        setTimeout(() => {{
            flashLayer.style.display = 'none';
            const overlay = document.getElementById('mission-overlay');
            overlay.style.display = 'flex';
            setTimeout(() => {{
                overlay.style.display = 'none';
                enterGame();
            }}, 3500);
        }}, 2500); 
    }}

    function enterGame() {{
        document.getElementById('top-ui').style.display = 'block';
        document.getElementById('minimap').style.display = 'block';
        document.getElementById('hint-log').style.display = 'block';
        canvas.style.display = 'block';
        canvas.focus();
        isGameRunning = true;
        
        recalculateWorldThreat();

        if(gameTimerId) clearInterval(gameTimerId);
        gameTimerId = setInterval(() => {{
            if (!isGameRunning || activeUI) return;
            timeLeft--;
            updateTimerDisplay();
            if (timeLeft <= 0) gameOver();
        }}, 1000);
        loop();
    }}

    function updateTimerDisplay() {{
        let m = Math.floor(timeLeft / 60), s = timeLeft % 60;
        document.getElementById("timer-ui").innerText = String(m).padStart(2,'0') + ":" + String(s).padStart(2,'0');
    }}

    function loop() {{ 
        if (!isGameRunning) return; 
        update(); 
        draw(); 
        updateMinimap(); 
        requestAnimationFrame(loop); 
    }}

    function update() {{
        if (activeUI) return;

        if (keys["ArrowUp"] || keys["KeyW"]) player.y -= player.speed;
        if (keys["ArrowDown"] || keys["KeyS"]) player.y += player.speed;
        if (keys["ArrowLeft"] || keys["KeyA"]) player.x -= player.speed;
        if (keys["ArrowRight"] || keys["KeyD"]) player.x += player.speed;

        if (player.x < 50) player.x = 50; if (player.x > 950) player.x = 950;
        if (player.y < 50) player.y = 50; if (player.y > 950) player.y = 950;

        LOCS.forEach(loc => {{
            if (!auditStates[loc.id].cleared && Math.sqrt((player.x-loc.x)**2 + (player.y-loc.y)**2) < 35) {{ 
                openFacility(loc); 
            }}
        }});

        let clearedCount = Object.values(auditStates).filter(s => s.cleared).length;
        document.getElementById("progress-ui").innerText = clearedCount + " / 3 Sectors Audited";

        collectors.forEach(c => {{
            let dx = player.x - c.x, dy = player.y - c.y; 
            let dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < 0.001) dist = 0.001;
            
            let currentAngle = Math.atan2(dy, dx);
            let angleDiff = Math.abs(currentAngle - c.angle);
            if (angleDiff > Math.PI) angleDiff = Math.PI * 2 - angleDiff;

            let dynamicViewDist = c.viewDist * (currentThreatMultiplier * 0.9);
            let dynamicFOV = Math.min(1.2, c.fov + dynamicFOVBonus);
            let inSight = (dist < dynamicViewDist && angleDiff < dynamicFOV);

            if (inSight) {{
                c.angle = currentAngle;
                let dynamicChaseSpeed = c.baseChaseSpeed * currentThreatMultiplier;
                c.x += (dx / dist) * dynamicChaseSpeed;
                c.y += (dy / dist) * dynamicChaseSpeed;
                if (dist < 26) {{ gameOver(); }}
            }} else {{
                let tdx = c.targetX - c.x, tdy = c.targetY - c.y; 
                let tDist = Math.sqrt(tdx*tdx + tdy*tdy);
                if (tDist < 0.001) tDist = 0.001;
                
                if (tDist < 20) {{ 
                    c.targetX = 100 + Math.random()*800; 
                    c.targetY = 100 + Math.random()*800; 
                }} else {{ 
                    let dynamicPatrolSpeed = c.baseSpeed * currentThreatMultiplier;
                    c.x += (tdx / tDist) * dynamicPatrolSpeed; 
                    c.y += (tdy / tDist) * dynamicPatrolSpeed; 
                    let targetAngle = Math.atan2(tdy, tdx);
                    let delta = normalizeAngle(targetAngle - c.angle);
                    c.angle += delta * 0.04;
                }}
            }}
        }});

        bats.forEach(b => {{
            let textNoiseX = (Math.random() - 0.5) * dynamicSeverityGlitchIntensity * 0.5;
            let textNoiseY = (Math.random() - 0.5) * dynamicSeverityGlitchIntensity * 0.5;
            b.x += (b.vx * currentThreatMultiplier) + textNoiseX; 
            b.y += (b.vy * currentThreatMultiplier) + textNoiseY;
            if (b.x < 50 || b.x > 950) b.vx *= -1;
            if (b.y < 50 || b.y > 950) b.vy *= -1;
        }});
    }}

    function draw() {{
        ctx.clearRect(0, 0, cw, ch); 
        ctx.save(); 

        let glitchOffsetX = 0;
        let glitchOffsetY = 0;
        if (dynamicSeverityGlitchIntensity > 0 && Math.random() < 0.3) {{
            glitchOffsetX = (Math.random() - 0.5) * dynamicSeverityGlitchIntensity;
            glitchOffsetY = (Math.random() - 0.5) * dynamicSeverityGlitchIntensity;
        }}

        ctx.translate(cw/2 - player.x + glitchOffsetX, ch/2 - player.y + glitchOffsetY);
        
        ctx.strokeStyle = "rgba(0, 40, 0, 0.3)"; ctx.lineWidth = 1;
        for(let i=0; i<=1000; i+=100) {{
            ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, 1000); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(1000, i); ctx.stroke();
        }}
        
        ctx.strokeStyle = "rgba(0, 200, 0, 0.4)"; ctx.lineWidth = 2; ctx.strokeRect(40, 40, 920, 920);
        
        LOCS.forEach(loc => {{ 
            ctx.save();
            if (auditStates[loc.id].cleared) ctx.globalAlpha = 0.15;
            ctx.font = "28px Arial"; ctx.fillText(loc.icon, loc.x-14, loc.y+10); 
            ctx.restore();
        }});
        
        collectors.forEach(c => {{
            ctx.save();
            ctx.beginPath(); ctx.moveTo(c.x, c.y);
            let dynamicViewDist = c.viewDist * (currentThreatMultiplier * 0.9);
            let dynamicFOV = Math.min(1.2, c.fov + dynamicFOVBonus); 
            ctx.arc(c.x, c.y, dynamicViewDist, c.angle - dynamicFOV, c.angle + dynamicFOV);
            ctx.closePath();
            ctx.fillStyle = "rgba(0, 255, 0, 0.03)"; ctx.fill();
            ctx.strokeStyle = "rgba(255, 0, 0, 0.25)"; ctx.stroke();
            ctx.font = "26px serif"; ctx.fillText("👤", c.x-14, c.y+10);
            ctx.restore();
        }});

        ctx.font = "14px serif"; ctx.fillStyle = "#383";
        bats.forEach(b => {{ ctx.fillText("🛸", b.x, b.y); }});

        ctx.font = "28px serif"; ctx.fillStyle = "white"; ctx.fillText("🤖", player.x-14, player.y+10); 
        ctx.restore();
        
        ctx.save(); 
        ctx.globalCompositeOperation = 'destination-in';
        
        // 【修正結合】プレイヤーの視界制限ロジックを確定適用
        let playerViewRadius = Math.max(90, 170 - dynamicViewRadiusDebuff);
        
        let grad = ctx.createRadialGradient(cw/2, ch/2, playerViewRadius, cw/2, ch/2, 360); 
        grad.addColorStop(0, 'rgba(0,0,0,1)'); 
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = grad; ctx.fillRect(0,0,cw,ch); 
        ctx.restore();
    }}

    function updateMinimap() {{
        let dot = document.getElementById("player-dot");
        if(dot) {{
            dot.style.left = (player.x / 1000 * 120) + "px";
            dot.style.top = (player.y / 1000 * 120) + "px";
        }}
    }}

    function openFacility(loc) {{
        activeUI = loc.id; 
        keys = {{}}; 
        
        document.getElementById('fac-name').innerText = loc.name; 
        document.getElementById('fac-desc').innerText = loc.desc;
        
        const grid = document.getElementById('audit-grid-container');
        grid.innerHTML = "";

        grid.appendChild(createReportCard(loc.id, "A", loc.reportA));
        grid.appendChild(createReportCard(loc.id, "B", loc.reportB));
        
        document.getElementById("facility-ui").style.display = "flex";
    }}

    function createReportCard(sectorId, label, signalData) {{
        let card = document.createElement("div");
        card.id = "card-" + sectorId + "-" + label;
        card.className = "report-card";
        if (auditStates[sectorId].fakeMarked === label) {{
            card.classList.add("marked-fake");
        }}

        card.innerHTML = `
            <div>
                <div class="card-header">📋 AUDIT INFERENCE LOG [${{label}}] (Suspicion: ${{signalData.suspicion}} / Confidence: ${{signalData.confidence}} / Fallacy Severity: ${{signalData.severity}})</div>
                <div class="card-body">${{signalData.report}}</div>
                <div class="card-contradiction"><b>⚠️ IDENTIFIED LOGICAL DISCREPANCY:</b><br>${{signalData.contradiction}}</div>
            </div>
            <div style="margin-top:15px;">
                <button class="btn ${{auditStates[sectorId].fakeMarked === label ? 'purged-active' : ''}}" 
                        id="btn-${{sectorId}}-${{label}}"
                        onclick="markAsFake('${{sectorId}}', '${{label}}')">
                    ${{auditStates[sectorId].fakeMarked === label ? '🔴 ISOLATION TARGET ACTIVE' : '❌ FLAG THIS INFERENCE AS HALLUCINATION'}}
                </button>
            </div>
        `;
        return card;
    }}

    window.markAsFake = function(sectorId, label) {{
        auditStates[sectorId].fakeMarked = label;
        
        let otherLabel = (label === "A") ? "B" : "A";
        document.getElementById("card-" + sectorId + "-" + label).classList.add("marked-fake");
        document.getElementById("btn-" + sectorId + "-" + label).classList.add("purged-active");
        document.getElementById("btn-" + sectorId + "-" + label).innerText = "🔴 ISOLATION TARGET ACTIVE";

        document.getElementById("card-" + sectorId + "-" + otherLabel).classList.remove("marked-fake");
        document.getElementById("btn-" + sectorId + "-" + otherLabel).classList.remove("purged-active");
        document.getElementById("btn-" + sectorId + "-" + otherLabel).innerText = "❌ FLAG THIS INFERENCE AS HALLUCINATION";
        
        document.getElementById('log-content').innerHTML += "> Telemetry Updated: Isolated sector [" + sectorId + "] candidate [" + label + "]. Recalculating environmental coherence vectors.<br>";
    }}

    function closeUI() {{ 
        let currentSector = activeUI;
        if (auditStates[currentSector].fakeMarked !== null) {{
            auditStates[currentSector].cleared = true;
            document.getElementById('log-content').innerHTML += "<span style='color:gold;'>> Mitigation Success: Isolated anomaly inside [" + currentSector + "] sector node.</span><br>";
        }} else {{
            document.getElementById('log-content').innerHTML += "<span style='color:#aaa;'>> System Warning: Evaluation routine deferred. Structural stability un-neutralized.</span><br>";
        }}

        activeUI = null; 
        keys = {{}}; 
        player.y += 55;

        recalculateWorldThreat();

        document.getElementById("facility-ui").style.display = "none"; 

        window.focus();
        canvas.focus();

        let allCleared = Object.values(auditStates).every(s => s.cleared);
        if (allCleared) {{
            goToBattle();
        }}
    }}

    function gameOver() {{
        isGameRunning = false;
        if(gameTimerId) clearInterval(gameTimerId);
        document.getElementById("gameover-overlay").style.display = "flex";
    }}

    function goToBattle() {{
        activeUI = "battle"; 
        isGameRunning = false;
        if(gameTimerId) {{ clearInterval(gameTimerId); gameTimerId = null; }}
        document.getElementById("top-ui").style.display = "none"; 
        document.getElementById("battle-ui").style.display = "flex";
    }}

    window.executeFinalCheck = function(targetSector) {{
        let isBioCorrect = (auditStates["BIO"].fakeMarked === "B");
        let isMecCorrect = (auditStates["MEC"].fakeMarked === "B");
        let isCybCorrect = (auditStates["CYB"].fakeMarked === "B");

        if (isBioCorrect && isMecCorrect && isCybCorrect) {{
            alert("🏆 [SIMULATION SUCCESSFUL]\\nAll hallucinations (Flawed Deductions B) successfully purged.\\nSpatial coordinate systems stabilized. Secure transit achieved through " + targetSector + " exit corridor.");
        }} else {{
            alert("⚠️ [CRITICAL ARCHITECTURAL EXPLOSION]\\nHallucinated parameters successfully locked into core security logic arrays.\\nLogical contamination triggered complete geometric collapse. Core captured.");
        }}
        location.reload();
    }}
    
    window.addEventListener("keydown", e => {{ 
        if (!activeUI) {{
            keys[e.code] = true;
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space"].indexOf(e.code) > -1) {{
                e.preventDefault();
            }}
        }}
    }});
    window.addEventListener("keyup", e => {{ keys[e.code] = false; }});
    window.addEventListener('resize', () => {{ cw = canvas.width = window.innerWidth; ch = canvas.height = window.innerHeight; }});
</script>

<style>
@keyframes blink {{
    0% {{ opacity: 0.3; }}
    100% {{ opacity: 1.0; }}
}}
</style>
</body>
</html>
"""

components.html(game_html, height=830)
