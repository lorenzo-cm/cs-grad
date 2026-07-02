# Trabalho Prático - Agentes de IA

Sistema de atendimento automatizado para o setor imobiliário.

O objetivo do projeto é atender interessados em imóveis de forma automática, responder dúvidas sobre o catálogo, qualificar leads, sugerir próximos passos e encaminhar o usuário para um vendedor humano quando necessário. A solução usa um agente com LLM, ferramentas de busca no catálogo, envio de mídia, moderação de conteúdo e recuperação híbrida de informação com RAG.

## Visão Geral

O fluxo principal foi pensado como um funil de atendimento:

1. contato inicial;
2. resposta objetiva sobre o imóvel;
3. nutrição e qualificação do lead;
4. sugestão de agendamento ou transferência para humano.

O agente conversa com o usuário via Chatwoot/WhatsApp, consulta dados do catálogo de imóveis, recupera trechos relevantes com RAG e pode enviar texto, fotos, vídeos e documentos.

## Stack E Infraestrutura

- FastAPI para a API principal.
- PostgreSQL para dados de usuários, conversas e catálogo.
- Redis para cache e fila.
- Celery para tarefas assíncronas, como reindexação.
- Qdrant para busca vetorial do catálogo.
- BM25 para a parte lexical do RAG.
- Cloudflare R2 para mídia e documentos.
- OpenAI e Anthropic para o agente.
- OpenAI ou ElevenLabs para transcrição de áudio.
- OpenAI Moderation para filtro NSFW.
- Docker para subir a infraestrutura local.

## Como Rodar Localmente

### 1. Instalar dependências

```sh
uv sync
```

### 2. Subir a infraestrutura

O projeto depende de PostgreSQL, Redis e Qdrant.

```sh
docker compose up -d postgres redis qdrant
```

Se quiser processar tarefas assíncronas localmente também, suba o worker:

```sh
docker compose up -d worker
```

### 3. Configurar o `.env`

Copie `.env.example` para `.env` e ajuste os valores.

```sh
cp .env.example .env
```

O arquivo de exemplo já está organizado por blocos. As variáveis principais são:

- `ENVIRONMENT` -> Obrigatório (`local` ou `prod`)
- `SECRET_KEY` -> Obrigatório
- `JWT_SECRET_KEY` -> Obrigatório
- `DATABASE_URL` -> Obrigatório
- `R2_ENDPOINT_URL`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME`
- `R2_PUB_URL`
- `CHATWOOT_API_URL`
- `CHATWOOT_API_KEY`
- `CHATWOOT_ACCOUNT_ID`
- `CHATWOOT_INBOX_ID`
- `REDIS_HOST`
- `REDIS_PORT`
- `NSFW_PROVIDER`
- `QDRANT_URL`
- `OPENAI_API_KEY` -> Obrigatório (ou usar a chave da Anthropic)

As demais variáveis no `.env.example` também são válidas e podem ser ativadas para outras configurações ou funcionalidades, como valores da Anthropic, transcrição via ElevenLabs, ajustes do RAG ou Celery. O principal é configurar o banco de dados e acesso a alguma LLM. Embora seja recomendado a configuração do Chatwoot, o sistema funciona sem ele, mas não é possível receber mensagens de WhatsApp.

### 4. Executar a aplicação

```sh
bash ./scripts/run.sh
```

A aplicação sobe em `http://localhost:8000` por padrão, ou então fazendo:

