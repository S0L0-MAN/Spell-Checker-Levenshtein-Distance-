import streamlit as st
import nltk
from nltk.corpus import words

# Download the word list once
nltk.download('words')

# Load word list
word_list = words.words()

def levenshteinDista(s1, s2, len1, len2):
    dp = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i

    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],     # deletion
                    dp[i][j - 1],     # insertion
                    dp[i - 1][j - 1]  # replacement
                )

    return dp[len1][len2]

# --- Streamlit UI ---
st.title("Spell Checker Using Levenshtein Distance Algorithm")
st.write("Enter a word and we'll suggest the most similar valid words using minimum edit distance.")

user_input = st.text_input("Enter a word:")

if user_input:
    user_input = user_input.lower()

    suggestions = []

    for word in word_list:
        distance = levenshteinDista(user_input, word.lower(), len(user_input), len(word))
        suggestions.append((word, distance))

    # Sort by distance, then alphabetically
    suggestions.sort(key=lambda x: (x[1], x[0]))

    # Get top 5 suggestions
    top_matches = suggestions[:5]

    st.subheader("🔍 Did you mean:")
    for match in top_matches:
        st.write(f"- {match[0]}  (distance: {match[1]})")
