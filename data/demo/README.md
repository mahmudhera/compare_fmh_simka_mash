# Commands to run

## FMH
```
/usr/bin/time -v python ../../run_using_fmh/run_by_fmh_wrapper.py -i filelist_testrun_fmh -k 21 -s 1000 -m cosine -c 128 -o testrun_fmh_output -S 42 -p -P 8 -C 32
```

## SIMKA
```
python ../../run_using_simka/run_simka_wrapper.py -i filelist_testrun_fmh -k 21 -o ./simka_results -r simka_resource_usages
```