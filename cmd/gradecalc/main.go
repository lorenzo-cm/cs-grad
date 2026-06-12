package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/lorenzocm/github-actions/gradecalc"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "usage: gradecalc <grade> [<grade>...]")
		os.Exit(1)
	}

	grades, err := parseGrades(os.Args[1:])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	result, err := gradecalc.FinalResult(grades)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	status := "reprovado"
	if result.Passed {
		status = "aprovado"
	}

	fmt.Printf("Media: %.2f\nConceito: %s\nStatus: %s\n", result.Average, result.Letter, status)
}

func parseGrades(values []string) ([]float64, error) {
	grades := make([]float64, 0, len(values))
	for _, value := range values {
		grade, err := strconv.ParseFloat(value, 64)
		if err != nil {
			return nil, fmt.Errorf("invalid grade %q", value)
		}
		grades = append(grades, grade)
	}

	return grades, nil
}
