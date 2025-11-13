# Importing essential libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from collections import Counter

file_path = r"C:\Users\Brian\Desktop\PLP\data\metadata.csv"

try:
    df = pd.read_csv(file_path)
    st.write("File loaded successfully ✅")
except PermissionError:
    st.error("Permission denied: cannot read the CSV file. Please check file permissions.")
except FileNotFoundError:
    st.error("File not found: make sure the path is correct.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Display the first few rows
df.head()
# Shape of the dataset (rows, columns)
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])
# Display column names and their data types
print("\nData types of each column:")
print(df.dtypes)
# Count missing values in each column
print("\nMissing values in each column:")
print(df.isnull().sum())
important_cols = ['title', 'authors', 'journal', 'year', 'abstract']
print("\nMissing values in key columns:")
print(df[important_cols].isnull().sum())
# Generate summary statistics for numeric columns
print("\nBasic statistics for numerical columns:")
print(df.describe())
print("\nGeneral information about the dataset:")
df.info()
# Count missing values in each column
missing_values = df.isnull().sum().sort_values(ascending=False)

# Calculate percentage of missing values
missing_percent = (missing_values / len(df)) * 100

# Combine both into a single table
missing_table = pd.DataFrame({
    'Missing Values': missing_values,
    'Percent (%)': missing_percent.round(2)
})

print("Missing values summary:")
print(missing_table.head(15))  # show top 15 columns with most missing values
# Drop columns with more than 80% missing values
threshold = 0.8
df_clean = df.loc[:, df.isnull().mean() < threshold]

# Drop rows missing essential information
df_clean = df_clean.dropna(subset=['title', 'abstract', 'publish_time'])

print("New shape after cleaning:", df_clean.shape)
# Convert publish_time to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Verify conversion
print(df_clean['publish_time'].head())
# Extract year from publish_time
df_clean['year'] = df_clean['publish_time'].dt.year

# Check the most common years
print(df_clean['year'].value_counts().sort_index())
# Create a new column for abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].fillna("").apply(lambda x: len(x.split()))

# Display example
df_clean[['title', 'abstract_word_count']].head()
# Check if missing values are handled
print("\nRemaining missing values in cleaned data:")
print(df_clean.isnull().sum().sort_values(ascending=False).head(10))

# Preview final cleaned dataset
df_clean.head()
# Count number of papers per year
papers_per_year = df_clean['year'].value_counts().sort_index()

print("Number of papers published each year:")
print(papers_per_year)
plt.figure(figsize=(10,5))
sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o")
plt.title("Number of COVID-19 Research Papers Over Time", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.tight_layout()
plt.show()
# Count top 10 journals
top_journals = df_clean['journal'].value_counts().head(10)

print("Top Journals Publishing COVID-19 Research:")
print(top_journals)
plt.figure(figsize=(10,5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title("Top 10 Journals Publishing COVID-19 Research", fontsize=14)
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.tight_layout()
plt.show()

# Combine all titles into one large string
titles = " ".join(df_clean['title'].dropna()).lower()

# Remove punctuation and numbers
titles = re.sub(r'[^a-z\s]', '', titles)

# Split into words
words = titles.split()

# Count frequency
word_freq = Counter(words)

# Get the 15 most common words
common_words = word_freq.most_common(15)
print("Most frequent words in titles:")
print(common_words)
words, counts = zip(*common_words)
plt.figure(figsize=(10,5))
sns.barplot(x=list(counts), y=list(words), palette="cool")
plt.title("Most Frequent Words in Paper Titles", fontsize=14)
plt.xlabel("Frequency")
plt.ylabel("Word")
plt.tight_layout()
plt.show()
# Generate word cloud
wordcloud = WordCloud(width=1000, height=600, background_color='white').generate(" ".join(words for words in df_clean['title'].dropna()))

plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Paper Titles", fontsize=14)
plt.show()
if 'source_x' in df_clean.columns:
    source_col = 'source_x'
elif 'source' in df_clean.columns:
    source_col = 'source'
else:
    source_col = None

if source_col:
    top_sources = df_clean[source_col].value_counts().head(10)

    plt.figure(figsize=(10,5))
    sns.barplot(x=top_sources.values, y=top_sources.index, palette="magma")
    plt.title("Top Sources of COVID-19 Research Papers", fontsize=14)
    plt.xlabel("Number of Papers")
    plt.ylabel("Source")
    plt.tight_layout()
    plt.show()
else:
    print("No source column found in dataset.")
