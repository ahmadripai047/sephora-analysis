"""
app.py — Sephora Products & Skincare Dashboard
Tema: Luxury Beauty — Dark Glamour with Rose Gold accents

"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ast
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ─── Page Config ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Sephora Beauty Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── TEMA: Luxury Dark Beauty ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Jost:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #12091a 50%, #0f0a14 100%);
    color: #f0e6d3;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a2e 0%, #0d0618 100%);
    border-right: 1px solid rgba(212, 175, 55, 0.2);
}
[data-testid="stSidebar"] * { color: #e8d5c4 !important; }

/* ── Title ── */
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #d4af37 0%, #f5d76e 40%, #c9965a 70%, #d4af37 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    line-height: 1.1;
    margin-bottom: 0;
}
.hero-subtitle {
    font-family: 'Jost', sans-serif;
    font-size: 0.95rem;
    color: #b09070;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Metric Cards ── */
.kpi-card {
    background: linear-gradient(135deg, rgba(212,175,55,0.08) 0%, rgba(180,120,80,0.05) 100%);
    border: 1px solid rgba(212, 175, 55, 0.25);
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
}
.kpi-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #d4af37;
    line-height: 1;
}
.kpi-label {
    font-size: 0.72rem;
    color: #9a8070;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 6px;
}
.kpi-sub {
    font-size: 0.8rem;
    color: #c4a882;
    margin-top: 4px;
}

/* ── Section Headers ── */
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: #d4af37;
    letter-spacing: 1px;
    border-bottom: 1px solid rgba(212,175,55,0.2);
    padding-bottom: 8px;
    margin: 24px 0 16px;
}

/* ── Insight Boxes ── */
.insight-box {
    background: linear-gradient(135deg, rgba(212,175,55,0.06), rgba(180,100,80,0.04));
    border: 1px solid rgba(212,175,55,0.2);
    border-left: 3px solid #d4af37;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #d4c4b0;
    line-height: 1.6;
}

/* ── Filter Pills ── */
.stMultiSelect [data-baseweb="tag"] {
    background-color: rgba(212,175,55,0.2) !important;
    border: 1px solid rgba(212,175,55,0.4) !important;
    color: #d4af37 !important;
}

/* ── Divider ── */
hr { border-color: rgba(212,175,55,0.15) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
    font-family: 'Jost', sans-serif;
    letter-spacing: 1px;
    color: #9a8070;
}
.stTabs [aria-selected="true"] {
    color: #d4af37 !important;
    border-bottom: 2px solid #d4af37 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border: 1px solid rgba(212,175,55,0.15); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly Theme ─────────────────────────────────────────────────
PLOT_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,10,20,0.6)",
    font=dict(family="Jost, sans-serif", color="#d4c4b0", size=11),
    title_font=dict(family="Cormorant Garamond, serif", color="#d4af37", size=16),
    colorway=["#d4af37","#c9965a","#e8a4c9","#7ec8c8","#9b8dc4","#e07b6e","#8dc49b"],
)
GOLD = "#d4af37"
ROSE = "#e8a4c9"
TEAL = "#7ec8c8"

# ─── Load & Prepare Data ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("product_info.csv")

    def parse_list(x):
        try: return ast.literal_eval(x)
        except: return []

    df["highlights_list"] = df["highlights"].apply(parse_list)
    bins   = [0,25,50,100,200,5000]
    labels = ["Budget (<$25)","Mid ($25–50)","Premium ($50–100)","Luxury ($100–200)","Ultra-Luxury ($200+)"]
    df["price_segment"] = pd.cut(df["price_usd"], bins=bins, labels=labels)
    df["log_loves"] = np.log1p(df["loves_count"])
    df["rating_bucket"] = pd.cut(df["rating"], bins=[0,2,3,4,4.5,5],
                                  labels=["Poor","Fair","Good","Great","Excellent"])
    return df

df = load_data()

# ─── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-family:Cormorant Garamond,serif; font-size:1.5rem; color:#d4af37; letter-spacing:3px;'>✦ SEPHORA ✦</div>
        <div style='font-size:0.65rem; color:#9a8070; letter-spacing:4px; text-transform:uppercase; margin-top:4px;'>Beauty Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("**✦ Navigate**")
    page = st.radio("", [
        "Overview",
        "Brand Analysis",
        "Price Intelligence",
        "Ratings & Popularity",
        "Product Features",
        "Skincare Deep Dive",
        "Product Explorer",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**✦ Filters**")
    all_cats = ["All"] + sorted(df["primary_category"].unique().tolist())
    sel_cat = st.selectbox("Category", all_cats)

    price_range = st.slider("Price Range (USD)", 0, 500, (0, 300))

    excl_filter = st.multiselect("Product Type",
        ["Sephora Exclusive","New Arrivals","Online Only","Limited Edition"],
        default=[])

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.72rem; color:#6a5a4a; text-align:center; line-height:1.8;'>
    Dataset: Kaggle<br>
    Sephora Products & Skincare<br>
    {len(df):,} products · {df['brand_name'].nunique()} brands
    </div>""", unsafe_allow_html=True)

