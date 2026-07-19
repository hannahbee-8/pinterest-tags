import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="pinterest tag generator", layout="centered")

st.title("pinterest tag generator")
st.write("generate and manage optimized pinterest tags for the aesthetic stickers niche.")

default_data = {
    "hyper realistic": [
        "hyper realistic stickers", "realistic sticker aesthetic", "3d sticker design", 
        "realistic printable stickers", "clear stickers aesthetic", "realistic vinyl stickers", 
        "detailed sticker art", "object stickers realistic"
    ],
    "reading": [
        "bookish stickers", "reading aesthetic stickers", "book lover sticker", 
        "kindle stickers aesthetic", "library sticker design", "reading journal stickers", 
        "book club stickers", "cozy reading stickers"
    ],
    "typography": [
        "typography stickers", "cool font stickers", "graphic design stickers", 
        "lettering stickers aesthetic", "y2k typography stickers", "bold text stickers", 
        "minimalist font stickers", "word art stickers"
    ],
    "quotes": [
        "quote stickers aesthetic", "inspirational quote stickers", "relatable quote stickers", 
        "short quotes stickers", "manifestation stickers", "daily reminder stickers", 
        "funny quote stickers", "positive vibe stickers"
    ],
    "base": [
        "aesthetic stickers", "sticker printable", "sticker shop", 
        "sticker design", "cute stickers", "journal stickers", 
        "laptop stickers", "scrapbook stickers"
    ]
}

if "tag_df" not in st.session_state:
    st.session_state.tag_df = pd.DataFrame(default_data)

st.subheader("edit tag database")
st.write("modify tags directly in the column categories below. add rows at the bottom to expand.")

edited_df = st.data_editor(st.session_state.tag_df, num_rows="dynamic", use_container_width=True)
st.session_state.tag_df = edited_df

csv = st.session_state.tag_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="download database csv",
    data=csv,
    file_name="pinterest_stickers_tags.csv",
    mime="text/csv"
)

st.subheader("generate tags")

all_categories = list(st.session_state.tag_df.columns)
selected_categories = st.multiselect("select categories to include", all_categories, default=all_categories)

available_tags = []
for col in selected_categories:
    column_tags = st.session_state.tag_df[col].dropna().tolist()
    cleaned_tags = [str(t).strip().lower() for t in column_tags if str(t).strip()]
    available_tags.extend(cleaned_tags)

available_tags = list(set(available_tags))

max_tags = max(1, len(available_tags))
num_tags = st.number_input("number of tags to generate", min_value=1, max_value=max_tags, value=min(10, max_tags))

if st.button("generate tags"):
    if not available_tags:
        st.warning("no tags available for the selected categories.")
    else:
        random.shuffle(available_tags)
        final_tags = random.sample(available_tags, min(num_tags, len(available_tags)))
        
        st.subheader("your tags")
        
        st.write("text format:")
        comma_separated = ", ".join(final_tags)
        st.code(comma_separated, language="text")
        
        st.write("hashtag format:")
        hashtags = " ".join([f"#{tag.replace(' ', '')}" for tag in final_tags])
        st.code(hashtags, language="text")

