import requests

def detectar_tag(dúvida):
    tags_comuns = [
        "python", "java", "javascript", "html", "css", "reactjs", "django",
        "git", "mysql", "sql", "c#", "c++", "node.js", "pandas", "flutter",
        "android", "spring", "kotlin", "typescript"
    ]

    for tag in tags_comuns:
        if tag in dúvida.lower():
            return tag
    return None


def buscar_perguntas(duvida, max_resultados=10):
    topico_tag = detectar_tag(duvida)

    # Parâmetros para a API
    params = {
        "order": "desc",
        "sort": "relevance",
        "intitle": duvida,
        "site": "stackoverflow"
    }

    if topico_tag:
        print(f"\n Tag detectada: {topico_tag}")
        params["tagged"] = topico_tag

    response = requests.get("https://api.stackexchange.com/2.3/search/advanced", params=params)
    perguntas = response.json()

    #Retorna primeiras perguntas
    return perguntas.get("items", [])[:max_resultados]


def main():
    entrada = input("Digite sua dúvida:\n").strip()
    print("\nBuscando perguntas relacionadas no Stack Overflow...\n")

    resultados = buscar_perguntas(entrada)

    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    #exibe resultados coletados
    print('Exibindo resultados aproximados para a sua dúvida:\n')
    for i, pergunta in enumerate(resultados, 1):
        print('#===================================================================#')
        print(f"{i}. {pergunta['title']}")
        print(f"Veja mais em:{pergunta['link']}")
        print('#===================================================================#\n')
if __name__ == "__main__":
    main()