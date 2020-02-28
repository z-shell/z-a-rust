# z-a-rust

A Zsh-Zinit annex that installs rust and cargo packages locally inside the
plugin or snippet directories. The crate can then have a so called *shim*
created (name borrowed from `rbenv`) – a script that's located in the standard
`$PATH` entry "`$ZPFX/bin`" of following contents (example):

```zsh
#!/usr/bin/env zsh

function lsd {
    local bindir="/root/.zinit/plugins/zdharma---null/bin"
    local -x PATH="/root/.zinit/plugins/zdharma---null"/bin:"$PATH" # -x means export
    local -x RUSTUP_HOME="/root/.zinit/plugins/zdharma---null"/rustup \
            CARGO_HOME="/root/.zinit/plugins/zdharma---null"

    "$bindir"/"lsd" "$@"
}

lsd "$@"
```

As it can be seen shim ultimately provides the binary to the command line.

## Usage

The Zinit annex provides two new ices: `rustup` and `cargo''`. The first one
installs rust inside the plugin's folder using the official `rustup` installer.
The second one has the following syntax:

`cargo"[name-of-the-binary-or-path <-] [[!][c|N|E|O]:]{crate-name} [-> {shim-script-name}]'`

Example uses are:

```zsh
# Installs rust and then the `lsd' crate and creates
# the `lsd' shim exposing the binary
zinit ice rustup cargo'!lsd'
zinit load zdharma/null

# Installs rust and then the `exa' crate and creates
# the `ls' shim exposing the `exa' binary
zinit ice rustup cargo'!exa -> ls'
zinit load zdharma/null

# Installs rust and then the `exa' and `lsd' crates
zinit ice rustup cargo'exa;lsd'
zinit load zdharma/null

# Installs rust and then the `exa' and `lsd' crates
# and exposes their binaries by altering $PATH
zinit ice rustup cargo'exa;lsd' as"command" pick"bin/(exa|lsd)"
zinit load zdharma/null

# Installs rust and then the `exa' crate and creates
# its shim with standard error redirected to /dev/null
zinit ice rustup cargo'!E:exa'
zinit load zdharma/null

# Just install rust and make it available globally in the system
zinit ice id-as"rust" wait"0" lucid rustup as"command" \
            pick"bin/rustc" atload="export \
                CARGO_HOME=\$PWD RUSTUP_HOME=\$PWD/rustup"
zinit load zdharma/null

# A little more complex rustup configuration that uses Bin-Gem-Node annex
# and installs the cargo completion provided with rustup, using for-syntax
zinit id-as"rust" wait=1 as=null sbin="bin/*" lucid rustup \
    atload="[[ ! -f ${ZINIT[COMPLETIONS_DIR]}/_cargo ]] && zi creinstall rust; \
    export CARGO_HOME=\$PWD RUSTUP_HOME=\$PWD/rustup" for \
        zdharma/null

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
zinit light zinit-zsh/z-a-rust
```

This installs the annex and makes the `rustup` and `cargo''` ices available.

# Example

![example z-a-rust
use](https://raw.githubusercontent.com/zinit-zsh/z-a-rust/master/images/z-a-rust.png)

<!-- vim:set ft=markdown tw=80 fo+=an1 autoindent: -->
