# Trabalho Prático de Introdução a Ciência dos Dados

### Integrantes:
- Bruno Henrique Evangelista Pereira
- Francisco Teixeira Rocha Aragão
- Lorenzo Carneiro Magalhaes
- Tomas Lacerda Muniz
- Victor de Almeida Nunes Murta

### Objetivo
Analisar como os usuários do twitter encaram o chatGPT, de modo que também seja analisado esse fato ao longo do tempo e conforme localização geográfica.

<hr>

### Análise Exploratória dos Dados

Nessa segunda etapa do trabalho sobre o tema: **Como estão as reações sobre o ChatGPT no twitter?**

Buscamos realizar a análise exploratória dos dados para entender melhor o principal dataset selecionado, além de iniciar os preparativos para algumas funções que serão úteis para o desenvolvimento do trabalho.

Primeiramente, aumentamos a base de dados utilizando algumas fontes complementares, referenciadas a seguir: 

- [ChatGPT-1000-daily-tweets](https://www.kaggle.com/datasets/edomingo/chatgpt-1000-daily-tweets)

- [500k-chatGPT-tweets-jan-mar-2023](https://www.kaggle.com/datasets/khalidryder777/500k-chatgpt-tweets-jan-mar-2023)

- [Tweets-chatGPT](https://www.kaggle.com/datasets/manishabhatt22/tweets-onchatgpt-chatgpt)

- [chatGPT-twitter-dataset](https://www.kaggle.com/datasets/tariqsays/chatgpt-twitter-dataset)

Tal decisão foi motivada visto que a database selecionada primeiramente continha relativamente poucos dados, então buscamos novas fontes razoavelmente semelhantes a original contendo atributos importantes, como número de retweets, conteúdo do tweet, quantidade de likes, entre outros.

Dessa forma, algumas ações sobre os dados foram feitas a partir do dataset mais completo (**ChatGPT-1000-daily-tweets**), tais análises estão no notebook `analiseInicial.ipynb` . Assim, foi feito uma filtragem inicial, retirando algumas colunas com informações que não são relevantes, como *user_id* e *user_created*, além de uma filtragem nos tweets; usamos apenas tweets com mais de 0 curtidas. Após isso, outras análises foram feitas, tendo em vista o idioma e a quantidade de curtidas juntamente da análise de sentimento e da tradução de tweets em diferentes idiomas, que podem ser acompanhadas melhor seguindo o notebook.

Além disso, outros arquivos também foram desenvolvidos nessa etapa, como o teste e utilização de algumas bibliotecas e funcionalidades que serão úteis futuramente. Como exemplo, foram feitos notebooks voltados para a utilizacao da biblioteca "vader" que faz a análise de sentimento dos conteúdos dos tweets. Além disso, tal funcionalidade foi feita testando diferentes conjuntos de frases, como textos em português, inglês e outras línguas. Tal fato é importante pois além de nos familiarizarmos com a análise de sentimento, também iniciamos o processo de tradução com a utilização da biblioteca do Google tradutor para fazer esse trabalho. Todas essas ações estão representadas nos notebooks apresentados.

<hr>

#### Para instalar as dependências:
```
cd src/utils
python3 installPackages.py
```

<hr>

### Instruções para desenvolvimento
 
Primeiramente, é interessante a criação de um ambiente virtual para tal.

Utilizando o anaconda, é possível criar um ambiente de desenvolvimento utilizando o comando:

```conda create --name tpICD python=3.10.11```

Para ativá-lo em sistemas baseados em unix digite:

```conda activate tpICD```

Além disso, é importante que o desenvolvimento siga essas regras:

- Sempre ao instalar novas bibliotecas inserir as dependências novas no arquivo `requirements.txt`
- Sempre atualizar o decorrer das tarefas na aba projects

    OBS: para inserir a dependência instalada basta, no ambiente virtual do trabalho, utilizar o comando:

```
pip freeze > requirements.txt
```