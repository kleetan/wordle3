import pandas as pd
# Excelファイルからデータを読み込む
df = pd.read_excel('words.xlsx', sheet_name='Sheet1')

# 単語リストをCEFRレベル別に分けるための辞書
word_list = {
    'A1': [],
    'A2': [],
    'B1': [],
    'B2': [],
    'C1': [],
    'C2': []
}

# データフレームをループして辞書に単語を追加
for _, row in df.iterrows():
    word = row['単語']
    level = row['CEFRレベル']
    if level in word_list:
        word_list[level].append(word)

# セッションステートの初期化
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'A1'

if 'secret_word' not in st.session_state:
    st.session_state.secret_word = random.choice(word_list[st.session_state.difficulty])
    st.session_state.attempts = 0
    st.session_state.guessed_words = []
    st.session_state.feedbacks = []

st.title("Wordle Game")
st.write("Guess the 5-letter word:")

st.markdown("""
    正解と位置が一致する文字は緑、アルファベットが一致するが位置が違う文字は黄色、どちらも一致しない文字は赤で表示されます。
    """)

# ユーザーが難易度を選択できるようにする
st.sidebar.title("Select Difficulty Level")
difficulty = st.sidebar.radio("CEFR Level", ('A1', 'A2', 'B1', 'B2', 'C1', 'C2'))

if st.sidebar.button("Start Game"):
    st.session_state.difficulty = difficulty
    st.session_state.secret_word = random.choice(word_list[st.session_state.difficulty])
    st.session_state.attempts = 0
    st.session_state.guessed_words = []
    st.session_state.feedbacks = []

# フィードバックをより上部に大きく表示
if st.session_state.feedbacks:
    st.header("Feedback")
    st.markdown("<br>".join(st.session_state.feedbacks), unsafe_allow_html=True)

def get_feedback(guess, secret_word):
    feedback = [''] * 5
    secret_word_list = list(secret_word)
    for i in range(5):
        if guess[i] == secret_word[i]:
            feedback[i] = f'<span style="color:green; font-size:24px;">{guess[i].upper()}</span>'
            secret_word_list[i] = None
    for i in range(5):
        if feedback[i] == '' and guess[i] in secret_word_list:
            feedback[i] = f'<span style="color:orange; font-size:24px;">{guess[i].lower()}</span>'
            secret_word_list[secret_word_list.index(guess[i])] = None
    for i in range(5):
        if feedback[i] == '':
            feedback[i] = f'<span style="color:red; font-size:24px;">{guess[i].lower()}</span>'
    return feedback

# キーボードのレイアウトを定義
keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

# キーボード入力を保存するための変数
if 'current_guess' not in st.session_state:
    st.session_state.current_guess = ''

# キーボードを表示
for row in keys:
    cols = st.columns(len(row))
    for i, key in enumerate(row):
        if cols[i].button(key):
            if len(st.session_state.current_guess) < 5:
                st.session_state.current_guess += key.lower()

# バックスペースと送信ボタンを表示
if st.button("Backspace"):
    st.session_state.current_guess = st.session_state.current_guess[:-1]

if st.button("Submit"):
    if len(st.session_state.current_guess) == 5:
        st.session_state.attempts += 1
        st.session_state.guessed_words.append(st.session_state.current_guess)
        feedback = get_feedback(st.session_state.current_guess, st.session_state.secret_word)
        st.session_state.feedbacks.append(" ".join(feedback))

        if st.session_state.current_guess == st.session_state.secret_word:
            st.success(f"Congratulations! You guessed the word '{st.session_state.secret_word}' in {st.session_state.attempts} attempts.")
            st.session_state.current_guess = ''
        else:
            st.session_state.current_guess = ''
    else:
        st.error("Please enter a valid 5-letter word.")

# ユーザーの現在の入力を表示
st.text_input("Current Guess:", value=st.session_state.current_guess, key="current_input", disabled=True)
