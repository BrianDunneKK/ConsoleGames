wordlist3 = []
wordlist4 = []
wordlist5 = []
wordlist6 = []
wordlist7 = []
wordlist8 = []
wordlist9 = []

with open("words_alpha.txt", newline='') as f:
    all_words = f.read().splitlines()

for word in all_words:
    if (len(word) == 3):
        wordlist3.append(word.upper())
    if (len(word) == 4):
        wordlist4.append(word.upper())
    if (len(word) == 5):
        wordlist5.append(word.upper())
    if (len(word) == 6):
        wordlist6.append(word.upper())
    if (len(word) == 7):
        wordlist7.append(word.upper())
    if (len(word) == 8):
        wordlist8.append(word.upper())
    if (len(word) == 9):
        wordlist9.append(word.upper())

with open('wordlist3.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(wordlist3))
with open('wordlist4.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(wordlist4))
with open('wordlist5.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(wordlist5))
with open('wordlist6.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(wordlist6))
with open('wordlist7.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(wordlist7))
with open('wordlist8.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(wordlist8))
with open('wordlist9.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(wordlist9))
