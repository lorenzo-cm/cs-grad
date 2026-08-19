package gradecalc

import "testing"

func TestAverageCalculatesMean(t *testing.T) {
	got, err := Average([]float64{80, 90, 100})
	if err != nil {
		t.Fatalf("Average returned unexpected error: %v", err)
	}

	want := 90.0
	if got != want {
		t.Fatalf("Average() = %.2f, want %.2f", got, want)
	}
}

func TestAverageRejectsEmptyInput(t *testing.T) {
	_, err := Average(nil)
	if err == nil {
		t.Fatal("Average() expected an error for empty input")
	}
}

func TestAverageRejectsGradesBelowZero(t *testing.T) {
	_, err := Average([]float64{70, -1})
	if err == nil {
		t.Fatal("Average() expected an error for a negative grade")
	}
}

func TestAverageRejectsGradesAboveOneHundred(t *testing.T) {
	_, err := Average([]float64{70, 101})
	if err == nil {
		t.Fatal("Average() expected an error for a grade above 100")
	}
}

func TestLetterGradeBoundaries(t *testing.T) {
	tests := []struct {
		name  string
		score float64
		want  string
	}{
		{name: "A", score: 90, want: "A"},
		{name: "B", score: 80, want: "B"},
		{name: "C", score: 70, want: "C"},
		{name: "D", score: 60, want: "D"},
		{name: "F", score: 59.99, want: "F"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := LetterGrade(tt.score)
			if err != nil {
				t.Fatalf("LetterGrade returned unexpected error: %v", err)
			}

			if got != tt.want {
				t.Fatalf("LetterGrade(%.2f) = %q, want %q", tt.score, got, tt.want)
			}
		})
	}
}

func TestFinalResultApprovesPassingAverage(t *testing.T) {
	got, err := FinalResult([]float64{60, 70, 80})
	if err != nil {
		t.Fatalf("FinalResult returned unexpected error: %v", err)
	}

	if !got.Passed {
		t.Fatal("FinalResult() expected student to pass")
	}

	if got.Average != 70 || got.Letter != "C" {
		t.Fatalf("FinalResult() = %+v, want average 70 and letter C", got)
	}
}

func TestFinalResultRejectsFailingAverage(t *testing.T) {
	got, err := FinalResult([]float64{40, 50, 60})
	if err != nil {
		t.Fatalf("FinalResult returned unexpected error: %v", err)
	}

	if got.Passed {
		t.Fatal("FinalResult() expected student to fail")
	}

	if got.Letter != "F" {
		t.Fatalf("FinalResult() letter = %q, want F", got.Letter)
	}
}

func TestFinalResultUsesDisplayedAverageForDecision(t *testing.T) {
	got, err := FinalResult([]float64{10, 100, 100, 100, 100, 100, 100, 10, 10, 10, 19.99})
	if err != nil {
		t.Fatalf("FinalResult returned unexpected error: %v", err)
	}

	if got.Average != 60 {
		t.Fatalf("FinalResult() average = %.2f, want 60.00", got.Average)
	}

	if !got.Passed {
		t.Fatal("FinalResult() expected student to pass when displayed average is 60.00")
	}

	if got.Letter != "D" {
		t.Fatalf("FinalResult() letter = %q, want D", got.Letter)
	}
}
