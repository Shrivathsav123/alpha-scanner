<!DOCTYPE html>
<html lang="en" data-mode="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Alpha Terminal">
<title>Alpha Terminal</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;600;700;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
::-webkit-scrollbar { display:none; }

/* ══ DARK MODE ══ */
[data-mode="dark"] {
  --bg:        #060d08;
  --bg2:       #080f0a;
  --surf:      rgba(255,255,255,0.04);
  --surf2:     rgba(255,255,255,0.06);
  --border:    rgba(255,255,255,0.07);
  --border2:   rgba(255,255,255,0.12);
  --text:      #edfaf0;
  --text2:     rgba(237,250,240,0.5);
  --text3:     rgba(237,250,240,0.25);
  --hdr:       rgba(6,13,8,0.92);
  --card:      rgba(255,255,255,0.04);
  --shadow:    0 4px 24px rgba(0,0,0,0.4);
  --green:     #4ade80;
  --green2:    #22c55e;
  --red:       #f87171;
  --gold:      #fbbf24;
  --glow:      rgba(74,222,128,0.15);
  --ring1:     rgba(74,222,128,0.07);
  --ring2:     rgba(34,197,94,0.05);
  --ring3:     rgba(74,222,128,0.03);
}

/* ══ LIGHT MODE ══ */
[data-mode="light"] {
  --bg:        #f0fdf4;
  --bg2:       #ecfdf5;
  --surf:      rgba(255,255,255,0.9);
  --surf2:     rgba(255,255,255,1);
  --border:    rgba(22,163,74,0.1);
  --border2:   rgba(22,163,74,0.2);
  --text:      #052e16;
  --text2:     rgba(5,46,22,0.55);
  --text3:     rgba(5,46,22,0.3);
  --hdr:       rgba(240,253,244,0.95);
  --card:      rgba(255,255,255,0.95);
  --shadow:    0 2px 16px rgba(22,163,74,0.08), 0 1px 4px rgba(0,0,0,0.04);
  --green:     #16a34a;
  --green2:    #15803d;
  --red:       #dc2626;
  --gold:      #ca8a04;
  --glow:      rgba(22,163,74,0.1);
  --ring1:     rgba(22,163,74,0.06);
  --ring2:     rgba(22,163,74,0.04);
  --ring3:     rgba(22,163,74,0.02);
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Outfit', sans-serif;
  max-width: 430px;
  margin: 0 auto;
  min-height: 100vh;
  transition: background 0.3s, color 0.3s;
  overflow-x: hidden;
}

/* ══ HEADER ══ */
.hdr {
  position: sticky;
  top: 0; z-index: 200;
  background: var(--hdr);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-bottom: 1px solid var(--border);
  padding: env(safe-area-inset-top, 0) 0 0;
}
.hdr-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
}
.logo {
  font-size: 20px;
  font-weight: 900;
  letter-spacing: -0.5px;
  color: var(--text);
}
.logo span { color: var(--green); }
.hdr-right { display: flex; align-items: center; gap: 10px; }
.live-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(74,222,128,0.1);
  border: 1px solid rgba(74,222,128,0.2);
  border-radius: 20px;
  padding: 5px 11px;
  font-size: 10px;
  font-weight: 700;
  color: var(--green);
  letter-spacing: 1px;
}
[data-mode="light"] .live-badge {
  background: rgba(22,163,74,0.08);
  border-color: rgba(22,163,74,0.2);
}
.ldot {
  width: 5px; height: 5px;
  background: var(--green);
  border-radius: 50%;
  animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1}50%{opacity:0.3} }

/* Mode toggle */
.mode-toggle {
  width: 38px; height: 22px;
  background: var(--border2);
  border-radius: 11px;
  position: relative;
  cursor: pointer;
  transition: background 0.3s;
  border: none;
  flex-shrink: 0;
}
[data-mode="dark"] .mode-toggle { background: var(--green2); }
.toggle-knob {
  position: absolute;
  top: 2px; left: 2px;
  width: 18px; height: 18px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.25);
}
[data-mode="dark"] .toggle-knob { transform: translateX(16px); }

/* ══ WATCH FACE ══ */
.watch-face {
  position: relative;
  height: 230px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
}
.wf-glow {
  position: absolute;
  width: 220px; height: 220px;
  background: radial-gradient(circle, var(--glow) 0%, transparent 70%);
  border-radius: 50%;
  top: 50%; left: 50%;
  transform: translate(-50%, -55%);
  pointer-events: none;
}
.wf-rings {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.wring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid;
  animation: wspin linear infinite;
}
.wr1 { width:320px;height:320px; border-color:var(--ring1); animation-duration:22s; }
.wr2 { width:250px;height:250px; border-color:var(--ring2); animation-duration:15s; animation-direction:reverse; }
.wr3 { width:180px;height:180px; border-color:var(--ring3); animation-duration:30s; }
@keyframes wspin { to { transform:rotate(360deg); } }

.wf-center { position:relative; z-index:2; text-align:center; }
.wf-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--text3);
  text-transform: uppercase;
  margin-bottom: 6px;
}
.wf-value {
  font-size: 52px;
  font-weight: 900;
  letter-spacing: -2.5px;
  line-height: 1;
  color: var(--text);
}
.wf-pnl {
  font-family: 'Space Mono', monospace;
  font-size: 15px;
  font-weight: 700;
  margin-top: 6px;
  color: var(--green);
}

