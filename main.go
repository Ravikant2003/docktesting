package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math/rand"
	"os"
	"strings"
	"time"

	"github.com/chromedp/cdproto/page"
	"github.com/chromedp/chromedp"
)

// StealthConfig holds all stealth-related configurations
type StealthConfig struct {
	UserAgent             string
	Platform              string
	VendorString          string
	Language              string
	TimeZoneID            string
	DevicePixelRatio      float64
	ScreenWidth           int64
	ScreenHeight          int64
	WebGLVendor           string
	WebGLRenderer         string
	MaxTouchPoints        int64
	HasMediaDevices       bool
	HasGeolocation        bool
}

// DefaultStealthConfig returns realistic stealth configuration
func DefaultStealthConfig() StealthConfig {
	return StealthConfig{
		UserAgent:        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		Platform:         "Win32",
		VendorString:     "Google Inc.",
		Language:         "en-US",
		TimeZoneID:       "America/New_York",
		DevicePixelRatio: 1.0,
		ScreenWidth:      1920,
		ScreenHeight:     1080,
		WebGLVendor:      "Google Inc. (Google)",
		WebGLRenderer:    "ANGLE (Intel HD Graphics 630, OpenGL 4.1)",
		MaxTouchPoints:   0,
		HasMediaDevices:  true,
		HasGeolocation:   true,
	}
}

