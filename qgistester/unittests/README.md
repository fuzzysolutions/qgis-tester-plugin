To run unittest from CLI it is necessary to set some environment variables.
Here is an example using self-compiled QGIS:

```
export QGIS_PREFIX=/path/to/qgis/sources
export QGIS_PREFIX_PATH=${QGIS_PREFIX}"/build/output"
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${QGIS_PREFIX_PATH}"/lib"
export PYTHONPATH=${QGIS_PREFIX_PATH}"/python":${PYTHONPATH}
```

To run all tests:

```
python3 run_all_tests.py
```

To run a single suite of tests, e.g. for main plugin code:

```
python3 test_plugin.py
```