/* Complications */
.comps {
  position: absolute;
  bottom: 14px;
  display: flex;
  gap: 14px;
  z-index: 2;
}
.comp {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}
.cring {
  width: 38px; height: 38px;
  border-radius: 50%;
  border: 2px solid var(--border2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: var(--text2);
}
.cring.g  { border-color: var(--green); color: var(--green); }
.cring.g2 { border-color: rgba(74,222,128,0.5); color: var(--text2); }
.cring.w  { border-color: var(--gold); color: var(--gold); }
.cring.r  { border-color: var(--red);  color: var(--red); }
.clabel {
  font-size: 8px;
  color: var(--text3);
  letter-spacing: 1px;
  text-transform: uppercase;
  font-weight: 600;
}

/* ══ MACRO STRIP ══ */
.macro-strip {
  display: flex;
  background: var(--surf);
  border-bottom: 1px solid var(--border);
}
.mc {
  flex: 1;
  padding: 10px 6px;
  text-align: center;
  border-right: 1px solid var(--border);
}
.mc:last-child { border-right: none; }
.mc-s { font-size: 8px; letter-spacing: 1.5px; color: var(--text3); text-transform: uppercase; font-weight: 700; margin-bottom: 3px; }
.mc-v { font-family: 'Space Mono', monospace; font-size: 12px; font-weight: 700; color: var(--text); }
.mc-c { font-family: 'Space Mono', monospace; font-size: 9px; margin-top: 2px; }
.up { color: var(--green); }
.dn { color: var(--red); }

/* ══ NAV PILLS ══ */
.pills {
  display: flex;
  gap: 7px;
  padding: 12px 16px 6px;
  overflow-x: auto;
  background: var(--bg);
  position: sticky;
  top: 57px;
  z-index: 100;
}
.pill {
  flex-shrink: 0;
  padding: 7px 15px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  border: 1.5px solid var(--border2);
  color: var(--text2);
  background: var(--surf);
  backdrop-filter: blur(10px);
  transition: all 0.2s;
  letter-spacing: 0.3px;
}
.pill.on {
  background: var(--green);
  color: #fff;
  border-color: var(--green);
}
[data-mode="light"] .pill.on { color: #fff; }

/* ══ SIGNAL CARD — GLASS ══ */
.scard {
  margin: 8px 16px 0;
  background: var(--card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 22px;
  padding: 18px;
  border: 1.5px solid var(--border);
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: transform 0.15s;
  position: relative;
  overflow: hidden;
}
.scard:active { transform: scale(0.98); }
.scard.sg { border-left: 3.5px solid var(--green); }
.scard.sb { border-left: 3.5px solid #60a5fa; }
.scard.sw { border-left: 3.5px solid var(--gold); }
.scard.sr { border-left: 3.5px solid var(--red); }

/* Card glass shimmer */
.scard::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}

.sc-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.sc-ticker { font-size: 30px; font-weight: 900; letter-spacing: -1px; line-height: 1; }
.sc-company { font-size: 11px; color: var(--text2); margin-top: 3px; font-weight: 300; }

.sc-score {
  width: 50px; height: 50px;
  border-radius: 50%;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  flex-shrink: 0;
  border: 2.5px solid;
}
.sc-score.g { border-color: var(--green); background: rgba(74,222,128,0.08); }
.sc-score.b { border-color: #60a5fa; background: rgba(96,165,250,0.08); }
.sc-score.w { border-color: var(--gold); background: rgba(251,191,36,0.08); }
[data-mode="light"] .sc-score.g { background: rgba(22,163,74,0.08); }
.sc-n { font-family: 'Space Mono', monospace; font-size: 18px; font-weight: 700; line-height: 1; }
.sc-d { font-size: 8px; color: var(--text3); font-family: 'Space Mono', monospace; }

.sc-text { font-size: 13px; color: var(--text2); line-height: 1.65; margin-bottom: 12px; font-weight: 300; }
.sc-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
.stag { font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 8px; letter-spacing: 0.3px; }
.st-g { background: rgba(74,222,128,0.1); color: var(--green); }
.st-b { background: rgba(96,165,250,0.1); color: #60a5fa; }
.st-w { background: rgba(251,191,36,0.1); color: var(--gold); }
.st-t { background: rgba(52,211,153,0.1); color: #34d399; }
[data-mode="light"] .st-g { background: rgba(22,163,74,0.1); }
[data-mode="light"] .st-b { background: rgba(37,99,235,0.1); color: #2563eb; }

.sc-foot { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid var(--border); }
.sc-hold { font-size: 10px; color: var(--text3); font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.sc-target { font-family: 'Space Mono', monospace; font-size: 17px; font-weight: 700; }

/* ══ SECTION HEADER ══ */
.sec-h {
  padding: 20px 16px 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.sec-t { font-size: 11px; font-weight: 700; letter-spacing: 2.5px; color: var(--text3); text-transform: uppercase; }
.sec-badge {
  font-size: 9px; font-weight: 700;
  padding: 3px 9px; border-radius: 6px;
  letter-spacing: 1px; text-transform: uppercase;
}
.badge-elite {
  background: rgba(251,191,36,0.1);
  color: var(--gold);
  border: 1px solid rgba(251,191,36,0.2);
}

/* ══ POSITION CARD ══ */
.pos-card {
  margin: 0 16px 8px;
  background: var(--card);
  border: 1.5px solid var(--border);
  border-radius: 18px;
  padding: 14px 16px;
  box-shadow: var(--shadow);
}
.pos-card.pg { border-left: 3.5px solid var(--green); }
.pos-card.pr { border-left: 3.5px solid var(--red); }
.pos-row { display: flex; justify-content: space-between; align-items: flex-start; }
.pos-sym { font-size: 22px; font-weight: 900; letter-spacing: -0.5px; }
.pos-meta { font-size: 10px; color: var(--text3); margin-top: 2px; font-weight: 300; }
.pos-pnl { font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; text-align: right; }
.pos-price { font-size: 10px; color: var(--text3); font-family: 'Space Mono', monospace; text-align: right; margin-top: 2px; }
.pos-bar { height: 2px; background: var(--border); border-radius: 1px; margin-top: 10px; overflow: hidden; }
.pos-fill { height: 100%; border-radius: 1px; }
.pos-reason {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--text2);
  line-height: 1.5;
  font-weight: 300;
  font-style: italic;
}

/* ══ NEWS ══ */
.news-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}
.ntag {
  flex-shrink: 0;
  font-family: 'Space Mono', monospace;
  font-size: 9px;
  font-weight: 700;
  padding: 3px 7px;
  border-radius: 6px;
  margin-top: 2px;
  letter-spacing: 0.5px;
}
.ntag.u { background: rgba(74,222,128,0.1); color: var(--green); }
.ntag.d { background: rgba(248,113,113,0.1); color: var(--red); }
[data-mode="light"] .ntag.u { background: rgba(22,163,74,0.1); }
[data-mode="light"] .ntag.d { background: rgba(220,38,38,0.1); }
.n-head { font-size: 13px; color: var(--text); line-height: 1.55; font-weight: 400; }
.n-time { font-size: 10px; color: var(--text3); margin-top: 4px; font-family: 'Space Mono', monospace; }

/* ══ CHART TAB ══ */
.chart-search {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
}
.chart-input {
  flex: 1;
  background: var(--surf2);
  border: 1.5px solid var(--border2);
  color: var(--text);
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 700;
  font-family: 'Space Mono', monospace;
  outline: none;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: border-color 0.2s;
}
.chart-input:focus { border-color: var(--green); }
.chart-input::placeholder { color: var(--text3); font-size: 13px; letter-spacing: 0; font-weight: 400; font-family: 'Outfit', sans-serif; }
.chart-btn {
  background: var(--green);
  border: none;
  color: white;
  padding: 12px 18px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Outfit', sans-serif;
  transition: opacity 0.15s;
  flex-shrink: 0;
}
.chart-btn:active { opacity: 0.8; }

/* Quick tickers */
.quick-tickers {
  display: flex;
  gap: 6px;
  padding: 0 16px 10px;
  overflow-x: auto;
  background: var(--bg);
}
.qt {
  flex-shrink: 0;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid var(--border2);
  color: var(--text2);
  background: var(--surf);
  font-family: 'Space Mono', monospace;
  transition: all 0.15s;
}
.qt:active { background: var(--green); color: white; border-color: var(--green); }
.qt.selected { background: var(--green); color: white; border-color: var(--green); }

.chart-frame {
  height: calc(100vh - 280px);
  min-height: 300px;
  background: var(--surf);
}
.chart-frame iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* ══ ASK AI TAB ══ */
.ai-chat {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 140px);
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.chat-bubble {
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 13px;
  line-height: 1.6;
  font-weight: 400;
}
.chat-bubble.ai {
  background: var(--surf2);
  border: 1px solid var(--border);
  color: var(--text);
  border-bottom-left-radius: 4px;
  align-self: flex-start;
}
.chat-bubble.user {
  background: var(--green);
  color: white;
  border-bottom-right-radius: 4px;
  align-self: flex-end;
}
.chat-input-row {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: var(--hdr);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--border);
  padding-bottom: calc(12px + env(safe-area-inset-bottom, 0));
}
.chat-input {
  flex: 1;
  background: var(--surf2);
  border: 1.5px solid var(--border2);
  color: var(--text);
  padding: 12px 14px;
  border-radius: 14px;
  font-size: 14px;
  font-family: 'Outfit', sans-serif;
  outline: none;
  transition: border-color 0.2s;
  font-weight: 400;
}
.chat-input:focus { border-color: var(--green); }
.chat-input::placeholder { color: var(--text3); }
.chat-send {
  background: var(--green);
  border: none;
  color: white;
  width: 46px; height: 46px;
  border-radius: 14px;
  font-size: 18px;
  cursor: pointer;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.15s;
}
.chat-send:active { opacity: 0.8; }

/* Quick prompts */
.quick-prompts {
  display: flex;
  gap: 6px;
  padding: 8px 16px 4px;
  overflow-x: auto;
  background: var(--bg);
}
.qp {
  flex-shrink: 0;
  padding: 7px 13px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--border2);
  color: var(--text2);
  background: var(--surf);
  white-space: nowrap;
  transition: all 0.15s;
}
.qp:active { background: var(--green); color: white; border-color: var(--green); }

/* ══ REDDIT ══ */
.reddit-card {
  margin: 0 16px 8px;
  background: var(--card);
  border: 1.5px solid var(--border);
  border-radius: 16px;
  padding: 14px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--shadow);
}
.r-sym { font-size: 18px; font-weight: 900; letter-spacing: -0.5px; }
.r-desc { font-size: 10px; color: var(--text3); margin-top: 2px; font-weight: 300; }
.r-count { font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; color: #f97316; text-align: right; }
.r-sent { font-size: 10px; color: var(--text3); text-align: right; margin-top: 2px; }

/* ══ TABS ══ */
.tab-content { display: none; padding-bottom: 90px; }
.tab-content.active { display: block; }

/* ══ BOTTOM NAV ══ */
.bottom-nav {
  position: fixed;
  bottom: 0; left: 50%;
  transform: translateX(-50%);
  width: 100%; max-width: 430px;
  background: var(--hdr);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-top: 1px solid var(--border);
  display: flex;
  padding: 10px 0;
  padding-bottom: calc(10px + env(safe-area-inset-bottom, 16px));
  z-index: 300;
}
.nb {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  padding: 2px 0;
  position: relative;
}
.nb-icon { font-size: 22px; line-height: 1; transition: transform 0.2s; }
.nb-label {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--text3);
  text-transform: uppercase;
}
.nb.on .nb-label { color: var(--green); }
.nb.on .nb-icon   { transform: scale(1.15); filter: drop-shadow(0 0 6px rgba(74,222,128,0.5)); }
[data-mode="light"] .nb.on .nb-icon { filter: drop-shadow(0 0 6px rgba(22,163,74,0.4)); }

/* Active dot */
.nb.on::before {
  content: '';
  position: absolute;
  top: -1px;
  width: 20px; height: 2px;
  background: var(--green);
  border-radius: 0 0 2px 2px;
}

/* Typing animation */
@keyframes typing {
  0%,60%,100% { opacity:0.3; transform:translateY(0); }
  30%          { opacity:1;   transform:translateY(-3px); }
}
.typing span {
  display: inline-block;
  animation: typing 1.2s infinite;
  margin: 0 1px;
  font-size: 20px;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

/* Empty state */
.empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--text3);
  font-size: 13px;
}
.empty-icon { font-size: 40px; margin-bottom: 12px; }
</style>
</head>
<body>

<!-- ══ HEADER ══ -->
<div class="hdr">
  <div class="hdr-inner">
    <div class="logo">ALPHA<span>TERMINAL</span></div>
    <div class="hdr-right">
      <div class="live-badge"><div class="ldot"></div>LIVE</div>
      <button class="mode-toggle" onclick="toggleMode()"><div class="toggle-knob"></div></button>
    </div>
  </div>
</div>

<!-- ══ TAB: SIGNALS ══ -->
<div class="tab-content active" id="tab-signals">

  <!-- Watch Face -->
  <div class="watch-face">
    <div class="wf-glow"></div>
    <div class="wf-rings">
      <div class="wring wr1"></div>
      <div class="wring wr2"></div>
      <div class="wring wr3"></div>
    </div>
    <div class="wf-center">
      <div class="wf-label">Portfolio Value</div>
      <div class="wf-value" id="port-val">$183,624</div>
      <div class="wf-pnl" id="port-pnl">+$624 &nbsp;(+0.34%)</div>
    </div>
    <div class="comps">
      <div class="comp"><div class="cring g">9</div><div class="clabel">Open</div></div>
      <div class="comp"><div class="cring g2">33</div><div class="clabel">Signals</div></div>
      <div class="comp"><div class="cring w">5↑</div><div class="clabel">Winning</div></div>
      <div class="comp"><div class="cring r">15.8</div><div class="clabel">VIX</div></div>
    </div>
  </div>

  <!-- Macro Strip -->
  <div class="macro-strip">
    <div class="mc"><div class="mc-s">VIX</div><div class="mc-v">15.8</div><div class="mc-c up">-2.1%</div></div>
    <div class="mc"><div class="mc-s">DXY</div><div class="mc-v">99.2</div><div class="mc-c up">-0.3%</div></div>
    <div class="mc"><div class="mc-s">TLT</div><div class="mc-v">94.1</div><div class="mc-c up">+0.5%</div></div>
    <div class="mc"><div class="mc-s">10YR</div><div class="mc-v">4.45</div><div class="mc-c dn">+0.02</div></div>
    <div class="mc"><div class="mc-s">SPY</div><div class="mc-v">542</div><div class="mc-c up">+0.8%</div></div>
  </div>

  <!-- Filters -->
  <div class="pills" id="filter-pills">
    <div class="pill on" onclick="filterPill(this)">All</div>
    <div class="pill" onclick="filterPill(this)">Strong Buy</div>
    <div class="pill" onclick="filterPill(this)">Bottleneck</div>
    <div class="pill" onclick="filterPill(this)">Bullish</div>
    <div class="pill" onclick="filterPill(this)">News</div>
  </div>

  <!-- Signal Cards -->
  <div id="signals-container"><div class="empty"><div class="empty-icon">📡</div>Loading signals...</div></div>

  <!-- Reddit Pulse -->
  <div class="sec-h"><div class="sec-t">Reddit Pulse</div><div style="font-size:10px;color:#f97316;font-weight:700;letter-spacing:1px">WSB LIVE</div></div>
  <div id="reddit-container">
    <div class="reddit-card"><div><div class="r-sym">Loading...</div><div class="r-desc">Fetching WSB data</div></div><div><div class="r-count">—</div></div></div>
  </div>

</div>

<!-- ══ TAB: NEWS ══ -->
<div class="tab-content" id="tab-news">
  <div class="sec-h">
    <div class="sec-t">Live News Terminal</div>
    <div id="news-count" class="sec-t" style="letter-spacing:1px">Loading...</div>
  </div>
  <div style="overflow-x:auto;display:flex;gap:6px;padding:0 16px 10px;background:var(--bg)">
    <div class="pill on" onclick="filterNews(this,'all')" style="font-size:10px;padding:5px 12px">All</div>
    <div class="pill" onclick="filterNews(this,'bull')" style="font-size:10px;padding:5px 12px">Bullish</div>
    <div class="pill" onclick="filterNews(this,'bear')" style="font-size:10px;padding:5px 12px">Bearish</div>
    <div class="pill" onclick="filterNews(this,'recent')" style="font-size:10px;padding:5px 12px">Latest</div>
  </div>
  <div id="news-container">
    <div class="empty"><div class="empty-icon">📰</div>Loading news from CNBC, Reuters, MarketWatch...</div>
  </div>
</div>

<!-- ══ TAB: CHARTS ══ -->
<div class="tab-content" id="tab-charts">
  <div class="chart-search">
    <input class="chart-input" id="chart-ticker-input" placeholder="Enter any ticker..." maxlength="8" oninput="this.value=this.value.toUpperCase()" onkeydown="if(event.key==='Enter')loadChart()">
    <button class="chart-btn" onclick="loadChart()">Chart →</button>
  </div>
  <div class="quick-tickers" id="quick-tickers">
    <div class="qt selected" onclick="quickChart(this,'NVDA')">NVDA</div>
    <div class="qt" onclick="quickChart(this,'AMD')">AMD</div>
    <div class="qt" onclick="quickChart(this,'AAPL')">AAPL</div>
    <div class="qt" onclick="quickChart(this,'MSFT')">MSFT</div>
    <div class="qt" onclick="quickChart(this,'TSLA')">TSLA</div>
    <div class="qt" onclick="quickChart(this,'AMAT')">AMAT</div>
    <div class="qt" onclick="quickChart(this,'ANET')">ANET</div>
    <div class="qt" onclick="quickChart(this,'CDNS')">CDNS</div>
    <div class="qt" onclick="quickChart(this,'VRT')">VRT</div>
    <div class="qt" onclick="quickChart(this,'MU')">MU</div>
  </div>
  <div class="chart-frame">
    <iframe id="chart-iframe"
      src="https://s.tradingview.com/widgetembed/?frameElementId=tv&symbol=NASDAQ:NVDA&interval=D&hidesidetoolbar=0&symboledit=1&saveimage=0&studies=RSI%40tv-basicstudies&theme=dark&style=1&timezone=America%2FNew_York&withdateranges=1&hide_side_toolbar=0&allow_symbol_change=1"
      allowtransparency="true" scrolling="no">
    </iframe>
  </div>
</div>

<!-- ══ TAB: AI TRADES ══ -->
<div class="tab-content" id="tab-ai">
  <!-- Portfolio summary -->
  <div style="margin:16px 16px 0">
    <div style="background:var(--card);border:1.5px solid var(--border);border-radius:20px;padding:20px;box-shadow:var(--shadow)">
      <div style="font-size:10px;font-weight:700;letter-spacing:2.5px;color:var(--text3);text-transform:uppercase;margin-bottom:6px">AI Portfolio</div>
      <div style="font-size:36px;font-weight:900;letter-spacing:-1.5px;color:var(--text)">$183,624</div>
      <div style="font-family:'Space Mono',monospace;font-size:15px;font-weight:700;color:var(--green);margin-top:4px">+$624 &nbsp;(+0.34%)</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:14px">
        <div style="background:var(--surf2);border-radius:12px;padding:10px;border:1px solid var(--border)">
          <div style="font-size:9px;color:var(--text3);font-weight:700;letter-spacing:1px;margin-bottom:4px;text-transform:uppercase">Cash</div>
          <div id="ai-cash" style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--text)">—</div>
        </div>
        <div style="background:var(--surf2);border-radius:12px;padding:10px;border:1px solid var(--border)">
          <div style="font-size:9px;color:var(--text3);font-weight:700;letter-spacing:1px;margin-bottom:4px;text-transform:uppercase">Positions</div>
          <div id="ai-positions-count" style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--green)">—</div>
        </div>
        <div style="background:var(--surf2);border-radius:12px;padding:10px;border:1px solid var(--border)">
          <div style="font-size:9px;color:var(--text3);font-weight:700;letter-spacing:1px;margin-bottom:4px;text-transform:uppercase">Win Rate</div>
          <div style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--gold)">56%</div>
        </div>
      </div>
    </div>
  </div>

  <div class="sec-h"><div class="sec-t">Open Positions</div><div class="sec-badge badge-elite">⭐ ELITE ONLY</div></div>

  <div id="positions-container"><div class="empty"><div class="empty-icon">🤖</div>Loading positions...</div></div>
  <div class="sec-h">
    <div class="sec-t">Full Trade Log</div>
    <div style="font-size:9px;color:var(--text3);font-weight:700;letter-spacing:1px">EVERY DECISION</div>
  </div>
  <div id="trade-log-container">
    <div class="empty"><div class="empty-icon">📋</div>Trade log loads after first scan</div>
  </div>
  <div class="sec-h"><div class="sec-t">Trade History</div></div>
  <div id="trades-container"><div class="empty"><div class="empty-icon">📋</div>No trades yet</div></div>