```sh
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Etapas opcionais mas que melhoram a experiência

### 1. Chatwoot

O chatwoot é fundamental para o fluxo de atendimento. As chamadas de APIs podem ocorrer localmente via `curl`, porém para integração com o Whatsapp, essas etapas precisam ser feitas:

- O serviço do Chatwoot precisa estar em execução.
- O Chatwoot precisa estar configurado com o WhatsApp (dentro do painel de configurações da Meta)
- Dentro do Chatwoot, é necessário criar uma conta, caixa de entrada com telefone alvo além de configurar o webhook para o sistema de atendimento ser notificado quando houver novas mensagens.

### 2. R2

O R2 é usado para armazenar mídia e documentos. Para usar, é necessário criar um bucket e configurar as variáveis de ambiente corretamente. É necessário criar um link de acesso público ao bucket, que será usado para gerar links de mídia e documentos. Não é necessário usar essa estrutura, basta adicionar os links das midias e documentos diretamente no catálogo da DB, mas o R2 é útil para centralizar o armazenamento e gerar links públicos de forma automática.

### 3. Seed do catálogo

Hoje temos um registro simples de imóveis somente para testes, mas o script `seed_buildings.py` pode ser usado para popular a base com dados externos. O script também pode reindexar o catálogo no Qdrant. 

### 4. Qdrant

O Qdrant é usado para busca vetorial do catálogo. Para usar, é necessário subir o container do Qdrant e configurar a variável de ambiente `QDRANT_URL`. O script `reindex_buildings.py` pode ser usado para reindexar o catálogo no Qdrant.

Ao subir o Qdrant, os documentos podem ser indexados em uma collection única. A busca combina embeddings para similaridade e BM25 para correspondência textual.

O sistema funciona sem isso usando apenas a database, porém a busca vetorialé mais precisa.

### 5. Áudio

O sistema pode receber áudios de WhatsApp, transcrevê-los e processá-los. Para isso, é necessário configurar as variáveis de ambiente com chaves de API para realizar a transcrição. Mesmo sem isso, a troca de mensagens ainda funciona (com o chatwoot funcionando corretamente).

### 6. Moderação

A etapa de moderação de conteúdo pode ser feita com a API da OpenAI caso as variáveis de ambiente forem definidas corretamente. Hoje temos os guardrails implementados em código, porém como uma etapa adicional é importante ter uma maior verificação do conteúdo.

## Funcionalidades

### RAG do catálogo

O catálogo pode ser indexado em uma collection única no Qdrant. A busca combina:

- embeddings para similaridade semântica;
- BM25 para correspondência textual.

Se `QDRANT_URL` estiver vazio, o serviço usa um backend em memória como fallback. Quando `OPENAI_API_KEY` estiver disponível, os embeddings usam OpenAI; caso contrário, há fallback determinístico local.

### Moderação e agente

- o agente principal pode usar OpenAI ou Anthropic;
- a transcrição pode usar OpenAI ou ElevenLabs;
- a moderação NSFW usa OpenAI Moderation quando habilitada.

## Seed E Reindex

Popular a base com dataset embutido:

```sh
uv run python scripts/seed_buildings.py --upsert --index-now
```

Popular a base com JSON externo:

```sh
uv run python scripts/seed_buildings.py --input ./buildings.json --upsert --index-now
```

Reindexar o catálogo inteiro:

```sh
uv run python scripts/reindex_buildings.py
```

## Tools

As tools de catálogo, mídia e qualificação cobrem:

- listar imóveis;
- buscar informações de um imóvel específico;
- buscar trechos relevantes no catálogo;
- enviar foto;
- enviar vídeo;
- enviar documento.

Além disso, o agente pode usar tools de qualificação e handoff para avançar o funil:

- registrar o imóvel de interesse do lead;
- marcar a qualidade do lead como `low`, `medium` ou `high`;
- transferir a conversa para atendimento humano quando houver intenção clara, negociação ou fora de escopo.

O objetivo é permitir que o agente responda dúvidas com conteúdo factual, conduza a qualificação do lead e só faça handoff quando fizer sentido comercial.

## Banco E Métricas

O banco foi definido com as seguintes tabelas:

- `users`: usuários internos que podem operar rotas protegidas;
- `buildings`: catálogo de imóveis -> Adpatado para etender esse dominio especifico do trabalho.
- `contacts`: contatos vindos do Chatwoot;
- `conversations`: conversa principal, com status, inbox e metadados;
- `conversation_participants`: vínculo entre conversa e participantes;
- `messages`: mensagens enviadas ou recebidas, incluindo texto, tool calls e respostas;
- `message_attachments`: anexos e mídia vinculados a mensagens;
- `conversation_metrics`: métricas do atendimento e do funil -> Usado especificamente nesse trabalho para coleta de resultados e desempenho geral.

As métricas guardam informação útil para análise do atendimento, como:

- `lead_quality`;
- `qualification_reason`;
- `final_outcome` (`retained`, `handoff`, `dropped`);
- uso de handoff humano;
- tempo de resposta;
- contagem de respostas;
- uso de tools.

## Guardrails

O pipeline inclui guardrails determinísticos para reduzir erros de atendimento:

- detecção de prompt injection na entrada;
- validação centralizada de tool calls;
- sanitização de saída antes de persistir ou responder.

## Observações

- Os dados do projeto usam exemplos artificiais para simular o contexto imobiliário (script `seed_buildings.py`).
- Algumas features e estrutura estão prontas para uso em produção em larga escala, porém no trabalho essas etapas foram feitas localmente (ex: existe a infraestrutura de filas e organização do container, porém o projeto foi testado localmente).
