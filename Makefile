.PHONY: build publish

build:
	docker build . -t eamonnfaherty83/aws-statement-builder

publish:
	docker push eamonnfaherty83/aws-statement-builder
