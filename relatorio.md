# Relatório Técnico: Pré-processamento Textual de Comentários - Legends of Etheria

## 1. Introdução
A PixelStorm Studios identificou um aumento considerável nas reclamações e avaliações negativas do seu título multiplayer "Legends of Etheria". O grande volume de dados não estruturados gerados diariamente pela comunidade dificulta a extração de insights por parte da equipe de análise de dados. Este relatório detalha a implementação de um sistema experimental de pré-processamento textual em Python, focado em transformar comentários ruidosos (contendo gírias, abreviações e erros) em dados estruturados para futuras análises de sentimento e mineração de texto.

## 2. Fundamentação Teórica
O Processamento de Linguagem Natural (PLN) é uma subárea da inteligência artificial que visa a interação entre computadores e linguagem humana. O pré-processamento é a etapa inicial crucial no pipeline de PLN, envolvendo:
- **Tokenização**: Segmentação do texto em unidades atômicas (tokens), geralmente palavras ou pontuação.
- **Remoção de Stopwords**: Descarte de palavras muito frequentes no idioma (como artigos e preposições) que não agregam valor semântico à análise.
- **Radicalização (Stemming)**: Processo heurístico de cortar prefixos e sufixos das palavras para reduzi-las ao seu radical.
- **Lematização**: Processo linguístico que considera o vocabulário e a análise morfológica para retornar a forma canônica da palavra (o lema).

## 3. Desenvolvimento
O projeto foi desenvolvido em Python, utilizando as bibliotecas `pandas` (para manipulação de dados), `nltk` e `spacy` (para PLN).
A base de dados utilizada foi a `metacritic_reviews.csv`, contendo comentários e notas simulando avaliações da plataforma Metacritic, elaborados para simular a linguagem característica de jogadores (com presença de termos como "lag", "bug", "p2w", além de abreviações e erros ortográficos).
O pipeline de processamento foi estruturado nas seguintes etapas:
1. Conversão para letras minúsculas e remoção de caracteres especiais/pontuações.
2. Tokenização da sentença através do `word_tokenize` (NLTK).
3. Filtragem de stopwords utilizando o corpus da língua portuguesa do NLTK.
4. Aplicação do `SnowballStemmer` (NLTK) aos tokens filtrados para obter seus radicais.
5. Utilização do modelo `pt_core_news_sm` (Spacy) para lematizar as palavras.

## 4. Resultados
A execução do código obteve êxito ao converter frases inteiras em listas estruturadas de palavras significativas.
Exemplo de processamento obtido:
- **Original**: "o novo update quebrou o jogo inteiro, crasha toda hora"
- **Tokens**: `['o', 'novo', 'update', 'quebrou', 'o', 'jogo', 'inteiro', 'crasha', 'toda', 'hora']`
- **Sem Stopwords**: `['novo', 'update', 'quebrou', 'jogo', 'inteiro', 'crasha', 'toda', 'hora']`
- **Stemming**: `['nov', 'updat', 'quebr', 'jog', 'inteir', 'crash', 'tod', 'hor']`
- **Lematização**: `['novo', 'update', 'quebrar', 'jogo', 'inteiro', 'crasha', 'todo', 'hora']`

É perceptível que a Lematização manteve o significado das palavras de forma muito mais legível (como transformar "quebrou" em "quebrar"), enquanto o Stemming produziu apenas prefixos genéricos ("quebr"). Termos próprios de jogos em inglês como "update" e "crasha" apresentaram desafios, mas o pipeline conseguiu isolá-los perfeitamente para possíveis customizações.

## 5. Conclusão

**1. Qual a importância do pré-processamento textual em aplicações de PLN?**
O pré-processamento elimina o ruído e padroniza o texto, reduzindo o espaço de características (features) que o modelo precisa aprender. Sem ele, variações de uma mesma palavra ou termos sem valor semântico comprometeriam a eficiência e precisão das análises automatizadas.

**2. Quais dificuldades foram encontradas ao trabalhar com comentários de jogadores?**
A principal dificuldade reside no jargão não padronizado (como "p2w", "nerfaram", "crasha") e uso de gírias/abreviações ("mt", "pqp", "pls"). Como essas palavras geralmente não existem nos vocabulários oficiais ou nos dicionários internos das ferramentas, técnicas tradicionais como lematização tendem a falhar ou retornar o próprio token original, exigindo etapas adicionais de normalização (como dicionários customizados).

**3. Qual a diferença prática entre stemming e lematização?**
Na prática, o stemming é mais rápido, porém agressivo e não linguístico, apenas "cortando" o final das palavras e podendo gerar palavras inexistentes (ex: "inteiro" -> "inteir"). A lematização é um processo morfológico mais complexo e lento, que considera o contexto gramatical para converter a palavra à sua forma base ou dicionário (ex: "inteiro" -> "inteiro", "quebrou" -> "quebrar"). 

**4. Como o pré-processamento pode auxiliar empresas de jogos digitais?**
Ao estruturar comentários, as empresas podem aplicar modelos de *Análise de Sentimentos* ou *Modelagem de Tópicos* com maior precisão para descobrir automaticamente quais são as principais queixas dos jogadores. A PixelStorm Studios pode, por exemplo, quantificar rapidamente que o tópico "lag" ou "balanceamento" é a causa principal da recente onda de avaliações negativas.

## 6. Referências
- BIRD, Steven; KLEIN, Ewan; LOPER, Edward. Natural Language Processing with Python. O'Reilly Media, 2009.
- HONNIBAL, Matthew; MONTANI, Ines. spaCy 2: Natural language understanding with Bloom embeddings. 2017.
