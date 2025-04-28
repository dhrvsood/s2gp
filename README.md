# s2gp
A [Songsterr](https://www.songsterr.com/) cli client to download files to guitar pro through links and search.

# Usage
Specify `SAVE_DIR` in a .env file. Otherwise program will default to current directory. After installing requirements, run python script.py using the following argument. 

- `--l`, `--links` : Links mode. Enter list separated songsterr.com links.
- `--p`, `--pattern` : Pattern mode. Enter a pattern similar to how you would search in the songsterr search bar.
  - `--n`, `--number` : Number of results to show up when applying pattern mode.