# Top-level Makefile

# Specify the directory where the other Makefile is located
MODELS_DIR := models

# Default target
all:
	$(MAKE) -C $(MODELS_DIR)

# Catch-all target: any target not defined here will be passed to the models Makefile
%:
	$(MAKE) -C $(MODELS_DIR) $@

