package lab

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

type Config struct{ OutDir string }
type Check struct {
	Name   string `json:"name"`
	Passed bool   `json:"passed"`
	Detail string `json:"detail"`
}
type Report struct {
	Version int     `json:"version"`
	Checks  []Check `json:"checks"`
}
type fixture struct {
	ID        string `json:"id"`
	WAV       string `json:"wav"`
	PCM       string `json:"pcm"`
	Bytes     int64  `json:"bytes"`
	SHA256    string `json:"sha256"`
	PCMSHA256 string `json:"pcm_sha256"`
	ETag      string `json:"etag"`
}
type manifest struct {
	Version  int       `json:"version"`
	Formula  string    `json:"formula"`
	Format   string    `json:"format"`
	Model    Model     `json:"model"`
	Fixtures []fixture `json:"fixtures"`
}
type receipt struct {
	Number        int    `json:"number"`
	Offset        int64  `json:"offset"`
	Status        int    `json:"status"`
	ContentRange  string `json:"content_range"`
	ETag          string `json:"etag"`
	ContentLength int64  `json:"content_length"`
	Body          string `json:"body"`
	ReadError     string `json:"read_error"`
}
type transfer struct {
	ID         string     `json:"id"`
	Body       string     `json:"body"`
	Ready      string     `json:"ready"`
	Reason     string     `json:"reason"`
	Trace      Trace      `json:"trace"`
	Receipts   []receipt  `json:"receipts"`
	Comparison Comparison `json:"comparison"`
}
type evidence struct {
	Name         string           `json:"name"`
	Before       []string         `json:"source_before"`
	After        []string         `json:"source_after"`
	Transfers    []transfer       `json:"transfers"`
	Budget       int64            `json:"budget"`
	Required     int64            `json:"required"`
	Reserved     string           `json:"reserved"`
	Denied       bool             `json:"denied"`
	Reservations map[string]int64 `json:"reservations"`
}

type window struct {
	limit   int64
	objects map[string]int64
}

func (w *window) reserve(id string, size int64) bool {
	if existing, ok := w.objects[id]; ok {
		return existing == size
	}
	used := int64(0)
	for _, bytes := range w.objects {
		used += bytes
	}
	if size > w.limit-used {
		return false
	}
	w.objects[id] = size
	return true
}

var caseNames = []string{"clean", "corrupt", "truncate", "resume", "changed-etag", "stall", "budget"}
var labModel = Model{SampleRate: 48000, FrameBytes: 4, PeriodFrames: 480, PrebufferFrames: 960}

const formula = "sample(frame,channel) = int16((frame*97 + channel*1009) % 65536 - 32768); track 2 starts at frame 24000"

func digest(b []byte) string { s := sha256.Sum256(b); return hex.EncodeToString(s[:]) }
func fixtureBytes(track int) ([]byte, []byte) {
	pcm := make([]byte, 24000*4)
	for frame := 0; frame < 24000; frame++ {
		for channel := 0; channel < 2; channel++ {
			value := int16((((track-1)*24000+frame)*97+channel*1009)%65536 - 32768)
			binary.LittleEndian.PutUint16(pcm[frame*4+channel*2:], uint16(value))
		}
	}
	wav := make([]byte, 44+len(pcm))
	copy(wav, "RIFF")
	binary.LittleEndian.PutUint32(wav[4:], uint32(len(wav)-8))
	copy(wav[8:], "WAVEfmt ")
	binary.LittleEndian.PutUint32(wav[16:], 16)
	binary.LittleEndian.PutUint16(wav[20:], 1)
	binary.LittleEndian.PutUint16(wav[22:], 2)
	binary.LittleEndian.PutUint32(wav[24:], 48000)
	binary.LittleEndian.PutUint32(wav[28:], 192000)
	binary.LittleEndian.PutUint16(wav[32:], 4)
	binary.LittleEndian.PutUint16(wav[34:], 16)
	copy(wav[36:], "data")
	binary.LittleEndian.PutUint32(wav[40:], uint32(len(pcm)))
	copy(wav[44:], pcm)
	return wav, pcm
}
func expectedManifest() manifest {
	m := manifest{Version: 1, Formula: formula, Format: "WAV PCM stereo 48000 Hz signed 16-bit little-endian; interleaved left/right; 24000 frames per track", Model: labModel}
	for i := 1; i <= 2; i++ {
		wav, pcm := fixtureBytes(i)
		id := fmt.Sprintf("track-%d", i)
		hash := digest(wav)
		m.Fixtures = append(m.Fixtures, fixture{ID: id, WAV: "fixtures/" + id + ".wav", PCM: "fixtures/" + id + ".pcm", Bytes: int64(len(wav)), SHA256: hash, PCMSHA256: digest(pcm), ETag: `"` + hash + `"`})
	}
	return m
}
func writeJSON(path string, value any) error {
	b, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, append(b, '\n'), 0600)
}
func readJSON(path string, value any) error {
	b, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	return json.Unmarshal(b, value)
}
func sourceHashes(root string, m manifest) ([]string, error) {
	var hashes []string
	for _, f := range m.Fixtures {
		for _, p := range []string{f.WAV, f.PCM} {
			b, err := os.ReadFile(filepath.Join(root, p))
			if err != nil {
				return nil, err
			}
			hashes = append(hashes, digest(b))
		}
	}
	return hashes, nil
}

