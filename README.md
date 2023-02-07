# argo-probe-onboarding

ARGO probes checking the quality of the information collected during the on-boarding process. The package contains the `check_catalog` probe which can be used to check if the catalog contains the necessary field, can check if URLs defined in the fields are valid and also can check when the entry has last been updated.

## Synopsis

The probe has three required and four optional parameters. The required ones are the catalog URL, ID of entry being checked, and timeout in seconds. Optional parameters are the space separated list of keys (for some checks), and flags for checking URLs or date in `updated_at` flag.

```
# /usr/libexec/argo/probes/onboarding/check_catalog -h
usage: 
  ARGO probe that checks validity of entries in the service catalog
    -u URL -i SERVICE_ID -t TIMEOUT [-k KEY [KEY ...]] [--check-url | --check-age] [--age AGE_MONTHS] [-h]

required arguments:
  -u URL, --url URL     API endpoint URL
  -i ID, --id ID        Entry ID in the catalog
  -t TIMEOUT, --timeout TIMEOUT
                        Seconds before the connection times out (default 30)

optional arguments:
  -k [KEYS [KEYS ...]], --key [KEYS [KEYS ...]]
                        Space separated list of keys in API response that are going to be checked; probe returns CRITICAL if the key does not exist in API response or if its value is undefined
  --check-url           Flag to check the keys' value as URL; the probe returns CRITICAL if the URL response is different than OK
  --check-date          Flag to check the 'updated_at' key value as date; must be used with -a/--age parameter
  -a AGE, --age AGE     Age in months; used with --check-date; the probe returns WARNING if the date is older than AGE - 1, andCRITICAL if it is older than AGE
  -h, --help            Show this help message and exit
```

Example execution of probe if we want to test if a list of keys is available and non-empty in the catalog:

```
# /usr/libexec/argo/probes/onboarding/check_catalog -u https://catalog-url.example.com -i <entry_id> -t 30 -k <key1> <key2> <key3>
OK - Keys <key1>, <key2>, <key3> all defined
```

Example execution of probe if we want to test the URL defined in `<key>`:

```
# /usr/libexec/argo/probes/onboarding/check_catalog -u https://catalog-url.example.com -i <entry_id> -t 30 -k <key>
OK - URL valid
```

Example execution of probe if we want to test if the information is up-to-date. We use `--age` parameter (in months) to define the age after which the probe will return CRITICAL. If the `updated_at` entry in the catalog is one month from being marked as CRITICAL, the probe will start returning WARNING status.

```
# /usr/libexec/argo/probes/onboarding/check_catalog -u https://catalog-url.example.com -i <entry_id> -t 30 --check-date --age 12
OK - Resource description is up-to-date
```
