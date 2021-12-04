from spellchecker import SpellChecker
# Module containing word frequency list
spell = SpellChecker()

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def break_cipher(text):
    letters = list(text)
    newWords = []
    for i in range(0,26):
        newWord = []
        for letter in letters:
            originalIndex = alphabet.index(letter)
            newIndex = originalIndex + i
            if newIndex > 25:
                newWord.append(alphabet[newIndex - 26])
            else:
                newWord.append(alphabet[newIndex])
        newWords.append(newWord)
    foundWords = []

    for combination in newWords:
        word = ''.join(combination)
        # Check if word is in word frequency list
        if word in spell:
            foundWords.append(word)
    return foundWords[0]

# Using example HELLO encrypted to URYYB
print(break_cipher('URYYB'))