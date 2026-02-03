package main

import (
	"fmt"
	"net/url"
	"os"
	"strings"
)

// ScraperAPIConfig holds ScraperAPI configuration
type ScraperAPIConfig struct {
	APIKey    string
	Enabled   bool
	RenderJS  bool
	CountryCode string
	Timeout   int
}

// NewScraperAPIConfig creates a new ScraperAPI configuration from environment
func NewScraperAPIConfig() *ScraperAPIConfig {
	apiKey := os.Getenv("SCRAPER_API_KEY")
	
	config := &ScraperAPIConfig{
		APIKey:      apiKey,
		Enabled:     apiKey != "" && apiKey != "none",
		RenderJS:    strings.ToLower(os.Getenv("SCRAPER_RENDER_JS")) == "true",
		CountryCode: os.Getenv("SCRAPER_COUNTRY_CODE"),
		Timeout:     10000, // Default 10 seconds
	}

	return config
}

// GetScraperURL converts a regular URL to ScraperAPI URL
func (sc *ScraperAPIConfig) GetScraperURL(targetURL string) string {
	if !sc.Enabled {
		return targetURL
	}

	// Base URL
	scraperURL := "http://api.scraperapi.com?api_key=" + sc.APIKey

	// Add target URL
	scraperURL += "&url=" + url.QueryEscape(targetURL)

	// Add optional parameters
	if sc.RenderJS {
		scraperURL += "&render=true"
	}

	if sc.CountryCode != "" {
		scraperURL += "&country_code=" + sc.CountryCode
	}

	if sc.Timeout > 0 {
		scraperURL += fmt.Sprintf("&timeout=%d", sc.Timeout)
	}

	return scraperURL
}

// IsEnabled checks if ScraperAPI is configured
func (sc *ScraperAPIConfig) IsEnabled() bool {
	return sc.Enabled
}

// GetStats returns ScraperAPI configuration statistics
func (sc *ScraperAPIConfig) GetStats() map[string]interface{} {
	return map[string]interface{}{
		"enabled":        sc.Enabled,
		"has_api_key":    sc.APIKey != "",
		"render_js":      sc.RenderJS,
		"country_code":   sc.CountryCode,
		"timeout_ms":     sc.Timeout,
		"cloudflare":     "✅ Automatically bypassed",
		"free_tier":      "1,000 requests/month",
		"api_endpoint":   "https://api.scraperapi.com",
	}
}

// PrintConfiguration prints ScraperAPI configuration to console
func (sc *ScraperAPIConfig) PrintConfiguration() {
	if !sc.Enabled {
		fmt.Println("🔗 ScraperAPI Configuration:")
		fmt.Println("   • Status: ❌ DISABLED (no API key configured)")
		fmt.Println("   • Setup: export SCRAPER_API_KEY=your_key")
		fmt.Println()
		return
	}

	fmt.Println("🔗 ScraperAPI Configuration:")
	fmt.Println("   • Status: ✅ ENABLED")
	fmt.Printf("   • API Key: %s...%s\n", sc.APIKey[:4], sc.APIKey[len(sc.APIKey)-4:])
	fmt.Printf("   • JavaScript Rendering: %v\n", sc.RenderJS)
	
	if sc.CountryCode != "" {
		fmt.Printf("   • Country Code: %s\n", sc.CountryCode)
	}
	
	fmt.Printf("   • Timeout: %dms\n", sc.Timeout)
	fmt.Println("   • Cloudflare Bypass: ✅ YES")
	fmt.Println("   • Free Tier: 1,000 requests/month")
	fmt.Println()
}

// ValidateConfiguration checks if ScraperAPI configuration is valid
func (sc *ScraperAPIConfig) ValidateConfiguration() error {
	if !sc.Enabled {
		return nil // ScraperAPI is optional
	}

	if sc.APIKey == "" {
		return fmt.Errorf("SCRAPER_API_KEY environment variable is not set")
	}

	if len(sc.APIKey) < 10 {
		return fmt.Errorf("API key appears to be invalid (too short)")
	}

	return nil
}

// GetEnvironmentExample returns example environment variables
func GetScraperAPIEnvironmentExample() string {
	return `
# Example .env or docker-compose environment variables:

# ScraperAPI Configuration
SCRAPER_API_KEY=your_free_api_key_from_dashboard

# Optional: Enable JavaScript rendering (slower but handles dynamic content)
SCRAPER_RENDER_JS=false

# Optional: Set country code for exit IP
SCRAPER_COUNTRY_CODE=US

# Or use as proxy in PROXY_URL
# PROXY_URL=http://api.scraperapi.com?api_key=YOUR_KEY

# Get free API key at: https://www.scraperapi.com/signup
# Free tier: 1,000 requests/month
`
}

// ExampleUsage shows how to use ScraperAPI
func ExampleScraperAPIUsage() string {
	return `
# Example 1: Set environment variable
export SCRAPER_API_KEY="your_free_api_key"

# Example 2: Run tests with ScraperAPI enabled
go run main.go profiles.go behavior.go config.go scraperapi.go

# Example 3: Check dashboard for usage
# https://dashboard.scraperapi.com

# Example 4: Test directly with curl
curl "http://api.scraperapi.com?api_key=YOUR_KEY&url=https://booking.com" | head -20

# Expected: HTML from booking.com (not Cloudflare challenge)
`
}