type origin struct {
	root     string
	fixtures map[string]fixture
}

func (o origin) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	parts := strings.Split(strings.Trim(r.URL.Path, "/"), "/")
	if len(parts) != 2 || r.Method != "GET" {
		http.NotFound(w, r)
		return
	}
	f, ok := o.fixtures[parts[1]]
	if !ok {
		http.NotFound(w, r)
		return
	}
	data, err := os.ReadFile(filepath.Join(o.root, f.WAV))
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	mode := parts[0]
	etag := f.ETag
	if mode == "changed-etag" && r.Header.Get("Range") != "" {
		etag = `"changed"`
	}
	w.Header().Set("ETag", etag)
	if mode == "corrupt" {
		data[4096] ^= 1
	}
	if (mode == "truncate" || mode == "resume" || mode == "changed-etag") && r.Header.Get("Range") == "" {
		w.Header().Set("Content-Length", strconv.Itoa(len(data)))
		w.Header().Set("Accept-Ranges", "bytes")
		w.WriteHeader(200)
		_, _ = w.Write(data[:8192])
		return
	}
	if mode == "stall" {
		w.Header().Set("Content-Length", strconv.Itoa(len(data)))
		w.WriteHeader(200)
		_, _ = w.Write(data[:8192])
		w.(http.Flusher).Flush()
		select {
		case <-time.After(300 * time.Millisecond):
		case <-r.Context().Done():
			return
		}
		_, _ = w.Write(data[8192:])
		return
	}
	http.ServeContent(w, r, f.ID+".wav", time.Time{}, bytes.NewReader(data))
}