# ─── Apply Filters ────────────────────────────────────────────────
dff = df.copy()
if sel_cat != "All":
    dff = dff[dff["primary_category"] == sel_cat]
dff = dff[dff["price_usd"].between(price_range[0], price_range[1])]
if "Sephora Exclusive" in excl_filter: dff = dff[dff["sephora_exclusive"]==1]
if "New Arrivals" in excl_filter:      dff = dff[dff["new"]==1]
if "Online Only" in excl_filter:       dff = dff[dff["online_only"]==1]
if "Limited Edition" in excl_filter:   dff = dff[dff["limited_edition"]==1]

# ═══════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════
if page == " Overview":
    st.markdown("""
    <div style='padding: 30px 0 20px;'>
        <div class='hero-title'>SEPHORA<br>BEAUTY ANALYTICS</div>
        <div class='hero-subtitle'>Product Intelligence Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.8rem; color:#7a6a5a;'>Showing <b style='color:#d4af37'>{len(dff):,}</b> of {len(df):,} products after filters</div>", unsafe_allow_html=True)
    st.divider()

    # KPIs
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    kpis = [
        (f"{len(dff):,}", "Total Products", f"{len(df)-len(dff):+,} filtered"),
        (f"{dff['brand_name'].nunique():,}", "Unique Brands", "across all categories"),
        (f"${dff['price_usd'].median():.0f}", "Median Price", f"avg ${dff['price_usd'].mean():.0f}"),
        (f"{dff['rating'].mean():.2f}★", "Avg Rating", f"from {dff['reviews'].sum():,.0f} reviews"),
        (f"{dff['loves_count'].sum()/1e6:.1f}M", "Total Loves", "community favorites"),
        (f"{(dff['sephora_exclusive'].mean()*100):.0f}%", "Sephora Excl.", "exclusive products"),
    ]
    for col, (num, label, sub) in zip([c1,c2,c3,c4,c5,c6], kpis):
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-number'>{num}</div>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    col_a, col_b = st.columns([1.2, 0.8])

    with col_a:
        st.markdown("<div class='section-title'>Category Distribution</div>", unsafe_allow_html=True)
        cat_c = dff["primary_category"].value_counts().reset_index()
        cat_c.columns = ["Category","Count"]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=cat_c["Count"], y=cat_c["Category"],
            orientation="h",
            marker=dict(
                color=cat_c["Count"],
                colorscale=[[0,"#3d1a5c"],[0.5,"#9b2d78"],[1,"#d4af37"]],
                showscale=False
            ),
            text=cat_c["Count"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(color="#d4c4b0", size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=340,
                          margin=dict(l=0,r=60,t=10,b=0),
                          xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Price Segments</div>", unsafe_allow_html=True)
        seg_c = dff["price_segment"].value_counts().reset_index()
        seg_c.columns = ["Segment","Count"]
        fig = go.Figure(go.Pie(
            labels=seg_c["Segment"], values=seg_c["Count"],
            hole=0.65,
            marker=dict(colors=["#4a9d6f","#5b8dc4","#d4af37","#c9965a","#e8a4c9"],
                        line=dict(color="#0a0a0f", width=2)),
            textinfo="percent", textfont=dict(size=11, color="#f0e6d3")
        ))
        fig.update_layout(**PLOT_THEME, height=340,
                          margin=dict(l=0,r=0,t=10,b=0),
                          legend=dict(font=dict(size=9), orientation="v"),
                          annotations=[dict(text="Price<br>Mix", x=0.5, y=0.5,
                                           font=dict(size=13, color="#d4af37",
                                                    family="Cormorant Garamond"),
                                           showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    # Category × Avg Rating heatmap-style
    st.markdown("<div class='section-title'>Category Performance Matrix</div>", unsafe_allow_html=True)
    cat_matrix = dff.groupby(["primary_category","price_segment"], observed=True).agg(
        count=("product_id","count"),
        avg_rating=("rating","mean"),
        avg_loves=("loves_count","mean")
    ).reset_index().dropna()

    fig = px.scatter(cat_matrix, x="price_segment", y="primary_category",
                     size="count", color="avg_rating",
                     color_continuous_scale=["#3d1a5c","#9b2d78","#d4af37","#f5e47a"],
                     size_max=60,
                     labels={"price_segment":"Price Segment","primary_category":"Category",
                              "avg_rating":"Avg Rating","count":"# Products"})
    fig.update_layout(**PLOT_THEME, height=380,
                      margin=dict(l=0,r=0,t=10,b=0),
                      coloraxis_colorbar=dict(title="Rating", tickfont=dict(size=9)))
    fig.update_traces(marker=dict(line=dict(width=1, color="rgba(212,175,55,0.3)")))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    ✦ <b>Key Insight:</b> Skincare and Makeup lead in volume, but Fragrance commands the highest median price.
    Most products cluster in the Mid ($25–50) and Budget (<$25) segments, while Ultra-Luxury products
    represent only ~2% of catalog but drive significant brand prestige.
    </div>""", unsafe_allow_html=True)

    # ── Business Problem & Recommendation ──
    st.markdown("<div class='section-title'>Business Problem</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px;'>
        <div class='insight-box'>
            <b style='color:#d4af37;'>Problem Statement</b><br><br>
            Tidak semua produk Sephora sukses di pasar, mayoritas gagal menarik perhatian konsumen
            meskipun tersedia di platform. Analisis ini menjawab:<br><br>
            • Faktor apa yang mendorong <b>popularitas produk</b>?<br>
            • Apakah <b>harga tinggi</b> = produk lebih disukai?<br>
            • Klaim apa yang paling <b>relevan</b> di pasar saat ini?<br>
            • Brand mana yang punya <b>value proposition terkuat</b>?
        </div>
        <div class='insight-box'>
            <b style='color:#d4af37;'>🔍 Approach</b><br><br>
            Analisis menggunakan <b>8.494 produk</b> dari 300+ brand di platform Sephora dengan metodologi:<br><br>
            1. <b>Data cleaning</b> & feature engineering<br>
            2. <b>EDA</b> distribusi, korelasi, segmentasi<br>
            3. <b>Deep dive</b> per kategori & brand<br>
            4. <b>Dashboard interaktif</b> untuk eksplorasi mandiri
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📊 Key Findings</div>", unsafe_allow_html=True)
    findings = [
        ("Harga ≠ Kualitas", "Korelasi harga vs rating hampir nol (r ≈ 0.04). Produk budget memiliki rating setara produk luxury."),
        ("Ethical Beauty Wajib", "Vegan (31%) & Cruelty-Free (21%) sudah jadi ekspektasi dasar, bukan diferensiasi."),
        ("Reviews Drives Loves", "Korelasi reviews vs loves > 0.7 , winner-takes-most dynamic di platform."),
        ("Exclusive = Edge", "Produk Sephora Exclusive rata-rata lebih tinggi ratingnya, efek kurasi, & eksklusivitas."),
        ("Skincare = Paling Kompetitif", "28.5% katalog, tapi niche brands dengan positioning kuat mengalahkan brand besar."),
        ("Luxury = Lebih Engaged", "Volume didominasi Mid-tier, tapi avg loves tertinggi ada di segmen Luxury ($100–200)."),
    ]
    cols = st.columns(3)
    for i, (title, desc) in enumerate(findings):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='background:rgba(212,175,55,0.05); border:1px solid rgba(212,175,55,0.15);
                        border-radius:12px; padding:16px; margin-bottom:12px; min-height:110px;'>
                <div style='color:#d4af37; font-weight:600; font-size:0.9rem; margin-bottom:6px;'>{title}</div>
                <div style='color:#c4a882; font-size:0.82rem; line-height:1.5;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>💡 Recommendations</div>", unsafe_allow_html=True)
    recs = [
        ("For Brand Managers", [
            "Prioritaskan ethical certifications, bukan lagi opsional",
            "Fokus ke product storytelling, bukan price war",
            "Agresif di review generation pada 30 hari pertama launch",
        ], "#d4af37"),
        ("For Retail Strategist", [
            "Perluas program Sephora Exclusive untuk loyalty retention",
            "Jaga proporsi budget segment agar customer base tetap luas",
            "Gunakan love & review data sebagai sinyal kurasi produk",
        ], "#e8a4c9"),
        ("For New Entrants", [
            "Skincare: positioning niche > volume play",
            "Luxury segment konsumennya lebih engaged & loyal",
            "Ingredient transparency jadi daya tarik utama Gen Z",
        ], "#7ec8c8"),
    ]
    rec_cols = st.columns(3)
    for col, (title, points, color) in zip(rec_cols, recs):
        with col:
            bullets = "".join([f"<li style='margin-bottom:5px;'>{p}</li>" for p in points])
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.3); border:1px solid {color}33;
                        border-top:3px solid {color}; border-radius:12px;
                        padding:18px; min-height:160px;'>
                <div style='color:{color}; font-weight:600; font-size:0.9rem;
                            margin-bottom:10px; letter-spacing:1px;'>{title}</div>
                <ul style='color:#c4a882; font-size:0.8rem; line-height:1.6;
                           padding-left:16px; margin:0;'>{bullets}</ul>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: BRAND
