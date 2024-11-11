a_text = "rag baby"


# alphabet = "ALPHBETCDFGIKMNOQRSUVWYZ".lower()

# encrypting a word


def rag_baby(text, direction=1, key=None):
    alphabet = "ALPHBETCDFGIKMNOQRSUVWYZ".lower()
    words_in_text = text.split(" ")
    encrypted_text_string = ""
    for word in words_in_text:
        letter_index = 0
        word_index = words_in_text.index(word) + 1
        encrypted_word_string = "" if word_index == 1 else " "
        for letter in word:
            if not letter.isalpha():
                encrypted_char = letter
            else:
                offset = letter_index + word_index
                letter_index += 1
                alphabet_char_index = alphabet.index(letter)
                encrypted_char = alphabet[((alphabet_char_index + direction * offset) % len(alphabet))]
            encrypted_word_string += encrypted_char
        encrypted_text_string += encrypted_word_string
    print(encrypted_text_string)




rag_baby("rag baby")
rag_baby("spm thdh",direction=-1)

def get_keyed_alphabet(key):
    common_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
    std_key = key.lower()
    translation_table = str.maketrans('', '', std_key)
    total_alphabet_string = key + common_alphabet.translate(translation_table)
    print(total_alphabet_string)


get_keyed_alphabet("amogus")