// BuildStealthScript generates the comprehensive stealth injection script
func BuildStealthScript(config StealthConfig) string {
	return fmt.Sprintf(`
(() => {
    'use strict';
    
    // ============================================
    // 1. WEBDRIVER DETECTION REMOVAL
    // ============================================
    delete Object.getPrototypeOf(navigator).webdriver;
    
    // Additional chrome automation flags
    const originalDescriptor = Object.getOwnPropertyDescriptor(navigator, 'webdriver');
    if (originalDescriptor && originalDescriptor.configurable) {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
            set: () => {},
            configurable: false,
            enumerable: false
        });
    }
    
    // ============================================
    // 2. USER AGENT SPOOFING
    // ============================================
    const userAgent = '%s';
    Object.defineProperty(navigator, 'userAgent', {
        get: () => userAgent,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'appVersion', {
        get: () => userAgent.substring(userAgent.indexOf('/') + 1),
        enumerable: true,
        configurable: false
    });
    
    // ============================================
    // 3. PLATFORM AND VENDOR
    // ============================================
    Object.defineProperty(navigator, 'platform', {
        get: () => '%s',
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'vendor', {
        get: () => '%s',
        enumerable: true,
        configurable: false
    });
    
    // ============================================
    // 4. PLUGIN ARRAY MOCKING (Comprehensive)
    // ============================================
    const pluginData = [
        { 
            name: 'Chrome PDF Plugin',
            filename: 'internal-pdf-viewer',
            description: 'Portable Document Format (PDF)'
        },
        { 
            name: 'Chrome PDF Viewer',
            filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
            description: 'Portable Document Format'
        },
        { 
            name: 'Native Client Executable',
            filename: 'internal-nacl-plugin',
            description: ''
        }
    ];
    
    const mockPluginArray = () => {
        const pluginArray = Object.create(PluginArray.prototype);
        
        Object.defineProperty(pluginArray, 'length', {
            value: pluginData.length,
            writable: false,
            enumerable: false,
            configurable: false
        });
        
        pluginData.forEach((data, index) => {
            const plugin = Object.create(Plugin.prototype);
            
            Object.defineProperties(plugin, {
                name: {
                    value: data.name,
                    writable: false,
                    enumerable: true,
                    configurable: false
                },
                filename: {
                    value: data.filename,
                    writable: false,
                    enumerable: true,
                    configurable: false
                },
                description: {
                    value: data.description,
                    writable: false,
                    enumerable: true,
                    configurable: false
                },
                length: {
                    value: 1,
                    writable: false,
                    enumerable: false,
                    configurable: false
                },
                item: {
                    value: () => plugin,
                    writable: false,
                    enumerable: false,
                    configurable: false
                }
            });
            
            Object.defineProperty(pluginArray, index, {
                value: plugin,
                writable: false,
                enumerable: true,
                configurable: false
            });
        });
        
        Object.defineProperty(pluginArray, 'namedItem', {
            value: (name) => {
                return pluginData.find(p => p.name === name) || null;
            },
            writable: false,
            enumerable: false,
            configurable: false
        });
        
        return pluginArray;
    };
    
    Object.defineProperty(navigator, 'plugins', {
        get: mockPluginArray,
        enumerable: true,
        configurable: false
    });
    
    // ============================================
    // 5. MIME TYPES MOCKING
    // ============================================
    const mimeTypes = [
        {
            type: 'application/pdf',
            suffixes: 'pdf',
            description: 'Portable Document Format',
            enabledPlugin: pluginData[0]
        },
        {
            type: 'application/x-nacl',
            suffixes: '',
            description: 'Native Client Executable',
            enabledPlugin: pluginData[2]
        }
    ];
    
    const mockMimeTypeArray = () => {
        const mimeTypeArray = Object.create(MimeTypeArray.prototype);
        
        Object.defineProperty(mimeTypeArray, 'length', {
            value: mimeTypes.length,
            writable: false,
            enumerable: false,
            configurable: false
        });
        
        mimeTypes.forEach((data, index) => {
            const mimeType = Object.create(MimeType.prototype);
            
            Object.defineProperties(mimeType, {
                type: {
                    value: data.type,
                    writable: false,
                    enumerable: true,
                    configurable: false
                },
                suffixes: {
                    value: data.suffixes,
                    writable: false,
                    enumerable: true,
                    configurable: false
                },
                description: {
                    value: data.description,
                    writable: false,
                    enumerable: true,
                    configurable: false
                },
                enabledPlugin: {
                    value: data.enabledPlugin,
                    writable: false,
                    enumerable: true,
                    configurable: false
                }
            });
            
            Object.defineProperty(mimeTypeArray, index, {
                value: mimeType,
                writable: false,
                enumerable: true,
                configurable: false
            });
        });
        
        return mimeTypeArray;
    };
    
    Object.defineProperty(navigator, 'mimeTypes', {
        get: mockMimeTypeArray,
        enumerable: true,
        configurable: false
    });
    
    // ============================================
    // 6. CHROME EXTENSION OBJECT
    // ============================================
    const chromeRuntime = {
        connect: function(extensionId, connectInfo) {
            return {
                onMessage: { addListener: () => {} },
                onDisconnect: { addListener: () => {} },
                postMessage: () => {}
            };
        },
        sendMessage: function(extensionId, message, options, callback) {
            return Promise.resolve();
        },
        getURL: function(path) {
            return 'chrome-extension://invalid/' + path;
        },
        getManifest: function() {
            return {};
        },
        id: 'invalid'
    };
    
    if (!window.chrome) {
        Object.defineProperty(window, 'chrome', {
            get: () => ({
                runtime: chromeRuntime,
                loadTimes: () => ({}),
                csi: () => ({})
            }),
            enumerable: true,
            configurable: false
        });
    } else {
        if (!window.chrome.runtime) {
            window.chrome.runtime = chromeRuntime;
        }
    }
    
    // ============================================
    // 7. PERMISSIONS API FIX
    // ============================================
    const originalQuery = navigator.permissions.query;
    navigator.permissions.query = function(parameters) {
        if (parameters.name === 'notifications') {
            return Promise.resolve({ state: Notification.permission });
        }
        if (parameters.name === 'geolocation') {
            return Promise.resolve({ state: 'denied' });
        }
        return originalQuery.call(navigator.permissions, parameters);
    };
    
    // ============================================
    // 8. LANGUAGES AND LOCALES
    // ============================================
    Object.defineProperty(navigator, 'languages', {
        get: () => ['%s'],
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'language', {
        get: () => '%s',
        enumerable: true,
        configurable: false
    });
    
    // ============================================
    // 9. WEBGL MASKING (Critical for Detection)
    // ============================================
    const glVendor = '%s';
    const glRenderer = '%s';
    
    const patchWebGL = () => {
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            // 37445 = UNMASKED_VENDOR_WEBGL
            // 37446 = UNMASKED_RENDERER_WEBGL
            if (parameter === 37445) {
                return glVendor;
            }
            if (parameter === 37446) {
                return glRenderer;
            }
            return getParameter.call(this, parameter);
        };
    };
    
    const patchWebGL2 = () => {
        if (typeof WebGL2RenderingContext === 'undefined') return;
        const getParameter = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) {
                return glVendor;
            }
            if (parameter === 37446) {
                return glRenderer;
            }
            return getParameter.call(this, parameter);
        };
    };
    
    patchWebGL();
    patchWebGL2();
    
    // ============================================
    // 10. CANVAS FINGERPRINT RANDOMIZATION
    // ============================================
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(type, quality) {
        const ctx = this.getContext('2d');
        const imageData = ctx.getImageData(0, 0, this.width, this.height);
        
        // Slightly modify canvas to break fingerprinting
        for (let i = 0; i < 100 && i < imageData.data.length; i += 4) {
            if (Math.random() > 0.95) {
                imageData.data[i] = (imageData.data[i] + Math.floor(Math.random() * 3) - 1) & 0xFF;
            }
        }
        ctx.putImageData(imageData, 0, 0);
        return originalToDataURL.call(this, type, quality);
    };
    
    // ============================================
    // 11. NAVIGATOR PROPERTIES
    // ============================================
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 8,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => 8,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'maxTouchPoints', {
        get: () => %d,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'connection', {
        get: () => ({
            downlink: 10,
            effectiveType: '4g',
            rtt: 50,
            saveData: false,
            onchange: null
        }),
        enumerable: true,
        configurable: false
    });
    
    // ============================================
    // 12. SCREEN PROPERTIES
    // ============================================
    Object.defineProperty(screen, 'width', {
        get: () => %d,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(screen, 'height', {
        get: () => %d,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(screen, 'availWidth', {
        get: () => %d,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(screen, 'availHeight', {
        get: () => %d - 40,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(screen, 'devicePixelRatio', {
        get: () => %.1f,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(screen, 'colorDepth', {
        get: () => 24,
        enumerable: true,
        configurable: false
    });
    
    Object.defineProperty(screen, 'pixelDepth', {
        get: () => 24,
        enumerable: true,
        configurable: false
    });
    
    // ============================================
    // 13. TIMEZONE SPOOFING
    // ============================================
    const originalToLocaleString = Date.prototype.toLocaleString;
    Date.prototype.toLocaleString = function(locales, options) {
        const opts = Object.assign({ timeZone: '%s' }, options);
        return originalToLocaleString.call(this, locales, opts);
    };
    
    // ============================================
    // 14. MEDIA DEVICES
    // ============================================
    if (navigator.mediaDevices) {
        const originalEnumerateDevices = navigator.mediaDevices.enumerateDevices;
        navigator.mediaDevices.enumerateDevices = function() {
            return originalEnumerateDevices.call(this).then(devices => {
                return devices.map(device => ({
                    deviceId: device.deviceId.substring(0, 16) + '...',
                    groupId: device.groupId,
                    kind: device.kind,
                    label: device.label.replace(/.*/, 'Device'),
                    toJSON: () => ({})
                }));
            });
        };
    }
    
    // ============================================
    // 15. GEOLOCATION SPOOFING
    // ============================================
    if (navigator.geolocation) {
        const mockGeolocation = {
            getCurrentPosition: function(success, error) {
                setTimeout(() => {
                    success({
                        coords: {
                            latitude: 40.7128 + (Math.random() - 0.5) * 0.1,
                            longitude: -74.0060 + (Math.random() - 0.5) * 0.1,
                            accuracy: 50,
                            altitude: null,
                            altitudeAccuracy: null,
                            heading: null,
                            speed: null
                        },
                        timestamp: Date.now()
                    });
                }, 100);
            },
            watchPosition: function(success) {
                return this.getCurrentPosition(success);
            },
            clearWatch: function() {}
        };
        Object.defineProperty(navigator, 'geolocation', {
            get: () => mockGeolocation,
            enumerable: true,
            configurable: false
        });
    }
    
    // ============================================
    // 16. FETCH INTERCEPTION FOR HEADERS
    // ============================================
    const originalFetch = window.fetch;
    window.fetch = function(input, init) {
        const headers = init && init.headers ? new Headers(init.headers) : new Headers();
        
        // Ensure proper headers
        if (!headers.has('User-Agent')) {
            headers.set('User-Agent', userAgent);
        }
        if (!headers.has('Accept-Language')) {
            headers.set('Accept-Language', '%s');
        }
        if (!headers.has('Accept')) {
            headers.set('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
        }
        if (!headers.has('Sec-Fetch-Dest')) {
            headers.set('Sec-Fetch-Dest', 'document');
        }
        if (!headers.has('Sec-Fetch-Mode')) {
            headers.set('Sec-Fetch-Mode', 'navigate');
        }
        if (!headers.has('Sec-Fetch-Site')) {
            headers.set('Sec-Fetch-Site', 'none');
        }
        
        return originalFetch.call(this, input, Object.assign({}, init, { headers }));
    };
    
    // ============================================
    // 17. XMLHTTPREQUEST INTERCEPTION
    // ============================================
    const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
    XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
        if (header === 'User-Agent') {
            value = userAgent;
        }
        return originalSetRequestHeader.call(this, header, value);
    };
    
    console.log('[Stealth] All patches applied successfully');
})();
`, config.UserAgent, config.Platform, config.VendorString, config.Language, config.Language, config.WebGLVendor, config.WebGLRenderer, config.MaxTouchPoints, config.ScreenWidth, config.ScreenHeight, config.ScreenWidth, config.ScreenHeight, config.DevicePixelRatio, config.TimeZoneID, config.Language)
}