func receive(ctx context.Context, client *http.Client, base, root, mode string, f fixture, m Model, reservations *window) (transfer, error) {
	t := transfer{ID: f.ID, Trace: Trace{ExpectedBytes: f.Bytes, HeaderBytes: 44, VerifiedAtNS: -1}}
	if !reservations.reserve(f.ID, f.Bytes) {
		return t, fmt.Errorf("window budget refused %s", f.ID)
	}
	partial, err := os.CreateTemp(filepath.Join(root, "partial"), mode+"-"+f.ID+"-*.partial")
	if err != nil {
		return t, err
	}
	defer partial.Close()
	start := time.Now()
	total := int64(0)
	validETag := true
	attempts := 1
	if mode == "resume" || mode == "changed-etag" {
		attempts = 2
	}
	for attempt := 0; attempt < attempts; attempt++ {
		req, err := http.NewRequestWithContext(ctx, "GET", base+"/"+mode+"/"+f.ID, nil)
		if err != nil {
			return t, err
		}
		if attempt > 0 {
			req.Header.Set("Range", fmt.Sprintf("bytes=%d-", total))
			req.Header.Set("If-Range", f.ETag)
		}
		response, err := client.Do(req)
		if err != nil {
			return t, err
		}
		receipt := receipt{Number: attempt + 1, Offset: total, Status: response.StatusCode, ContentRange: response.Header.Get("Content-Range"), ETag: response.Header.Get("ETag"), ContentLength: response.ContentLength, Body: fmt.Sprintf("cases/%s/%s-response-%d.bin", mode, f.ID, attempt+1)}
		appendBody := receipt.ETag == f.ETag && ((attempt == 0 && receipt.Status == 200) || (attempt > 0 && receipt.Status == 206 && receipt.ContentRange == fmt.Sprintf("bytes %d-%d/%d", total, f.Bytes-1, f.Bytes)))
		if !appendBody {
			validETag = false
		}
		raw, err := os.Create(filepath.Join(root, receipt.Body))
		if err != nil {
			response.Body.Close()
			return t, err
		}
		buffer := make([]byte, 4096)
		for {
			n, readErr := response.Body.Read(buffer)
			if n > 0 {
				if _, err = raw.Write(buffer[:n]); err != nil {
					raw.Close()
					response.Body.Close()
					return t, err
				}
				if appendBody {
					if _, err = partial.Write(buffer[:n]); err != nil {
						raw.Close()
						response.Body.Close()
						return t, err
					}
					total += int64(n)
					t.Trace.Arrivals = append(t.Trace.Arrivals, Arrival{AtNS: time.Since(start).Nanoseconds(), Bytes: total})
				}
			}
			if readErr != nil {
				if readErr != io.EOF {
					receipt.ReadError = readErr.Error()
				}
				break
			}
		}
		closeErr := raw.Close()
		response.Body.Close()
		if closeErr != nil {
			return t, closeErr
		}
		t.Receipts = append(t.Receipts, receipt)
	}
	if err = partial.Sync(); err != nil {
		return t, err
	}
	if err = partial.Close(); err != nil {
		return t, err
	}
	body, err := os.ReadFile(partial.Name())
	if err != nil {
		return t, err
	}
	t.Reason = "verified"
	if !validETag {
		t.Reason = "validator rejected"
	} else if int64(len(body)) != f.Bytes {
		t.Reason = "length rejected"
	} else if digest(body) != f.SHA256 {
		t.Reason = "integrity rejected"
	}
	destination := "rejected/" + filepath.Base(partial.Name())
	if t.Reason == "verified" {
		destination = "ready/" + mode + "-" + f.ID + ".wav"
		t.Ready = destination
	}
	if err = os.Rename(partial.Name(), filepath.Join(root, destination)); err != nil {
		return t, err
	}
	t.Body = destination
	if t.Ready != "" {
		t.Trace.VerifiedAtNS = time.Since(start).Nanoseconds()
	}
	t.Comparison, err = Analyze(t.Trace, m)
	return t, err
}

func Run(ctx context.Context, config Config) (Report, error) {
	var empty Report
	if config.OutDir == "" {
		return empty, fmt.Errorf("empty output directory")
	}
	if err := os.Mkdir(config.OutDir, 0700); err != nil {
		return empty, err
	}
	for _, dir := range []string{"fixtures", "cases", "ready", "partial", "rejected"} {
		if err := os.Mkdir(filepath.Join(config.OutDir, dir), 0700); err != nil {
			return empty, err
		}
	}
	m := expectedManifest()
	for i, f := range m.Fixtures {
		wav, pcm := fixtureBytes(i + 1)
		if err := os.WriteFile(filepath.Join(config.OutDir, f.WAV), wav, 0400); err != nil {
			return empty, err
		}
		if err := os.WriteFile(filepath.Join(config.OutDir, f.PCM), pcm, 0400); err != nil {
			return empty, err
		}
	}
	if err := writeJSON(filepath.Join(config.OutDir, "manifest.json"), m); err != nil {
		return empty, err
	}
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		return empty, err
	}
	server := &http.Server{Handler: origin{root: config.OutDir, fixtures: map[string]fixture{m.Fixtures[0].ID: m.Fixtures[0], m.Fixtures[1].ID: m.Fixtures[1]}}}
	go server.Serve(listener)
	defer server.Close()
	transport := &http.Transport{Proxy: nil}
	defer transport.CloseIdleConnections()
	client := &http.Client{Transport: transport, Timeout: 5 * time.Second}
	for _, name := range caseNames {
		if err := ctx.Err(); err != nil {
			return empty, err
		}
		if err := os.Mkdir(filepath.Join(config.OutDir, "cases", name), 0700); err != nil {
			return empty, err
		}
		reservations := &window{limit: m.Fixtures[0].Bytes + m.Fixtures[1].Bytes, objects: make(map[string]int64)}
		e := evidence{Name: name}
		e.Before, err = sourceHashes(config.OutDir, m)
		if err != nil {
			return empty, err
		}
		if name == "budget" {
			e.Reserved = "ready/clean-track-1.wav"
			reserved, statErr := os.Stat(filepath.Join(config.OutDir, e.Reserved))
			if statErr != nil {
				return empty, statErr
			}
			e.Required = reserved.Size() + m.Fixtures[1].Bytes
			e.Budget = e.Required - 1
			reservations.limit = e.Budget
			if !reservations.reserve(m.Fixtures[0].ID, reserved.Size()) {
				return empty, fmt.Errorf("current reservation exceeds budget")
			}
			e.Denied = !reservations.reserve(m.Fixtures[1].ID, m.Fixtures[1].Bytes)
		} else {
			fixtures := m.Fixtures[:1]
			if name == "clean" {
				fixtures = m.Fixtures
			}
			for _, f := range fixtures {
				t, err := receive(ctx, client, "http://"+listener.Addr().String(), config.OutDir, name, f, m.Model, reservations)
				if err != nil {
					return empty, err
				}
				e.Transfers = append(e.Transfers, t)
			}
		}
		e.Reservations = reservations.objects
		e.After, err = sourceHashes(config.OutDir, m)
		if err != nil {
			return empty, err
		}
		if err = writeJSON(filepath.Join(config.OutDir, "cases", name, "case.json"), e); err != nil {
			return empty, err
		}
	}
	report, err := Verify(config.OutDir)
	if err != nil {
		return report, err
	}
	err = writeJSON(filepath.Join(config.OutDir, "report.json"), report)
	return report, err
}

