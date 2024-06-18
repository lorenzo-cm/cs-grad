## 1- kernel/syscall.h

- add syscall settickets and getpinfo
- update number of syscalls

## 2- kernel/syscall.c

OBS: Aqui percebo que possivelmente fiz um erro no último trabalho, pois fiz uma definição de variável em syscall.h, mas aparentemente as definições ficam em defs.h por padrão, mas deixarei em syscall.h por desconhecimento e facilidade de acesso/mudança

- add the protoype functions for each syscall
- add the functions to the map array that maps the syscall number to the syscall function

## 3- kernel/sysproc.c

OBS: colocando a implementação das duas funções aqui pois aparentemente esse arquivo engloba funcionalidades relacionadas aos processos

- comecei a implementar mas não sei se está correto, pois não é possível incrementar os tickets recebendo apenas com um parâmetro de número de tickets
- movi para a próxima etapa sem concluir essa

## 4- kernel/proc.c

- O professor indicou esse arquivo, o que me levou a mudanças no proc.h

## 5- kernel/proc.h

- Adicionei o campo tickets na struct proc

## 6- kernel/proc.c

- descobri como era feita a implementação do argint, que basicamente recebe um número e um endereço de memória. Esse número pode ir de 0 a 7, que representa os registradores de argumentos do RISC V. O registrador é escolhido através da função argraw, que acessa os registradores do trapframe. Após o retorno do argraw, ele atribui o valor do registrador de parâmetro de função para o endereço de memória passado como segundo parâmetro

- entendi como funciona o escalonador e as funções auxiliares: **mycpu**, que retorna um struct com informações da cpu atual, incluindo o processo que está sendo executado no momento, e da função **myproc**, que usa a função mycpu para retornar um struct com informações do atual processo

- entendendo isso, consigo acabar a função sys_settickets

## 7- kernel/sysproc.c

- terminei de implementar sys_settickets com auxílio da função myproc
- fiz o esqueleto da função sys_getpinfo de maneira a retornar sempre 0 para teste

## 8- kernel/proc.c

#### PROC TICKETS

- Tentativa de implementar o lottery scheduler: percebi a existência de um array proc, que armazena os processos a serem escalonados (percebi que apenas 64 procesos podem estar na fila de escalonamento; não seria pouco?)

- lembrei que teria que inicializar cada ticket por default com 1 e procurei na internet e descobri que o allocproc era o que estava procurando. Percebi que o processo seria um pouco complicado pois teria que mudar no fork também.

- terminei a implementação e considerei que processos filhos herdam os tickets do pai, conforme enunciado

#### SCHEDULER

- Realizei a implementação do scheduler, mas não entendi a linha c->proc = 0 depois do context switch, pois para mim já estaria zero por causa dessa mesma linha no início da função

### 9- user/usys.pl

- Adicionei as novas entradas com as novas funções

### 10- user/user.h

- Definição dos cabeçalhos das novas funções de chamada de sistema

### 11- user/settickets.c

- Implementação da função na área do usuário

### 12- user/getpinfo.c

- Implementação de uma função de teste

### 13- Testes

- Falhou, pois a função rand da stdlib aparentemente está definida somente quando se compila pelo gcc, portanto farei uma personalizada

- Falhou novamente ao executar as funções em ambiente de usuário, dessa vez não sei o porque, mas aparentemente o escalonador funcionou, pois as outras sys calls funcionam

- Achei o erro, não havia adicionado ao UPROG do Makefile. Após isso o código de usuário falhou na compilação, mas ao menos foi executado. Assim, consertei os pequenos erros nos códigos do usuário