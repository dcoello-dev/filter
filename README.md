# filter

filter g++ and gtest terminal output to give more readable output

```bash
# add this function to your .bashrc and place filter.py in ~/.config/filter
function flt () {
    CMD="$*"
    script -q -O /tmp/typescript -c "${CMD} 2>&1" | python3 ~/.config/filter/filter.py
}
```
