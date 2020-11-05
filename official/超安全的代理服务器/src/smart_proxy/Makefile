build:
	clean
	go build -o build/ssv .

clean:
	rm -f build/ssv*

darwin:
	CGO_ENABLED=0 GOOS=darwin  GOARCH=amd64  go build -o build/ssv .
linux:
	CGO_ENABLED=0 GOOS=linux   GOARCH=amd64  go build -o build/ssv-linux .

all: clean darwin linux