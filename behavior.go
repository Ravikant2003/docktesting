package main

import (
	"context"
	"fmt"
	"math/rand"
	"time"

	"github.com/chromedp/chromedp"
)

// BehaviorSimulator provides human-like browser behavior
type BehaviorSimulator struct {
	MinDelay time.Duration
	MaxDelay time.Duration
}

// NewBehaviorSimulator creates a new behavior simulator
func NewBehaviorSimulator() *BehaviorSimulator {
	return &BehaviorSimulator{
		MinDelay: 500 * time.Millisecond,
		MaxDelay: 3000 * time.Millisecond,
	}
}

// RandomDelay adds a random delay between min and max
func (bs *BehaviorSimulator) RandomDelay() time.Duration {
	delay := time.Duration(rand.Intn(int(bs.MaxDelay-bs.MinDelay))) + bs.MinDelay
	return delay
}

// SimulateScrolling simulates random scrolling behavior
func (bs *BehaviorSimulator) SimulateScrolling(ctx context.Context) error {
	// Random number of scroll actions
	scrollCount := rand.Intn(3) + 1

	for i := 0; i < scrollCount; i++ {
		// Random scroll distance
		scrollDistance := rand.Intn(500) + 200
		scrollScript := fmt.Sprintf(`window.scrollBy(0, %d);`, scrollDistance)

		err := chromedp.Evaluate(scrollScript, nil).Do(ctx)
		if err != nil {
			return err
		}

		// Random delay between scrolls
		time.Sleep(bs.RandomDelay())
	}

	return nil
}

// SimulateMouseMovement simulates random mouse movements
func (bs *BehaviorSimulator) SimulateMouseMovement(ctx context.Context) error {
	// Simulate multiple random mouse movements
	moveCount := rand.Intn(3) + 1

	for i := 0; i < moveCount; i++ {
		x := rand.Intn(1920)
		y := rand.Intn(1080)

		// JavaScript to simulate mouse move (logging)
		script := fmt.Sprintf(`
			(function() {
				const evt = new MouseEvent('mousemove', {
					bubbles: true,
					cancelable: true,
					view: window,
					clientX: %d,
					clientY: %d
				});
				document.dispatchEvent(evt);
			})();
		`, x, y)

		err := chromedp.Evaluate(script, nil).Do(ctx)
		if err != nil {
			return err
		}

		// Random delay between movements
		time.Sleep(bs.RandomDelay())
	}

	return nil
}

// SimulateTyping simulates text input with human-like timing
func (bs *BehaviorSimulator) SimulateTyping(ctx context.Context, selector string, text string) error {
	// Focus on element
	err := chromedp.Focus(selector).Do(ctx)
	if err != nil {
		return err
	}

	// Type character by character with random delays
	for _, char := range text {
		err := chromedp.Evaluate(fmt.Sprintf(`
			document.querySelector('%s').value += '%c';
			document.querySelector('%s').dispatchEvent(new Event('input', { bubbles: true }));
		`, selector, char, selector), nil).Do(ctx)

		if err != nil {
			return err
		}

		// Random delay between keystrokes (simulate human typing speed)
		keystrokeDelay := time.Duration(rand.Intn(100)+30) * time.Millisecond
		time.Sleep(keystrokeDelay)
	}

	return nil
}

// WaitForContent waits for page content with retry logic
func (bs *BehaviorSimulator) WaitForContent(ctx context.Context, minContentLength int, maxWaitTime time.Duration) error {
	startTime := time.Now()

	for {
		var contentLength int
		err := chromedp.Evaluate(`document.body.innerHTML.length`, &contentLength).Do(ctx)

		if err == nil && contentLength >= minContentLength {
			return nil
		}

		if time.Since(startTime) > maxWaitTime {
			return fmt.Errorf("timeout waiting for content (got %d bytes, expected %d)", contentLength, minContentLength)
		}

		// Wait a bit before retrying
		time.Sleep(500 * time.Millisecond)
	}
}

// SimulateUserInteraction performs random user-like interactions
func (bs *BehaviorSimulator) SimulateUserInteraction(ctx context.Context) error {
	// Randomly choose interaction type
	interactionType := rand.Intn(3)

	switch interactionType {
	case 0:
		// Scroll
		return bs.SimulateScrolling(ctx)
	case 1:
		// Mouse movement
		return bs.SimulateMouseMovement(ctx)
	case 2:
		// Wait and do nothing (human-like reading time)
		time.Sleep(bs.RandomDelay())
		return nil
	}

	return nil
}
