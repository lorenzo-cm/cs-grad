package gradecalc

import (
	"errors"
	"fmt"
	"math"
)

const passingScore = 60.0

type Result struct {
	Average float64
	Passed  bool
	Letter  string
}

func Average(grades []float64) (float64, error) {
	if len(grades) == 0 {
		return 0, errors.New("at least one grade is required")
	}

	total := 0.0
	for _, grade := range grades {
		if err := validateGrade(grade); err != nil {
			return 0, err
		}
		total += grade
	}

	return total / float64(len(grades)), nil
}

func FinalResult(grades []float64) (Result, error) {
	average, err := Average(grades)
	if err != nil {
		return Result{}, err
	}
	average = roundToTwoDecimals(average)

	letter, err := LetterGrade(average)
	if err != nil {
		return Result{}, err
	}

	return Result{
		Average: average,
		Passed:  average >= passingScore,
		Letter:  letter,
	}, nil
}

func LetterGrade(score float64) (string, error) {
	if err := validateGrade(score); err != nil {
		return "", err
	}

	switch {
	case score >= 90:
		return "A", nil
	case score >= 80:
		return "B", nil
	case score >= 70:
		return "C", nil
	case score >= passingScore:
		return "D", nil
	default:
		return "F", nil
	}
}

func validateGrade(grade float64) error {
	if grade < 0 || grade > 100 {
		return fmt.Errorf("grade %.2f must be between 0 and 100", grade)
	}

	return nil
}

func roundToTwoDecimals(value float64) float64 {
	return math.Round(value*100) / 100
}
