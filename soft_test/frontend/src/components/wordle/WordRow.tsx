"use client";


import { HStack } from "@chakra-ui/react";
import { LetterBox, LetterState } from "./LetterBox";
import { useEffect, useState } from "react";

interface WordRowProps {
  word: string;
  states: LetterState[];
  maxLength?: number;
  size?: "sm" | "md" | "lg";
  gap?: number;
}

export const WordRow: React.FC<WordRowProps> = ({ 
  word, 
  states, 
  maxLength = 5, 
  size = "md",
  gap = 2
}) => {
  // Ensure word and states arrays match the expected length
  const letters = word.padEnd(maxLength, ' ').split('').slice(0, maxLength);
  const [revealed, setRevealed] = useState<number>(0);

  // Reveal each cell one by one after 600ms * index
  useEffect(() => {
    if (!states.some(s => s === "correct" || s === "present" || s === "absent")) {
      setRevealed(0);
      return;
    }
    setRevealed(0);
    let cancelled = false;
    const revealNext = (i: number) => {
      if (cancelled) return;
      setRevealed(i + 1);
      if (i + 1 < maxLength) {
        setTimeout(() => revealNext(i + 1), 600);
      }
    };
    revealNext(0);
    return () => { cancelled = true; };
  }, [states.join("|"), maxLength]);

  // Fill missing states with 'empty'
  const letterStates = letters.map((_, i) => {
    if (i < revealed) return states[i] || "empty";
    if (states[i] === "correct" || states[i] === "present" || states[i] === "absent") return "pending";
    return states[i] || "empty";
  });

  return (
    <HStack gap={gap}>
      {letters.map((letter, index) => (
        <LetterBox
          key={`${index}-${letterStates[index]}-${letter}`}
          letter={letter.trim()}
          state={letterStates[index]}
          index={index}
          size={size}
        />
      ))}
    </HStack>
  );
};
