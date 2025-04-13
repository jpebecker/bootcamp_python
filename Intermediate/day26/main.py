import pandas
dataframe_test = pandas.DataFrame(pandas.read_csv('nato_alphabet.csv').to_dict())
answerList = []
def translate():
    entry = input('Digite uma palavra para receber sua tradução fonética em NATO: ').strip().upper()

    for l in entry:
        code = dataframe_test.loc[dataframe_test['letter'] == l, 'code']
        if not code.empty:
            answerList.append(code.values[0])
        else:
            print('*\n'*10)
            print('Valor inserido não faz parte do alfabeto!')
            return

    print(answerList)

while True:
    translate()
    answerList.clear()