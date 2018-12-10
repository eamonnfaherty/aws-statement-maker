.PHONY: build publish

build:
	docker build . -t eamonnfaherty83/statement-builder

publish:
	docker push eamonnfaherty83/statement-builder