package main

import (
	"fmt"
	"math/rand"
	"os"
	"strings"
	"sync"
	"time"
)

// ProxyConfig holds proxy configuration
type ProxyConfig struct {
	URL            string
	Username       string
	Password       string
	Server         string
	Port           string
	Type           string // http, https, socks5
	RotationEnabled bool
	ProxyList      []string
	CurrentIndex   int
	mu             sync.RWMutex
}

// NewProxyConfig creates a new proxy configuration from environment
func NewProxyConfig() *ProxyConfig {
	config := &ProxyConfig{
		URL:             os.Getenv("PROXY_URL"),
		Username:        os.Getenv("PROXY_USERNAME"),
		Password:        os.Getenv("PROXY_PASSWORD"),
		Server:          os.Getenv("PROXY_SERVER"),
		Port:            os.Getenv("PROXY_PORT"),
		Type:            os.Getenv("PROXY_TYPE"),
		RotationEnabled: strings.ToLower(os.Getenv("PROXY_ROTATION_ENABLED")) == "true",
		ProxyList:       make([]string, 0),
	}

	// If PROXY_TYPE not set, infer from URL
	if config.Type == "" && config.URL != "" {
		if strings.HasPrefix(config.URL, "socks5://") {
			config.Type = "socks5"
		} else if strings.HasPrefix(config.URL, "https://") {
			config.Type = "https"
		} else {
			config.Type = "http"
		}
	}

	return config
}

// IsEnabled checks if proxy is configured
func (pc *ProxyConfig) IsEnabled() bool {
	return pc.URL != "" && pc.URL != "none" && pc.URL != "disabled"
}

// GetProxyURL returns the current proxy URL
func (pc *ProxyConfig) GetProxyURL() string {
	pc.mu.RLock()
	defer pc.mu.RUnlock()

	return pc.URL
}

// GetChromeLaunchArg returns the Chrome launch argument for proxy
func (pc *ProxyConfig) GetChromeLaunchArg() string {
	if !pc.IsEnabled() {
		return ""
	}

	// Format for Chrome: --proxy-server="http://proxy:port"
	return fmt.Sprintf("--proxy-server=%q", pc.URL)
}

// SetProxyURL updates the proxy URL
func (pc *ProxyConfig) SetProxyURL(url string) {
	pc.mu.Lock()
	defer pc.mu.Unlock()

	pc.URL = url
}

// AddProxyToList adds a proxy to the rotation list
func (pc *ProxyConfig) AddProxyToList(proxy string) {
	pc.mu.Lock()
	defer pc.mu.Unlock()

	pc.ProxyList = append(pc.ProxyList, proxy)
}

// GetNextProxy returns the next proxy in rotation
func (pc *ProxyConfig) GetNextProxy() string {
	if !pc.RotationEnabled || len(pc.ProxyList) == 0 {
		return pc.URL
	}

	pc.mu.Lock()
	defer pc.mu.Unlock()

	if len(pc.ProxyList) == 0 {
		return pc.URL
	}

	proxy := pc.ProxyList[pc.CurrentIndex]
	pc.CurrentIndex = (pc.CurrentIndex + 1) % len(pc.ProxyList)

	return proxy
}

// LoadProxyList loads proxies from file or environment
func (pc *ProxyConfig) LoadProxyList(filePath string) error {
	if filePath == "" {
		// Try default locations
		filePath = os.Getenv("PROXY_LIST_FILE")
	}

	if filePath == "" {
		return fmt.Errorf("no proxy list file specified")
	}

	content, err := os.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("failed to read proxy list: %w", err)
	}

	pc.mu.Lock()
	defer pc.mu.Unlock()

	lines := strings.Split(string(content), "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line != "" && !strings.HasPrefix(line, "#") {
			pc.ProxyList = append(pc.ProxyList, line)
		}
	}

	return nil
}

// GetStats returns proxy configuration statistics
func (pc *ProxyConfig) GetStats() map[string]interface{} {
	pc.mu.RLock()
	defer pc.mu.RUnlock()

	return map[string]interface{}{
		"enabled":            pc.IsEnabled(),
		"proxy_url":          pc.URL,
		"proxy_type":         pc.Type,
		"rotation_enabled":   pc.RotationEnabled,
		"rotation_list_size": len(pc.ProxyList),
		"current_index":      pc.CurrentIndex,
	}
}

// PrintConfiguration prints proxy configuration to console
func (pc *ProxyConfig) PrintConfiguration() {
	stats := pc.GetStats()

	if !pc.IsEnabled() {
		fmt.Println("🌐 Proxy Configuration:")
		fmt.Println("   • Status: ❌ DISABLED (no proxy configured)")
		fmt.Println()
		return
	}

	fmt.Println("🌐 Proxy Configuration:")
	fmt.Printf("   • Status: ✅ ENABLED\n")
	fmt.Printf("   • Proxy URL: %s\n", pc.URL)
	fmt.Printf("   • Proxy Type: %s\n", pc.Type)

	if pc.RotationEnabled && len(pc.ProxyList) > 0 {
		fmt.Printf("   • Rotation: ✅ ENABLED (%d proxies)\n", stats["rotation_list_size"])
	} else {
		fmt.Printf("   • Rotation: ❌ DISABLED\n")
	}

	fmt.Println()
}

// ValidateConfiguration checks if proxy configuration is valid
func (pc *ProxyConfig) ValidateConfiguration() error {
	if !pc.IsEnabled() {
		return nil // Proxy is optional
	}

	if pc.URL == "" {
		return fmt.Errorf("proxy URL is empty")
	}

	// Basic URL validation
	if !strings.Contains(pc.URL, "://") {
		return fmt.Errorf("invalid proxy URL format: %s", pc.URL)
	}

	validTypes := map[string]bool{
		"http":   true,
		"https":  true,
		"socks5": true,
	}

	if pc.Type != "" && !validTypes[pc.Type] {
		return fmt.Errorf("invalid proxy type: %s", pc.Type)
	}

	return nil
}

// GetEnvironmentExample returns example environment variables
func GetEnvironmentExample() string {
	return `
# Example .env or docker-compose environment variables:

# Single Proxy Configuration
PROXY_URL=http://username:password@proxy.example.com:8080
PROXY_TYPE=http

# Or SOCKS5
PROXY_URL=socks5://proxy.example.com:1080

# Proxy Rotation Configuration
PROXY_ROTATION_ENABLED=true
PROXY_LIST_FILE=/app/proxies.txt

# Additional proxy details (optional)
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
PROXY_SERVER=proxy.example.com
PROXY_PORT=8080
`
}

// Sleep utility for rate limiting between proxy requests
func SleepBetweenProxyRequests(minMs int, maxMs int) time.Duration {
	if minMs <= 0 {
		minMs = 1000
	}
	if maxMs <= minMs {
		maxMs = minMs + 2000
	}

	delay := time.Duration(minMs+rand.Intn(maxMs-minMs)) * time.Millisecond
	time.Sleep(delay)
	return delay
}