func artifact(root, path string) ([]byte, error) {
	if path == "" || filepath.IsAbs(path) || filepath.Clean(path) != path || path == ".." || strings.HasPrefix(path, "../") {
		return nil, fmt.Errorf("invalid artifact path %q", path)
	}
	return os.ReadFile(filepath.Join(root, path))
}
func equalJSON(a, b any) bool {
	x, _ := json.Marshal(a)
	y, _ := json.Marshal(b)
	return bytes.Equal(x, y)
}
func verifyTransfer(root, mode string, t transfer, f fixture, track int, m Model) error {
	fail := func(why string) error { return fmt.Errorf("%s/%s: %s", mode, f.ID, why) }
	expected, _ := fixtureBytes(track)
	admitted := mode == "clean" || mode == "resume" || mode == "stall"
	body, err := artifact(root, t.Body)
	if err != nil {
		return err
	}
	wanted := append([]byte(nil), expected...)
	reason := "verified"
	switch mode {
	case "corrupt":
		wanted[4096] ^= 1
		reason = "integrity rejected"
	case "truncate":
		wanted = wanted[:8192]
		reason = "length rejected"
	case "changed-etag":
		wanted = wanted[:8192]
		reason = "validator rejected"
	}
	if !bytes.Equal(body, wanted) || t.ID != f.ID || t.Reason != reason {
		return fail("body or rejection reason differs")
	}
	if admitted {
		if t.Ready != "ready/"+mode+"-"+f.ID+".wav" || t.Body != t.Ready || digest(body) != f.SHA256 || digest(body[44:]) != f.PCMSHA256 {
			return fail("invalid ready object")
		}
	} else if t.Ready != "" || !strings.HasPrefix(t.Body, "rejected/") || t.Trace.VerifiedAtNS != -1 {
		return fail("rejected object admitted")
	}
	if t.Trace.ExpectedBytes != f.Bytes || t.Trace.HeaderBytes != 44 || len(t.Trace.Arrivals) == 0 || t.Trace.Arrivals[len(t.Trace.Arrivals)-1].Bytes != int64(len(body)) {
		return fail("trace length differs from received body")
	}
	comparison, err := Analyze(t.Trace, m)
	if err != nil {
		return err
	}
	if !equalJSON(comparison, t.Comparison) || (admitted && comparison.StagedStartNS < t.Trace.VerifiedAtNS) || (admitted && t.Trace.VerifiedAtNS < 0) {
		return fail("invalid model or verification time")
	}
	if mode == "stall" && (comparison.ProgressiveMissingPeriods < 1 || comparison.StagedStartNS <= comparison.ProgressiveStartNS) {
		return fail("stall did not cross buffer limit")
	}
	count := 1
	if mode == "resume" || mode == "changed-etag" {
		count = 2
	}
	if len(t.Receipts) != count {
		return fail("missing HTTP receipt")
	}
	for i, r := range t.Receipts {
		raw, err := artifact(root, r.Body)
		if err != nil {
			return err
		}
		rawExpected := wanted
		status := 200
		offset := int64(0)
		length := f.Bytes
		etag := f.ETag
		contentRange := ""
		readError := ""
		if mode == "truncate" || mode == "resume" || mode == "changed-etag" {
			if i == 0 {
				rawExpected = expected[:8192]
				readError = "unexpected EOF"
			} else {
				offset = 8192
				if mode == "resume" {
					rawExpected = expected[8192:]
					status = 206
					length = f.Bytes - 8192
					contentRange = fmt.Sprintf("bytes 8192-%d/%d", f.Bytes-1, f.Bytes)
				} else {
					rawExpected = expected
					etag = `"changed"`
				}
			}
		}
		if r.Body != fmt.Sprintf("cases/%s/%s-response-%d.bin", mode, f.ID, i+1) || !bytes.Equal(raw, rawExpected) || r.Number != i+1 || r.Offset != offset || r.Status != status || r.ContentLength != length || r.ETag != etag || r.ContentRange != contentRange || r.ReadError != readError {
			return fail("HTTP receipt or raw response differs")
		}
	}
	return nil
}