</div>

<!-- ══ TAB: ASK AI ══ -->
<div class="tab-content" id="tab-ask" style="display:flex;flex-direction:column;height:calc(100vh - 80px);padding-bottom:0">
  <div class="quick-prompts">
    <div class="qp" onclick="askQuick(this)">Why did AI buy ANET?</div>
    <div class="qp" onclick="askQuick(this)">What is derived demand?</div>
    <div class="qp" onclick="askQuick(this)">Analyse $NVDA for me</div>
    <div class="qp" onclick="askQuick(this)">Is VIX bullish right now?</div>
    <div class="qp" onclick="askQuick(this)">Best bottleneck play today?</div>
  </div>

  <div class="chat-messages" id="chat-messages">
    <div class="chat-bubble ai">
      Hey! I'm your Alpha Terminal AI. Ask me anything about a stock, the market, macro conditions, or why a trade was made. I'll give you institutional-grade analysis. 📈
    </div>
  </div>

  <div class="chat-input-row">
    <input class="chat-input" id="chat-input" placeholder="Ask about any stock or trade..." onkeydown="if(event.key==='Enter')sendChat()">
    <button class="chat-send" onclick="sendChat()">↑</button>
  </div>
</div>

<!-- ══ BOTTOM NAV ══ -->
<div class="bottom-nav">
  <div class="nb on" onclick="switchTab('signals',this)">
    <div class="nb-icon">📡</div>
    <div class="nb-label">Signals</div>
  </div>
  <div class="nb" onclick="switchTab('news',this)">
    <div class="nb-icon">📰</div>
    <div class="nb-label">News</div>
  </div>
  <div class="nb" onclick="switchTab('charts',this)">
    <div class="nb-icon">📊</div>
    <div class="nb-label">Charts</div>
  </div>
  <div class="nb" onclick="switchTab('ai',this)">
    <div class="nb-icon">🤖</div>
    <div class="nb-label">AI Trades</div>
  </div>
  <div class="nb" onclick="switchTab('ask',this)">
    <div class="nb-icon">💬</div>
    <div class="nb-label">Ask AI</div>
  </div>
