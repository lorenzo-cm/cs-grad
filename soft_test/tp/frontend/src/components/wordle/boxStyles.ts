import { LetterState } from "./LetterBox";

export function getBoxStyles(state: LetterState, size: "sm" | "md" | "lg") {
  const sizeConfig = {
    sm: { width: "40px", height: "40px", fontSize: "lg" },
    md: { width: "60px", height: "60px", fontSize: "2xl" },
    lg: { width: "80px", height: "80px", fontSize: "3xl" }
  };
  const baseStyles = {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "2px solid",
    borderRadius: "md",
    fontWeight: "bold",
    textTransform: "uppercase" as const,
    ...sizeConfig[size]
  };
  const stateStyles = {
    empty: {
      borderColor: "gray.300",
      bg: "white",
      color: "gray.800",
      _dark: {
        borderColor: "gray.600",
        bg: "gray.800",
        color: "white"
      }
    },
    pending: {
      borderColor: "gray.500",
      bg: "white",
      color: "gray.800",
      _dark: {
        borderColor: "gray.400",
        bg: "gray.800",
        color: "white"
      }
    },
    correct: {
      borderColor: "green.500",
      bg: "green.500",
      color: "white"
    },
    present: {
      borderColor: "yellow.500",
      bg: "yellow.500",
      color: "white"
    },
    absent: {
      borderColor: "gray.500",
      bg: "gray.500",
      color: "white"
    }
  };
  return { ...baseStyles, ...stateStyles[state] };
}
