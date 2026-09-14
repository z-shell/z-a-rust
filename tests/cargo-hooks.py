#!/usr/bin/env python3
"""Run with python3 tests/cargo-hooks.py; no Rust toolchain or network needed."""
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[1]
handler = Path(os.environ.get("RUST_HANDLER", repo / "functions/.za-rust-atclone-handler"))
with tempfile.TemporaryDirectory(prefix="rust-hooks-") as temporary:
    root = Path(temporary)
    installed = root / "installed crates"
    system = root / "system"
    for directory in (installed / "bin", system):
        directory.mkdir(parents=True)
        cargo = directory / "cargo"
        cargo.write_text('#!/bin/sh\nprintf "%s\\n" "$0" "$@" > "$CARGO_LOG"\nexit "$CARGO_EXIT"\n')
        cargo.chmod(0o755)
    rustup = installed / "bin/rustup"
    rustup.write_text("#!/bin/sh\nexit 0\n")
    rustup.chmod(0o755)
    for local in (False, True):
        for hook in ("atclone-20", "atpull-20"):
            for failure in (0, 17):
                log = root / "cargo.log"
                log.unlink(missing_ok=True)
                environment = dict(os.environ, PATH=str(system) + os.pathsep + os.environ["PATH"],
                                   CARGO_LOG=str(log), CARGO_EXIT=str(failure))
                script = r'''
builtin emulate -R zsh
typeset -A ICE=(cargo 'cargo-expand;cargo-audit') OPTS=('opt_-q,--quiet' 1) ZI
[[ $4 == True ]] && ICE[rustup]=''
+zi-message() { :; }
.za-rust-download-file-stdout() { print -r -- $'#!/bin/sh\nexit 0'; }
run_hook() { source "$1" plugin z-shell fixture fixture "$2" "$3"; }
run_hook "$1" "$2" "$3"
'''
                result = subprocess.run(["zsh", "-f", "-c", script, "test", str(handler),
                                         str(installed), hook, str(local)], env=environment,
                                        capture_output=True, text=True)
                assert result.returncode == failure, (local, hook, failure, result.stderr)
                expected = installed / "bin/cargo" if local else system / "cargo"
                assert log.read_text().splitlines() == [str(expected), "install", "--root",
                                                        str(installed), "cargo-expand", "cargo-audit"]
print("ok - clone/update use selected Cargo, preserve spaced roots and propagate failures")
