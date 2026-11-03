BOOKS := $(notdir $(wildcard books/*))
.PHONY: all list clean $(BOOKS)
all: $(BOOKS)
list:
	@for b in $(BOOKS); do printf '%-28s %s\n' $$b "$$(cat books/$$b/VERSION)"; done
$(BOOKS):
	./books/$@/build.sh
clean:
	rm -rf books/*/dist books/*/_work books/*/preview
