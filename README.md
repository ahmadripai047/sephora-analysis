# Sephora Products & Skincare Analytics

> **Exploratory Data Analysis + Interactive Dashboard**

[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20beff?logo=kaggle&logoColor=white)](https://kaggle.com)
[![Plotly](https://img.shields.io/badge/Viz-Plotly-3d4db7?logo=plotly&logoColor=white)](https://plotly.com)

---

## Deskripsi Dataset

Dataset berasal dari Kaggle: **"Sephora Products and Skincare Reviews"** yang berisi **8.494 produk** dari platform Sephora — salah satu retailer beauty terbesar di dunia.

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

## Struktur Proyek

```
sephora-analysis/
├── app.py                    ← Dashboard Streamlit (Luxury Dark Theme)
├── sephora_analysis.ipynb    ← Jupyter Notebook EDA
├── product_info.csv          ← Dataset dari Kaggle
├── requirements.txt
└── .streamlit/
    └── config.toml           ← Tema dark luxury
```

---

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

---

## 🚀 Cara Menjalankan

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan dashboard
streamlit run app.py

# Buka notebook
jupyter notebook sephora_analysis.ipynb
```

---

## Key Findings

1. **Skincare (28.5%)** dan **Makeup (27.9%)** mendominasi katalog Sephora
2. **Median harga $35** — mayoritas produk di segmen Mid ($25–50)
3. **Rata-rata rating 4.19/5** — kualitas produk secara keseluruhan sangat tinggi
4. **Vegan (31%)** dan **Cruelty-Free (21%)** adalah klaim paling populer — tren ethical beauty
5. **Harga tidak berkorelasi** dengan rating (r ≈ 0.04)
6. Brand **SEPHORA COLLECTION** memiliki produk terbanyak (352 produk)

---

## Tech Stack

```python
pandas      # Data manipulation
numpy       # Numerical computing
plotly      # Interactive visualizations
streamlit   # Dashboard framework
matplotlib  # Static plots (notebook)
seaborn     # Statistical viz (notebook)
```

---

## 👤 Author

**Muhammad Rifai, S.Stat**
- GitHub: [@ahmadripai047](https://github.com/ahmadripai047)
- Instagram: [@ahmadripai_](https://instagram.com/ahmadripai_)
- LinkedIn: [in/muhammad-rifai047](https://linkedin.com/in/muhammad-rifai047)

---

*📚 Portofolio | Dataset: Kaggle — Sephora Products and Skincare Reviews*