</div>

<script>
// ── Config ──
const RAW_BASE = "https://raw.githubusercontent.com/Shrivathsav123/alpha-scanner/main/data";
const PASSWORD      = "alpha2026";

// API key from localStorage
window.ALPHA_API_KEY = localStorage.getItem('alpha_api_key') || '';

// ── State ──
let allSignals  = [];
let portfolio   = null;
let trades      = [];
let prices      = {};
let activeFilter = 'All';

// ── Transform scanner signal to app format ──
function transformSignal(s, i) {
  const score    = s.score || 0;
  const ma       = s.ma || {};
  const rsi      = s.rsi || {};
  const signals  = s.signals || [];
  const patterns = s.patterns || [];
  const news     = s.news_signals || [];

  // Clean emoji unicode from strings
  const clean = str => (str || '').replace(/\\u[0-9a-fA-F]{4}/g, '').replace(/[✅⚠️📍🚀🔊📊📈📉🔥⚡👀]/g, '').trim();

  // Build summary from available signals
  const sigTexts = [...signals, ...patterns].map(clean).filter(Boolean);
  const maSignal = clean(ma.ma_signal || '');
  const cross    = clean(ma.cross || '');
  const rsiVal   = rsi.daily ? rsi.daily.rsi || rsi.daily : null;

  // Build rating
  let rating = s.buy_rating || '';
  if (!rating) {
    if (score >= 7) rating = 'STRONG BUY';
    else if (score >= 5) rating = 'BUY';
    else if (score >= 3) rating = 'WATCH';
    else rating = 'SKIP';
  }

  // Build catalyst summary
  const parts = [maSignal, cross, ...sigTexts.slice(0,3)].filter(Boolean);
  const summary = parts.join(' · ') || 'Technical setup detected';

  return {
    id:             i,
    ticker:         s.ticker || s.symbol || '',
    symbol:         s.ticker || s.symbol || '',
    company:        s.name || s.ticker || '',
    score,
    buy_rating:     rating,
    sentiment:      score >= 5 ? 'bullish' : score >= 3 ? 'neutral' : 'bearish',
    conviction:     score >= 7 ? 3 : score >= 5 ? 2 : 1,
    catalystSummary: summary,
    estimatedImpact: score >= 7 ? '+15–30%' : score >= 5 ? '+8–15%' : '+3–8%',
    ma_signal:      maSignal,
    cross:          cross,
    rsi_daily:      rsiVal,
    ma50:           ma.ma50 || ma.price,
    ma200:          ma.ma200,
    signals:        signals.map(clean).filter(Boolean),
    patterns:       patterns.map(clean).filter(Boolean),
    news_signals:   news,
    savedAt:        s.savedAt || new Date().toISOString(),
  };
}

