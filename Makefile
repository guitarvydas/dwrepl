#	'ensure that formatted text option in draw.io is disabled everywhere'

D2J=./das2json/mac/das2json

all:
	${D2J} test.drawio
	python3 repl.claude.py . - "Hello World" main test.drawio.json

## house-keeping

clean:
	rm -rf *.json
	rm -rf junk*
	rm -rf temp.*
	rm -rf *~
	rm -rf __pycache__

install-js-requires:
	npm install yargs prompt-sync ohm-js

