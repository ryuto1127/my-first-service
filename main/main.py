import openai
import streamlit as st
import random

# OpenAI API キーを設定
openai.api_key = st.secrets["streamlit_secrets"]["api_key"]

# タイトルを設定
st.title("EmoArtify")

st.markdown("### By Ryuto")

# プロンプト最適化関数
def optimize_prompt_for_dalle(prompt):
    # 画像生成に適した形にプロンプトを変換
    completion = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3 を使用
        prompt=f"Rewrite this to be more vivid and detailed for image generation: {prompt}",
        max_tokens=60,
        n=1
    )
    return completion.choices[0].text.strip()

# セッション状態の初期化
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
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
        "current emotional state",
        "recent enjoyable activity",
        # 他のテーマを追加
    ]

    # 質問の数を num_questions に制限
    selected_themes = random.sample(question_themes, num_questions)

    # 選択されたテーマに基づいて質問を生成
    for theme in selected_themes:
        prompt = f"Please create a simple and engaging question about {theme}. ..."
        chat_response = openai.ChatCompletion.create(
            engine="text-davinci-003",  # GPT-3 を使用
            prompt=prompt,
            max_tokens=60,
            temperature=1.0,
            n=1
        )
        question = chat_response.choices[0].text.strip()
        st.session_state.questions.append(question)
        st.session_state.answers.append("")

# ユーザーからの回答を取得
for i in range(len(st.session_state.questions)):
    if st.session_state.questions:
        st.session_state.answers[i] = st.text_input(f"Question {i+1}: {st.session_state.questions[i]}", key=f"user_answer_{st.session_state.input_key}_{i}")

# すべての質問に回答がある場合に画像生成
if all(st.session_state.answers):
    # 各回答を最適化
    optimized_answers = [optimize_prompt_for_dalle(answer) for answer in st.session_state.answers]

    # 最適化された回答を組み合わせて一つのプロンプトを形成
    combined_prompt = " ".join(optimized_answers)

    # 組み合わせたプロンプトで画像生成
    if st.button("Create Image"):
        try:
            # 画像生成のために DALL-E API を使用
            response = openai.Image.create(
                engine="text-to-image-dall-e-3",  # text-to-image-dall-e-3 を使用
                prompt=combined_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            st.image(image_url)
        except openai.error.InvalidRequestError as e:
            st.error("エラーが発生しました。もう一度お試しください。")
        except Exception as e:
            st.error("予期せぬエラーが発生しました。後でもう一度お試しください。")
