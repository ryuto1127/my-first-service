import openai
import streamlit as st
import random

openai.api_key = st.secrets["streamlit_secrets"]["openai_api_key"]


# タイトルを設定
st.title("EmoArtify")

st.markdown("""
### By Ryuto
""")

# OpenAIのAPIキーを設定

# プロンプト最適化関数
def optimize_prompt_for_dalle(prompt):
    # 画像生成に適した形にプロンプトを変換
    optimized_prompt = openai.completions.create(model="text-davinci-003",
    prompt=f"Rewrite this to be more vivid and detailed for image generation: {prompt}",
    max_tokens=60)
    return optimized_prompt.choices[0].text.strip()

# セッション状態の初期化
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'show_create_image_button' not in st.session_state:
    st.session_state.show_create_image_button = False

# 質問の数
num_questions = 3

# 画像生成ボタン
if st.button("Let's Start"):
    st.session_state.input_key += 1
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.show_create_image_button = False

    # 質問のテーマ
    question_themes = [
    "current emotional state",
    "recent enjoyable activity",
    "favorite memory",
    "an interesting dream",
    "a personal achievement",
    "a beloved hobby",
    "a cherished childhood memory",
    "a place you'd love to visit",
    "a favorite season and why",
    "a relaxing activity",
    "a memorable book or movie",
    "an important life lesson",
    "a favorite animal and why",
    "an inspiring historical figure",
    "a beautiful scenery you've seen",
    "a goal or dream for the future",
    "a favorite cuisine or dish",
    "a memorable celebration or event",
    "an exciting adventure or experience",
    "a cherished family tradition",
    "a moment of pride",
    "a funny or embarrassing memory",
    "a favorite work of art",
    "a musical or theatrical performance",
    "a meaningful friendship",
    "a hobby you'd like to try",
    "a favorite sport or game",
    "a moment of unexpected joy",
    "a person who has influenced your life",
    "a favorite city or country",
    "a historical event you find fascinating",
    "a technological innovation you admire",
    "a book or movie that changed your perspective",
    "a challenging experience and how you overcame it",
    "a dream vacation destination",
    "a moment of peace",
    "a favorite childhood activity",
    "an object with sentimental value",
    "a recent learning experience",
    "an outdoor experience you enjoyed"
    ]

    # 質問の数をnum_questionsに制限
    selected_themes = random.sample(question_themes, num_questions)

    # 選択されたテーマに基づいて質問を生成
    for theme in selected_themes:
        prompt = f"Please create a simple and engaging question about {theme}. The question should be easy to answer and encourage a detailed response.Please create questions using only simple English words and straightforward phrasing. The questions should be easy to understand, using basic vocabulary and clear sentence structures. Avoid complex terms, technical jargon, and lengthy explanations. Focus on direct and concise wording to ensure clarity and ease of comprehension. The goal is to generate questions that are accessible to users with varying levels of English proficiency."
        chat_response = openai.completions.create(model="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        temperature=1.0)
        question = chat_response.choices[0].text.strip()
        st.session_state.questions.append(question)
        st.session_state.answers.append("")

# ユーザーからの回答を取得
if st.session_state.questions:
    for i in range(len(st.session_state.questions)):
        answer = st.text_input(f"Question {i+1}: {st.session_state.questions[i]}", key=f"user_answer_{st.session_state.input_key}_{i}")
        st.session_state.answers.append(answer)

# すべての質問に回答があるかチェック
if all(st.session_state.answers) and not st.session_state.show_create_image_button:
    st.session_state.show_create_image_button = True

if st.session_state.show_create_image_button:
    optimized_answers = [optimize_prompt_for_dalle(answer) for answer in st.session_state.answers]

    # 最適化された回答を組み合わせて一つのプロンプトを形成
    combined_prompt = " ".join(optimized_answers)

    # 組み合わせたプロンプトで画像生成
    if st.button("Create Image"):
        response = openai.images.generate(prompt=combined_prompt,
        n=1,
        size="1024x1024",
        model="dall-e-3")
        image_url = response.data[0].url
        st.image(image_url)

