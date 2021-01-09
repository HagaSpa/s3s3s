.PHONY: build
build:
	${call build}

define build
	docker build -t s3s3s:latest .
endef
