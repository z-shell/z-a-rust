<h1> ZI Annex Rust </h1>

This repository not compatible with previous versions (zplugin, zinit). Please upgrade to [ZI](https://github.com/z-shell-zi)

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

## Usage

The ZI Annex provides two new ices: `rustup` and `cargo''`. The first one
installs rust inside the plugin's folder using the official `rustup` installer.
The second one has the following syntax:

`cargo"[name-of-the-binary-or-path <-] [[!][c|N|E|O]:]{crate-name} [-> {shim-script-name}]'`

Example uses are:

```zsh
# Installs rust and then the `lsd' crate and creates
# the `lsd' shim exposing the binary
zi ice rustup cargo'!lsd'
zi load z-shell/null

# Installs rust and then the `exa' crate and creates
# the `ls' shim exposing the `exa' binary
zi ice rustup cargo'!exa -> ls'
zi load z-shell/null

# Installs rust and then the `exa' and `lsd' crates
zi ice rustup cargo'exa;lsd'
zi load z-shell/null

# Installs rust and then the `exa' and `lsd' crates
# and exposes their binaries by altering $PATH
zi ice rustup cargo'exa;lsd' as"command" pick"bin/(exa|lsd)"
zi load z-shell/null

# Installs rust and then the `exa' crate and creates
# its shim with standard error redirected to /dev/null
zi ice rustup cargo'!E:exa'
zi load z-shell/null

# Just install rust and make it available globally in the system
zi ice id-as"rust" wait"0" lucid rustup as"command" pick"bin/rustc" atload="export \
CARGO_HOME=\$PWD RUSTUP_HOME=\$PWD/rustup"
zi load z-shell/null

# A little more complex rustup configuration that uses Bin-Gem-Node annex
# and installs the cargo completion provided with rustup, using for-syntax
zi id-as=rust wait=1 as=null sbin="bin/*" lucid rustup \
	atload="[[ ! -f ${ZI[COMPLETIONS_DIR]}/_cargo ]] && zi creinstall rust; \
	export CARGO_HOME=\$PWD RUSTUP_HOME=\$PWD/rustup" for \
z-shell/null

```

Flags meanings:

- `N` – redirect both standard output and error to `/dev/null`
- `E` – redirect standard error to `/dev/null`
- `O` – redirect standard output to `/dev/null`
- `c` – change the current directory to the plugin's or snippet's directory before
  executing the command

As the examples showed, the name of the binary to run and the shim name are
by default equal to the name of the crate. Specifying `{binary-name} <- …`
and/or `… -> {shim-name}` allows to override them.

## Installation

Simply load like a regular plugin, i.e.:

```zsh
zi light z-shell/z-a-rust
```

This installs the annex and makes the `rustup` and `cargo''` ices available.
