# Sephora Products & Skincare Analytics

> **"Does price, brand, or product claims actually drive customer love in the beauty industry?"**

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-ff4b4b?logo=streamlit&logoColor=white)](https://sephora-analysis-analytifai.streamlit.app/)
[![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20beff?logo=kaggle&logoColor=white)](https://kaggle.com)
[![Plotly](https://img.shields.io/badge/Viz-Plotly-3d4db7?logo=plotly&logoColor=white)](https://plotly.com)

---

## Business Problem

Sephora adalah salah satu retailer beauty terbesar di dunia dengan ribuan produk dari ratusan brand. Namun **tidak semua produk sukses di pasar**, sebagian besar produk gagal menarik perhatian konsumen meskipun sudah tersedia di platform.

**Pertanyaan bisnis yang ingin dijawab:**

1. Faktor apa yang paling mempengaruhi **popularitas produk** (loves count)?
2. Apakah **harga yang lebih tinggi** berarti produk lebih disukai konsumen?
3. Kategori dan brand mana yang **paling dominan** dan mengapa?
4. Apakah klaim produk seperti **"Vegan"** atau **"Cruelty-Free"** berpengaruh terhadap penerimaan pasar?
5. Segmen harga mana yang memberikan **nilai terbaik** bagi konsumen?

---

## Approach

### Data
- **Sumber:** Kaggle — *Sephora Products and Skincare Reviews*
- **Ukuran:** 8.494 produk · 300+ brand · 27 variabel
- **Periode:** Data aktif di platform Sephora

| Fitur | Deskripsi |
|---|---|
| `product_name` | Nama produk |
| `brand_name` | Nama brand (300+ brands) |
| `loves_count` | Jumlah pengguna yang "love" produk |
| `rating` | Rating rata-rata (1–5) |
| `reviews` | Jumlah ulasan produk |
| `price_usd` | Harga dalam USD ($3–$1,900) |
| `primary_category` | Skincare, Makeup, Hair, Fragrance, dll |
| `highlights` | Klaim produk (Vegan, Cruelty-Free, dll) |
| `sephora_exclusive` | Produk eksklusif Sephora |
| `limited_edition` | Produk edisi terbatas |
---

### Metodologi
```
1. Data Cleaning & Feature Engineering
   └── Parsing highlight list, price segmentation, rating bucketing

2. Exploratory Data Analysis (EDA)
   ├── Distribusi kategori, harga, rating
   ├── Brand performance analysis
   ├── Korelasi antar variabel numerik
   └── Analisis klaim & fitur produk

3. Deep Dive Analysis
   ├── Skincare category (terbesar & paling kompetitif)
   ├── Price intelligence per segmen
   └── Popularity driver analysis

4. Visualisasi & Dashboard
   └── Interactive Streamlit dashboard
```
## Dashboard Features

Dashboard menggunakan tema **Luxury Dark Beauty** dengan aksen Rose Gold — terinspirasi dari estetika brand premium beauty.

| Halaman | Konten |
|---|---|
| Overview | KPI cards, category distribution, price segments, performance matrix |
| Brand Analysis | Top brands by products/rating/loves, brand bubble chart |
| Price Intelligence | Price distribution, category pricing, price vs rating analysis |
| Ratings & Popularity | Rating distribution, top loved & top rated products |
| Product Features | Highlights/claims ranking, boolean features, exclusive analysis |
| Skincare Deep Dive | Sub-category analysis, brand positioning, price intelligence |
| Product Explorer | Search & filter interaktif dengan sorting |

### Tools
| Tool | Fungsi |
|---|---|
| `pandas` + `numpy` | Data wrangling & feature engineering |
| `plotly` | Interactive visualization (dashboard) |
| `matplotlib` + `seaborn` | Static plots (notebook) |
| `streamlit` | Dashboard deployment |

---

## Key Findings

1. **Skincare (28.5%)** dan **Makeup (27.9%)** mendominasi katalog Sephora
2. **Median harga $35** menandakan mayoritas produk di segmen Mid ($25–50)
3. **Rata-rata rating 4.19/5** menunjukkan kualitas produk secara keseluruhan sangat tinggi
4. **Vegan (31%)** dan **Cruelty-Free (21%)** adalah klaim paling populer, tren ethical beauty
5. **Harga tidak berkorelasi** dengan rating (r ≈ 0.04)
6. Brand **SEPHORA COLLECTION** memiliki produk terbanyak (352 produk)

=======
### 1. Harga Bukan Penentu Kualitas
> **Korelasi harga vs rating hampir nol (r ≈ 0.04)**

Konsumen Sephora tidak menghubungkan harga dengan kualitas. Produk budget (<$25) memiliki rata-rata rating setara dengan produk luxury ($100–200). Ini menunjukkan bahwa **persepsi nilai, bukan harga yang mendorong kepuasan**.

### 2. Ethical Beauty adalah Tren Dominan
> **Vegan (31%) dan Cruelty-Free (21%) adalah klaim paling populer**

Lebih dari 1 dari 3 produk Sephora mengklaim vegan. Ini bukan sekadar tren melainkan sudah menjadi **ekspektasi dasar konsumen modern**, terutama di kategori skincare dan makeup.

### 3. Skincare Memimpin, Tapi Paling Kompetitif
> **Skincare = 28.5% katalog, median harga $38, avg rating 4.2★**

Skincare adalah kategori terbesar sekaligus paling padat kompetisi. Brand seperti CLINIQUE, Peter Thomas Roth, dan Kiehl's mendominasi dengan volume produk tinggi, namun brand niche seperti Kate Somerville justru unggul di rata-rata loves.

### 4. Reviews dan Loves Sangat Berkorelasi (r > 0.7)
> **Produk yang banyak diulas = produk yang banyak dicintai**

Engagement konsumen bersifat self-reinforcing, yakni produk dengan banyak ulasan mendapat lebih banyak visibility serta mendorong lebih banyak loves. Ini menciptakan **winner-takes-most dynamic** di platform.

### 5. Sephora Exclusive Punya Edge
> **Produk eksklusif Sephora memiliki avg rating lebih tinggi**

Dari 2.373 produk eksklusif (28% katalog), rata-rata rating sedikit lebih tinggi dibanding non-eksklusif. Hal ini mencerminkan **kurasi yang lebih ketat** dan **halo effect** dari label eksklusivitas.

### 6. Mid-Tier Mendominasi Volume, Luxury Mendominasi Engagement
> **43.6% produk di segmen Mid ($25–50), tapi avg loves tertinggi di Luxury**

Konsumen di segmen luxury lebih engaged lebih banyak loves dan reviews per produk, meskipun volume produknya lebih sedikit.

---

## Recommendation

### Untuk Brand / Product Manager:
1. **Prioritaskan ethical claims** — Vegan & Cruelty-Free bukan lagi diferensiasi, tapi syarat masuk pasar modern. Brand yang belum memiliki sertifikasi ini perlu roadmap yang jelas.

2. **Jangan compete on price** — Data menunjukkan harga tidak menentukan kepuasan. Fokuslah pada **product storytelling** dan **ingredient transparency** sebagai diferensiasi utama.

3. **Investasi di review generation awal** — Karena reviews dan loves berkorelasi kuat, strategi early-launch seharusnya agresif dalam mendorong ulasan pertama untuk memancing snowball effect.

4. **Skincare = peluang untuk niche brands** — Market besar tapi pemain niche dengan avg loves tinggi membuktikan bahwa **positioning yang tepat mengalahkan budget marketing besar**.

### Untuk Retail Strategist (Sephora):
5. **Perluas program Sephora Exclusive** — Produk eksklusif menunjukkan performa lebih baik. Ini bisa menjadi strategi untuk mempertahankan loyalitas pelanggan dari platform kompetitor.

6. **Price accessibility matters** — Dengan 43% produk di Mid tier, Sephora perlu memastikan budget segment tetap terwakili untuk menjaga breadth of customer base.

---

## Struktur Proyek

```
sephora-analysis/
├── app.py                    ← Dashboard Streamlit (Luxury Dark Theme)
├── sephora_analysis.ipynb    ← Jupyter Notebook EDA lengkap
├── product_info.csv          ← Dataset (Kaggle)
├── requirements.txt
└── .streamlit/
    └── config.toml
```

---

## Cara Menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 👤 Author

**Muhammad Rifai, S.Stat**
- GitHub: [@ahmadripai047](https://github.com/ahmadripai047)
- Instagram: [@ahmadripai_](https://instagram.com/ahmadripai_)
- LinkedIn: [in/muhammad-rifai047](https://linkedin.com/in/muhammad-rifai047)

---

*Portofolio | Analityfai | Dataset: Kaggle — Sephora Products and Skincare Reviews*
