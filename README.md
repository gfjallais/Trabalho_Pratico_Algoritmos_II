# Compressão de Texto com Algoritmo LZ78

Este projeto é uma implementação do algoritmo de compressão de texto LZ78, utilizando como dicionário do algoritmo uma árvore de prefixos (Trie padrão). O objetivo é reduzir o tamanho de arquivos de texto, economizando espaço em armazenamento e transmissão.

## Como funciona

O algoritmo implementado utiliza uma estrutura de dados chamada Trie para identificar e codificar sequências de caracteres repetidos no texto. A codificação gera um dicionário de pares (índice, caractere), onde o índice é um valor numérico que representa a sequência de caracteres repetidos.

Ao comprimir um arquivo de texto, o algoritmo percorre o texto e adiciona cada novo caractere encontrado à Trie. Quando uma sequência de caracteres repetidos é identificada, o algoritmo adiciona o par (índice, próximo caractere) ao dicionário e continua a busca a partir do próximo caractere.

A descompressão é realizada a partir do dicionário gerado durante a compressão. O algoritmo percorre o dicionário e substitui cada índice pela sequência de caracteres correspondente.

## Como usar

Para utilizar o algoritmo de compressão, basta executar o script `TP_ALG2.py` com a flag `-c` e informar o caminho do arquivo de texto que deseja comprimir:

```
python3 TP_ALG2.py -c input.txt output.z78
```

O arquivo comprimido será gerado com o nome `output.z78`.

Para descomprimir o arquivo, execute o script `python3` com a flag `-x` e informe o caminho do arquivo comprimido:

```
python3 TP_ALG2.py -x input.z78 output.txt
```

O arquivo descomprimido será gerado com o nome `output.txt`.

Os arquivos de output não precisam ser informados, neste caso serão gerados arquivos .z78 e .txt, em cada caso, com o nome do arquivo de entrada decrescido da extensão

## Resultados

Foram realizados testes de compressão em 10 arquivos de texto obtidos do projeto Gutenberg, com tamanhos entre 168K e 860K bytes. A taxa de compressão média obtida foi de 22,22%. É importante ressaltar que a eficiência do algoritmo pode variar de acordo com o tipo de texto que está sendo comprimido.

## Autores

Este projeto foi desenvolvido por Gabriel Franco Jallis como parte da discipla de Algoritmos II da UFMG.
