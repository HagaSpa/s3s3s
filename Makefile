.PHONY: build
build:
	${call build}

.PHONY: test
test:
	if [ ! -d "test_libs" ]; then ${call install}; fi
	${call test}

.PHONY: rm-test-libs
rm-test-libs:
	rm -rf test_libs

define build
	docker build -t s3s3s:latest .
endef

define test
	docker run -it --rm -v `pwd`/tests:/usr/src/app/tests -v `pwd`/test_libs:/usr/src/test_libs -e PYTHONPATH=/usr/src/test_libs s3s3s:latest python -m pytest -v -p no:warnings
endef

define install
	docker run -it --rm -v `pwd`:/usr/src/app -w /usr/src/app python:3.8-alpine sh -c "apk add build-base libffi-dev && apk add openssl-dev && pip install -t test_libs pytest moto"
endef