func Verify(outDir string) (Report, error) {
	report := Report{Version: 1}
	var m manifest
	if err := readJSON(filepath.Join(outDir, "manifest.json"), &m); err != nil {
		return report, err
	}
	canonical := expectedManifest()
	if !equalJSON(m, canonical) {
		return report, fmt.Errorf("manifest does not describe canonical fixtures")
	}
	hashes, err := sourceHashes(outDir, m)
	if err != nil {
		return report, err
	}
	var expectedHashes []string
	for _, f := range m.Fixtures {
		expectedHashes = append(expectedHashes, f.SHA256, f.PCMSHA256)
	}
	if !equalJSON(hashes, expectedHashes) {
		return report, fmt.Errorf("source fixture modified")
	}
	readyExpected := map[string]bool{}
	for _, name := range caseNames {
		var e evidence
		if err = readJSON(filepath.Join(outDir, "cases", name, "case.json"), &e); err != nil {
			return report, err
		}
		if e.Name != name || !equalJSON(e.Before, hashes) || !equalJSON(e.After, hashes) {
			return report, fmt.Errorf("%s: source hashes differ", name)
		}
		count := 1
		if name == "clean" {
			count = 2
		}
		if name == "budget" {
			count = 0
		}
		if len(e.Transfers) != count {
			return report, fmt.Errorf("%s: missing or extra transfer", name)
		}
		expectedReservations := map[string]int64{m.Fixtures[0].ID: m.Fixtures[0].Bytes}
		if name == "clean" {
			expectedReservations[m.Fixtures[1].ID] = m.Fixtures[1].Bytes
		}
		if !equalJSON(e.Reservations, expectedReservations) {
			return report, fmt.Errorf("%s: reservations differ", name)
		}
		for i, t := range e.Transfers {
			if err = verifyTransfer(outDir, name, t, m.Fixtures[i], i+1, m.Model); err != nil {
				return report, err
			}
			if t.Ready != "" {
				readyExpected[filepath.Base(t.Ready)] = true
			}
		}
		if name == "budget" {
			reserved, err := artifact(outDir, e.Reserved)
			if err != nil {
				return report, err
			}
			if e.Reserved != "ready/clean-track-1.wav" || digest(reserved) != m.Fixtures[0].SHA256 || e.Required != m.Fixtures[0].Bytes+m.Fixtures[1].Bytes || e.Budget != e.Required-1 || !e.Denied {
				return report, fmt.Errorf("budget: invalid reservation or denial")
			}
		}
		report.Checks = append(report.Checks, Check{Name: name, Passed: true, Detail: "raw bodies, source hashes, HTTP receipts and admission/model oracles verified"})
	}
	entries, err := os.ReadDir(filepath.Join(outDir, "ready"))
	if err != nil {
		return report, err
	}
	if len(entries) != len(readyExpected) {
		return report, fmt.Errorf("unexpected ready objects")
	}
	for _, entry := range entries {
		if !readyExpected[entry.Name()] || entry.IsDir() {
			return report, fmt.Errorf("unexpected ready object %s", entry.Name())
		}
	}
	partials, err := os.ReadDir(filepath.Join(outDir, "partial"))
	if err != nil {
		return report, err
	}
	if len(partials) != 0 {
		return report, fmt.Errorf("unfinished transfer")
	}
	return report, nil
}
