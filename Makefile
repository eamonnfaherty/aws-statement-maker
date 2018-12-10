.PHONY: build publish

TAG=eamonnfaherty83/aws-statement-maker

build:
	docker build . -t $(TAG)

publish:
	docker push $(TAG)