# ═══════════════════════════════════════════════════════════
elif page == "Brand Analysis":
    st.markdown("<div class='hero-title' style='font-size:2.2rem;'>BRAND INTELLIGENCE</div>", unsafe_allow_html=True)
    st.divider()

    brand_stats = dff.groupby("brand_name").agg(
        products=("product_id","count"),
        avg_rating=("rating","mean"),
        avg_loves=("loves_count","mean"),
        total_loves=("loves_count","sum"),
        avg_price=("price_usd","mean"),
        excl_rate=("sephora_exclusive","mean")
    ).reset_index()

    tab1, tab2, tab3 = st.tabs(["Most Products", "Highest Rated", "Most Loved"])

    with tab1:
        top20 = brand_stats.nlargest(20, "products")
        fig = go.Figure(go.Bar(
            x=top20["products"], y=top20["brand_name"],
            orientation="h",
            marker=dict(color=top20["products"],
                        colorscale=[[0,"#2d1040"],[1,"#d4af37"]]),
            text=top20["products"], textposition="outside",
            textfont=dict(color="#d4af37", size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=560,
                          margin=dict(l=0,r=60,t=10,b=0),
                          title="Top 20 Brands by Product Count",
                          yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        top_rated = brand_stats[brand_stats["products"]>=15].nlargest(15,"avg_rating")
        fig = go.Figure(go.Bar(
            x=top_rated["avg_rating"], y=top_rated["brand_name"],
            orientation="h",
            marker=dict(color=top_rated["avg_rating"],
                        colorscale=[[0,"#2d1040"],[0.5,"#9b2d78"],[1,"#f5d76e"]]),
            text=top_rated["avg_rating"].round(2), textposition="outside",
            textfont=dict(color="#d4af37", size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=500,
                          margin=dict(l=0,r=60,t=10,b=0),
                          title="Top 15 Brands by Avg Rating (min 15 products)",
                          xaxis=dict(range=[3.8,5]),
                          yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        top_loved = brand_stats[brand_stats["products"]>=10].nlargest(15,"avg_loves")
        fig = go.Figure(go.Bar(
            x=top_loved["avg_loves"]/1000, y=top_loved["brand_name"],
            orientation="h",
            marker=dict(color=top_loved["avg_loves"],
                        colorscale=[[0,"#2d1040"],[0.5,"#c9965a"],[1,"#e8a4c9"]]),
            text=(top_loved["avg_loves"]/1000).round(1).astype(str)+"K",
            textposition="outside",
            textfont=dict(color="#e8a4c9", size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=500,
                          margin=dict(l=0,r=80,t=10,b=0),
                          title="Top 15 Brands by Avg Loves (min 10 products)",
                          xaxis_title="Avg Loves ('000)",
                          yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

    # Brand bubble chart
    st.markdown("<div class='section-title'>Brand Landscape — Price vs Rating</div>", unsafe_allow_html=True)
    bub = brand_stats[(brand_stats["products"]>=10) & brand_stats["avg_rating"].notna()]
    fig = px.scatter(bub, x="avg_price", y="avg_rating",
                     size="total_loves", color="products",
                     hover_name="brand_name",
                     color_continuous_scale=[[0,"#3d1a5c"],[0.5,"#9b2d78"],[1,"#d4af37"]],
                     size_max=50,
                     labels={"avg_price":"Avg Price (USD)","avg_rating":"Avg Rating",
                              "products":"# Products","total_loves":"Total Loves"})
    fig.update_layout(**PLOT_THEME, height=420,
                      margin=dict(l=0,r=0,t=10,b=0))
    fig.update_traces(marker=dict(line=dict(width=0.5, color="rgba(212,175,55,0.3)")),
                      textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# PAGE: PRICE
# ═══════════════════════════════════════════════════════════
elif page == "Price Intelligence":
    st.markdown("<div class='hero-title' style='font-size:2.2rem;'>PRICE INTELLIGENCE</div>", unsafe_allow_html=True)
    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-title'>Price Distribution</div>", unsafe_allow_html=True)
        trim = dff[dff["price_usd"]<=300]
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=trim["price_usd"], nbinsx=60,
                                   marker=dict(color="#d4af37", opacity=0.75,
                                               line=dict(color="#0a0a0f", width=0.5))))
        fig.add_vline(x=dff["price_usd"].median(), line_dash="dash",
                      line_color="#e8a4c9", line_width=1.5,
                      annotation_text=f"Median ${dff['price_usd'].median():.0f}",
                      annotation_font_color="#e8a4c9")
        fig.update_layout(**PLOT_THEME, height=320,
                          margin=dict(l=0,r=0,t=10,b=0),
                          xaxis_title="Price (USD)", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Price by Category</div>", unsafe_allow_html=True)
        cat_price = dff.groupby("primary_category")["price_usd"].median().sort_values()
        fig = go.Figure(go.Bar(
            x=cat_price.values, y=cat_price.index,
            orientation="h",
            marker=dict(color=cat_price.values,
                        colorscale=[[0,"#3d1a5c"],[1,"#d4af37"]]),
            text=[f"${v:.0f}" for v in cat_price.values],
            textposition="outside",
            textfont=dict(color="#d4af37", size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=320,
                          margin=dict(l=0,r=60,t=10,b=0),
                          xaxis_title="Median Price (USD)")
        st.plotly_chart(fig, use_container_width=True)

    # Price vs Rating
    st.markdown("<div class='section-title'>Price vs Rating Relationship</div>", unsafe_allow_html=True)
    sample = dff[dff["price_usd"]<=400].dropna(subset=["rating"]).sample(min(2000,len(dff)))
    fig = px.scatter(sample, x="price_usd", y="rating",
                     color="primary_category",
                     size="loves_count", size_max=25,
                     opacity=0.6,
                     hover_data=["product_name","brand_name","price_usd","rating"],
                     color_discrete_sequence=["#d4af37","#e8a4c9","#7ec8c8","#c9965a","#9b8dc4","#e07b6e","#8dc49b","#f5d76e"],
                     labels={"price_usd":"Price (USD)","rating":"Rating","primary_category":"Category"})
    fig.update_layout(**PLOT_THEME, height=420,
                      margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

    # Price segment analysis
    st.markdown("<div class='section-title'>Performance by Price Segment</div>", unsafe_allow_html=True)
    seg_stats = dff.groupby("price_segment", observed=True).agg(
        count=("product_id","count"),
        avg_rating=("rating","mean"),
        avg_loves=("loves_count","mean"),
        avg_reviews=("reviews","mean")
    ).reset_index().dropna()

    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=["Avg Rating","Avg Loves","Avg Reviews"])
    colors_seg = ["#4a9d6f","#5b8dc4","#d4af37","#c9965a","#e8a4c9"]
    for i, (col_name, title) in enumerate([("avg_rating","Avg Rating"),
                                            ("avg_loves","Avg Loves"),
                                            ("avg_reviews","Avg Reviews")], 1):
        fig.add_trace(go.Bar(
            x=seg_stats["price_segment"], y=seg_stats[col_name],
            marker_color=colors_seg[:len(seg_stats)],
            showlegend=False,
            text=seg_stats[col_name].round(1), textposition="outside",
            textfont=dict(color="#d4af37", size=9)
        ), row=1, col=i)
    fig.update_layout(**PLOT_THEME, height=340,
                      margin=dict(l=0,r=0,t=40,b=0))
    fig.update_xaxes(tickfont=dict(size=8), tickangle=20)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    ✦ <b>Price Insight:</b> Higher price does NOT guarantee higher ratings, correlation is near zero (r ≈ 0.04).
    The Mid ($25–50) segment dominates volume while Luxury products ($100–200) show slightly higher avg loves,
    suggesting premium buyers are more engaged. Value-for-money products in Budget tier punch above their weight in ratings.
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: RATINGS
# ═══════════════════════════════════════════════════════════
elif page == "Ratings & Popularity":
    st.markdown("<div class='hero-title' style='font-size:2.2rem;'>RATINGS & POPULARITY</div>", unsafe_allow_html=True)
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='section-title'>Rating Distribution</div>", unsafe_allow_html=True)
        rated = dff.dropna(subset=["rating"])
        fig = go.Figure(go.Histogram(
            x=rated["rating"], nbinsx=50,
            marker=dict(color="#d4af37", opacity=0.8,
                        line=dict(color="#0a0a0f", width=0.5))
        ))
        fig.add_vline(x=rated["rating"].mean(), line_dash="dash",
                      line_color="#e8a4c9", line_width=1.5,
                      annotation_text=f"Mean {rated['rating'].mean():.2f}",
                      annotation_font_color="#e8a4c9")
        fig.update_layout(**PLOT_THEME, height=300,
                          margin=dict(l=0,r=0,t=10,b=0),
                          xaxis_title="Rating", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Loves vs Reviews</div>", unsafe_allow_html=True)
        sample = dff.dropna(subset=["rating"]).sample(min(1500,len(dff)))
        fig = px.scatter(sample, x=np.log1p(sample["reviews"]),
                         y=np.log1p(sample["loves_count"]),
                         color="rating", color_continuous_scale="YlOrRd",
                         opacity=0.5, size_max=8,
                         labels={"x":"log(Reviews+1)","y":"log(Loves+1)","rating":"Rating"})
        fig.update_layout(**PLOT_THEME, height=300,
                          margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # Top products
    st.markdown("<div class='section-title'>Top 10 Most Loved Products</div>", unsafe_allow_html=True)
    top_loved = dff.nlargest(10, "loves_count")[
        ["product_name","brand_name","loves_count","rating","price_usd","primary_category"]
    ].reset_index(drop=True)
    top_loved.index += 1
    top_loved["loves_count"] = top_loved["loves_count"].apply(lambda x: f"{x:,.0f}")
    top_loved["price_usd"]   = top_loved["price_usd"].apply(lambda x: f"${x:,.0f}")
    top_loved["rating"]      = top_loved["rating"].apply(lambda x: f"{'★'*int(x//1)} {x:.2f}" if pd.notna(x) else "N/A")
    st.dataframe(top_loved.rename(columns={
        "product_name":"Product","brand_name":"Brand","loves_count":"Loves",
        "rating":"Rating","price_usd":"Price","primary_category":"Category"
    }), use_container_width=True)

    st.markdown("<div class='section-title'>Top 10 Highest Rated (min 100 reviews)</div>", unsafe_allow_html=True)
    top_rated = (dff[dff["reviews"]>=100]
                 .nlargest(10,"rating")
                 [["product_name","brand_name","rating","reviews","price_usd","primary_category"]]
                 .reset_index(drop=True))
    top_rated.index += 1
    top_rated["price_usd"] = top_rated["price_usd"].apply(lambda x: f"${x:,.0f}")
    top_rated["reviews"]   = top_rated["reviews"].apply(lambda x: f"{x:,}")
    top_rated["rating"]    = top_rated["rating"].round(3)
    st.dataframe(top_rated.rename(columns={
        "product_name":"Product","brand_name":"Brand","rating":"Rating",
        "reviews":"Reviews","price_usd":"Price","primary_category":"Category"
    }), use_container_width=True)

# ═══════════════════════════════════════════════════════════
# PAGE: FEATURES
# ═══════════════════════════════════════════════════════════
elif page == "Product Features":
    st.markdown("<div class='hero-title' style='font-size:2.2rem;'>PRODUCT FEATURES</div>", unsafe_allow_html=True)
    st.divider()

    # Highlights
    all_hl = [h for sub in dff["highlights_list"] for h in sub]
    hl_counts = Counter(all_hl).most_common(25)
    hl_df = pd.DataFrame(hl_counts, columns=["Highlight","Count"])

    st.markdown("<div class='section-title'>Top 25 Product Claims & Highlights</div>", unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=hl_df["Count"], y=hl_df["Highlight"],
        orientation="h",
        marker=dict(color=hl_df["Count"],
                    colorscale=[[0,"#2d1040"],[0.4,"#9b2d78"],[0.7,"#c9965a"],[1,"#d4af37"]]),
        text=hl_df["Count"], textposition="outside",
        textfont=dict(color="#d4af37", size=9)
    ))
    fig.update_layout(**PLOT_THEME, height=650,
                      margin=dict(l=0,r=60,t=10,b=0),
                      yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig, use_container_width=True)

    # Boolean features
    st.markdown("<div class='section-title'>Product Status Breakdown</div>", unsafe_allow_html=True)
    bool_cols   = ["limited_edition","new","online_only","out_of_stock","sephora_exclusive"]
    bool_labels = ["Limited Edition","New Arrival","Online Only","Out of Stock","Sephora Exclusive"]
    values = [dff[c].mean()*100 for c in bool_cols]

    col_a, col_b = st.columns(2)
    with col_a:
        fig = go.Figure(go.Bar(
            x=bool_labels, y=values,
            marker=dict(color=["#c9965a","#4a9d6f","#5b8dc4","#e07b6e","#d4af37"],
                        line=dict(color="#0a0a0f", width=1)),
            text=[f"{v:.1f}%" for v in values], textposition="outside",
            textfont=dict(color="#d4af37", size=11)
        ))
        fig.update_layout(**PLOT_THEME, height=340,
                          margin=dict(l=0,r=0,t=10,b=30),
                          yaxis_title="% of Products",
                          xaxis=dict(tickangle=15))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Exclusive vs non-exclusive rating
        excl_r   = dff[dff["sephora_exclusive"]==1]["rating"].dropna()
        nonexcl_r= dff[dff["sephora_exclusive"]==0]["rating"].dropna()
        fig = go.Figure()
        fig.add_trace(go.Violin(x=excl_r, name="Excl.", side="positive",
                                line_color="#d4af37", fillcolor="rgba(212,175,55,0.2)"))
        fig.add_trace(go.Violin(x=nonexcl_r, name="Non-Excl.", side="negative",
                                line_color="#7ec8c8", fillcolor="rgba(126,200,200,0.2)"))
        fig.update_layout(**PLOT_THEME, height=340,
                          margin=dict(l=0,r=0,t=10,b=0),
                          title="Rating: Sephora Exclusive vs Others",
                          xaxis_title="Rating")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    ✦ <b>Trend Insight:</b> <b>Vegan</b> (31%) and <b>Cruelty-Free</b> (21%) are the most common claims,
    reflecting a major industry shift toward ethical beauty. <b>Clean at Sephora</b> (18%) shows
    the retailer's own certification program is gaining traction. Skincare-focused claims like
    "Hyaluronic Acid" and "Hydrating" rank in top 10, confirming the skincare boom.
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: SKINCARE DEEP DIVE
# ═══════════════════════════════════════════════════════════
elif page == "Skincare Deep Dive":
    st.markdown("<div class='hero-title' style='font-size:2.2rem;'>SKINCARE DEEP DIVE</div>", unsafe_allow_html=True)
    st.divider()

    skincare = dff[dff["primary_category"]=="Skincare"].copy()
    if skincare.empty:
        st.warning("No skincare products match current filters.")
    else:
        c1,c2,c3,c4 = st.columns(4)
        for col, (num, label) in zip([c1,c2,c3,c4], [
            (f"{len(skincare):,}", "Skincare Products"),
            (f"${skincare['price_usd'].median():.0f}", "Median Price"),
            (f"{skincare['rating'].mean():.2f}★", "Avg Rating"),
            (f"{skincare['loves_count'].sum()/1e6:.1f}M", "Total Loves"),
        ]):
            with col:
                st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-number'>{num}</div>
                    <div class='kpi-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("<div class='section-title'>Sub-Categories</div>", unsafe_allow_html=True)
            sub_cat = skincare["secondary_category"].value_counts().head(12)
            fig = go.Figure(go.Bar(
                x=sub_cat.values, y=sub_cat.index, orientation="h",
                marker=dict(color=sub_cat.values,
                            colorscale=[[0,"#2d1040"],[1,"#e8a4c9"]]),
                text=sub_cat.values, textposition="outside",
                textfont=dict(color="#e8a4c9", size=9)
            ))
            fig.update_layout(**PLOT_THEME, height=380,
                              margin=dict(l=0,r=50,t=10,b=0),
                              yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.markdown("<div class='section-title'>Price Distribution</div>", unsafe_allow_html=True)
            trim_sk = skincare[skincare["price_usd"]<=250]
            fig = go.Figure(go.Histogram(
                x=trim_sk["price_usd"], nbinsx=50,
                marker=dict(color="#e8a4c9", opacity=0.8,
                            line=dict(color="#0a0a0f", width=0.5))
            ))
            fig.add_vline(x=skincare["price_usd"].median(), line_dash="dash",
                          line_color="#d4af37",
                          annotation_text=f"Median ${skincare['price_usd'].median():.0f}",
                          annotation_font_color="#d4af37")
            fig.update_layout(**PLOT_THEME, height=380,
                              margin=dict(l=0,r=0,t=10,b=0),
                              xaxis_title="Price (USD)", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)

        # Top skincare brands
        st.markdown("<div class='section-title'>Top Skincare Brands by Avg Loves</div>", unsafe_allow_html=True)
        sk_brands = (skincare.groupby("brand_name")
                     .agg(avg_loves=("loves_count","mean"),
                          count=("product_id","count"),
                          avg_rating=("rating","mean"),
                          avg_price=("price_usd","mean"))
                     .query("count >= 5")
                     .nlargest(15,"avg_loves"))

        fig = px.scatter(sk_brands.reset_index(), x="avg_price", y="avg_rating",
                         size="avg_loves", color="avg_loves",
                         hover_name="brand_name", size_max=60,
                         color_continuous_scale=[[0,"#3d1a5c"],[0.5,"#c9965a"],[1,"#d4af37"]],
                         labels={"avg_price":"Avg Price (USD)","avg_rating":"Avg Rating",
                                 "avg_loves":"Avg Loves"})
        fig.update_layout(**PLOT_THEME, height=400,
                          margin=dict(l=0,r=0,t=10,b=0),
                          title="Skincare Brands: Price vs Rating (size = Loves)")
        for _, row in sk_brands.reset_index().iterrows():
            fig.add_annotation(x=row["avg_price"], y=row["avg_rating"],
                               text=row["brand_name"].split()[0],
                               font=dict(size=7, color="#d4c4b0"),
                               showarrow=False, yshift=12)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# PAGE: PRODUCT EXPLORER
# ═══════════════════════════════════════════════════════════
elif page == "Product Explorer":
    st.markdown("<div class='hero-title' style='font-size:2.2rem;'>PRODUCT EXPLORER</div>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("Search Product / Brand", placeholder="e.g. moisturizer, Charlotte Tilbury...")
    with col2:
        sort_by = st.selectbox("Sort By", ["loves_count","rating","reviews","price_usd"])
    with col3:
        sort_order = st.radio("Order", ["Descending","Ascending"], horizontal=True)

    # Apply search
    result = dff.copy()
    if search:
        mask = (result["product_name"].str.contains(search, case=False, na=False) |
                result["brand_name"].str.contains(search, case=False, na=False))
        result = result[mask]

    result = result.sort_values(sort_by, ascending=(sort_order=="Ascending"))

    st.markdown(f"<div style='color:#9a8070; font-size:0.8rem; margin-bottom:10px;'>Found <b style='color:#d4af37'>{len(result):,}</b> products</div>",
                unsafe_allow_html=True)

    display_cols = ["product_name","brand_name","primary_category","secondary_category",
                    "price_usd","rating","reviews","loves_count",
                    "sephora_exclusive","new","online_only"]
    show = result[display_cols].head(100).copy()
    show["price_usd"] = show["price_usd"].apply(lambda x: f"${x:.0f}")
    show["rating"]    = show["rating"].round(2)
    show["loves_count"]= show["loves_count"].apply(lambda x: f"{x:,}")
    show["reviews"]   = show["reviews"].apply(lambda x: f"{x:,}" if pd.notna(x) else "—")
    show.columns = ["Product","Brand","Category","Sub-Category",
                    "Price","Rating","Reviews","Loves","Excl.","New","Online Only"]
    st.dataframe(show, use_container_width=True, height=520)

# ─── Footer ───────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; padding: 10px 0;
     font-size:0.72rem; color:#4a3a2a; letter-spacing:2px;'>
✦ SEPHORA BEAUTY ANALYTICS ✦ MUHAMMAD RIFAI ✦ ANALYTIFAI ✦
</div>""", unsafe_allow_html=True)
