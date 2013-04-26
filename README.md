# wadlToWfuzz

## Execution
```
usage: wadlToWfuzz.py [-h] -d DOMAIN -f FILENAME [-w]

optional arguments:
  -h, --help            show this help message and exit

main arguments:
  -d DOMAIN, --domain DOMAIN Domain to check
  -f FILENAME, --filename FILENAME default : application.wadl
  -w, --wfuzz  wizzard for wfuzz url

```

Only display methods
```
./wadlToWfuzz.py -d <domain> -f application.wadl
```

Wizzard interaction [If no value input for a variable, variable = FUZZ]
```
./wadlToWfuzz.py -d <domain> -f application.wadl -w
```


