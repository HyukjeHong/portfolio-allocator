import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Portfolio Allocator", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

header[data-testid="stHeader"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

.stApp { background-color: #0d0d0d !important; }
.block-container { padding: 3rem 3.5rem 2rem 3.5rem !important; max-width: 1500px !important; }

html, body, [class*="css"], p, span, div, label {
    color: #EAEAEA !important;
    font-family: 'DM Sans', sans-serif !important;
}
h1, h2, h3 { font-family: 'DM Mono', monospace !important; color: #EAEAEA !important; }

div[data-testid="stNumberInput"] input,
div[data-baseweb="input"],
div[data-baseweb="base-input"],
input[type="number"] {
    background-color: #1a1a1a !important;
    background: #1a1a1a !important;
    color: #EAEAEA !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
    -webkit-text-fill-color: #EAEAEA !important;
}
div[data-testid="stNumberInput"] input:focus,
input[type="number"]:focus {
    border: 1px solid #1E88E5 !important;
    box-shadow: 0 0 0 3px rgba(30,136,229,0.12) !important;
    outline: none !important;
}
div[data-testid="stNumberInput"] label {
    color: rgba(234,234,234,0.35) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.5px !important;
}
div[data-testid="stNumberInput"] button {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    color: #EAEAEA !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #161616 !important;
    border: 1px solid #252525 !important;
    border-radius: 12px !important;
    padding: 4px !important; gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 9px !important;
    color: rgba(234,234,234,0.25) !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: #1E88E5 !important;
    color: #fff !important;
    border: none !important;
}

div[data-testid="metric-container"] {
    background: #141414 !important;
    border: 1px solid #222 !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
}
div[data-testid="metric-container"] label {
    color: rgba(234,234,234,0.3) !important;
    font-size: 0.68rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #EAEAEA !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.55rem !important;
    font-weight: 400 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] svg { display: none; }

div[data-testid="stDataFrame"] {
    border: 1px solid #222 !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

hr { border: none !important; border-top: 1px solid #1e1e1e !important; margin: 28px 0 !important; }

.cat-wrap {
    border-radius: 16px;
    padding: 20px 24px 20px 24px;
    margin-bottom: 14px;
    border: 1px solid;
    position: relative;
}
.cat-equity  { background: rgba(30,136,229,0.04);  border-color: rgba(30,136,229,0.18) !important; }
.cat-fixed   { background: rgba(34,197,94,0.04);   border-color: rgba(34,197,94,0.18) !important; }
.cat-alt     { background: rgba(249,115,22,0.04);  border-color: rgba(249,115,22,0.18) !important; }
.cat-cash    { background: rgba(168,85,247,0.04);  border-color: rgba(168,85,247,0.18) !important; }

.cat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.cat-title-ko {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 1px;
}
.cat-title-en {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    color: rgba(234,234,234,0.25) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-left: 10px;
}
.cat-subtotal {
    font-family: 'DM Mono', monospace;
    font-size: 1.15rem;
    font-weight: 400;
}
.cat-amt {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: rgba(234,234,234,0.22) !important;
    margin-left: 10px;
}

.total-pill {
    display: inline-flex;
    align-items: center;
    gap: 18px;
    background: #141414;
    border: 1px solid #222;
    border-radius: 50px;
    padding: 10px 24px;
    margin: 12px 0 20px 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
}
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: rgba(234,234,234,0.2);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 28px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 14px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: #1e1e1e; }

.action-card-buy {
    background: linear-gradient(135deg, rgba(74,222,128,0.05) 0%, transparent 100%);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 12px; padding: 15px 18px; margin: 7px 0;
}
.action-card-sell {
    background: linear-gradient(135deg, rgba(248,113,113,0.05) 0%, transparent 100%);
    border: 1px solid rgba(248,113,113,0.15);
    border-radius: 12px; padding: 15px 18px; margin: 7px 0;
}
.action-name { font-size: 0.86rem; font-weight: 500; color: #EAEAEA; margin-bottom: 5px; }
.action-amt  { font-family: 'DM Mono', monospace; font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)

# ── 최종 자산 분류 체계 ───────────────────────────────────────────────
카테고리 = {
    "주식": {
        "label": "Equities",
        "color": "#1E88E5",
        "css": "cat-equity",
        "items": [
            ("미국 대형주",  "S&P500"),
            ("미국 성장주",  "NASDAQ"),
            ("미국 개별주",  "Individual Stocks"),
            ("선진국",       "유럽·일본"),
            ("한국 주식",    "KOSPI/KOSDAQ"),
            ("이머징마켓",   "EM"),
        ]
    },
    "채권": {
        "label": "Fixed Income",
        "color": "#22c55e",
        "css": "cat-fixed",
        "items": [
            ("미국 장기채",      "TLT"),
            ("국내 장기채",      "10년+"),
            ("투자등급 회사채",  "IG"),
            ("하이일드 회사채",  "HY"),
            ("이머징 채권",      "EM Bond"),
            ("JBBB",             "CLO BBB"),
        ]
    },
    "대체투자": {
        "label": "Alternatives",
        "color": "#f97316",
        "css": "cat-alt",
        "items": [
            ("리츠",       "REITs"),
            ("금",         "Gold"),
            ("은",         "Silver"),
            ("원자재 지수","DJP"),
            ("농산물",     "Agriculture"),
            ("비트코인",   "BTC"),
        ]
    },
    "현금성 자산": {
        "label": "Cash & Equivalents",
        "color": "#a855f7",
        "css": "cat-cash",
        "items": [
            ("현금/MMF",   "Cash"),
            ("미국 단기채","T-Bill"),
            ("국내 단기채","1~3년"),
            ("JPST",       "초단기 우량채"),
            ("JAAA",       "CLO AAA"),
        ]
    },
}

통화목록 = [
    ("원화","KRW","🇰🇷"), ("달러","USD","🇺🇸"), ("유로","EUR","🇪🇺"),
    ("엔화","JPY","🇯🇵"), ("기타","ETC","🌐"),
]

for k in ["현재자산","목표자산","현재통화","목표통화"]:
    if k not in st.session_state:
        st.session_state[k] = {}

def 금액(p): return round(total * p / 100) if 'total' in dir() else 0

# ── 헤더 ──────────────────────────────────────────────────────────────
col_t, col_inp = st.columns([3, 1])
with col_t:
    st.markdown('''
    <div style="padding:8px 0 28px 0;border-bottom:1px solid #1e1e1e;margin-bottom:28px;">
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:#1E88E5;letter-spacing:4px;text-transform:uppercase;margin-bottom:12px;">
            ● LIVE &nbsp;&nbsp; PORTFOLIO MANAGEMENT SYSTEM
        </div>
        <div style="font-family:'DM Mono',monospace;font-size:2.8rem;font-weight:300;color:#EAEAEA;letter-spacing:-2px;line-height:0.9;">
            PORTFOLIO<br><span style="color:#1E88E5;">ALLOCATOR</span>
        </div>
        <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:rgba(234,234,234,0.2);letter-spacing:3px;text-transform:uppercase;margin-top:14px;">
            현재 비중 &nbsp;/&nbsp; 목표 비중 &nbsp;/&nbsp; 리밸런싱 계산
        </div>
    </div>
    ''', unsafe_allow_html=True)
with col_inp:
    st.markdown("<br><br>", unsafe_allow_html=True)
    total = st.number_input("총 투자금액 (원)", min_value=100000, value=100000000, step=1000000, format="%d")

def 금액(p): return round(total * p / 100)

# ── 카테고리 입력 렌더링 함수 ─────────────────────────────────────────
def 카테고리_입력(prefix, sa, cat_key):
    info = 카테고리[cat_key]
    items = info["items"]
    color = info["color"]
    css = info["css"]

    소계 = sum(sa.get(이름, 0) for 이름, _ in items)
    색 = color

    st.markdown(f'''
    <div class="cat-wrap {css}">
        <div class="cat-header">
            <div>
                <span class="cat-title-ko" style="color:{color};">{cat_key}</span>
                <span class="cat-title-en">/ {info["label"]}</span>
            </div>
            <div>
                <span class="cat-subtotal" style="color:{색};">{소계:.1f}%</span>
                <span class="cat-amt">{금액(소계):,}원</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 4열 그리드로 입력창 배치
    n = len(items)
    rows = (n + 3) // 4  # 올림 나눗셈

    for row in range(rows):
        cols = st.columns(4)
        for col_idx in range(4):
            item_idx = row * 4 + col_idx
            if item_idx < n:
                이름, 티커 = items[item_idx]
                with cols[col_idx]:
                    v = st.number_input(
                        f"{이름} ({티커})",
                        min_value=0.0, max_value=100.0,
                        value=float(sa.get(이름, 0)),
                        step=0.5,
                        key=f"{prefix}_a_{이름}"
                    )
                    sa[이름] = v
            # 빈 칸은 그냥 비워둠 (자연스럽게 정렬됨)

    st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

# ── 입력 탭 함수 ──────────────────────────────────────────────────────
def 입력탭(prefix, sa, sc):

    # 전체 합계 미리 계산 (도넛용)
    cat_sums = {cat: sum(sa.get(이름, 0) for 이름, _ in info["items"]) for cat, info in 카테고리.items()}
    전체합 = sum(cat_sums.values())

    # 도넛 차트
    if 전체합 > 0:
        st.markdown('<div class="section-label">포트폴리오 구성 요약</div>', unsafe_allow_html=True)
        c_chart, c_bar = st.columns([1, 1])

        with c_chart:
            labels = [f"{cat}" for cat in 카테고리]
            values = [cat_sums[cat] for cat in 카테고리]
            colors = [info["color"] for info in 카테고리.values()]
            fig = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.65,
                marker=dict(colors=colors, line=dict(color="#0d0d0d", width=3)),
                textinfo="label+percent",
                textfont=dict(size=12, color="rgba(234,234,234,0.85)"),
                hovertemplate="<b>%{label}</b><br>%{value:.1f}%<br>%{customdata:,}원<extra></extra>",
                customdata=[금액(cat_sums[cat]) for cat in 카테고리]
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=280,
                margin=dict(t=10, b=10, l=0, r=0),
                font=dict(color="rgba(234,234,234,0.4)"),
                legend=dict(font=dict(size=11, color="rgba(234,234,234,0.45)"), bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(text=f'<b>{전체합:.0f}%</b>', x=0.5, y=0.5,
                                  font_size=26, showarrow=False, font=dict(color="#EAEAEA"))]
            )
            st.plotly_chart(fig, use_container_width=True)

        with c_bar:
            st.markdown("<br>", unsafe_allow_html=True)
            for cat, info in 카테고리.items():
                s = cat_sums[cat]
                bar_w = min(int(s), 100)
                st.markdown(f'''
                <div style="margin-bottom:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="font-family:'DM Mono',monospace;font-size:0.72rem;color:rgba(234,234,234,0.5);">
                            {cat}
                            <span style="color:rgba(234,234,234,0.2);font-size:0.6rem;margin-left:6px;">/ {info["label"]}</span>
                        </span>
                        <span style="font-family:'DM Mono',monospace;font-size:1rem;color:{info["color"]};">
                            {s:.1f}%
                            <span style="color:rgba(234,234,234,0.2);font-size:0.68rem;margin-left:6px;">{금액(s):,}원</span>
                        </span>
                    </div>
                    <div style="height:3px;background:#1e1e1e;border-radius:2px;">
                        <div style="height:3px;width:{bar_w}%;background:{info["color"]};border-radius:2px;opacity:0.65;"></div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

    # 카테고리별 입력
    st.markdown('<div class="section-label">자산군 비중 (%)</div>', unsafe_allow_html=True)
    for cat_key in 카테고리:
        카테고리_입력(prefix, sa, cat_key)

    # 전체 합계
    전체합 = sum(sa.values())
    색_전체 = "#4ade80" if abs(전체합-100)<0.1 else "#f87171" if 전체합>100 else "#f59e0b"
    st.markdown(f'''
    <div class="total-pill">
        <span style="color:rgba(234,234,234,0.3);font-size:0.7rem;letter-spacing:1px;">전체 자산 합계</span>
        <span style="color:{색_전체};font-size:1.2rem;font-weight:500;">{전체합:.1f}%</span>
        <span style="color:rgba(234,234,234,0.18);font-size:0.75rem;">{금액(전체합):,}원</span>
    </div>''', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 통화 입력
    st.markdown('<div class="section-label">통화 비중 (%)</div>', unsafe_allow_html=True)
    tcols = st.columns(5)
    통합 = 0
    for i, (이름, 티커, 아이콘) in enumerate(통화목록):
        with tcols[i]:
            v = st.number_input(f"{아이콘} {이름}", 0.0, 100.0, float(sc.get(이름, 0)), 0.5, key=f"{prefix}_c_{이름}")
            sc[이름] = v; 통합 += v

    통색 = "#4ade80" if abs(통합-100)<0.1 else "#f87171" if 통합>100 else "#f59e0b"
    st.markdown(f'''
    <div class="total-pill">
        <span style="color:rgba(234,234,234,0.3);font-size:0.7rem;letter-spacing:1px;">통화 합계</span>
        <span style="color:{통색};font-size:1.2rem;font-weight:500;">{통합:.1f}%</span>
        <span style="color:rgba(234,234,234,0.18);font-size:0.75rem;">{금액(통합):,}원</span>
    </div>''', unsafe_allow_html=True)

    # 통화 도넛
    통d = [(n, sc[n]) for n,_,_ in 통화목록 if sc.get(n,0)>0]
    if 통d:
        fig2 = go.Figure(go.Pie(
            labels=[x[0] for x in 통d], values=[x[1] for x in 통d], hole=0.65,
            marker=dict(colors=["#1E88E5","#ec4899","#22c55e","#f97316","#a855f7"][:len(통d)],
                        line=dict(color="#0d0d0d", width=3)),
            textinfo="label+percent", textfont=dict(size=11, color="rgba(234,234,234,0.8)"),
            hovertemplate="<b>%{label}</b><br>%{value}%<br>%{customdata:,}원<extra></extra>",
            customdata=[금액(x[1]) for x in 통d]
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=260,
            margin=dict(t=10,b=10,l=0,r=0),
            font=dict(color="rgba(234,234,234,0.35)"),
            legend=dict(font=dict(size=10,color="rgba(234,234,234,0.35)"),bgcolor="rgba(0,0,0,0)"),
            annotations=[dict(text=f'<b>{통합:.0f}%</b>', x=0.5, y=0.5,
                              font_size=20, showarrow=False, font=dict(color="#EAEAEA"))]
        )
        col_통, _ = st.columns([1, 1])
        with col_통:
            st.plotly_chart(fig2, use_container_width=True)

# ── 탭 ───────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["  📌  현재 비중  ", "  🎯  목표 비중  ", "  ⚡  비교 & 리밸런싱  "])

with tab1:
    입력탭("현재", st.session_state["현재자산"], st.session_state["현재통화"])
with tab2:
    입력탭("목표", st.session_state["목표자산"], st.session_state["목표통화"])

# ── 탭3: 비교 & 리밸런싱 ─────────────────────────────────────────────
with tab3:
    현자 = st.session_state["현재자산"]
    목자 = st.session_state["목표자산"]
    현통 = st.session_state["현재통화"]
    목통 = st.session_state["목표통화"]

    현_cat = {cat: sum(현자.get(이름,0) for 이름,_ in info["items"]) for cat, info in 카테고리.items()}
    목_cat = {cat: sum(목자.get(이름,0) for 이름,_ in info["items"]) for cat, info in 카테고리.items()}

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("현재 자산 합계", f"{sum(현자.values()):.1f}%", f"{금액(sum(현자.values())):,}원")
    k2.metric("목표 자산 합계", f"{sum(목자.values()):.1f}%", f"{금액(sum(목자.values())):,}원")
    k3.metric("현재 통화 합계", f"{sum(현통.values()):.1f}%", f"{금액(sum(현통.values())):,}원")
    k4.metric("목표 통화 합계", f"{sum(목통.values()):.1f}%", f"{금액(sum(목통.values())):,}원")

    st.markdown("<hr>", unsafe_allow_html=True)

    # 카테고리별 도넛 비교
    if any(v>0 for v in 현_cat.values()) or any(v>0 for v in 목_cat.values()):
        st.markdown('<div class="section-label">카테고리별 현재 vs 목표</div>', unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        colors = [info["color"] for info in 카테고리.values()]
        cats = list(카테고리.keys())

        with cc1:
            fig_현 = go.Figure(go.Pie(
                labels=cats, values=[현_cat[c] for c in cats], hole=0.6,
                marker=dict(colors=colors, line=dict(color="#0d0d0d", width=3)),
                textinfo="label+percent", textfont=dict(size=11, color="rgba(234,234,234,0.85)"),
            ))
            fig_현.update_layout(
                title=dict(text="현재 포트폴리오", font=dict(color="rgba(234,234,234,0.35)", size=11, family="DM Mono"), x=0.5),
                paper_bgcolor="rgba(0,0,0,0)", height=300,
                margin=dict(t=30,b=10,l=0,r=0),
                font=dict(color="rgba(234,234,234,0.35)"),
                legend=dict(font=dict(size=9,color="rgba(234,234,234,0.35)"),bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(text=f'<b>{sum(현_cat.values()):.0f}%</b>', x=0.5, y=0.5,
                                  font_size=20, showarrow=False, font=dict(color="#EAEAEA"))]
            )
            st.plotly_chart(fig_현, use_container_width=True)

        with cc2:
            fig_목 = go.Figure(go.Pie(
                labels=cats, values=[목_cat[c] for c in cats], hole=0.6,
                marker=dict(colors=colors, line=dict(color="#0d0d0d", width=3)),
                textinfo="label+percent", textfont=dict(size=11, color="rgba(234,234,234,0.85)"),
            ))
            fig_목.update_layout(
                title=dict(text="목표 포트폴리오", font=dict(color="rgba(234,234,234,0.35)", size=11, family="DM Mono"), x=0.5),
                paper_bgcolor="rgba(0,0,0,0)", height=300,
                margin=dict(t=30,b=10,l=0,r=0),
                font=dict(color="rgba(234,234,234,0.35)"),
                legend=dict(font=dict(size=9,color="rgba(234,234,234,0.35)"),bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(text=f'<b>{sum(목_cat.values()):.0f}%</b>', x=0.5, y=0.5,
                                  font_size=20, showarrow=False, font=dict(color="#EAEAEA"))]
            )
            st.plotly_chart(fig_목, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 전체 자산 비교표
    st.markdown('<div class="section-label">자산군 현재 vs 목표</div>', unsafe_allow_html=True)
    모든자산 = [(이름, 티커, cat) for cat, info in 카테고리.items() for 이름, 티커 in info["items"]]

    자rows = []
    for 이름, 티커, 카테 in 모든자산:
        현 = 현자.get(이름,0); 목 = 목자.get(이름,0)
        차 = round(목-현,1); 조 = 금액(차)
        if 현>0 or 목>0:
            자rows.append({
                "자산":이름, "구분":카테, "티커":티커,
                "현재(%)":현, "목표(%)":목, "차이(%)":차,
                "현재금액":f"{금액(현):,}원", "목표금액":f"{금액(목):,}원",
                "조정금액":f"{'▲+' if 조>0 else '▼' if 조<0 else '—'}{abs(조):,}원",
                "_조정":조
            })

    def 스타(v):
        s = str(v)
        if "▲" in s: return "color:#4ade80;font-weight:600"
        if "▼" in s: return "color:#f87171;font-weight:600"
        if isinstance(v,float) and v>0: return "color:#4ade80"
        if isinstance(v,float) and v<0: return "color:#f87171"
        return ""

    if 자rows:
        df = pd.DataFrame(자rows)[["자산","구분","티커","현재(%)","목표(%)","차이(%)","현재금액","목표금액","조정금액"]]
        st.dataframe(df.style.applymap(스타, subset=["차이(%)","조정금액"]), use_container_width=True, hide_index=True)

        fig_b = go.Figure()
        ns = [r["자산"] for r in 자rows]
        fig_b.add_bar(name="현재", x=ns, y=[r["현재(%)"] for r in 자rows],
                      marker=dict(color="rgba(30,136,229,0.75)", line=dict(color="rgba(30,136,229,0.2)",width=1)))
        fig_b.add_bar(name="목표", x=ns, y=[r["목표(%)"] for r in 자rows],
                      marker=dict(color="rgba(74,222,128,0.75)", line=dict(color="rgba(74,222,128,0.2)",width=1)))
        fig_b.update_layout(
            barmode="group", height=380,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(234,234,234,0.35)", family="DM Sans"),
            xaxis=dict(tickangle=-35, gridcolor="rgba(255,255,255,0.03)",
                       color="rgba(234,234,234,0.3)", tickfont=dict(size=11)),
            yaxis=dict(title="비중 (%)", gridcolor="rgba(255,255,255,0.05)",
                       color="rgba(234,234,234,0.3)"),
            legend=dict(font=dict(color="rgba(234,234,234,0.45)"),
                        bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
            margin=dict(t=20,b=80,l=0,r=0), bargap=0.2
        )
        st.plotly_chart(fig_b, use_container_width=True)
    else:
        st.markdown('<p style="color:rgba(234,234,234,0.15);font-size:0.82rem;margin-top:8px;">탭1, 탭2에서 비중을 먼저 입력해주세요.</p>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 통화 비교표
    st.markdown('<div class="section-label">통화 비중 현재 vs 목표</div>', unsafe_allow_html=True)
    통rows = []
    for 이름,티커,아이콘 in 통화목록:
        현 = 현통.get(이름,0); 목 = 목통.get(이름,0)
        차 = round(목-현,1); 조 = 금액(차)
        if 현>0 or 목>0:
            통rows.append({
                "통화":f"{아이콘} {이름}", "티커":티커,
                "현재(%)":현, "목표(%)":목, "차이(%)":차,
                "현재금액":f"{금액(현):,}원", "목표금액":f"{금액(목):,}원",
                "조정금액":f"{'▲+' if 조>0 else '▼' if 조<0 else '—'}{abs(조):,}원",
                "_조정":조
            })
    if 통rows:
        df2 = pd.DataFrame(통rows)[["통화","티커","현재(%)","목표(%)","차이(%)","현재금액","목표금액","조정금액"]]
        st.dataframe(df2.style.applymap(스타, subset=["차이(%)","조정금액"]), use_container_width=True, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 리밸런싱 액션
    st.markdown('<div class="section-label">리밸런싱 액션</div>', unsafe_allow_html=True)
    전체 = 자rows + 통rows
    매수 = sorted([r for r in 전체 if r["_조정"]>0], key=lambda x:-x["_조정"])
    매도 = sorted([r for r in 전체 if r["_조정"]<0], key=lambda x:x["_조정"])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:#4ade80;letter-spacing:2px;margin-bottom:10px;">▲ BUY — 부족한 자산</p>', unsafe_allow_html=True)
        if 매수:
            for r in 매수:
                n = r.get("자산") or r.get("통화","")
                st.markdown(f'''<div class="action-card-buy">
                    <div class="action-name">{n}</div>
                    <div class="action-amt" style="color:#4ade80">+{r["_조정"]:,}원</div>
                    <div class="action-amt" style="color:rgba(234,234,234,0.22);margin-top:3px">{r["차이(%)"]:.1f}% 부족</div>
                </div>''', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:rgba(234,234,234,0.15);font-size:0.8rem;">매수할 자산 없음</p>', unsafe_allow_html=True)
    with c2:
        st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:#f87171;letter-spacing:2px;margin-bottom:10px;">▼ SELL — 초과한 자산</p>', unsafe_allow_html=True)
        if 매도:
            for r in 매도:
                n = r.get("자산") or r.get("통화","")
                st.markdown(f'''<div class="action-card-sell">
                    <div class="action-name">{n}</div>
                    <div class="action-amt" style="color:#f87171">{r["_조정"]:,}원</div>
                    <div class="action-amt" style="color:rgba(234,234,234,0.22);margin-top:3px">{r["차이(%)"]:.1f}% 초과</div>
                </div>''', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:rgba(234,234,234,0.15);font-size:0.8rem;">매도할 자산 없음</p>', unsafe_allow_html=True)

st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.6rem;color:rgba(234,234,234,0.07);text-align:center;letter-spacing:1px;margin-top:40px;">FOR REFERENCE ONLY · NOT FINANCIAL ADVICE</p>', unsafe_allow_html=True)