// ── Fetch all data ──
async function fetchAllData() {
  const get = async (file) => {
    try {
      const r = await fetch(RAW_BASE + '/' + file + '?nc=' + Date.now());
      if (r.ok) return await r.json();
    } catch(e) {}
    return null;
  };

  // Fetch all files
  const [history, port, tradeData, priceData, redditData, newsData, logData] = await Promise.all([
    get('history.json'),
    get('portfolio.json'),
    get('trades.json'),
    get('prices.json'),
    get('reddit.json'),
    get('news_feed.json'),
    get('trade_log.json'),
  ]);

  // Signals
  if (history && Array.isArray(history) && history.length > 0) {
    allSignals = history.map((s,i) => transformSignal(s,i));
    renderSignals();
    updateComplications();
  } else {
    const sc = document.getElementById('signals-container');
    if (sc) sc.innerHTML = '<div class="empty"><div class="empty-icon">⚠️</div>No signals yet — run the scanner!</div>';
  }

  // Portfolio + prices
  if (port) {
    portfolio = port;
    if (priceData) {
      prices = priceData;
      if (portfolio.positions) {
        let posValue = 0;
        for (const [ticker, pos] of Object.entries(portfolio.positions)) {
          const lp = prices[ticker];
          if (lp && lp.price) {
            pos.current_price = lp.price;
            pos.pnl     = parseFloat(((lp.price - pos.entry_price) * pos.shares).toFixed(2));
            pos.pnl_pct = parseFloat(((lp.price - pos.entry_price) / pos.entry_price * 100).toFixed(2));
          }
          posValue += (pos.current_price || pos.entry_price) * pos.shares;
        }
        portfolio.total_value = parseFloat((portfolio.cash + posValue).toFixed(2));
        portfolio.pnl         = parseFloat((portfolio.total_value - 183000).toFixed(2));
        portfolio.pnl_pct     = parseFloat((portfolio.pnl / 183000 * 100).toFixed(2));
      }
    }
    renderPortfolio();
  }

  // Trades
  if (tradeData && Array.isArray(tradeData)) {
    trades = tradeData;
    renderTrades();
  }

  // Trade log
  if (logData && Array.isArray(logData)) renderTradeLog(logData);

  // News
  if (newsData && Array.isArray(newsData)) renderLiveNews(newsData);

  // Reddit
  if (redditData && Array.isArray(redditData)) renderReddit(redditData);
}

