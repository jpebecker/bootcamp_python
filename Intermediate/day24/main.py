
names_list = []
with open("Input/Names/invited_names.txt", mode='r') as names:
    names_list = [name.strip() for name in names]

for name in names_list:
    with open("Input/Letters/starting_letter.txt", mode='r') as initLetter:
        letter_contents = initLetter.read()
        personalized_letter = letter_contents.replace('[name]', name.strip())

    with open(f'Output/ReadyToSend/letter_to_{name.strip()}.txt', mode='w') as completed_letter:
        completed_letter.write(personalized_letter)