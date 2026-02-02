package main

import (
	"fmt"
	"math/rand"
	"time"
)

// BrowserProfile represents a complete browser fingerprint
type BrowserProfile struct {
	Name                string
	UserAgent           string
	Platform            string
	VendorString        string
	Language            string
	TimeZone            string
	ScreenWidth         int64
	ScreenHeight        int64
	WebGLVendor         string
	WebGLRenderer       string
	MaxTouchPoints      int64
	DeviceMemory        int64
	HardwareConcurrency int64
}

// StealthProfiles contains various realistic browser profiles
var StealthProfiles = []BrowserProfile{
	// Windows Chrome 120 - Most common
	{
		Name:                "Windows Chrome 120",
		UserAgent:           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		Platform:            "Win32",
		VendorString:        "Google Inc.",
		Language:            "en-US",
		TimeZone:            "America/New_York",
		ScreenWidth:         1920,
		ScreenHeight:        1080,
		WebGLVendor:         "Google Inc. (Google)",
		WebGLRenderer:       "ANGLE (Intel HD Graphics 630, OpenGL 4.1)",
		MaxTouchPoints:      0,
		DeviceMemory:        8,
		HardwareConcurrency: 8,
	},
	// MacOS Chrome 120
	{
		Name:                "MacOS Chrome 120",
		UserAgent:           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		Platform:            "MacIntel",
		VendorString:        "Google Inc.",
		Language:            "en-US",
		TimeZone:            "America/Los_Angeles",
		ScreenWidth:         1440,
		ScreenHeight:        900,
		WebGLVendor:         "Apple Inc.",
		WebGLRenderer:       "Apple M1",
		MaxTouchPoints:      0,
		DeviceMemory:        16,
		HardwareConcurrency: 8,
	},
	// MacOS M1 Chrome 120
	{
		Name:                "MacOS M1 Chrome 120",
		UserAgent:           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		Platform:            "MacIntel",
		VendorString:        "Google Inc.",
		Language:            "en-US",
		TimeZone:            "America/Denver",
		ScreenWidth:         1680,
		ScreenHeight:        1050,
		WebGLVendor:         "Apple Inc.",
		WebGLRenderer:       "ANGLE (Apple, Apple M1, OpenGL 4.1)",
		MaxTouchPoints:      0,
		DeviceMemory:        16,
		HardwareConcurrency: 8,
	},
	// Linux Chrome 120
	{
		Name:                "Linux Chrome 120",
		UserAgent:           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		Platform:            "Linux x86_64",
		VendorString:        "Google Inc.",
		Language:            "en-US",
		TimeZone:            "Europe/London",
		ScreenWidth:         1920,
		ScreenHeight:        1080,
		WebGLVendor:         "Google Inc. (Google)",
		WebGLRenderer:       "ANGLE (Intel HD Graphics, OpenGL 4.1)",
		MaxTouchPoints:      0,
		DeviceMemory:        8,
		HardwareConcurrency: 4,
	},
	// Windows Edge 120
	{
		Name:                "Windows Edge 120",
		UserAgent:           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
		Platform:            "Win32",
		VendorString:        "Google Inc.",
		Language:            "en-US",
		TimeZone:            "America/Chicago",
		ScreenWidth:         1920,
		ScreenHeight:        1080,
		WebGLVendor:         "Google Inc. (Google)",
		WebGLRenderer:       "ANGLE (NVIDIA GeForce RTX 3090, OpenGL 4.1)",
		MaxTouchPoints:      0,
		DeviceMemory:        16,
		HardwareConcurrency: 12,
	},
	// Windows Firefox 121
	{
		Name:                "Windows Firefox 121",
		UserAgent:           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
		Platform:            "Win32",
		VendorString:        "",
		Language:            "en-US",
		TimeZone:            "America/New_York",
		ScreenWidth:         1920,
		ScreenHeight:        1080,
		WebGLVendor:         "Google Inc. (Google)",
		WebGLRenderer:       "ANGLE (NVIDIA GeForce GTX 1080, OpenGL 4.1)",
		MaxTouchPoints:      0,
		DeviceMemory:        8,
		HardwareConcurrency: 8,
	},
	// MacOS Firefox 121
	{
		Name:                "MacOS Firefox 121",
		UserAgent:           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
		Platform:            "MacIntel",
		VendorString:        "",
		Language:            "en-US",
		TimeZone:            "America/Los_Angeles",
		ScreenWidth:         1440,
		ScreenHeight:        900,
		WebGLVendor:         "Apple Inc.",
		WebGLRenderer:       "Apple M1",
		MaxTouchPoints:      0,
		DeviceMemory:        16,
		HardwareConcurrency: 8,
	},
	// Linux Firefox 121
	{
		Name:                "Linux Firefox 121",
		UserAgent:           "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
		Platform:            "Linux x86_64",
		VendorString:        "",
		Language:            "en-US",
		TimeZone:            "Europe/Berlin",
		ScreenWidth:         1920,
		ScreenHeight:        1080,
		WebGLVendor:         "Google Inc. (Google)",
		WebGLRenderer:       "ANGLE (Intel Iris Xe Graphics, OpenGL 4.1)",
		MaxTouchPoints:      0,
		DeviceMemory:        8,
		HardwareConcurrency: 4,
	},
	// Windows Chrome 121 (Latest)
	{
		Name:                "Windows Chrome 121",
		UserAgent:           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
		Platform:            "Win32",
		VendorString:        "Google Inc.",
		Language:            "en-US",
		TimeZone:            "America/New_York",
		ScreenWidth:         1920,
		ScreenHeight:        1080,
		WebGLVendor:         "Google Inc. (Google)",
		WebGLRenderer:       "ANGLE (Intel HD Graphics 630, OpenGL 4.1)",
		MaxTouchPoints:      0,
		DeviceMemory:        8,
		HardwareConcurrency: 8,
	},
	// MacOS Chrome 121 (Latest)
	{
		Name:                "MacOS Chrome 121",
		UserAgent:           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
		Platform:            "MacIntel",
		VendorString:        "Google Inc.",
		Language:            "en-US",
		TimeZone:            "America/Los_Angeles",
		ScreenWidth:         1440,
		ScreenHeight:        900,
		WebGLVendor:         "Apple Inc.",
		WebGLRenderer:       "Apple M1",
		MaxTouchPoints:      0,
		DeviceMemory:        16,
		HardwareConcurrency: 8,
	},
}

