"use client";

import { useState, useEffect, useCallback } from "react";
import { Box, VStack, Text, Button, HStack, Spinner } from "@chakra-ui/react";
import { GameBoard, Keyboard, LetterState } from "./index";
import { createGame, makeGuess, getGameState } from "../../api/wordle";

export const WordleGame: React.FC = () => {
  // --- States ---
  const [gameId, setGameId] = useState<string | null>(null);
  const [gameState, setGameState] = useState<any>(null);
  const [currentGuess, setCurrentGuess] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // --- Vars ---
  const wordLength = 5;
  const maxGuesses = 6;

  // --- Start new game or reset ---
  const startNewGame = useCallback(async () => {
    setLoading(true);
    setErrorMessage("");
    setCurrentGuess("");

    try {
      const id = await createGame();
      setGameId(id);
      const state = await getGameState(id);
      setGameState(state);
    }
    catch (err: any) {
      setErrorMessage("Erro ao iniciar novo jogo");
    }
    finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    startNewGame();
  }, [startNewGame]);

  // --- Map backend states to frontend states (not present -> absent) for ease ---
  function mapBackendResultToLetterState(result: string): LetterState {
    if (result === "correct") return "correct";
    if (result === "present") return "present";
    return "absent";
  }

  function mapResultToLetterState(result: string[]): LetterState[] {
    return result.map(mapBackendResultToLetterState);
  }

  // Determina a cor de cada letra no teclado baseado em todas as tentativas
  function buildLetterStates(attempts: any[]): Record<string, LetterState> {
    const letterStates: Record<string, LetterState> = {};

    attempts.forEach((attempt: any) => {
      attempt.result.forEach((letterResult: string, letterIndex: number) => {
        const letter = attempt.guess[letterIndex];
        const newState = mapBackendResultToLetterState(letterResult);
        const currentState = letterStates[letter];

        // Aplicar apenas se for um estado "melhor" (prioridade: correct > present > absent)
        if (shouldUpdateLetterState(currentState, newState)) {
          letterStates[letter] = newState;
        }
      });
    });

    return letterStates;
  }

  // Helper: determina se devemos atualizar o estado da letra (prioridade: correct > present > absent)
  function shouldUpdateLetterState(current: LetterState | undefined, newState: LetterState): boolean {
    const getPriority = (state: LetterState) => {
      if (state === "correct") return 3;
      if (state === "present") return 2;
      return 1; // absent
    };

    return !current || getPriority(newState) > getPriority(current);
  }

  // --- Guess submission ---
  const submitGuess = useCallback(async () => {
    if (!gameId || !gameState) return;
    if (gameState.game_over) return;
    const guess = currentGuess.trim().toLowerCase();

    // Basic validation
    if (guess.length !== wordLength) {
      setErrorMessage(`A palavra deve ter ${wordLength} letras.`);
      return;
    }
    if (!/^[a-zA-Z]+$/.test(guess)) {
      setErrorMessage("Apenas letras são permitidas.");
      return;
    }
    if (gameState.attempts.some((a: any) => a.guess === guess)) {
      setErrorMessage("Palavra já tentada.");
      return;
    }

    setErrorMessage("");
    setSubmitting(true);
    try {
      const response = await makeGuess(gameId, guess);
      setGameState({
        ...gameState,
        ...response,
        attempts: [
          ...(gameState.attempts || []),
          { guess: response.guess, result: response.result }
        ],
        game_over: response.game_over,
        won: response.won,
        target_word: response.target_word
      });
      setCurrentGuess("");
    }
    catch (err: any) {
      setErrorMessage(err.message || "Erro ao enviar palpite");
    }
    finally {
      setSubmitting(false);
    }
  }, [gameId, gameState, currentGuess]);

  // --- Keyboard handlers ---
  const handleKeyPress = useCallback((key: string) => {
    if (!gameState || gameState.game_over) return;
    if (currentGuess.length < wordLength) {
      setCurrentGuess(prev => prev + key.toUpperCase());
    }
  }, [currentGuess, wordLength, gameState]);

  const handleBackspace = useCallback(() => {
    if (!gameState || gameState.game_over) return;
    setCurrentGuess(prev => prev.slice(0, -1));
  }, [gameState]);

  // --- Render ---
  if (loading) {
    return (
      <Box maxW="600px" mx="auto" p={4} textAlign="center">
        <Spinner size="xl" />
        <Text mt={4}>Carregando jogo...</Text>
      </Box>
    );
  }

  const attempts = gameState?.attempts || [];
  const guesses = attempts.map((a: any) => a.guess.toUpperCase());
  const guessStates = attempts.map((a: any) => mapResultToLetterState(a.result));
  const letterStates = buildLetterStates(attempts);
  const gameStatus = gameState?.game_over ? (gameState.won ? "won" : "lost") : "playing";

  return (
    <Box maxW="600px" mx="auto" p={4}>
      <VStack gap={4}>
        <GameBoard
          guesses={guesses}
          guessStates={guessStates}
          currentGuess={currentGuess}
          maxGuesses={maxGuesses}
          wordLength={wordLength}
        />

        {errorMessage && (
          <Text color="red.500" fontSize="sm" textAlign="center">
            {errorMessage}
          </Text>
        )}

        {gameStatus !== "playing" && (
          <VStack gap={4}>
            <Text fontSize="lg" fontWeight="bold" color={gameStatus === "won" ? "green.500" : "red.500"}>
              {gameStatus === "won" ? "🎉 Você venceu!" : `😞 Fim de jogo - A palavra era: ${gameState?.target_word?.toUpperCase()}`}
            </Text>
            <HStack>
              <Button onClick={startNewGame} colorScheme="blue" loading={loading}>
                Jogar novamente
              </Button>
            </HStack>
          </VStack>
        )}

        <Keyboard
          onKeyPress={handleKeyPress}
          onEnter={submitGuess}
          onBackspace={handleBackspace}
          letterStates={letterStates}
          disabled={gameStatus !== "playing" || submitting}
        />

        <Text fontSize="sm" color="gray.500" textAlign="center">
          Tentativa {attempts.length + (gameStatus === "playing" ? 1 : 0)} de {maxGuesses}
        </Text>
      </VStack>
    </Box>
  );
};
