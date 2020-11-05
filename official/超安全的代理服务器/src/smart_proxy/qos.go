package main

import (
	"time"
)

var qosTable = make(map[string]int)

const (
	maxPerPeriod = 1
	period       = 1 * time.Second
)

func init() {
	go qosClear()
}

func qosClear() {
	tr := time.NewTicker(period)
	defer tr.Stop()

	for {
		<-tr.C
		qosTable = make(map[string]int)
	}
}

func qosAdd(ip string) {
	qosTable[ip]++
}

func qosCheck(ip string) bool {
	c, ok := qosTable[ip]
	if !ok {
		return true
	}
	return c <= maxPerPeriod
}
