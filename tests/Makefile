REGRESSIONS :=  $(shell ls test_cases/)

.PHONY: $(REGRESSIONS)

all: $(REGRESSIONS)

$(REGRESSIONS):
	cd test_cases/$@ && $(MAKE)