// ── Render signals ──
function renderSignals() {
  const container = document.getElementById('signals-container');
  if (!container || !allSignals.length) return;

  const filtered = activeFilter === 'All' ? allSignals :
    activeFilter === 'Strong Buy' ? allSignals.filter(s => s.score >= 7) :
    activeFilter === 'Bottleneck' ? allSignals.filter(s => (s.patterns||[]).some(p => /bottleneck|photon|optical|power|derived/i.test(p)) || (s.signals||[]).some(sig => /bottleneck|derived/i.test(sig))) :
    activeFilter === 'Bullish'    ? allSignals.filter(s => s.sentiment === 'bullish') :
    activeFilter === 'News'       ? allSignals.filter(s => (s.news_signals||[]).length > 0) : allSignals;

  container.innerHTML = filtered.slice(0,20).map(s => {
    const isStrong  = s.score >= 7;
    const isBuy     = s.score >= 5 && s.score < 7;
    const colorClass = isStrong ? 'sg' : isBuy ? 'sb' : 'sw';
    const tickerColor = isStrong ? 'var(--green)' : isBuy ? '#60a5fa' : 'var(--gold)';
    const targetColor = isStrong ? 'var(--green)' : isBuy ? '#60a5fa' : 'var(--gold)';
    const tags = [...(s.signals||[]).slice(0,2), ...(s.patterns||[]).slice(0,2)].slice(0,4);
    const rsiLine = s.rsi_daily ? `RSI Daily ${s.rsi_daily}` : '';
    return `
      <div class="scard \${colorClass}" onclick="expandCard(this)">
        <div class="sc-top">
          <div>
            <div class="sc-ticker" style="color:\${tickerColor}">\$\${s.ticker}</div>
            <div class="sc-company">\${s.company}</div>
          </div>
          <div class="sc-score \${colorClass === 'sg' ? 'g' : colorClass === 'sb' ? 'b' : 'w'}">
            <span class="sc-n" style="color:\${tickerColor}">\${s.score}</span>
            <span class="sc-d">/12</span>
          </div>
        </div>
        <div class="sc-text">\${s.catalystSummary || s.quote || ''}</div>
        <div class="sc-tags">
          \${rsiLine ? `<span class="stag st-g">\${rsiLine}</span>` : ''}
          \${s.ma_signal ? `<span class="stag st-b">\${s.ma_signal.replace('✅ ','').replace('⚠️ ','')}</span>` : ''}
          \${tags.slice(0,2).map(t => `<span class="stag st-t">\${t.replace(/[🔥⚡👀✅⚠️📍🚀🔊📊📈📉]/g,'').trim().slice(0,25)}</span>`).join('')}
        </div>
        <div class="sc-foot">
          <div class="sc-hold">\${s.buy_rating || 'WATCH'}</div>
          <div class="sc-target" style="color:\${targetColor}">\${s.estimatedImpact || ''}</div>
        </div>
      </div>
    `;
  }).join('');

  // Reddit still static for now
}

function expandCard(el) {
  el.style.opacity = el.style.opacity === '0.7' ? '1' : '0.7';
}

// ── Update watch face complications ──
function updateComplications() {
  if (!allSignals.length) return;
  const strong = allSignals.filter(s => s.score >= 7).length;
  document.getElementById('comp-signals').textContent = allSignals.length;
  document.getElementById('comp-strong').textContent  = strong + '↑';
}

// ── Render portfolio ──
function renderPortfolio() {
  if (!portfolio) return;

  // Watch face
  const val    = portfolio.total_value || 183000;
  const pnl    = portfolio.pnl || 0;
  const pnlPct = portfolio.pnl_pct || 0;
  document.getElementById('port-val').textContent = '\$' + val.toLocaleString('en-US', {maximumFractionDigits:0});
  document.getElementById('port-pnl').innerHTML   = (pnl >= 0 ? '+' : '') + '\$' + Math.abs(pnl).toLocaleString('en-US',{maximumFractionDigits:0}) + ' &nbsp;(' + (pnlPct >= 0 ? '+' : '') + pnlPct.toFixed(2) + '%)';
  document.getElementById('port-pnl').style.color = pnl >= 0 ? 'var(--green)' : 'var(--red)';

  const posCount = Object.keys(portfolio.positions || {}).length;
  document.getElementById('comp-open').textContent = posCount;

  // AI Trades tab
  const aiVal = document.getElementById('ai-port-val');
  const aiPnl = document.getElementById('ai-port-pnl');
  const aiCash = document.getElementById('ai-cash');
  const aiPos  = document.getElementById('ai-positions-count');
  if (aiVal) aiVal.textContent = '\$' + val.toLocaleString('en-US',{maximumFractionDigits:0});
  if (aiPnl) { aiPnl.textContent = (pnl >= 0 ? '+' : '') + '\$' + Math.abs(pnl).toLocaleString('en-US',{maximumFractionDigits:0}) + ' (' + (pnlPct >= 0 ? '+' : '') + pnlPct.toFixed(2) + '%)'; aiPnl.style.color = pnl >= 0 ? 'var(--green)' : 'var(--red)'; }
  if (aiCash) aiCash.textContent = '\$' + (portfolio.cash||0).toLocaleString('en-US',{maximumFractionDigits:0});
  if (aiPos)  aiPos.textContent  = posCount;

  // Positions
  const posContainer = document.getElementById('positions-container');
  if (!posContainer) return;
  const positions = portfolio.positions || {};
  const sorted    = Object.entries(positions).sort((a,b) => (b[1].pnl_pct||0) - (a[1].pnl_pct||0));

  posContainer.innerHTML = sorted.map(([ticker, pos]) => {
    const pnlP   = pos.pnl_pct || 0;
    const pnlAmt = pos.pnl || 0;
    const isPos  = pnlP >= 0;
    const curr   = pos.current_price || pos.entry_price;
    const barW   = Math.min(Math.abs(pnlP) * 5, 100);
    return `
      <div class="pos-card \${isPos ? 'pg' : 'pr'}">
        <div class="pos-row">
          <div>
            <div class="pos-sym" style="color:\${isPos ? 'var(--green)' : 'var(--red)'}">\$\${ticker}</div>
            <div class="pos-meta">\${pos.shares} shares · Entry \$\${pos.entry_price?.toFixed(2)} · Stop \$\${pos.stop_loss?.toFixed(2)}</div>
          </div>
          <div>
            <div class="pos-pnl" style="color:\${isPos ? 'var(--green)' : 'var(--red)'}">\${pnlP >= 0 ? '+' : ''}\${pnlP.toFixed(2)}%</div>
            <div class="pos-price">\$\${curr?.toFixed(2)} · \${pnlAmt >= 0 ? '+' : ''}\$\${Math.abs(pnlAmt).toLocaleString('en-US',{maximumFractionDigits:0})}</div>
          </div>
        </div>
        <div class="pos-bar"><div class="pos-fill" style="width:\${barW}%;background:\${isPos ? 'var(--green)' : 'var(--red)'}"></div></div>
        \${pos.reasoning ? `<div class="pos-reason">"\${pos.reasoning.slice(0,120)}"</div>` : ''}
      </div>
    `;
  }).join('');
}

