# GitHub Actions

## Objetivo

Explorar o uso do [GitHub Actions](https://docs.github.com/en/actions) para teste em múltiplos sistemas operacionais e versões de linguagens de programação.

## Descrição

1. **Criar programa com testes no GitHub:** Crie um reposiórtio no GitHub. Implemente um pequeno programa (na linguagem de sua escolha) e escreva pelo menos 5 testes de unidade.
   
2. **Executar os testes no GitHub Actions**: Configure a ferramenta de CI/CD GitHub Actions executar os testes automaticamente a cada commit. No GitHub, você encontra exemplos sobre como utilizar o GitHub Actions em linguagens (https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing).

3. **Executar Actions nos sistemas operacionais Ubuntu, MacOS e Windows**: Configure o seu workflow do GitHub Actions para dar o build e testar o programa em três sistemas operacionais: Ubuntu, MacOS e Windows. 

4. **Executar Actions em pelo menos duas versões da linguagem de programação**: Configure o seu workflow do GitHub Actions para dar o build testar o programa em pelo menos duas versões da linguagem escolhida. 

## Submissão

Submeter no Moodle o link do último build com sucesso do GitHub Actions.
Por exemplo: https://github.com/Textualize/rich/actions/runs/18370672554

## Programa implementado

Este repositório contém um pequeno programa em Go chamado `gradecalc`.
Ele recebe notas numéricas, calcula a média, informa o conceito final e diz se o estudante foi aprovado ou reprovado.

Exemplo:

```bash
go run ./cmd/gradecalc 80 90 100
```

Saída esperada:

```text
Media: 90.00
Conceito: A
Status: aprovado
```

## Testes locais

Para executar os testes unitários:

```bash
go test -v ./...
```

Para verificar também se todos os pacotes compilam:

```bash
go build ./...
```

## GitHub Actions

O workflow está em `.github/workflows/go-ci.yml` e executa automaticamente em `push` e `pull_request`.

A matriz de CI testa todas as combinações abaixo:

| Sistema operacional | Versões do Go |
| --- | --- |
| Ubuntu | 1.25.x e 1.26.x |
| macOS | 1.25.x e 1.26.x |
| Windows | 1.25.x e 1.26.x |

Isso gera 6 execuções no total, cobrindo os 3 sistemas operacionais pedidos e 2 versões da linguagem.
