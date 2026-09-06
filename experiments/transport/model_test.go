package lab_test

import (
	"testing"

	lab "kuro/transportlab"
)

func TestAnalyzeIndependentTimelines(t *testing.T) {
	model := lab.Model{SampleRate: 1000, FrameBytes: 4, PeriodFrames: 10, PrebufferFrames: 20}
	for _, tt := range []struct {
		name  string
		trace lab.Trace
		want  lab.Comparison
	}{
		{"complete at origin", lab.Trace{Arrivals: []lab.Arrival{{AtNS: 0, Bytes: 444}}, ExpectedBytes: 444, HeaderBytes: 44, VerifiedAtNS: 0}, lab.Comparison{ProgressiveStartNS: 0, StagedStartNS: 0}},
		{"fixed deadlines across stall", lab.Trace{Arrivals: []lab.Arrival{{AtNS: 0, Bytes: 124}, {AtNS: 65_000_000, Bytes: 444}}, ExpectedBytes: 444, HeaderBytes: 44, VerifiedAtNS: 65_000_001}, lab.Comparison{ProgressiveStartNS: 0, ProgressiveMissingPeriods: 4, StagedStartNS: 70_000_000}},
		{"fragmented header and incomplete frame", lab.Trace{Arrivals: []lab.Arrival{{AtNS: 0, Bytes: 20}, {AtNS: 1_000_000, Bytes: 44}, {AtNS: 2_000_000, Bytes: 123}, {AtNS: 3_000_000, Bytes: 124}, {AtNS: 4_000_000, Bytes: 444}}, ExpectedBytes: 444, HeaderBytes: 44, VerifiedAtNS: 4_000_000}, lab.Comparison{ProgressiveStartNS: 3_000_000, StagedStartNS: 10_000_000}},
		{"arrival on deadline counts", lab.Trace{Arrivals: []lab.Arrival{{AtNS: 0, Bytes: 124}, {AtNS: 30_000_000, Bytes: 444}}, ExpectedBytes: 444, HeaderBytes: 44, VerifiedAtNS: 30_000_000}, lab.Comparison{ProgressiveStartNS: 0, StagedStartNS: 30_000_000}},
		{"never buffered or admitted", lab.Trace{Arrivals: []lab.Arrival{{AtNS: 0, Bytes: 44}}, ExpectedBytes: 444, HeaderBytes: 44, VerifiedAtNS: -1}, lab.Comparison{ProgressiveStartNS: -1, StagedStartNS: -1}},
		{"complete bytes without admission", lab.Trace{Arrivals: []lab.Arrival{{AtNS: 0, Bytes: 444}}, ExpectedBytes: 444, HeaderBytes: 44, VerifiedAtNS: -1}, lab.Comparison{ProgressiveStartNS: 0, StagedStartNS: -1}},
	} {
		t.Run(tt.name, func(t *testing.T) {
			got, err := lab.Analyze(tt.trace, model)
			if err != nil {
				t.Fatal(err)
			}
			if got != tt.want {
				t.Fatalf("Analyze() = %+v, want %+v", got, tt.want)
			}
			again, err := lab.Analyze(tt.trace, model)
			if err != nil || again != got {
				t.Fatalf("recalculation differs: %+v, %v", again, err)
			}
		})
	}
}

func TestAnalyzeRejectsInvalidInputs(t *testing.T) {
	for _, tt := range []struct {
		name   string
		change func(*lab.Trace, *lab.Model)
	}{
		{"zero sample rate", func(_ *lab.Trace, m *lab.Model) { m.SampleRate = 0 }},
		{"negative sample rate", func(_ *lab.Trace, m *lab.Model) { m.SampleRate = -1 }},
		{"zero frame size", func(_ *lab.Trace, m *lab.Model) { m.FrameBytes = 0 }},
		{"zero period", func(_ *lab.Trace, m *lab.Model) { m.PeriodFrames = 0 }},
		{"negative prebuffer", func(_ *lab.Trace, m *lab.Model) { m.PrebufferFrames = -1 }},
		{"negative arrival time", func(tr *lab.Trace, _ *lab.Model) { tr.Arrivals[0].AtNS = -1 }},
		{"time decreases", func(tr *lab.Trace, _ *lab.Model) { tr.Arrivals[0].AtNS = 2 }},
		{"bytes decrease", func(tr *lab.Trace, _ *lab.Model) { tr.Arrivals[1].Bytes = 100; tr.VerifiedAtNS = -1 }},
		{"bytes exceed expected length", func(tr *lab.Trace, _ *lab.Model) { tr.Arrivals[1].Bytes = 445 }},
		{"negative bytes", func(tr *lab.Trace, _ *lab.Model) { tr.Arrivals[0].Bytes = -1 }},
		{"negative header", func(tr *lab.Trace, _ *lab.Model) { tr.HeaderBytes = -1 }},
		{"header exceeds object", func(tr *lab.Trace, _ *lab.Model) { tr.HeaderBytes = 445 }},
		{"negative object length", func(tr *lab.Trace, _ *lab.Model) { tr.ExpectedBytes = -1 }},
		{"invalid verification sentinel", func(tr *lab.Trace, _ *lab.Model) { tr.VerifiedAtNS = -2 }},
	} {
		t.Run(tt.name, func(t *testing.T) {
			tr := lab.Trace{Arrivals: []lab.Arrival{{AtNS: 0, Bytes: 124}, {AtNS: 1, Bytes: 444}}, ExpectedBytes: 444, HeaderBytes: 44, VerifiedAtNS: 1}
			m := lab.Model{SampleRate: 1000, FrameBytes: 4, PeriodFrames: 10, PrebufferFrames: 20}
			tt.change(&tr, &m)
			if _, err := lab.Analyze(tr, m); err == nil {
				t.Fatal("Analyze accepted invalid input")
			}
		})
	}
}
