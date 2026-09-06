package lab

import "fmt"

type Arrival struct {
	AtNS  int64 `json:"at_ns"`
	Bytes int64 `json:"bytes"`
}
type Trace struct {
	Arrivals      []Arrival `json:"arrivals"`
	ExpectedBytes int64     `json:"expected_bytes"`
	HeaderBytes   int64     `json:"header_bytes"`
	VerifiedAtNS  int64     `json:"verified_at_ns"`
}
type Model struct {
	SampleRate      int64 `json:"sample_rate"`
	FrameBytes      int64 `json:"frame_bytes"`
	PeriodFrames    int64 `json:"period_frames"`
	PrebufferFrames int64 `json:"prebuffer_frames"`
}
type Comparison struct {
	ProgressiveStartNS        int64 `json:"progressive_start_ns"`
	ProgressiveMissingPeriods int64 `json:"progressive_missing_periods"`
	StagedStartNS             int64 `json:"staged_start_ns"`
}

func Analyze(t Trace, m Model) (Comparison, error) {
	c := Comparison{ProgressiveStartNS: -1, StagedStartNS: -1}
	if m.SampleRate <= 0 || m.FrameBytes <= 0 || m.PeriodFrames <= 0 || m.PrebufferFrames <= 0 || m.PeriodFrames > 1e9 || t.HeaderBytes < 0 || t.ExpectedBytes <= t.HeaderBytes || t.VerifiedAtNS < -1 {
		return c, fmt.Errorf("invalid trace or model dimensions")
	}
	period := m.PeriodFrames * 1e9 / m.SampleRate
	frames := (t.ExpectedBytes - t.HeaderBytes) / m.FrameBytes
	if period < 1 || frames < 1 || frames/m.PeriodFrames > 10000000 || t.ExpectedBytes-t.HeaderBytes != frames*m.FrameBytes {
		return c, fmt.Errorf("invalid or excessive period schedule")
	}
	periods := (frames-1)/m.PeriodFrames + 1
	if periods > (int64(1<<63-1)-1e15)/period {
		return c, fmt.Errorf("period schedule overflows time")
	}
	var previous Arrival
	for i, a := range t.Arrivals {
		if a.AtNS < 0 || a.AtNS > 1e15 || a.Bytes < 0 || a.Bytes > t.ExpectedBytes || (i > 0 && (a.AtNS < previous.AtNS || a.Bytes < previous.Bytes)) {
			return c, fmt.Errorf("invalid arrival %d", i)
		}
		if c.ProgressiveStartNS < 0 && (a.Bytes-t.HeaderBytes)/m.FrameBytes >= m.PrebufferFrames {
			c.ProgressiveStartNS = a.AtNS
		}
		previous = a
	}
	if t.VerifiedAtNS >= 0 {
		if len(t.Arrivals) == 0 || previous.Bytes != t.ExpectedBytes || t.VerifiedAtNS < previous.AtNS || t.VerifiedAtNS > 1e15 {
			return c, fmt.Errorf("verification precedes complete delivery")
		}
		c.StagedStartNS = ((t.VerifiedAtNS + period - 1) / period) * period
	}
	if c.ProgressiveStartNS >= 0 {
		next := 0
		var available int64
		for consumed, deadline := int64(0), c.ProgressiveStartNS+period; consumed < frames; deadline += period {
			consumed += min(m.PeriodFrames, frames-consumed)
			for next < len(t.Arrivals) && t.Arrivals[next].AtNS <= deadline {
				available = max(int64(0), (t.Arrivals[next].Bytes-t.HeaderBytes)/m.FrameBytes)
				next++
			}
			if available < consumed {
				c.ProgressiveMissingPeriods++
			}
		}
	}
	return c, nil
}
