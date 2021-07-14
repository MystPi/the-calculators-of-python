# the-calculators-of-python
A few calculators made with different Python parsing libraries. These are the ones I used in this repo:
* [PLY](https://github.com/dabeaz/ply) | [plyCalc.py](src/plyCalc.py)
* [SLY](https://github.com/dabeaz/sly) | [slyCalc.py](src/slyCalc.py)
* [Lark](https://github.com/lark-parser/lark) | [larkCalc.py](src/larkCalc.py)

## Lark Calculator Example
```
> 1 + 1
2.0
> sin 45
0.8509035245341184
> sin 1 / cos 1
1.557407724654902
> tan 1
1.557407724654902
> 2*(3+4)
14.0
> round sin 1
1
```

## Usage
Assuming you're on Linux:
```bash
# PLY Calculator
python3 ~/the-calculators-of-python-main/src/plyCalc.py

# SLY Calculator
python3 ~/the-calculators-of-python-main/src/slyCalc.py

# Lark Calculator
python3 ~/the-calculators-of-python-main/src/larkCalc.py
```
Probably somewhat the same on Windows.