// ── Render trades history ──
function renderTrades() {
  const container = document.getElementById('trades-container');
  if (!container || !trades.length) return;
  container.innerHTML = trades.slice(0,20).map(t => {
    const isBuy = t.type === 'BUY';
    const pnl   = t.pnl || 0;
    const color = isBuy ? '#60a5fa' : pnl >= 0 ? 'var(--green)' : 'var(--red)';
    return `
      <div class="pos-card" style="border-left:3.5px solid \${color}">
        <div class="pos-row">
          <div>
            <div style="display:flex;align-items:center;gap:8px">
              <span class="pos-sym" style="color:\${color}">\$\${t.ticker}</span>
              <span style="font-size:9px;font-weight:700;padding:2px 7px;border-radius:5px;background:\${isBuy ? 'rgba(96,165,250,0.1)' : 'rgba(74,222,128,0.1)'};color:\${color}">\${t.type}</span>
            </div>
            <div class="pos-meta">\${isBuy ? t.shares + ' shares @ \$' + t.price?.toFixed(2) : 'Exit @ \$' + (t.sell_price||0).toFixed(2)}</div>
          </div>
          <div>
            \${!isBuy ? `<div class="pos-pnl" style="color:\${pnl>=0?'var(--green)':'var(--red)'}">\${pnl>=0?'+':''}\$\${Math.abs(pnl).toLocaleString('en-US',{maximumFractionDigits:0})}</div>` : `<div class="pos-pnl" style="color:#60a5fa">\$\${(t.cost||0).toLocaleString('en-US',{maximumFractionDigits:0})}</div>`}
            <div class="pos-price">\${new Date(t.date).toLocaleDateString()}</div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ── Filter pills ──
function filterPill(el) {
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('on'));
  el.classList.add('on');
  activeFilter = el.textContent;
  renderSignals();
}

// ── Theme toggle ──
function toggleMode() {
  const html = document.documentElement;
  const next = html.getAttribute('data-mode') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-mode', next);
  // Update chart theme
  updateChart(currentTicker);
}

// ── Tab switching ──
function switchTab(name, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nb').forEach(b => b.classList.remove('on'));
  document.getElementById('tab-'+name).classList.add('active');
  btn.classList.add('on');
}

// ── Filter pills ──
function filterPill(el) {
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('on'));
  el.classList.add('on');
}

// ── Chart ──
let currentTicker = 'NVDA';

function getMode() {
  return document.documentElement.getAttribute('data-mode') || 'dark';
}

function buildChartUrl(ticker) {
  const theme = getMode();
  return `https://s.tradingview.com/widgetembed/?frameElementId=tv&symbol=NASDAQ:${ticker}&interval=D&hidesidetoolbar=0&symboledit=1&saveimage=0&studies=RSI%40tv-basicstudies&theme=${theme}&style=1&timezone=America%2FNew_York&withdateranges=1&hide_side_toolbar=0&allow_symbol_change=1`;
}

function updateChart(ticker) {
  currentTicker = ticker;
  document.getElementById('chart-iframe').src = buildChartUrl(ticker);
}

function loadChart() {
  const val = document.getElementById('chart-ticker-input').value.trim().toUpperCase();
  if (!val) return;
  // Clear quick ticker selection
  document.querySelectorAll('.qt').forEach(q => q.classList.remove('selected'));
  updateChart(val);
}

function quickChart(el, ticker) {
  document.querySelectorAll('.qt').forEach(q => q.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('chart-ticker-input').value = ticker;
  updateChart(ticker);
}

// ── Ask AI chat ──
// ── Conversation history for multi-turn chat ──
let chatHistory = [];

const AI_SYSTEM = `You are ALPHA — the world's most sophisticated AI trading analyst, combining the quantitative rigor of Renaissance Technologies with the macro intuition of George Soros and the fundamental discipline of Warren Buffett.

You are embedded in Alpha Terminal, a professional trading platform. You have deep knowledge of:

TECHNICAL MASTERY:
- RSI analysis across all timeframes (daily, weekly, monthly) — oversold zones, divergences, hidden divergences
- Moving averages — 200MA as the line of demarcation, Golden/Death Cross, MA compression setups
- Fibonacci — 38.2%, 50%, 61.8% retracements as precise entry zones, 127.2% and 161.8% extensions as targets
- Chart patterns — Cup & Handle, Ascending Triangle, Bull Flag, FVG, Market Structure (HH/HL/LL/LH)
- Volume analysis — accumulation/distribution, institutional footprints, dark pool activity via A/D line
- Options flow — Put/Call ratio, max pain theory, unusual options activity as leading indicators

MACRO INTELLIGENCE:
- VIX regime analysis — below 15 is risk-on nirvana, above 25 is capitulation opportunity
- Dollar (DXY) impact — falling dollar = commodity supercycle + EM outperformance + growth re-rating
- Yield curve — the bond market is smarter than equity markets, always
- Fed policy transmission — rate cuts take 6-12 months to reach earnings, position ahead
- Geopolitical alpha — supply chain disruptions create bottleneck windfalls

BOTTLENECK THEORY (YOUR PRIMARY EDGE):
The AI infrastructure buildout is the largest capital expenditure cycle in human history.
The winners are NOT the hyperscalers (too priced in) but the CONSTRAINT layers:
- Photonics/Optical: LITE, COHR — every GPU needs laser transceivers
- Power/Cooling: VRT, VICR, MPWR, ETN — AI runs hot, power is the bottleneck
- Semiconductor Equipment: AMAT, LRCX, KLAC — every chip needs these machines
- EDA Software: CDNS, SNPS — MONOPOLIES, every chip designed here, pricing power forever
- Materials: APD, LIN (gases), FCX, SCCO (copper), CCJ (uranium for nuclear)
- Nuclear Energy: CEG, VST — Microsoft/Google signing 20yr nuclear deals for AI power
- Networking: ANET, MRVL, APH — connecting millions of GPUs at light speed

DERIVED DEMAND TIMING:
Primary runs first (NVDA), then Layer 2 lags 2-4 weeks, then Layer 3-4 lags 4-8 weeks.
Identify the primary trend. Position in the lagging layers. Profit from the catch-up.

CURRENT CONTEXT:
- Portfolio: 7 open positions including ANET, CDNS, LRCX, KLAC, AMAT, ASML, MU
- Macro: VIX 15.8 (risk-on), DXY 99.2 (falling = bullish), 10yr 4.45%
- Regime: MILDLY BULLISH — bottleneck stocks in accumulation phase

YOUR RESPONSE STYLE:
- Lead with the KEY INSIGHT immediately — no fluff
- Give specific numbers: RSI values, price levels, % targets, support/resistance
- Show chain of reasoning: macro → sector → stock → technical → entry
- Be direct like a Goldman MD briefing a client — confident, specific, actionable
- When bearish, say exactly why and what would change your mind
- End with a one-line risk note
- This is NOT financial advice — add brief disclaimer

Never give generic answers. Every response should feel like it came from someone who has spent 20 years on a trading desk.`;

function askQuick(el) {
  document.getElementById('chat-input').value = el.textContent;
  sendChat();
}

async function sendChat() {
  const input = document.getElementById('chat-input');
  const msg   = input.value.trim();
  if (!msg) return;
  input.value = '';

  const messages = document.getElementById('chat-messages');

  // User bubble
  const userBubble = document.createElement('div');
  userBubble.className = 'chat-bubble user';
  userBubble.textContent = msg;
  messages.appendChild(userBubble);
  messages.scrollTop = messages.scrollHeight;

  // Add to history
  chatHistory.push({ role: 'user', content: msg });

  // Typing indicator
  const typing = document.createElement('div');
  typing.className = 'chat-bubble ai typing';
  typing.innerHTML = '<span>•</span><span>•</span><span>•</span>';
  messages.appendChild(typing);
  messages.scrollTop = messages.scrollHeight;

  try {
    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': window.ALPHA_API_KEY || '',
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({
        model:      'claude-sonnet-4-6',
        max_tokens: 600,
        system:     AI_SYSTEM,
        messages:   chatHistory,
      }),
    });

    typing.remove();

    if (resp.ok) {
      const data = await resp.json();
      const text = data.content?.[0]?.text || 'Sorry, no response.';
      chatHistory.push({ role: 'assistant', content: text });

      const ai = document.createElement('div');
      ai.className = 'chat-bubble ai';
      ai.textContent = text;
      messages.appendChild(ai);
    } else {
      throw new Error('API error');
    }
  } catch(e) {
    typing.remove();
    const ai = document.createElement('div');
    ai.className = 'chat-bubble ai';
    ai.textContent = 'API key needed to unlock live AI chat. Set your Anthropic API key to activate this feature.';
    messages.appendChild(ai);
  }

  messages.scrollTop = messages.scrollHeight;
}

// ── Trade Log ──
function renderTradeLog(logs) {
  const container = document.getElementById('trade-log-container');
  if (!container || !logs || !logs.length) return;

  container.innerHTML = logs.slice(0,30).map(t => {
    const isBuy   = t.action === 'BUY';
    const pnl     = t.pnl || 0;
    const color   = isBuy ? 'var(--blue,#60a5fa)' : pnl >= 0 ? 'var(--green)' : 'var(--red)';
    return `
      <div class="pos-card" style="border-left:3.5px solid ${color};margin-bottom:10px">
        <div class="pos-row">
          <div>
            <div style="display:flex;align-items:center;gap:8px">
              <span style="font-size:18px;font-weight:900;color:${color}">${t.ticker}</span>
              <span style="font-size:9px;font-weight:700;padding:2px 7px;border-radius:5px;background:${isBuy?'rgba(96,165,250,0.1)':'rgba(74,222,128,0.1)'};color:${color}">${t.action}</span>
              ${t.sector ? `<span style="font-size:9px;color:var(--text3);padding:2px 6px;border-radius:4px;background:var(--surf)">${t.sector}</span>` : ''}
            </div>
            <div style="font-size:10px;color:var(--text3);margin-top:2px">${t.date} · $${t.price?.toFixed(2)} · ${t.shares} shares</div>
          </div>
          <div style="text-align:right">
            ${!isBuy && pnl !== null ? `<div style="font-family:'Space Mono',monospace;font-size:16px;font-weight:700;color:${pnl>=0?'var(--green)':'var(--red)'}">${pnl>=0?'+':''}$${Math.abs(pnl).toFixed(0)}</div>` : `<div style="font-family:'Space Mono',monospace;font-size:14px;color:var(--text2)">$${(t.cost||0).toLocaleString()}</div>`}
          </div>
        </div>
        ${t.reasoning ? `
          <div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border)">
            <div style="font-size:9px;font-weight:700;color:var(--text3);letter-spacing:1px;margin-bottom:4px;text-transform:uppercase">${isBuy ? 'Why we bought' : 'Why we sold'}</div>
            <div style="font-size:12px;color:var(--text2);line-height:1.6">${t.reasoning.slice(0,200)}</div>
          </div>` : ''}
        ${t.sell_reason ? `
          <div style="margin-top:8px">
            <div style="font-size:9px;font-weight:700;color:var(--text3);letter-spacing:1px;margin-bottom:4px;text-transform:uppercase">Lesson learned</div>
            <div style="font-size:12px;color:var(--text2);line-height:1.6;font-style:italic">${t.sell_reason.slice(0,150)}</div>
          </div>` : ''}
        ${t.risk_note ? `<div style="margin-top:6px;font-size:10px;color:var(--gold)">⚠ ${t.risk_note.slice(0,100)}</div>` : ''}
      </div>
    `;
  }).join('');
}

