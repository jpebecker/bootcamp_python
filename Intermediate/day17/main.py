import random
import arts
from question import Question
from data import questions
######################################### final do quiz
def call_end(acertos):
    print('*' * 100)
    arts.EndQUIZ()
    print('VOCÊ CHEGOU AO FIM DO QUIZ')
    print(f'VOCÊ ACERTOU {acertos} QUESTÕES DE 30 NO TOTAL')
    print(f'SUA PORCENTAGEM DE ACERTOS FOI DE {round((acertos / 30) * 100, 2)}%')
    print('PARABÉNS!')
########################################### inicializando variaveis
acertos = 0
act_question = 0
erros = 0
############################################# Criando a lista de perguntas
banco_perguntas = [Question(q['pergunta'], q['resposta']) for q in questions]
random.shuffle(banco_perguntas)

##############################################titulo
arts.Title()
print('Começando as perguntas...\n')

######################################### Loop principal do quiz
while act_question < 30:
    print('*' * 30)
    print(f'QUESTÃO {act_question + 1}')
    print(f'ACERTOS: {acertos}/30')

    if act_question == 29:
        print('ÚLTIMA QUESTÃO:')

    pergunta_atual = banco_perguntas[act_question]
    print(pergunta_atual.text)
    entry = input('Verdadeiro ou Falso?\n').strip().lower()

    if entry == 'verdadeiro':
        entry = True
    elif entry == 'falso':
        entry = False
    else:
        print('Resposta não aceita. Chutando questão aleatoriamente...')
        entry = random.choice([True, False])

    if entry == pergunta_atual.answer:
        acertos += 1
    else:
        print('Você errou a questão!')
        erros += 1
        if erros > 15:
            print('\n' * 5)
            arts.EndGame()
            print('VOCÊ ERROU QUESTÕES DEMAIS!')
            break

    act_question += 1

    if act_question == 30:
        call_end(acertos)
        break