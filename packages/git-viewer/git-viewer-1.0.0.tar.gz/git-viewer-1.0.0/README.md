An interactive git viewer based on urwid.
Similar to gitk but in a terminal.

![screenshot of log view and details view being displayed next to each other](screenshot/log_and_details.png)
The log view showing the history of commits (left) and a details view showing more information for the selected commit incl diff with line numbers and a list of other commits referencing this commit (right)

![screenshot of the details view showing link hints after pressing f](screenshot/follow.png)
A details view showing link hints after pressing f, pressing the key indicated in the square brackets with blue background will open that git object.
Line numbers are not available if `--word-diff` is used which can be toggled with `W`.

![screenshot of the list of keyboard shortcuts](screenshot/list_of_keyboard_shortcuts.png)
The list of keyboard shortcuts can be opened by pressing `F2` or `s`.
It adapts automatically if you (re)map keys in your config file.


Advantages over `gitk`:

- you can stay on the command line, no need to open a new window, although you can open a separate terminal and run it there if you want to
- no problems with resizing window
- window does not need to be as big
- keyboard navigation
- shows untracked files
- shows stashes
- line numbers in front of changed lines
- shows commits which mention the current commit in their commit message
- uses the colors of your terminal, no need to change the colors in yet another program
- more configurable
- you can directly open the current file at the current line in an editor

Advantages over `git log`/`git diff`:

- interactively select a commit and look into it without needing to copy and paste a hash
- hash ids are recognized as links which you can follow
- separators between different files in diff for a better overview
- easy copy of different information via keyboard (requires `wl-copy`, `xclip` or `xsel`)
- line numbers in front of changed lines

Implemented features:

- display git log
- select a commit
- open a commit (display details including a diff)
- show referencing commits
- open an annotated tag
- open a file (display it's entire contents at a certain commit)
- hash ids are recognized as links which you can follow
- yank different information (`yy` for hash, `yt` for title, `yc` for committer, ...)
- display unstaged changes and index
- display stashed changes
- show line numbers in front of changed lines referring to the version after the change
- switch to line numbers referring to the version before the change with `X`
- jump to commit with `"`
- search with `/` (forward) or `?` (backward)
- passing through command line arguments to git
- show unreachable commits with `gitl --unreachable` (in case you accidentally dropped a still needed stash, see also git stash --help/Recovering stash entries)
- enable or disable line breaks with the settings app.wrap and details-view.wrap
- `Control+o`/`Control+i` jump to previously/next selected line
- jump to next file in details view with `]]` and to previous with `[[`
- jump to next hunk in details view with `}` and to previous with `{`
- side by side view of log and details (enable with `e` and disable with `w`)
- open the file in the working directory with `o`
- open the file as it was after the current commit with `i`
- open the file as it was before the current commit with `U`/`I` (left/right version in case of a merge)
- reload with `F5`
- config with `p`
- help with `F1`
- list of all keyboard short cuts with `F2` (changes automatically if you rebind keys)
- help for all commands which can be used in config files or that keys can be bound (`F3`)
- help for all settings (`F4`)
- help for command line options with `gitl --help`, `gitd --help` and `gits --help`

Ideas for future versions:

- open commit in ranger
- bash auto completion
- list of tags (for the time being: `gitl --no-walk --tags`)
- list of changed/added/deleted files (expand/collapse diff)
- command line
- show content of new files
- mark a line with mx, jump to it with 'x or `x (In this program there is no difference between a backtick and a single quote because there is only linewise motion.)
- jump to next merge with `{ and jump to last split with `}
- star/hash: search for current title
- set terminal title

Known bugs:

