# ------------------------------------------------------------------
# Makefile
#
# Bash automation.
#
# Usage:
#	$ make <target>
# ------------------------------------------------------------------
# Run all targets.
all: web flask

# Run the python flask web app.
flask:
	konsole -e flask run

# Launch the web app with a browser.
web:
	command google-chrome 127.0.0.1:5000

# Clean up.
clean:
	rm re sys output.txt