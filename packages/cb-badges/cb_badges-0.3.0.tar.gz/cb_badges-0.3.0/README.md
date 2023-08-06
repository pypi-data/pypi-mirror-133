# cb-badges

`cb-badges` aims at creating meaningful & stylish badges for your project's `README` file - batteries included.

This project is a Python port of @lhinderberger's [`dot-slash-badges`](https://codeberg.org/lhinderberger/dot-slash-badges), which is written in Go.


## Getting started

This will install `cb-badges` along its dependencies inside a virtual environment, ready for action:

```bash
# Set up & activate virtualenv
virtualenv -p python3 venv && source venv/bin/activate

# Install dependencies
python -m pip install --editable .
```


## Usage

The following commands are available:

```text
$ badges --help
Usage: badges [OPTIONS] OUTPUT

  Writes SVG file to OUTPUT

Options:
  -s, --style TEXT     Set style (name or directory).
  -t, --theme TEXT     Set theme (name or file path).
  -p, --provider TEXT  Set provider (Codeberg, GitHub, ..).
  -m, --minify         Whether to minify SVG output.
  -v, --verbose        Enable verbose mode.
  --version            Show the version and exit.
  --help               Show this message and exit.
```

**Note:** All CLI options not listed above are passed to the template as-is - so if you wanted to change the font size to 18, passing `--font_size 18` does the trick, same goes for any other option including `text` properties like `--text_left` and `--text_right` (required by default style).


## Roadmap

- [x] Add tests
- [ ] Support fetching data on repositories like ..
    - .. stars, downloads, etc (GitHub / Codeberg)
    - .. build status (Drone / Woodpecker CI)
    - .. you-name-it


**Happy coding!**