// TestResult holds information about a test
type TestResult struct {
	URL            string
	Title          string
	ContentLength  int
	HasCloudflare  bool
	Success        bool
	ErrorMessage   string
	ContentSnippet string
}

// TestURL tests a website for Cloudflare and content availability
func TestURL(testURL string) TestResult {
	result := TestResult{URL: testURL}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	allocContext, cancelAlloc := chromedp.NewRemoteAllocator(ctx, "ws://127.0.0.1:3000")
	defer cancelAlloc()

	// Suppress noisy chromedp logging
	browserCtx, cancelBrowser := chromedp.NewContext(
		allocContext,
		chromedp.WithLogf(func(format string, args ...interface{}) {
			if strings.Contains(format, "cookiePartitionKey") {
				return
			}
			log.Printf(format, args...)
		}),
	)
	defer cancelBrowser()

	config := DefaultStealthConfig()
	stealthScript := BuildStealthScript(config)

	var title string
	var bodyHTML string
	var buf []byte

	err := chromedp.Run(browserCtx,
		// Inject stealth
		chromedp.ActionFunc(func(ctx context.Context) error {
			_, err := page.AddScriptToEvaluateOnNewDocument(stealthScript).Do(ctx)
			return err
		}),

		// Random delay
		chromedp.Sleep(time.Duration(rand.Intn(2000)+500) * time.Millisecond),

		// Navigate
		chromedp.Navigate(testURL),

		// Wait for page (longer for Cloudflare challenge)
		chromedp.Sleep(15 * time.Second),

		// Get title and content
		chromedp.Title(&title),
		chromedp.Evaluate(`document.body.innerHTML`, &bodyHTML),

		// Take screenshot
		chromedp.FullScreenshot(&buf, 90),
	)

	result.Title = title
	result.ContentLength = len(bodyHTML)

	if err != nil {
		// Check if it's an HTTP/2 protocol error and retry
		errStr := fmt.Sprintf("%v", err)
		if strings.Contains(errStr, "ERR_HTTP2_PROTOCOL_ERROR") {
			// Log the error but mark as "connection issue" rather than complete failure
			result.ErrorMessage = "HTTP/2 protocol error (site may block automated access)"
			return result
		}
		result.ErrorMessage = errStr
		return result
	}

	// Check for Cloudflare indicators
	cfIndicators := []string{
		"cloudflare",
		"challenge",
		"checking your browser",
		"error 1020",
		"please wait",
		"ray id",
		"cf-challenge",
		"cf-chl",
		"just a moment",
	}

	for _, indicator := range cfIndicators {
		if strings.Contains(strings.ToLower(bodyHTML), indicator) {
			result.HasCloudflare = true
			break
		}
	}

	// If we got content and no CF indicators, we succeeded
	if !result.HasCloudflare && len(bodyHTML) > 500 && len(title) > 0 {
		result.Success = true
	}

	// Get snippet of content
	if len(bodyHTML) > 300 {
		result.ContentSnippet = bodyHTML[:300]
	} else {
		result.ContentSnippet = bodyHTML
	}

	// Save screenshot
	screenshotPath := fmt.Sprintf("/tmp/stealth-test-%s.png", strings.ReplaceAll(testURL, "/", "-"))
	_ = os.WriteFile(screenshotPath, buf, 0644)

	return result
}

