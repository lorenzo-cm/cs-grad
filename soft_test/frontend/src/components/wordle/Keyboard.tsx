"use client";

import { VStack, HStack, Button } from "@chakra-ui/react";
import { useEffect } from "react";
import { LetterState } from "./LetterBox";

interface KeyboardProps {
  onKeyPress: (key: string) => void;
  onEnter: () => void;
  onBackspace: () => void;
  letterStates: Record<string, LetterState>;
  disabled?: boolean;
}

const KEYBOARD_ROWS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACKSPACE']
];


export const Keyboard: React.FC<KeyboardProps> = ({
  onKeyPress,
  onEnter,
  onBackspace,
  letterStates,
  disabled = false
}) => {
  // Handle physical keyboard input
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (disabled) return;
      
      const key = event.key;
      if (key === 'Enter') {
        event.preventDefault();
        onEnter();
      } else if (key === 'Backspace') {
        event.preventDefault();
        onBackspace();
      } else if (/^[a-zA-Z]$/.test(key)) {
        event.preventDefault();
        onKeyPress(key);
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [disabled, onEnter, onBackspace, onKeyPress]);


  const getKeyColor = (key: string) => {
    if (key === 'ENTER' || key === 'BACKSPACE') {
      return { bg: 'gray.300', color: 'black', _dark: { bg: 'gray.600', color: 'white' } };
    }

    const state = letterStates[key.toLowerCase()];
    switch (state) {
      case 'correct':
        return { bg: 'green.500', color: 'white' };
      case 'present':
        return { bg: 'yellow.500', color: 'white' };
      case 'absent':
        return { bg: 'gray.500', color: 'white' };
      default:
        return { bg: 'gray.200', color: 'black', _dark: { bg: 'gray.700', color: 'white' } };
    }
  };

  const handleKeyClick = (key: string) => {
    if (disabled) return;

    if (key === 'ENTER') {
      onEnter();
    } else if (key === 'BACKSPACE') {
      onBackspace();
    } else {
      onKeyPress(key.toLowerCase());
    }
  };

  const getKeyWidth = (key: string) => {
    if (key === 'ENTER' || key === 'BACKSPACE') {
      return { minW: '65px', fontSize: 'xs' };
    }
    return { minW: '40px', w: '40px', h: '58px' };
  };

  return (
    <VStack gap={2} mt={8}>
      {KEYBOARD_ROWS.map((row, rowIndex) => (
        <HStack key={rowIndex} gap={1}>
          {row.map((key) => (
            <Button
              key={key}
              onClick={() => handleKeyClick(key)}
              disabled={disabled}
              {...getKeyColor(key)}
              {...getKeyWidth(key)}
              borderRadius="md"
              fontWeight="bold"
              _hover={{
                transform: disabled ? 'none' : 'scale(1.05)',
                transition: 'transform 0.1s'
              }}
              _active={{
                transform: disabled ? 'none' : 'scale(0.95)'
              }}
            >
              {key === 'BACKSPACE' ? '⌫' : key}
            </Button>
          ))}
        </HStack>
      ))}
    </VStack>
  );
};