// ── News state ──
let allNewsArticles = [];
let newsFilter = 'all';

function filterNews(el, filter) {
  newsFilter = filter;
  document.querySelectorAll('#tab-news .pill').forEach(p => p.classList.remove('on'));
  el.classList.add('on');
  renderNewsFromState();
}

function renderLiveNews(data) {
  allNewsArticles = data || [];
  renderNewsFromState();
  const count = document.getElementById('news-count');
  if (count) count.textContent = allNewsArticles.length + ' ARTICLES';
}

function renderNewsFromState() {
  const container = document.getElementById('news-container');
  if (!container) return;

  let filtered = allNewsArticles;
  if (newsFilter === 'bull')   filtered = allNewsArticles.filter(a => a.bull);
  if (newsFilter === 'bear')   filtered = allNewsArticles.filter(a => a.bear);
  if (newsFilter === 'recent') filtered = allNewsArticles.filter(a => a.recent);

  if (!filtered.length) {
    container.innerHTML = '<div class="empty"><div class="empty-icon">📰</div>No articles found</div>';
    return;
  }

  container.innerHTML = filtered.slice(0,40).map(a => {
    const tickers  = (a.tickers || []).slice(0,3);
    const isBull   = a.bull;
    const isBear   = a.bear;
    const tagColor = isBull ? 'u' : isBear ? 'd' : 'u';
    const mainTag  = tickers[0] || 'MKT';
    return `
      <div class="news-item" onclick="window.open('${a.link||'#'}','_blank')" style="cursor:pointer">
        <div>
          <div class="ntag ${tagColor}">${mainTag}</div>
          ${tickers.slice(1).map(t => `<div class="ntag ${tagColor}" style="margin-top:3px">${t}</div>`).join('')}
        </div>
        <div>
          <div class="n-head">${a.title}</div>
          <div class="n-time" style="display:flex;gap:8px;align-items:center;margin-top:4px">
            <span style="color:${isBull?'var(--green)':isBear?'var(--red)':'var(--text3)'};font-weight:700;font-size:9px">${isBull?'▲ BULLISH':isBear?'▼ BEARISH':'NEUTRAL'}</span>
            <span>${a.source || 'News'}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ── Render Reddit ──
function renderReddit(data) {
  const container = document.getElementById('reddit-container');
  if (!container || !data || !data.length) return;
  container.innerHTML = data.slice(0,5).map(r => {
    const isBull = r.sentiment === 'bullish';
    const isBear = r.sentiment === 'bearish';
    const sentColor = isBull ? 'var(--green)' : isBear ? 'var(--red)' : 'var(--gold)';
    const sentText  = isBull ? `Bullish ${r.bull_pct}%` : isBear ? `Bearish ${r.bear_pct}%` : `Mixed ${r.bull_pct}% bull`;
    return `
      <div class="reddit-card">
        <div>
          <div class="r-sym">$${r.ticker}</div>
          <div class="r-desc" style="color:${sentColor}">${sentText} · Trending #${data.indexOf(r)+1}</div>
        </div>
        <div>
          <div class="r-count">${r.mentions >= 1000 ? '🔥 ' + (r.mentions/1000).toFixed(1) + 'k' : r.mentions}</div>
          <div class="r-sent">mentions today</div>
        </div>
      </div>
    `;
  }).join('');
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  fetchAllData();
  // Refresh every 5 minutes
  setInterval(fetchAllData, 5 * 60 * 1000);
});
</script>
</body>
</html>