- depending on the color settings of your terminal colored text has a different background color.
  [Monokai](https://github.com/adi1090x/kitty-cat/blob/master/colors/Monokai.conf)
  and [Gruvbox_light](https://github.com/adi1090x/kitty-cat/blob/master/colors/Gruvbox_light.conf)
  do not have this problem.
- with some terminals (e.g. kitty and alacritty) when decreasing the window width and thus causing lines containing full width characters to break duplicates of the full width characters appear in the first column of the indentation.
  When increasing the window width again those duplicates disappear.
  You can avoid this with `--explicit-spaces` (if your urwid version is new enough),
  by disabling the indentation using `--align left` possibly in combination with `--wrap clip` (or `--wrap ellipsis` if your urwid version is new enough)
  or using another terminal (e.g. termite or sakura).
- urwid crashes if you reduce the window width down to two screen columns and use full width characters and the log history is longer than your screen, see https://github.com/urwid/urwid/issues/468

Known issues with outdated urwid versions:

- urwid 2.0.1: `--wrap ellipsis` and `--explicit-spaces` are not supported
- urwid 1.3.1: search does not work well (selected line is sometimes not updated)


# Installation

## Installation via pip

```bash
$ pip install git-viewer
```

## Development install

If you want to tinker with the code:

```bash
$ git clone https://gitlab.com/erzo/git-viewer.git git-viewer
$ pip install -e git-viewer
```

## Manual install

This program requires Python 3.5 or newer and is *not* compatible with Python 2.
It depends on the nonstandard library [urwid](https://pypi.org/project/urwid/) for the user interface which can be installed with `pip3 install --user urwid` or via the system package manager.
This program is a wrapper around git therefore git needs to be installed.

Most features work with urwid 1.3.1 but not all of them, see the list of *Known issues with outdated urwid versions* above.
I recommend using a newer version.

Since this program is installable via pip it is not possible to execute it directly.
Instead the code must be placed somewhere where python finds it as a package and then you can run it with `python -m git_viewer`.

### Installing dependencies on Arch

```bash
$ sudo pacman -Syu
$ sudo pacman -S python python-urwid git
```

### Installing dependencies on Debian

```bash
$ sudo apt install python3
$ sudo apt install python3-urwid
$ sudo apt install git
```

### Installing this program

Run the following commands from the directory where you want to keep the git repository.
Keeping the git repository is important so you can easily do updates.

```bash
$ git clone 'https://gitlab.com/erzo/git-viewer.git' git-viewer
$ # if several versions of python3 are installed be careful to replace the * with the correct version
$ ln -s "$(realpath git-viewer/src/git_viewer)" ~/.local/lib/python3*/site-packages/
$ echo 'python -m git_viewer "$@"' >  ~/.local/bin/gitl
$ echo 'python -m git_viewer.diff "$@"' >  ~/.local/bin/gitd
$ echo 'python -m git_viewer.show "$@"' >  ~/.local/bin/gits
$ chmod a+x ~/.local/bin/git[lds]
```

If `ln` or `echo` fail with `No such file or directory` create the necessary directories with `mkdir -p <path>` and repeat the command.

Make sure ~/.local/bin is contained in your PATH variable.
(You can check this using `echo "$PATH"`.)
If it is not, add it:

```bash
$ echo 'export PATH="$PATH:$HOME/.local/bin"' >>~/.profile
```

If ~/.profile is not loaded automatically, load it from .xsessionrc or however that config file is called on your system:

```bash
$ echo '[ -f ~/.profile ] && . ~/.profile' >>~/.xsessionrc
```

## Optional dependencies

- `wl-copy` (on Wayland) or `xclip` (on X) for copying to the clipboard
- the python library `packaging` for checking the version of the urwid library,
  you don't need this if you are using urwid 2.1.0 or newer
  but with older urwid versions unsupported options can otherwise lead to unexpected crashes
- one of the python libraries `appdirs`, `xdgappdirs` or `platformdirs` in order to look for config files.
  Without these libraries "$XDG_CONFIG_HOME/git-viewer/config" and "~/.config/git-viewer/config" are tried.


# Updates

Change directory to the git repository and run `git pull`.


# Usage

This program has three entry points:
- `python3 -m git_viewer` which is equivalent to `python3 -m git_viewer.log` aka `gitl`, the main entry point.
- `python3 -m git_viewer.diff` aka `gitd`, a wrapper around `git diff` using the details view of `gitl`.
- `python3 -m git_viewer.show` aka `gits`, a wrapper around `git show` using the details view of `gitl`.

See `gitl --help`, `gitd --help` and `gits --help` for the supported command line arguments.

Run gitl and
- press `F1` or `x` for an introduction how to use git-viewer
- press `F2` or `s` for a list of all keyboard shortcuts
- press `F3` or `c` for a list of all commands which can be mapped to keys and used in config files
- press `F4` or `d` for a list of all settings

A raw version of the introduction (without the automatically added keyboard shortcuts for the corresponding commands) can be displayed [here](doc/intro.md).


# vim integration

Putting the following line in your vimrc will show the commit under the cursor when pressing Ctrl+C (one of the few keyboard shortcuts which is not defined by default).
This is useful when writing commit messages or doing an interactive rebase.

```vim
map <c-c> :!gits <c-r><c-w><cr><cr>
```

Open the commit in a new window (using kitty):

```vim
map <c-c> :call OpenCommitInNewWindow()<cr>

let b:cmdpipe = ""
function! OpenCommitInNewWindow() abort
	if ! filereadable(b:cmdpipe)
		echo "no pipe"
		let b:cmdpipe = substitute(system('mktemp -u'), '\n\+$', '', '')
		call system("mkfifo '" . b:cmdpipe . "'")
		execute "silent ! kitty gits --command-pipe '" . b:cmdpipe . "' &"
	endif
	execute "silent !echo 'select " . expand('<cword>') . "' >>'" . b:cmdpipe . "'"
	redraw!
endfunction
```

(The `--command-pipe` option uses polling to check if something has been read from the pipe. The polling time can be adjusted with `set app.command-pipe-poll-time=<time-in-seconds>`.)
