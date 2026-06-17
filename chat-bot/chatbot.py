import os
from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

load_dotenv()

st.set_page_config(page_title="Gemini", page_icon="✦", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #0b0f1a !important; }
section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ height: 100%; background: #0b0f1a; font-family: 'Inter', sans-serif; overflow: hidden; }}

.app {{
  display: flex; flex-direction: column;
  height: 100vh; max-width: 760px;
  margin: 0 auto; background: #0b0f1a;
}}

.topbar {{
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(255,255,255,0.07);
  padding: 14px 22px;
  display: flex; align-items: center; gap: 13px;
  flex-shrink: 0;
}}
.logo {{
  width: 40px; height: 40px; border-radius: 11px;
  background: linear-gradient(135deg,#1a3a2a,#0d4d35);
  border: 1px solid rgba(16,185,129,0.3);
  display: flex; align-items:center; justify-content:center;
  font-size: 16px; font-weight: 700; color: #34d399;
}}
.t-name {{ font-size: 15px; font-weight: 600; color: #f1f5f9; }}
.t-status {{ display:flex; align-items:center; gap:5px; margin-top:2px; }}
.pulse {{ width:6px; height:6px; border-radius:50%; background:#10b981; animation:pulse 2s infinite; }}
@keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.45}} }}
.t-stxt {{ font-size:11px; color:#4ade80; }}
.clr {{
  margin-left:auto; background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.08); color:#6b7280;
  font-size:12px; padding:6px 13px; border-radius:8px;
  cursor:pointer; font-family:inherit; transition:all .15s;
}}
.clr:hover {{ background:rgba(255,255,255,0.08); color:#9ca3af; }}

.msgs {{
  flex:1; overflow-y:auto; padding:22px 18px;
  display:flex; flex-direction:column; gap:14px;
  scrollbar-width:thin; scrollbar-color:rgba(255,255,255,0.06) transparent;
}}

.empty {{
  display:flex; flex-direction:column; align-items:center;
  justify-content:center; height:100%; gap:10px; opacity:0.25;
}}
.empty-icon {{ font-size:32px; }}
.empty-txt {{ font-size:13px; color:#fff; letter-spacing:.03em; }}

.row {{ display:flex; gap:10px; max-width:80%; animation:popIn .2s ease; }}
.row.u {{ align-self:flex-end; flex-direction:row-reverse; }}
.row.b {{ align-self:flex-start; }}
@keyframes popIn {{ from{{opacity:0;transform:translateY(6px)}} to{{opacity:1;transform:translateY(0)}} }}

.av {{
  width:29px; height:29px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:11px; font-weight:700; flex-shrink:0; margin-top:2px;
}}
.av.u {{ background:rgba(99,102,241,.15); color:#818cf8; border:1px solid rgba(99,102,241,.25); }}
.av.b {{ background:rgba(16,185,129,.12); color:#34d399; border:1px solid rgba(16,185,129,.22); }}

.bbl {{
  padding:10px 14px; font-size:13.5px; line-height:1.65;
  border-radius:16px; white-space:pre-wrap; word-break:break-word;
}}
.bbl.u {{
  background:rgba(99,102,241,.1); border:1px solid rgba(99,102,241,.2);
  border-radius:16px 4px 16px 16px; color:#c7d2fe;
}}
.bbl.b {{
  background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
  border-radius:4px 16px 16px 16px; color:#cbd5e1;
}}
.meta {{ font-size:10.5px; color:rgba(255,255,255,.18); margin-top:4px; }}
.row.u .meta {{ text-align:right; }}

.typing {{ display:flex; align-items:center; gap:4px; padding:13px 15px; }}
.d {{ width:5px; height:5px; border-radius:50%; background:rgba(255,255,255,.3); animation:bounce 1.2s infinite; }}
.d:nth-child(2){{animation-delay:.2s}} .d:nth-child(3){{animation-delay:.4s}}
@keyframes bounce {{ 0%,60%,100%{{transform:translateY(0)}} 30%{{transform:translateY(-5px)}} }}

.inputbar {{
  padding:12px 16px; border-top:1px solid rgba(255,255,255,.06);
  background:rgba(255,255,255,.02);
  display:flex; gap:10px; align-items:flex-end; flex-shrink:0;
}}
.inputbar textarea {{
  flex:1; background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.09); border-radius:13px;
  color:#e2e8f0; font-family:inherit; font-size:13.5px;
  line-height:1.5; padding:10px 14px; resize:none; outline:none;
  max-height:100px; overflow-y:auto;
  transition:border-color .2s, box-shadow .2s;
}}
.inputbar textarea::placeholder {{ color:rgba(255,255,255,.2); }}
.inputbar textarea:focus {{
  border-color:rgba(99,102,241,.45);
  box-shadow:0 0 0 3px rgba(99,102,241,.08);
  background:rgba(255,255,255,.07);
}}
.send {{
  width:38px; height:38px; border-radius:50%;
  background:rgba(99,102,241,.85); border:none;
  display:flex; align-items:center; justify-content:center;
  cursor:pointer; flex-shrink:0; transition:all .15s;
}}
.send:hover {{ background:rgba(99,102,241,1); transform:scale(1.06); }}
.send:active {{ transform:scale(0.94); }}
.send:disabled {{ opacity:0.4; cursor:not-allowed; transform:none; }}
.send svg {{ width:15px; height:15px; }}
</style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="logo">G</div>
    <div>
      <div class="t-name">Gemini</div>
      <div class="t-status"><div class="pulse"></div><span class="t-stxt">online</span></div>
    </div>
    <button class="clr" onclick="clearChat()">clear chat</button>
  </div>

  <div class="msgs" id="msgs"></div>

  <div class="inputbar">
    <textarea id="inp" rows="1" placeholder="Ask anything..." 
      onkeydown="onKey(event)" oninput="rsz(this)"></textarea>
    <button class="send" onclick="submitMsg()" id="sb">
      <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2"
        stroke-linecap="round" stroke-linejoin="round">
        <line x1="22" y1="2" x2="11" y2="13"/>
        <polygon points="22 2 15 22 11 13 2 9 22 2"/>
      </svg>
    </button>
  </div>
</div>

<script>
const GROQ_API_KEY = "{GROQ_API_KEY}";
const MODEL = "llama-3.3-70b-versatile";

// Saari history JS mein rehti hai — koi reload nahi
let history = [];
let loading = false;

function ftime() {{
  return new Date().toLocaleTimeString([], {{hour:'2-digit', minute:'2-digit'}});
}}

function rsz(el) {{
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 100) + 'px';
}}

function onKey(e) {{
  if (e.key === 'Enter' && !e.shiftKey) {{
    e.preventDefault();
    submitMsg();
  }}
}}

function escHtml(t) {{
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

function renderAll() {{
  const c = document.getElementById('msgs');
  
  // Typing row bachao agar ho
  const typingRow = document.getElementById('typing-row');
  
  c.innerHTML = '';

  if (history.length === 0) {{
    c.innerHTML = '<div class="empty"><div class="empty-icon">✦</div><div class="empty-txt">start a conversation</div></div>';
    if (typingRow) c.appendChild(typingRow);
    return;
  }}

  history.forEach(m => {{
    const isUser = m.role === 'user';
    const row = document.createElement('div');
    row.className = 'row ' + (isUser ? 'u' : 'b');
    row.innerHTML = `
      <div class="av ${{isUser?'u':'b'}}">${{isUser?'U':'G'}}</div>
      <div>
        <div class="bbl ${{isUser?'u':'b'}}">${{escHtml(m.text)}}</div>
        <div class="meta">${{m.time||''}}</div>
      </div>`;
    c.appendChild(row);
  }});

  // Typing indicator wapas lagao
  if (typingRow) c.appendChild(typingRow);

  c.scrollTop = c.scrollHeight;
}}

function showTyping() {{
  const c = document.getElementById('msgs');
  const row = document.createElement('div');
  row.className = 'row b';
  row.id = 'typing-row';
  row.innerHTML = '<div class="av b">G</div><div class="bbl b typing"><div class="d"></div><div class="d"></div><div class="d"></div></div>';
  c.appendChild(row);
  c.scrollTop = c.scrollHeight;
}}

function removeTyping() {{
  const t = document.getElementById('typing-row');
  if (t) t.remove();
}}

function setLoading(val) {{
  loading = val;
  document.getElementById('sb').disabled = val;
  document.getElementById('inp').disabled = val;
}}

function clearChat() {{
  if (loading) return;
  history = [];
  renderAll();
}}

async function submitMsg() {{
  const inp = document.getElementById('inp');
  const txt = inp.value.trim();
  if (!txt || loading) return;

  // User message add karo
  history.push({{ role: 'user', text: txt, time: ftime() }});
  inp.value = '';
  inp.style.height = 'auto';
  renderAll();
  showTyping();
  setLoading(true);

  // Groq ke liye messages format karo
  const messages = history.map(m => ({{
    role: m.role === 'user' ? 'user' : 'assistant',
    content: m.text
  }}));

  try {{
    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {{
      method: 'POST',
      headers: {{
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${{GROQ_API_KEY}}`
      }},
      body: JSON.stringify({{
        model: MODEL,
        messages: messages,
        max_tokens: 1024
      }})
    }});

    if (!res.ok) {{
      const err = await res.json();
      throw new Error(err.error?.message || 'API error');
    }}

    const data = await res.json();
    const reply = data.choices[0].message.content;

    removeTyping();
    history.push({{ role: 'bot', text: reply, time: ftime() }});
    renderAll();

  }} catch (err) {{
    removeTyping();
    history.push({{ role: 'bot', text: '⚠️ Error: ' + err.message, time: ftime() }});
    renderAll();
  }} finally {{
    setLoading(false);
  }}
}}

// Initial render
renderAll();
</script>
</body>
</html>
"""

components.html(html_code, height=700, scrolling=False)