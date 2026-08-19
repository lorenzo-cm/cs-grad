[![tests](https://github.com/andrehora/library/actions/workflows/tests.yml/badge.svg)](https://github.com/andrehora/library/actions/workflows/tests.yml)

# Library refactoring example - Parte 1

Neste exercício, iremos refatorar um sistema simples para aluguel de livros de uma biblioteca.
Este exercício é adaptado do livro Refactoring de Martin Fowler e Kent Beck.
Você deve realizar os commits descritos abaixo e submeter os links dos commits via Moodle.

### Overview

Primeiramente, explore o código do sistema em [model.py](https://github.com/andrehora/library/blob/main/model.py).
Note que temos três classes: `Book` (livros que podem ser alugados), `Rental` (dados de um aluguel) e `Client` (clientes da biblioteca).
A classe `Client` possui um método `statement`, responsável por gerar o recibo do aluguel para o cliente:

```python
    def statement(self) -> str:

        total_amount = 0
        frequent_renter_points = 0
        result = f"Rental summary for {self.name}\n"
        
        for rental in self._rentals:
            amount = 0
            
            # determine amounts for each line
            if rental.book.price_code == Book.REGULAR:
                amount += 2
                if rental.days_rented > 2:
                    amount += (rental.days_rented - 2) * 1.5
            elif rental.book.price_code == Book.NEW_RELEASE:
                amount += rental.days_rented * 3
            elif rental.book.price_code == Book.CHILDREN:
                amount += 1.5
                if rental.days_rented > 3:
                    amount += (rental.days_rented - 3) * 1.5

            # add frequent renter points
            frequent_renter_points += 1
            if rental.book.price_code == Book.NEW_RELEASE and rental.days_rented > 1:
                frequent_renter_points += 1

            # show each rental result
            result += f"- {rental.book.title}: {amount}\n"
            total_amount += amount
        
        # show total result
        result += f"Total: {total_amount}\n"
        result += f"Points: {frequent_renter_points}"
        return result
```

Reflita sobre os possíveis problemas do método `statement`:
- Esse método possui muitas responsabilidades?
- Como adicionar um novo tipo filme?
- Como adicionar um novo tipo de recibo, por exemplo, HTML, CSV, JSON, etc?

Explore também os testes em [tests.py](https://github.com/andrehora/library/blob/main/tests.py) para entender melhor como o sistema funciona.
Por exemplo, o teste `test_rent_regular_book_short_duration`:

```python
def test_rent_regular_book_short_duration():
    book = Book("Refactoring", Book.REGULAR)
    r = Rental(book, 2)

    c = Client("Fulano")
    c.add_rental(r)
    
    expected_report = (
        "Rental summary for Fulano\n"
        "- Refactoring: 2\n"
        "Total: 2\n"
        "Points: 1"
    )
    
    assert c.statement() == expected_report
```

# Commit 1: Running the tests

Antes de iniciar as atividades de refatoração, precisamos configurar o repositório de trabalho.

### Crie um fork deste repositório

Primeiramente, crie um fork deste repositório.
Para isso, basta clicar no botão `Fork` no canto superior direito.
Caso tenha dúvidas, verifique a documentação do GitHub sobre como [criar fork de um repositório](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

### Ative o GitHub Actions para rodar os testes a cada commit

Neste projeto, utilizamos o GitHub Actions (ferramenta de CI/CD do GitHub) para executar os testes automaticamente a cada commit.
Abra o arquivo`.github/workflows/tests.yml` e observe que os testes são executados em três sistemas operacionais (Ubuntu, macOS e Windows) e várias versões da linguagem Python. Veja um exemplo em https://github.com/andrehora/library/actions/runs/14231197771.

Ative o GitHub Actions no seu repositório.
Para isso, basta ir na aba `Actions` e clicar no botão verde.

### Clone o seu repositório

Em seguida, clone o seu repositório para uma pasta local e entre na pasta:

```
$ git clone https://github.com/<SEU-USUARIO>/library
$ cd library
```

### Instale o pytest

Nossos testes utilizam o framework de testes [pytest](https://docs.pytest.org).
Instale o pytest:

```
$ pip install pytest
```

### Rode os testes localmente

Para executar os testes localmente, basta rodar o comando `pytest -v tests.py`:

```
$ pytest -v tests.py
========================================== test session starts ==========================================
...                                                                                  
tests.py::test_rent_regular_book_short_duration PASSED                                            [  9%]
tests.py::test_rent_regular_book_long_duration PASSED                                             [ 18%]
tests.py::test_rent_multiple_regular_books PASSED                                                 [ 27%]
tests.py::test_rent_children_book_short_duration PASSED                                           [ 36%]
tests.py::test_rent_children_book_long_duration PASSED                                            [ 45%]
tests.py::test_rent_multiple_children_books PASSED                                                [ 54%]
tests.py::test_rent_new_release_book_short_duration PASSED                                        [ 63%]
tests.py::test_rent_new_release_book_long_duration PASSED                                         [ 72%]
tests.py::test_rent_multiple_new_release_books PASSED                                             [ 81%]
tests.py::test_rent_distinct_books_short_duration PASSED                                          [ 90%]
tests.py::test_rent_distinct_books_long_duration PASSED                                           [100%]
========================================== 11 passed in 0.01s ===========================================
```

### Rode os testes remotamente (via GitHub Actions)

Os testes são executados automaticamente no GitHub Actions sempre que um commit é realizado.
Portanto, para rodar os testes no GitHub Actions, realize uma alteração qualquer neste arquivo `README.md` e faça o commit da alteração com a seguinte mensagem: *Commit 1: Running the tests*.

Em seguida, clique na aba `Actions` e veja que os testes foram executados com sucesso no GitHub Actions. 
Observe as execuções em múltiplos sistemas operacionais e versões da linguagem Python.

# Commit 2: Removing getters @property and renaming attributes

Observe que as classes `Book`, `Rental` e `Client` possuem 5 propriedades `@property` que representam métodos getters.
Não iremos precisar dessas propriedades, portanto, remova todas as 5.
Em seguida, renomeie os 5 atributos das classes, removendo o underline (_). Por exemplo, mude de `self._book` para `self.book`.

**Rode os testes localmente para garantir que o comportamento do sistema não foi alterado.
Só faça o commit com os testes passando.
Refatoração não deve quebrar os teste.**

Para rodar os testes localmente, basta executar o pytest na linha comando:

```
$ pytest -v tests.py
========================================== test session starts ==========================================
...                                                                                  
tests.py::test_rent_regular_book_short_duration PASSED                                            [  9%]
tests.py::test_rent_regular_book_long_duration PASSED                                             [ 18%]
tests.py::test_rent_multiple_regular_books PASSED                                                 [ 27%]
tests.py::test_rent_children_book_short_duration PASSED                                           [ 36%]
tests.py::test_rent_children_book_long_duration PASSED                                            [ 45%]
tests.py::test_rent_multiple_children_books PASSED                                                [ 54%]
tests.py::test_rent_new_release_book_short_duration PASSED                                        [ 63%]
tests.py::test_rent_new_release_book_long_duration PASSED                                         [ 72%]
tests.py::test_rent_multiple_new_release_books PASSED                                             [ 81%]
tests.py::test_rent_distinct_books_short_duration PASSED                                          [ 90%]
tests.py::test_rent_distinct_books_long_duration PASSED                                           [100%]
========================================== 11 passed in 0.01s ===========================================
```

#### Faça o commit das alterações
Com os testes passando, faça o commit com a seguinte mensagem: *Commit 2: Removing getters @property and renaming attributes*.

# Commit 3: Extracting method get_charge from Client.statement

Extraia um método chamado `get_charge` de `Client.statement` para a própria classe `Client`.
O novo método deverá ter a seguinte assinatura:

```python
def get_charge(self, rental: Rental) -> float:
```

O método extraído deve conter o código relativo ao comentário *determine amounts for each line*.

#### Faça o commit das alterações
Com os testes passando, faça o commit com a seguinte mensagem: *Commit 3: Extracting method get_charge from Client.statement*.

# Commit 4: Moving method get_charge from Client to Rental

Mova o método `get_charge` da classe `Client` para a classe `Rental`, já que esse método não usa informações da primeira, mas sim da segunda classe.

Não esqueça de atualizar o método `get_charge` em `Rental` para chamar `self` ao invés de `rental`, por exemplo:

```python
# Em Client
if rental.book.price_code == Book.REGULAR:
# Em Rental
if self.book.price_code == Book.REGULAR:
```

Também não esqueça de atualizar a chamada do método `get_charge` em `statement`:
```python
# De...
amount = self.get_charge(rental)
# Para...
amount = rental.get_charge()
```

#### Faça o commit das alterações
Com os testes passando, faça o commit com a seguinte mensagem: *Commit 4: Moving method get_charge from Client to Rental*.

# Commit 5: Extracting get_frequent_renter_points from Client.statement to Rental

Vamos decompor mais uma vez `statement` para diminuir seu tamanho e complexidade. 

O método extraído deve conter o código relativo ao comentário *add frequent renter points*.
Extraia o seguinte método chamado `get_frequent_renter_points` e para classe `Rental`:

```python
def get_frequent_renter_points(self):
    points = 1
    if self.book.price_code == Book.NEW_RELEASE and self.days_rented > 1:
        points += 1
    return points
````

Atualize a chamada do método `get_frequent_renter_points` em `statement`:

```python
frequent_renter_points = rental.get_frequent_renter_points()
```

Rode os testes, e observe que vários testes falham.
Ou seja, inserimos uma regressão (BUG!) no sistema.
Testes funcionam como uma rede de proteção contra a inserção de bugs.

Encontre e corrija o bug!
Dica: o bug está no código acima.

#### Faça o commit das alterações
Com os testes passando, faça o commit com a seguinte mensagem: *Commit 5: Extracting get_frequent_renter_points from Client.statement to Rental*.
