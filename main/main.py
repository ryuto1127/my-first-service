import openai
import streamlit as st
import random

# Streamlit secretsを介してAPIキーを設定
openai.api_key = st.secrets["openai"]["api_key"]

# タイトルを設定
st.title("EmoArtify")

# 著者情報の追加
st.markdown("""
### By Ryuto
""")

# プロンプト最適化関数
def optimize_prompt_for_dalle(prompt):
    # 画像生成に適した形にプロンプトを変換
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Rewrite this to be more vivid and detailed for image generation: {prompt}",
        max_tokens=60
    )
    return completion.choices[0].text.strip()

# セッション状態の初期化
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 質問の数
num_questions = 3

# 画像生成ボタン
if st.button("Let's Start"):
    st.session_state.input_key += 1
    st.session_state.questions = []
    st.session_state.answers = []

    # 質問のテーマ
    question_themes = [
        # テーマリスト...
    ]

    # 質問の数をnum_questionsに制限
    selected_themes = random.sample(question_themes, num_questions)

    # 選択されたテーマに基づいて質問を生成
    for theme in selected_themes:
        prompt = f"Please create a simple and engaging question about {theme}."
        chat_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            temperature=1.0
        )
        question = chat_response.choices[0].text.strip()
        st.session_state.questions.append(question)

# ユーザーからの回答を取得
for i, question in enumerate(st.session_state.questions):
    st.session_state.answers.append(st.text_input(f"Question {i+1}: {question}", key=f"user_answer_{st.session_state.input_key}_{i}"))

# すべての質問に回答がある場合に画像生成
if all(st.session_state.answers) and st.button("Create Image"):
    # 各回答を最適化
    optimized_answers = [optimize_prompt_for_dalle(answer) for answer in st.session_state.answers]

    # 最適化された回答を組み合わせて一つのプロンプトを形成
    combined_prompt = " ".join(optimized_answers)

    # 組み合わせたプロンプトで画像生成（DALL-E API使用例）
    # この部分は、OpenAIが提供するDALL-Eのエンドポイントと認証方法に基づいて実装してください。
