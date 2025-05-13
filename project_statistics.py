import os
from collections import Counter

def contar_linhas_e_arquivos(diretorio_raiz="."):
    total_arquivos = 0
    total_linhas = 0
    linhas_por_arquivo = []
    contador_bibliotecas = Counter()

    for raiz, _, arquivos in os.walk(diretorio_raiz):
        for arquivo in arquivos:
            if arquivo.endswith(".py"):
                total_arquivos += 1
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    with open(caminho_completo, 'r', encoding='utf-8') as f:
                        linhas = f.readlines()
                        num_linhas = len(linhas)
                        total_linhas += num_linhas
                        linhas_por_arquivo.append(num_linhas)

                        for linha in linhas:
                            linha = linha.strip()
                            if linha.startswith("import "):
                                partes = linha.split()
                                if len(partes) >= 2:
                                    modulo = partes[1].split('.')[0]
                                    contador_bibliotecas[modulo] += 1
                            elif linha.startswith("from "):
                                partes = linha.split()
                                if len(partes) >= 2:
                                    modulo = partes[1].split('.')[0]
                                    contador_bibliotecas[modulo] += 1
                except Exception as e:
                    print(f"Erro ao ler {caminho_completo}: {e}")

    # Estatísticas de linhas por arquivo
    media = sum(linhas_por_arquivo) / len(linhas_por_arquivo) if linhas_por_arquivo else 0
    maximo = max(linhas_por_arquivo) if linhas_por_arquivo else 0
    minimo = min(linhas_por_arquivo) if linhas_por_arquivo else 0

    return {
        "arquivos": total_arquivos,
        "linhas": total_linhas,
        "media_linhas": media,
        "max_linhas": maximo,
        "min_linhas": minimo,
        "bibliotecas": contador_bibliotecas
    }

if __name__ == "__main__":
    stats = contar_linhas_e_arquivos()

    print(f"Arquivos .py: {stats['arquivos']}")
    print(f"Total de linhas: {stats['linhas']}")
    print(f"Média de linhas por arquivo: {stats['media_linhas']:.2f}")
    print(f"Arquivo mais longo: {stats['max_linhas']} linhas")
    print(f"Arquivo mais curto: {stats['min_linhas']} linhas")

    print("\n📚 Bibliotecas mais usadas:")
    for lib, count in stats['bibliotecas'].most_common(10):
        print(f"{lib}: {count}x")
