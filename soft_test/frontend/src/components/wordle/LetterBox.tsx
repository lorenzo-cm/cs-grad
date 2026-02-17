"use client";

import { useState, useEffect } from "react";
import { Box, Text } from "@chakra-ui/react";
import { getBoxStyles } from "./boxStyles";
import { motion } from "framer-motion";

export type LetterState = "empty" | "correct" | "present" | "absent" | "pending";

interface LetterBoxProps {
    letter: string;
    state: LetterState;
    index?: number;
    size?: "sm" | "md" | "lg";
    revealTrigger?: number; // new prop to trigger animation
}

const MotionBox = motion(Box);

// --- Animation Timing Constants ---
const FLIP_PER_LETTER_DELAY = 0; // ms between each cell's animation
const FLIP_TO_90_DURATION = 250;   // ms to flip to 90deg
const FLIP_BACK_DURATION = 250;    // ms to flip back to 0deg


export const LetterBox: React.FC<LetterBoxProps> = ({
    letter,
    state,
    index = 0,
    size = "md",
    revealTrigger = 0
}) => {
    // --- Animation State ---
    const [displayState, setDisplayState] = useState<LetterState>(state);
    const [flipPhase, setFlipPhase] = useState<0 | 1 | 2> (0); // 0: idle, 1: flipping to 90, 2: flipping back
    const [rotation, setRotation] = useState(0);
    const styles = getBoxStyles(displayState, size);

    // --- Animation Effect ---
    useEffect(() => {
        const timers: NodeJS.Timeout[] = [];
        if (state === "correct" || state === "present" || state === "absent") {
            // Each letter waits for the previous one to complete
            const startDelay = index * FLIP_PER_LETTER_DELAY;
            const flipTo90 = () => {
                setFlipPhase(1);
                setRotation(0);
                setTimeout(() => {
                    setRotation(90);
                    setTimeout(() => {
                        setDisplayState(state);
                        setFlipPhase(2);
                        setRotation(0); // flip back to 0deg
                        setTimeout(() => {
                            setFlipPhase(0);
                        }, FLIP_BACK_DURATION);
                    }, FLIP_TO_90_DURATION);
                }, 0);
            };
            timers.push(setTimeout(flipTo90, startDelay));
        } else {
            setDisplayState(state);
            setFlipPhase(0);
            setRotation(0);
        }
        return () => { timers.forEach(clearTimeout); };
    }, [state, index, revealTrigger]);

    // --- Render ---
    return (
        <MotionBox
            {...styles}
            initial={{ scale: 1, rotateX: 0 }}
            animate={{
                scale: letter && state === "pending" ? [1, 1.1, 1] : 1,
                rotateX: flipPhase === 1 ? 90 : 0
            }}
            transition={{
                scale: { duration: 0.2 },
                rotateX: { duration: FLIP_TO_90_DURATION / 1000, ease: "easeInOut" }
            }}
        >
            <Text>{letter}</Text>
        </MotionBox>
    );
};
