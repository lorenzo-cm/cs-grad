import random
import os


class Wordle:
    def __init__(self, word_list, game_id):
        self.game_id = game_id
        self.word_list = word_list
        self.target_word = random.choice(self.word_list).lower()
        self.attempts = []  # guess and result
        self.max_attempts = 6
        self.game_over = False
        self.won = False

    def guess(self, guess):
        """
        Processa a tentativa do jogador e retorna o resultado.
        1- Verifica validade da tentativa
        2- Compara com a palavra alvo
        3- Verifica se o jogo acabou
        4- Retorna informações do jogo

        Retorna um dicionário com as informações do jogo:
        - game_id: ID do jogo
        - guess: A tentativa do jogador
        - attempts: Lista de tentativas feitas
        - attempts_used: Número de tentativas usadas
        - target_word: Palavra alvo (se o jogo acabou)
        - game_over: Indica se o jogo acabou
        - won: Indica se o jogador ganhou
        """
        if self.game_over:
            raise ValueError("Game is already over. Please start a new game.")

        guess = guess.strip()

        # Valida a tentativa do jogador
        if len(guess) != 5 or not guess.isalpha():
            raise ValueError("Guess must be a 5-letter word.")

        if guess not in self.word_list:
            raise ValueError("Guess not in the word list.")

        # Verifica a tentativa e registra o resultado
        self.attempts.append({"guess": guess, "result": self._check_guess(guess)})

        # Win condition
        if guess == self.target_word:
            self.game_over = True
            self.won = True
            return self._return_info(guess)

        # Game over
        if len(self.attempts) >= self.max_attempts:
            self.game_over = True
            return self._return_info(guess)

        return self._return_info(guess)

    def _check_guess(self, guess: str) -> list[str]:
        """
        Compara a tentativa com a palavra alvo
        e retorna uma lista de resultados:
        - 'correct' se a letra está na posição correta
        - 'present' se a letra está na palavra, mas na posição errada
        - 'not present' se a letra não está na palavra
        """
        result = [""] * 5
        count_letters: dict[str, int] = {}

        # Contar letras na palavra alvo
        for letter in self.target_word:
            count_letters[letter] = count_letters.get(letter, 0) + 1

        # Primeira passada: marcar letras corretas
        for i, letter in enumerate(guess):
            if letter == self.target_word[i]:
                result[i] = "correct"
                count_letters[letter] -= 1

        # Segunda passada: marcar letras presentes mas na posição errada
        for i, letter in enumerate(guess):
            if result[i] == "":  # Ainda não foi marcada
                if letter in count_letters and count_letters[letter] > 0:
                    result[i] = "present"
                    count_letters[letter] -= 1
                else:
                    result[i] = "not present"

        return result

    def _return_info(self, guess):
        return {
            "game_id": self.game_id,
            "guess": guess,
            "attempts": self.attempts,
            "attempts_used": len(self.attempts),
            "target_word": self.target_word if self.game_over else None,
            "game_over": self.game_over,
            "won": self.won,
        }
