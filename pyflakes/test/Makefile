# ---------------------------------------------------------------

# Export which make was called
#export MAKE

# ---------------------------------------------------------------

# readlink -f  on LINUX

TOP 		?= $(shell stat -f %N .)/../..
CWD 		?= $(shell stat -f %N .)

# ---------------------------------------------------------------

# - terse or verbose make output
VERBOSE		?= 0

# ---------------------------------------------------------------

PYTHON	= python

# ---------------------------------------------------------------

define TEST_RUN_FILE
	echo TEST $(1) \
	&& $(PYTHON) $(CWD)/$(1)
endef

# ---------------------------------------------------------------
# list of all test files
#

TESTS.api             = test_api.py
TESTS.comparestmts    = test_comparestmts.py
TESTS.dict            = test_dict.py
TESTS.doctests        = test_doctests.py
TESTS.global          = test_global.py
TESTS.imports         = test_imports.py
TESTS.other           = test_other.py
TESTS.return          = test_return_with_arguments_inside_generator.py
TESTS.undefined_names = test_undefined_names.py

TESTS.all = \
	$(TESTS.api) \
	$(TESTS.comparestmts) \
	$(TESTS.dict) \
	$(TESTS.doctests) \
	$(TESTS.global) \
	$(TESTS.imports) \
	$(TESTS.other) \
	$(TESTS.return) \
	$(TESTS.undefined_names)

# ---------------------------------------------------------------
	
run.%:
	@echo running TESTS.$(subst run.,,$@)
	@for TST in $(TESTS.$(subst run.,,$@)) ; do $(call TEST_RUN_FILE,$$TST) ; done

# ---------------------------------------------------------------

all:: run.all

clean:: ; @rm -rf RESULTS

