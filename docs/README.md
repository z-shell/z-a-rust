<h2 align="center">
  <a href="https://github.com/z-shell/zi">
    <img src="https://github.com/z-shell/zi/raw/main/docs/images/logo.svg" alt="Logo" width="80" height="80" />
  </a>
❮ ZI ❯ Annex -Rust
</h2>

## **Wiki:** [z-a-rust](https://github.com/z-shell/zi/wiki/z-a-rust)

An Annex that installs rust and cargo packages locally inside the
plugin or snippet directories. The crate can then have a so called _shim_
created (name borrowed from `rbenv`) – a script that's located in the standard
`$PATH` entry "`$ZPFX/bin`" of following contents (example):

```zsh
#!/usr/bin/env zsh

function lsd {
	local bindir="/root/.zi/plugins/z-shell---null/bin"
	local -x PATH="/root/.zi/plugins/z-shell---null"/bin:"$PATH" # -x means export
	local -x RUSTUP_HOME="/root/.zi/plugins/z-shell---null"/rustup CARGO_HOME="/root/.zi/plugins/z-shell---null"

	"$bindir"/"lsd" "$@"
}

lsd "$@"
```

As it can be seen shim ultimately provides the binary to the command line.

## Installation

Simply load like a regular plugin, i.e.:

```zsh
zi light z-shell/z-a-rust
```

This installs the annex and makes the `rustup` and `cargo''` ices available.
