package lab_test

import (
	"context"
	"encoding/json"
	"io/fs"
	"os"
	"path/filepath"
	"reflect"
	"testing"
	"time"

	lab "kuro/transportlab"
)

type artifactSnapshot struct {
	Bytes    string
	Mode     fs.FileMode
	Modified time.Time
}

func snapshotProof(t *testing.T, dir string) map[string]artifactSnapshot {
	t.Helper()
	files := make(map[string]artifactSnapshot)
	err := filepath.WalkDir(dir, func(path string, entry fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		info, err := entry.Info()
		if err != nil {
			return err
		}
		rel, err := filepath.Rel(dir, path)
		if err != nil {
			return err
		}
		var body []byte
		if !entry.IsDir() {
			body, err = os.ReadFile(path)
			if err != nil {
				return err
			}
		}
		files[rel] = artifactSnapshot{Bytes: string(body), Mode: info.Mode(), Modified: info.ModTime()}
		return nil
	})
	if err != nil {
		t.Fatal(err)
	}
	return files
}

func copyProof(t *testing.T, baseline map[string]artifactSnapshot) string {
	t.Helper()
	dir := filepath.Join(t.TempDir(), "copy")
	for name, file := range baseline {
		path := filepath.Join(dir, name)
		if file.Mode.IsDir() {
			if err := os.MkdirAll(path, 0755); err != nil {
				t.Fatal(err)
			}
			continue
		}
		if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(path, []byte(file.Bytes), file.Mode.Perm()); err != nil {
			t.Fatal(err)
		}
	}
	return dir
}

func assertSevenPassingChecks(t *testing.T, report lab.Report) {
	t.Helper()
	want := map[string]bool{"clean": false, "corrupt": false, "truncate": false, "resume": false, "changed-etag": false, "stall": false, "budget": false}
	if report.Version < 1 {
		t.Errorf("invalid report version %d", report.Version)
	}
	if len(report.Checks) != len(want) {
		t.Fatalf("got %d checks, want seven", len(report.Checks))
	}
	for _, check := range report.Checks {
		seen, ok := want[check.Name]
		if !ok || seen {
			t.Errorf("unexpected or duplicate check %q", check.Name)
		}
		want[check.Name] = true
		if !check.Passed {
			t.Errorf("check %q failed: %s", check.Name, check.Detail)
		}
	}
	for name, seen := range want {
		if !seen {
			t.Errorf("missing check %q", name)
		}
	}
}

func TestRunAndVerifyIndependentEvidence(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	dir := filepath.Join(t.TempDir(), "proof")
	report, err := lab.Run(ctx, lab.Config{OutDir: dir})
	if err != nil {
		t.Fatal(err)
	}
	assertSevenPassingChecks(t, report)
	baseline := snapshotProof(t, dir)
	verified, err := lab.Verify(dir)
	if err != nil {
		t.Fatal(err)
	}
	assertSevenPassingChecks(t, verified)
	if !reflect.DeepEqual(report, verified) {
		t.Errorf("Run and Verify disagree: %+v / %+v", report, verified)
	}
	if after := snapshotProof(t, dir); !reflect.DeepEqual(baseline, after) {
		t.Fatal("Verify modified proof contents or metadata")
	}

	t.Run("summary is not evidence", func(t *testing.T) {
		copyDir := copyProof(t, baseline)
		for i := range report.Checks {
			report.Checks[i].Passed = false
		}
		body, err := json.Marshal(report)
		if err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(filepath.Join(copyDir, "report.json"), body, 0644); err != nil {
			t.Fatal(err)
		}
		got, err := lab.Verify(copyDir)
		if err != nil {
			t.Fatalf("summary booleans overrode valid raw evidence: %v", err)
		}
		assertSevenPassingChecks(t, got)
	})

	rawFiles := 0
	for name, file := range baseline {
		if file.Mode.IsDir() || name == "report.json" {
			continue
		}
		rawFiles++
		t.Run("missing/"+name, func(t *testing.T) {
			copyDir := copyProof(t, baseline)
			if err := os.Remove(filepath.Join(copyDir, name)); err != nil {
				t.Fatal(err)
			}
			if _, err := lab.Verify(copyDir); err == nil {
				t.Fatalf("Verify accepted missing evidence %s with passing summary", name)
			}
		})
		if filepath.Ext(name) == ".json" {
			continue
		}
		t.Run("corrupt/"+name, func(t *testing.T) {
			copyDir := copyProof(t, baseline)
			if err := os.Chmod(filepath.Join(copyDir, name), 0600); err != nil {
				t.Fatal(err)
			}
			body := []byte(file.Bytes)
			if len(body) == 0 {
				body = []byte{1}
			} else {
				body[len(body)/2] ^= 1
			}
			if err := os.WriteFile(filepath.Join(copyDir, name), body, 0644); err != nil {
				t.Fatal(err)
			}
			if _, err := lab.Verify(copyDir); err == nil {
				t.Fatalf("Verify accepted corrupted evidence %s with passing summary", name)
			}
		})
	}
	if rawFiles == 0 {
		t.Fatal("Run produced no raw evidence")
	}
}

func TestRunRefusesExistingOutput(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "sentinel")
	if err := os.WriteFile(path, []byte("keep this file"), 0600); err != nil {
		t.Fatal(err)
	}
	before := snapshotProof(t, dir)
	if _, err := lab.Run(context.Background(), lab.Config{OutDir: dir}); err == nil {
		t.Fatal("Run accepted existing output directory")
	}
	if after := snapshotProof(t, dir); !reflect.DeepEqual(before, after) {
		t.Fatal("refused Run changed existing output")
	}
}
