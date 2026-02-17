"use client";

import { VStack, Box, Heading, Container } from "@chakra-ui/react";
import { WordRow } from "./WordRow";
import { LetterState } from "./LetterBox";

interface GameBoardProps {
  guesses: string[];
  guessStates: LetterState[][];
  currentGuess: string;
  maxGuesses?: number;
  wordLength?: number;
  title?: string;
}

export const GameBoard: React.FC<GameBoardProps> = ({
  guesses,
  guessStates,
  currentGuess,
  maxGuesses = 6,
  wordLength = 5,
  title = "Wordle"
}) => {
  const rows = [];

  // Add completed guesses
  for (let i = 0; i < guesses.length; i++) {
    rows.push(
      <WordRow
        key={i}
        word={guesses[i]}
        states={guessStates[i] || []}
        maxLength={wordLength}
      />
    );
  }

  // Add current guess row (if not exceeding max guesses)
  if (guesses.length < maxGuesses) {
    const currentStates = new Array(wordLength).fill('pending');
    rows.push(
      <WordRow
        key={guesses.length}
        word={currentGuess}
        states={currentStates}
        maxLength={wordLength}
      />
    );
  }

  // Add empty rows for remaining guesses
  for (let i = rows.length; i < maxGuesses; i++) {
    const emptyStates = new Array(wordLength).fill('empty');
    rows.push(
      <WordRow
        key={i}
        word=""
        states={emptyStates}
        maxLength={wordLength}
      />
    );
  }

  return (
    <Container maxW="container.sm" py={8}>
      <VStack gap={4}>
        <Heading as="h1" size="2xl" textAlign="center" mb={8}>
          {title}
        </Heading>
        <Box>
          <VStack gap={2}>
            {rows}
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
};
