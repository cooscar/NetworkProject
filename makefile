SCRIPT = luma
BIN_PATH = /usr/local/bin
LIB_PATH = /usr/local/lib/luma

REQ_FILE = requirements.txt
PYTHON = python3
PIP = pip

install:
	@echo "Installing $(SCRIPT) to $(BIN_PATH)..."
	mkdir $(LIB_PATH)
	mkdir ${LIB_PATH}/commands
	cp luma $(LIB_PATH)/
	cp -r commands/* $(LIB_PATH)/commands/
	@echo "Copied commands"
	install -m 755 $(SCRIPT) $(BIN_PATH)/$(SCRIPT)
	@echo "Installing Python requirements..."
	$(PIP) install --user -r $(REQ_FILE)
	@echo "Installation complete!"

uninstall:
	@echo "Removing $(BIN_PATH)/$(SCRIPT)..."
	rm -f $(BIN_PATH)/$(SCRIPT)
	@echo "Removing $(LIB_PATH)..."
	rm -rf $(LIB_PATH)
	@echo "Uninstall complete."