// GetRandomProfile returns a random browser profile
func GetRandomProfile() BrowserProfile {
	return StealthProfiles[rand.Intn(len(StealthProfiles))]
}

// GetProfileByName returns a profile by name
func GetProfileByName(name string) BrowserProfile {
	for _, profile := range StealthProfiles {
		if profile.Name == name {
			return profile
		}
	}
	return StealthProfiles[0]
}

// GetAllProfiles returns all available profiles
func GetAllProfiles() []BrowserProfile {
	return StealthProfiles
}

// GetProfilesByPlatform returns profiles for a specific platform
func GetProfilesByPlatform(platform string) []BrowserProfile {
	var profiles []BrowserProfile
	for _, p := range StealthProfiles {
		if p.Platform == platform {
			profiles = append(profiles, p)
		}
	}
	return profiles
}

// TimeZones for different regions
var TimeZones = []string{
	"America/New_York",
	"America/Chicago",
	"America/Denver",
	"America/Los_Angeles",
	"America/Anchorage",
	"Pacific/Honolulu",
	"Europe/London",
	"Europe/Berlin",
	"Europe/Paris",
	"Europe/Amsterdam",
	"Europe/Moscow",
	"Europe/Istanbul",
	"Asia/Dubai",
	"Asia/Kolkata",
	"Asia/Bangkok",
	"Asia/Hong_Kong",
	"Asia/Shanghai",
	"Asia/Tokyo",
	"Asia/Seoul",
	"Asia/Singapore",
	"Australia/Sydney",
	"Australia/Melbourne",
	"Australia/Brisbane",
	"Pacific/Auckland",
}

// Languages for different regions
var Languages = []string{
	"en-US",
	"en-GB",
	"en-CA",
	"en-AU",
	"en-NZ",
	"de-DE",
	"de-AT",
	"de-CH",
	"fr-FR",
	"fr-CA",
	"it-IT",
	"es-ES",
	"es-MX",
	"pt-BR",
	"pt-PT",
	"nl-NL",
	"ru-RU",
	"ja-JP",
	"zh-CN",
	"zh-TW",
	"ko-KR",
	"th-TH",
	"ar-SA",
	"tr-TR",
}

// GetRandomTimeZone returns a random timezone
func GetRandomTimeZone() string {
	return TimeZones[rand.Intn(len(TimeZones))]
}

// GetRandomLanguage returns a random language
func GetRandomLanguage() string {
	return Languages[rand.Intn(len(Languages))]
}

// AIAgent represents an automated agent with its own profile
type AIAgent struct {
	ID           string
	Profile      BrowserProfile
	Headers      map[string]string
	Cookies      map[string]string
	RateLimit    int // requests per second
	Delay        int // milliseconds between requests
	RetryCount   int // number of retries on failure
	ProxyURL     string
	LastActivity time.Time
}

// NewAIAgent creates a new AI agent with a random profile
func NewAIAgent(id string) *AIAgent {
	profile := GetRandomProfile()
	return &AIAgent{
		ID:         id,
		Profile:    profile,
		Headers:    generateRealisticHeaders(profile),
		Cookies:    make(map[string]string),
		RateLimit:  1,
		Delay:      rand.Intn(5000) + 2000, // 2-7 seconds
		RetryCount: 3,
	}
}