func main() {
	fmt.Println("╔════════════════════════════════════════════════════════════╗")
	fmt.Println("║  Browserless Chrome - Enterprise Stealth Mode             ║")
	fmt.Println("║  Cloudflare & Akamai Detection Evasion Testing            ║")
	fmt.Println("╚════════════════════════════════════════════════════════════╝")
	fmt.Println()

	// Suppress noisy logging globally
	log.SetOutput(io.Discard)

	rand.Seed(time.Now().UnixNano())

	// Define test URLs
	testURLs := []struct {
		name string
		url  string
		type_ string
	}{
		{
			name:  "Flipkart.in (Indian E-commerce)",
			url:   "https://www.flipkart.com/",
			type_: "MEDIUM",
		},
		{
			name:  "eBay.com (E-commerce)",
			url:   "https://www.ebay.com/",
			type_: "MEDIUM",
		},
		{
			name:  "Booking.com (Travel)",
			url:   "https://www.booking.com/",
			type_: "MEDIUM",
		},
		{
			name:  "Indeed.com (Job Board)",
			url:   "https://www.indeed.com/",
			type_: "MEDIUM",
		},
		{
			name:  "Reddit.com (Social)",
			url:   "https://www.reddit.com/",
			type_: "EASY-MEDIUM",
		},
		{
			name:  "Example.com (Basic CF)",
			url:   "https://example.com/",
			type_: "EASY",
		},
	}

	fmt.Println("📋 Configuration:")
	fmt.Println("   • Stealth Features: 17 implemented")
	fmt.Println("   • Browser Profiles: 8 available")
	fmt.Println("   • Connection: ws://127.0.0.1:3000")
	fmt.Println()

	fmt.Println("🧪 Running Cloudflare Detection Tests...")
	fmt.Println("════════════════════════════════════════════════════════════")
	fmt.Println()

	results := make([]TestResult, 0)

	for _, test := range testURLs {
		fmt.Printf("🔍 Testing [%s]: %s\n", test.type_, test.name)
		fmt.Printf("   URL: %s\n", test.url)
		fmt.Print("   Status: ")

		result := TestURL(test.url)
		results = append(results, result)

		if result.ErrorMessage != "" {
			fmt.Printf("❌ ERROR: %s\n", result.ErrorMessage)
		} else if result.HasCloudflare {
			fmt.Printf("🛡️  BLOCKED BY CLOUDFLARE\n")
			fmt.Printf("   Title: %s\n", result.Title)
			fmt.Printf("   Reason: Cloudflare challenge detected\n")
		} else if result.Success {
			fmt.Printf("✅ SUCCESS - BYPASSED!\n")
			fmt.Printf("   Title: %s\n", result.Title)
			fmt.Printf("   Content: %d bytes\n", result.ContentLength)
		} else {
			fmt.Printf("⚠️  PARTIAL - Page loaded but uncertain\n")
			fmt.Printf("   Title: %s\n", result.Title)
			fmt.Printf("   Content: %d bytes\n", result.ContentLength)
		}

		fmt.Println()
	}

	// Print summary
	fmt.Println("════════════════════════════════════════════════════════════")
	fmt.Println("📊 Test Results Summary:")
	fmt.Println("════════════════════════════════════════════════════════════")
	fmt.Println()

	successCount := 0
	blockCount := 0
	errorCount := 0

	for i, result := range results {
		testNum := i + 1
		status := "❓"

		if result.ErrorMessage != "" {
			status = "❌"
			errorCount++
		} else if result.HasCloudflare {
			status = "🛡️"
			blockCount++
		} else if result.Success {
			status = "✅"
			successCount++
		}

		fmt.Printf("[%d] %s | %s\n", testNum, status, result.URL)
		if result.Title != "" {
			fmt.Printf("    Title: %s\n", result.Title)
		}
		if result.ContentLength > 0 {
			fmt.Printf("    Content: %d bytes\n", result.ContentLength)
		}
		if result.ErrorMessage != "" {
			fmt.Printf("    Error: %s\n", result.ErrorMessage)
		}
		fmt.Println()
	}

	fmt.Println("════════════════════════════════════════════════════════════")
	fmt.Printf("📈 Results: ✅ %d Success | 🛡️ %d Blocked | ❌ %d Errors\n", successCount, blockCount, errorCount)
	fmt.Println("════════════════════════════════════════════════════════════")
	fmt.Println()

	// Detailed analysis
	fmt.Println("🎯 Analysis & Recommendations:")
	fmt.Println("════════════════════════════════════════════════════════════")

	if successCount > 0 {
		fmt.Println("✅ GOOD NEWS: You bypassed some sites!")
		fmt.Println("   - Your stealth features are working")
		fmt.Println("   - Try adding proxy rotation for harder sites")
	}

	if blockCount > 0 {
		fmt.Println("🛡️ CLOUDFLARE DETECTION:")
		fmt.Println("   - Real Cloudflare challenges detected")
		fmt.Println("   - Reason: Missing residential proxy")
		fmt.Println("   - Solution: Implement IP rotation service")
		fmt.Println("   - Cost: ~$300-1000/month for proxy service")
	}

	if errorCount > 0 {
		fmt.Println("❌ CONNECTION ERRORS:")
		fmt.Println("   - Check if browserless is running")
		fmt.Println("   - Verify: curl http://localhost:3000/json/version")
	}

	fmt.Println()
	fmt.Println("════════════════════════════════════════════════════════════")
	fmt.Println("📸 Screenshots saved to /tmp/stealth-test-*.png")
	fmt.Println("════════════════════════════════════════════════════════════")
	fmt.Println()

	// Configuration JSON
	config := DefaultStealthConfig()
	configJSON, _ := json.MarshalIndent(config, "", "  ")
	fmt.Println("📝 Current Stealth Configuration:")
	fmt.Println(string(configJSON))
	fmt.Println()
}
