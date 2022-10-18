from Words import *

common_words = cdkkWords(8, common_words = True)
all_words = cdkkWords(word_length = 8, common_words = False)

found_words = common_words.match_pattern("^HOME[a-zA-Z]{4}$")
print(found_words)

found_words = all_words.match_pattern("^HOME[a-zA-Z]{4}$")
print(found_words)