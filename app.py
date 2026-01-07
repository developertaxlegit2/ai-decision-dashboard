import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="AI Decision Dashboard", layout="wide")

st.title("📊 AI Decision Dashboard")
st.caption("Upload CSV → Get Dashboard + AI Decisions")

file = st.file_uploader("Upload your CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df)

    st.subheader("📈 Auto Charts")
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        st.line_chart(df[numeric_cols])

    st.subheader("🧠 AI Decisions")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
    You are a senior financial decision-making AI.

    Analyze the following CSV data:
    {df.head(50).to_csv(index=False)}

    Provide:
    1. Cash flow assessment
    2. Profit or loss summary
    3. Key risks
    4. Actionable decisions
    5. Executive summary
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a CFO decision agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    st.markdown(response.choices[0].message.content)