// NewAIAgentWithProfile creates an AI agent with a specific profile
func NewAIAgentWithProfile(id string, profile BrowserProfile) *AIAgent {
	return &AIAgent{
		ID:         id,
		Profile:    profile,
		Headers:    generateRealisticHeaders(profile),
		Cookies:    make(map[string]string),
		RateLimit:  1,
		Delay:      rand.Intn(5000) + 2000,
		RetryCount: 3,
	}
}

// generateRealisticHeaders creates realistic HTTP headers for a profile
func generateRealisticHeaders(profile BrowserProfile) map[string]string {
	headers := map[string]string{
		"User-Agent":      profile.UserAgent,
		"Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
		"Accept-Language": profile.Language,
		"Accept-Encoding": "gzip, deflate, br",
		"Cache-Control":   "max-age=0",
		"Sec-Fetch-Dest":  "document",
		"Sec-Fetch-Mode":  "navigate",
		"Sec-Fetch-Site":  "none",
		"Sec-Fetch-User":  "?1",
		"Upgrade-Insecure-Requests": "1",
		"Sec-Ch-Ua":             `"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"`,
		"Sec-Ch-Ua-Mobile":      "?0",
		"Sec-Ch-Ua-Platform":    `"Windows"`,
		"DNT":                   "1",
		"Connection":            "keep-alive",
		"Pragma":                "no-cache",
	}

	// Add platform-specific headers
	if profile.Platform == "MacIntel" {
		headers["Sec-Ch-Ua-Platform"] = `"macOS"`
	} else if profile.Platform == "Linux x86_64" {
		headers["Sec-Ch-Ua-Platform"] = `"Linux"`
	}

	return headers
}

// HeadersWithDefaults merges custom headers with defaults
func (a *AIAgent) HeadersWithDefaults(customHeaders map[string]string) map[string]string {
	merged := make(map[string]string)

	// Copy default headers
	for k, v := range a.Headers {
		merged[k] = v
	}

	// Override with custom headers
	for k, v := range customHeaders {
		merged[k] = v
	}

	return merged
}

// AddCookie adds a cookie to the agent
func (a *AIAgent) AddCookie(name, value string) {
	a.Cookies[name] = value
}

// RemoveCookie removes a cookie from the agent
func (a *AIAgent) RemoveCookie(name string) {
	delete(a.Cookies, name)
}

// ClearCookies clears all cookies for the agent
func (a *AIAgent) ClearCookies() {
	a.Cookies = make(map[string]string)
}

// GetCookieHeader returns a properly formatted cookie header
func (a *AIAgent) GetCookieHeader() string {
	var cookieStr string
	for name, value := range a.Cookies {
		if cookieStr != "" {
			cookieStr += "; "
		}
		cookieStr += name + "=" + value
	}
	return cookieStr
}

// UpdateActivity updates the agent's last activity timestamp
func (a *AIAgent) UpdateActivity() {
	a.LastActivity = time.Now()
}

// GetIdleTime returns how long the agent has been idle
func (a *AIAgent) GetIdleTime() time.Duration {
	if a.LastActivity.IsZero() {
		return time.Duration(0)
	}
	return time.Since(a.LastActivity)
}

// BrowserPool manages multiple browser agents
type BrowserPool struct {
	Agents      map[string]*AIAgent
	MaxAgents   int
	RateLimiter map[string]time.Time
}

// NewBrowserPool creates a new browser agent pool
func NewBrowserPool(maxAgents int) *BrowserPool {
	return &BrowserPool{
		Agents:      make(map[string]*AIAgent),
		MaxAgents:   maxAgents,
		RateLimiter: make(map[string]time.Time),
	}
}

// AddAgent adds an agent to the pool
func (bp *BrowserPool) AddAgent(agent *AIAgent) error {
	if len(bp.Agents) >= bp.MaxAgents {
		return fmt.Errorf("pool is full (max %d agents)", bp.MaxAgents)
	}
	bp.Agents[agent.ID] = agent
	return nil
}

// GetAgent retrieves an agent by ID
func (bp *BrowserPool) GetAgent(id string) *AIAgent {
	return bp.Agents[id]
}

// RemoveAgent removes an agent from the pool
func (bp *BrowserPool) RemoveAgent(id string) {
	delete(bp.Agents, id)
}

// GetRandomAgent returns a random agent from the pool
func (bp *BrowserPool) GetRandomAgent() *AIAgent {
	if len(bp.Agents) == 0 {
		return nil
	}
	
	idx := rand.Intn(len(bp.Agents))
	for _, agent := range bp.Agents {
		if idx == 0 {
			return agent
		}
		idx--
	}
	return nil
}

// GetAllAgents returns all agents in the pool
func (bp *BrowserPool) GetAllAgents() []*AIAgent {
	agents := make([]*AIAgent, 0, len(bp.Agents))
	for _, agent := range bp.Agents {
		agents = append(agents, agent)
	}
	return agents
}

// GetPoolSize returns the current number of agents
func (bp *BrowserPool) GetPoolSize() int {
	return len(bp.Agents)
}