#TEXT to MORSE CODE converter

morse_dict = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
    'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
    'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
    'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
    'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/'
}

valid_chars = set(morse_dict.keys()) #set the valid chars for only the ones in dict keys
entry = input('Write down your text to convert in morse code:\n').lower()
valid_entry = ''.join(char for char in entry if char in valid_chars)
#print(valid_entry)
m_code = ''
for L in valid_entry:
    m_code += morse_dict[L]

print(f'Your morse code for "{valid_entry}" is:\n"{m_code}"')