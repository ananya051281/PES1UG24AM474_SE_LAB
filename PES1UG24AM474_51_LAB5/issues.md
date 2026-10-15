# Identified Issues

Line numbers refer to the original `parking_lot_system.py`. Rows are ordered by severity: Bandit High and Medium first, then bugs, then style.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605) | Security – High | 64 | `os.system("echo ... " + filename)` passes the filename to a shell, so a crafted filename such as `x & del *` would run extra commands. | Removed the shell call and used `print()` to report the export. |
| Weak MD5 hash (Bandit B324) | Security – High | 53 | `hashlib.md5` is broken and should not be used to identify vehicles. | Switched to `hashlib.sha256`. |
| Use of `eval` (Bandit B307, Pylint W0123) | Security – Medium | 46–49 | `eval(surge_expr)` runs any text it is given as Python code. | Changed the function to take a numeric `surge_multiplier` and compute `base_rate * float(surge_multiplier)`. |
| Hardcoded secret, printed (not flagged by Bandit) | Security | 76, 85 | The barrier gate token was in the source code and printed to the console. Bandit missed it because the variable name `gate_barrier_key` doesn't match its password patterns. | Read from the `GATE_BARRIER_KEY` environment variable. Only whether a key is set is printed, never its value. |
| Mutable default argument (Pylint W0102) | Bug | 15 | `entry_logs=[]` is created once and shared by every call, so entries leak between calls. The log was also never shown. | Default changed to `None` and a new list is created inside the function. `main()` passes its own log and prints it. |
| Bare `except: pass` (Bandit B110, Pylint W0702, Flake8 E722) | Bug / Security – Low | 28–33 | Every error was hidden, and releasing an unknown slot gave no feedback. | Replaced with an explicit check for the slot. The function returns `False` for unknown slots and `True` on success. |
| Insecure random (Bandit B311) | Security – Low | 57 | `random` is predictable, so ticket PINs could be guessed. | Used `1000 + secrets.randbelow(9000)`, which gives the same 1000–9999 range. |
| Global statement (Pylint W0603, C0103) | Code smell | 12, 16, 22 | `global total_collections` makes the function depend on hidden module state. The total was also never displayed. | Replaced with a module-level `collections` dictionary, which needs no `global`. `main()` now prints the total. |
| Log message hid the charge | Bug (not flagged by tools) | 23 | The entry said "with total charge calculated" but never included the charge. | The log now includes the actual charge, for example `charge 60.00`. |
| File not closed safely (Pylint R1732, W1514) | Bug | 61–63 | `open()`/`close()` leaks the file handle if `write()` fails, and the encoding depends on the platform. | Used a `with` block and `encoding="utf-8"`. |
| Shadowed name, unused loop variable (Pylint W0621, W0612) | Code smell | 67–72 | The parameter `parking_slots` hid the global of the same name, and the loop variable `s` was never used. | Renamed the parameter to `slots` and replaced the loop with `sum(...)` over `slots.values()`. |
| Unused variables (Pylint W0612, Flake8 F841) | Code smell | 37, 47 | `overtime_fee` was never used. `base_rate` only appeared to be unused because it was referenced inside the `eval` string. | Removed `overtime_fee`. `base_rate` is now used directly. |
| Unused import (Pylint W0611, Flake8 F401) | Style | 4 | `math` was imported but never used. | Removed the import. |
| `== None` comparison (Pylint C0121, Flake8 E711) | Style | 38 | Comparisons to `None` should use `is`. | Rewrote `check_slot_availability` to use `is not None`. |
| Overly complex if/else (Pylint R1703, R1705) | Style | 40–43 | An `if`/`else` that returns `True` or `False` can be a single expression. | Replaced with `return slot is not None and not slot["is_occupied"]`. |
| Naming convention (Pylint C0103) | Style | 15–67 | Eight functions used camelCase, such as `parkVehicle`, which breaks PEP 8. | Renamed them to snake_case, such as `park_vehicle`. |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 15–75 | Neither the module nor its functions were documented. | Added a module docstring and a docstring to each function. |
| Lines too long, `%` formatting (Flake8 E501, Pylint C0301, C0209) | Style | 7–9, 23 | Four lines were longer than 79 characters, one of them 131. | Wrapped the slot dictionaries and split the log message into f-strings. |
| Missing final newline (Pylint C0304, Flake8 W292) | Style | 88 | The file did not end with a newline. | Added the trailing newline. |
| `main()` runs on import | Bug (not flagged by tools) | 88 | Importing the module ran the whole demo and wrote a file. | Wrapped the call in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.10/10 (36 messages) | 10.00/10 (0 messages) |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 10 issues | 0 issues |
