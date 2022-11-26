
# ============================================================================
# FUNCTIONS

# $(call build_subproj,name)
define build_subproj
@echo "building $1 ..."
@cd $1 && bash build.sh
endef

# $(call clean_subproj,name)
define clean_subproj
@echo "removing $1/build ..."
@rm -rf $1/build
endef



# ============================================================================
# TARGETS

.PHONY: 00 01 02 03 clean


all: clean 00 01 02 03

00:
	$(call build_subproj,$@)

01:
	$(call build_subproj,$@)

02:
	$(call build_subproj,$@)

03:
	$(call build_subproj,$@)

clean:
	@echo "removing build directories..."
	@find . -type d -name build -mindepth 2 -prune -exec rm -rf {} \;
