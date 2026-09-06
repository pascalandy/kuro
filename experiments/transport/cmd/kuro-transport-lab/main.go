package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	lab "kuro/transportlab"
	"os"
)

func execute(args []string) error {
	if len(args) == 0 || (args[0] != "run" && args[0] != "verify") {
		return fmt.Errorf("usage: kuro-transport-lab (run|verify) --out DIRECTORY")
	}
	flags := flag.NewFlagSet(args[0], flag.ContinueOnError)
	out := flags.String("out", "", "artifact directory")
	if err := flags.Parse(args[1:]); err != nil {
		return err
	}
	if *out == "" || flags.NArg() != 0 {
		return fmt.Errorf("--out is required; positional arguments are not accepted")
	}
	var report lab.Report
	var err error
	if args[0] == "run" {
		report, err = lab.Run(context.Background(), lab.Config{OutDir: *out})
	} else {
		report, err = lab.Verify(*out)
	}
	if err != nil {
		return err
	}
	return json.NewEncoder(os.Stdout).Encode(report)
}
func main() {
	if err := execute(os.Args[1:]); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
