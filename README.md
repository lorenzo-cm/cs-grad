# Inteligência Artificial para o seu negócio

## Objetivo do sistema
Responder informações sobre o seu negócio a partir de informações fornecidas pelo cliente (pdf, site, forms).

Será desenvolvida uma aplicação com interface gráfica web focada em dialogar com clientes de determinado usuário do produto. O nosso usuário irá "contratar" nosso serviço e passar informações importantes do seu negócio, como por exemplo se tem estacionamento no local, quais horários o negócio fica aberto, se aceita pets, entre outros. A partir daí, o aplicativo web será um meio de comunicação entre os clientes do nosso usuário e um robô que responde as perguntas dos clientes de maneira fiel às informações do negócio fornecidas anteriormente. A grande vantagem é que o dono do negócio terá um suporte de 24 horas ao cliente e responderá satisfatoriamente a grande maioria das dúvidas. Além disso, caso o robô identifique que o tema é complexo demais para ser resolvido por ele, o robô direcionará o contato para humanos.

## Principais features
- Responde em linguagem natural e não repetitiva usando API do ChatGPT.
- Estrutura de chat aplicável em qualquer website.
- Compreensão de imagens e áudios.

## Membros da equipe
- Lorenzo Carneiro Magalhães - 2021031505 - Fullstack.
- Tomas Lacerda Muniz - 2021088116 - Fullstack.

## Tecnologias
### Python
- Pdfminer.
- Openai API.
- Pandas.

### JavaScript/TypeScript
- React Native, Tailwind e bibliotecas auxiliares (Frontend).
- Node.js (Backend).
- Python (Backend with OpenAI).

### PostgreSQL
- Banco de dados POSTGRESQL na AWS.
  
---

# BACKLOG

Como cliente, gostaria de me cadastrar no aplicativo

Como cliente, gostaria de fornecer as informações do meu negócio para serem usadas como banco de dados

Como cliente, gostaria de alterar as minhas informações pessoais e do meu negócio

Como usuário final, gostaria de entrar por um site

Como usuário final, gostaria de conversar com o chatbot especializado em certo negócio/empresa

Como usuário final, gostaria de poder mandar imagens e audios


# BACKLOG DO SPRINT
	
- Como cliente, gostaria de me cadastrar no aplicativo
	- integrar backend com sistema de login [Lorenzo]
	
- Como cliente, gostaria de fornecer as informações do meu negócio para serem usadas como banco de dados
	- Integrar informacoes do usuário, um arquivo pdf, com o backend [Tomas]
	
- Como cliente, gostaria de alterar as minhas informações pessoais e do meu negócio
	- configuracao de perfil atraves do node js com interacao com o front [Lorenzo]

- Como usuário final, gostaria de entrar por um site
	- fazer front end usando react [Lorenzo]
	- fazer backend para funcionamento do site usando node js usando express [Lorenzo]
	- fazer todo backend com api da openAi [Tomas]
	
- Como usuário final, gostaria de conversar com o chatbot especializado em certo negócio/empresa
	- para isso, deve-se integrar o front end do chat com uma db e com o backend do site [Lorenzo]
	
- Como usuário final, gostaria de poder mandar imagens e audios
	- integracao front e back para integracao de fotos e audios na interface [Lorenzo]
	- integracao com API da openAi [Tomas]
