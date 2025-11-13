# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Page title
st.title("CORD-19 Research Dataset Explorer 🧬")
st.markdown("""
Explore trends and insights from the COVID-19 Open Research Dataset (CORD-19).
This dashboard allows you to view publication trends, top journals, and common research topics.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Brian\Desktop\PLP\data\metadata.csv")
    # Basic cleaning
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))
    return df

df = load_data()

# Sidebar controls
st.sidebar.header("Filter Options")
years = sorted(df['year'].dropna().unique())
selected_years = st.sidebar.multiselect("Select publication year(s):", years, default=years)
df_filtered = df[df['year'].isin(selected_years)]

# Display data sample
st.subheader("📋 Dataset Preview")
st.write(df_filtered.head())

# Number of papers per year
st.subheader("📈 Number of Publications per Year")
papers_per_year = df_filtered['year'].value_counts().sort_index()

fig1, ax1 = plt.subplots()
sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o", ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
ax1.set_title("Publications Over Time")
st.pyplot(fig1)

# Top journals
st.subheader("🏛️ Top Journals Publishing COVID-19 Research")
top_n = st.slider("Select number of top journals to display", 5, 20, 10)
top_journals = df_filtered['journal'].value_counts().head(top_n)

fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
st.pyplot(fig2)

# Word cloud of titles
st.subheader("☁️ Word Cloud of Paper Titles")
titles = " ".join(df_filtered['title'].dropna().tolist())
if titles.strip():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)
    fig3, ax3 = plt.subplots()
    ax3.imshow(wordcloud, interpolation="bilinear")
    ax3.axis("off")
    st.pyplot(fig3)
else:
    st.warning("No titles available to generate word cloud.")

# Paper count by source (if available)
source_col = None
for col in df_filtered.columns:
    if "source" in col.lower():
        source_col = col
        break

if source_col:
    st.subheader("📚 Paper Distribution by Source")
    top_sources = df_filtered[source_col].value_counts().head(10)
    fig4, ax4 = plt.subplots()
    sns.barplot(x=top_sources.values, y=top_sources.index, palette="magma", ax=ax4)
    ax4.set_xlabel("Number of Papers")
    ax4.set_ylabel("Source")
    st.pyplot(fig4)
else:
    st.info("No source column found in this dataset.")
