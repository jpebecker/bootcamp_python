import pandas
dataframe_test = pandas.DataFrame(pandas.read_csv('nato_alphabet.csv').to_dict())
entry = input('Digite uma palavra para receber sua tradução fonética em NATO: ').strip().upper()
answerList = []
for l in entry:
    code = dataframe_test.loc[dataframe_test['letter'] == l, 'code']
    if not code.empty:
        answerList.append(code.values[0])
    else:
        answerList.append(f"[?{l}]")

print(answerList)