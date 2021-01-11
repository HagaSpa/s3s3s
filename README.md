# s3s3s
![Actions Status](https://github.com/HagaSpa/s3s3s/workflows/test/badge.svg)

S3 to S3 Sender

## s3 path

`s3://{src_bucket}/{table}/{yyyymmdd}/*` -> `s3://{dest_bucket}/{table}/{yyyymmdd}/*`

## Build

```
$ make build
```

## Test

```
$ make test
```

## Run
### Environment Parameter
| name | required | default_value | description |
|:---|:---|:---|:---|
| src_bucket | Y | - | source s3 name |
| dest_bucket | Y | - | destination s3 name |
| table | Y | - | table (directory) name in source s3 |
| src_access_key | N | - | (source) aws access key |
| src_secret_key | N | - | (source) aws secret key |
| dest_access_key | N | - | (destination) aws access key  |
| dest_secret_key | N | - | (destination) aws secret key |
| date | N | [ (JST) format(today-1, "%Y%m%d") ] | directory name in ddirectory in source s3 |


```
$ docker run \
    -e src_bucket=src_bucket_name \
    -e dest_bucket=dest_bucket_name \
    -e table=t1 \
    -e src_acccess_key=${src_access_key} \
    -e src_secret_key=${src_secret_key} \
    -e dest_access_key=${dest_access_key} \
    -e dest_secret_key=${dest_secret_key} \
    -e date=20191119
    <Image ID>:<tag>
```


