package main

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/gonum/plot"
	"github.com/gonum/plot/plotter"
	"github.com/gonum/plot/plotutil"
	"github.com/gonum/plot/vg"
)

func init() {
	rand.Seed(time.Now().UTC().UnixNano())
}

func main() {
	cm := make(chan bool)
	for runs := 0; runs < 100; runs++ {
		go startSim(cm, runs)
	}

	for runs := 0; runs < 100; runs++ {
		<-cm
	}
}

func startSim(cm chan bool, counter int) {
	history := run(5)
	c := make(chan bool)
	go generateHist(history, c, counter)
	go generateTimeSeries(history, c, counter)
	for i := 0; i < 2; i++ {
		<-c
	}
	cm <- true
}

func run(years int) []float64 {
	c := company{100, 5}
	max := years * 365
	inflation := 0.02
	history := make([]float64, max)

	for i := 0; i < max; i++ {
		c.Value += c.Value * (inflation / 365)

		r := rand.Float32()
		if r < 0.98 {

		} else if r < 0.9902 {
			c.Value = c.Value * (1.0 + (c.StandardDeviation / c.Value))
		} else {
			c.Value = c.Value * (1.0 - (c.StandardDeviation / c.Value))
		}

		history[i] = c.deviate()
	}

	return history
}

type company struct {
	Value             float64
	StandardDeviation float64
}

func (c *company) deviate() float64 {
	return rand.NormFloat64()*c.StandardDeviation + c.Value
}

func generateTimeSeries(data []float64, c chan bool, counter int) {
	p, _ := plot.New()
	p.Title.Text = "Company data"

	xyValues := make(plotter.XYs, len(data))
	for i := range data {
		xyValues[i].X, xyValues[i].Y = float64(i), data[i]
	}

	_ = plotutil.AddLinePoints(p, xyValues)

	p.Save(50*vg.Centimeter, 25*vg.Centimeter, fmt.Sprintf("out/timeseries_%d.png", counter))
	c <- true
}

func generateHist(data []float64, c chan bool, counter int) {
	p, _ := plot.New()
	p.Title.Text = "Company data"

	values := make(plotter.Values, len(data))
	for i := range data {
		values[i] = data[i]
	}

	hist, _ := plotter.NewHist(values, 100)
	hist.Normalize(1)
	p.Add(hist)

	p.Save(50*vg.Centimeter, 25*vg.Centimeter, fmt.Sprintf("out/hist_%d.png", counter))

	c <- true
}
