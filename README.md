# Enterprise Stealth Browser Automation System

**Production-grade browser automation with Cloudflare & Akamai detection evasion**

> Built on browserless/chrome, Go, and chromedp. Designed for AI agents, web scraping, and automated testing.

---

## 🎯 Overview

This system provides **industry-level bot detection evasion** through:

- **17 Anti-Detection Mechanisms** - JavaScript injection, WebGL masking, canvas randomization, and more
- **8 Realistic Browser Profiles** - Windows/macOS/Linux with Chrome/Firefox/Edge variations
- **Multi-Agent Orchestration** - Parallel execution with profile rotation
- **Enterprise Deployment** - Docker, Kubernetes, and proxy integration ready
- **Production-Hardened** - Error handling, retry logic, session persistence

### Perfect For:
- AI agent automation
- Web scraping (with proper authorization)
- Security testing
- Competitive intelligence
- Automated testing across platforms

---

## 📦 What's Included

```
browser-automation/
├── docker-compose.yml          # Browserless container config
├── main.go                      # Core stealth implementation (17 features)
├── profiles.go                  # 8 browser profiles + agent system
├── multi_agent.go              # Multi-agent orchestration
├── go.mod                       # Dependencies
├── DEPLOYMENT_GUIDE.md         # Comprehensive deployment guide
├── QUICK_REFERENCE.md          # Common usage patterns
└── README.md                    # This file
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites
```bash
# Check requirements
docker --version        # Docker 20.10+
docker-compose --version # Docker Compose 1.29+
go version              # Go 1.21+
```

### 2. Start Browserless
```bash
docker-compose up -d
```

Wait for container to be healthy:
```bash
curl http://localhost:3000/json/version
# Should return JSON with browser version info
```

### 3. Run Application
```bash
go run main.go profiles.go
```

Expected output:
```
╔════════════════════════════════════════════════════════════╗
║  Browserless Chrome - Enterprise Stealth Mode             ║
║  Designed for Cloudflare & Akamai Detection Evasion       ║
╚════════════════════════════════════════════════════════════╝

✅ Connected to browserless

🚀 Executing stealth injection and navigation...
✅ Page loaded successfully

📸 Screenshot saved: /tmp/stealth-browserless-test.png

✓ navigator.webdriver → REMOVED
✓ navigator.userAgent → SPOOFED
✓ navigator.plugins → MOCKED (3 fake plugins)
... [and 14 more features]
```

---

## 🛡️ 17 Anti-Detection Features

| # | Feature | Purpose | Impact |
|---|---------|---------|--------|
| 1 | Webdriver Removal | Hide automation flag | Critical |
| 2 | User-Agent Spoofing | Realistic browser ID | Critical |
| 3 | Platform Spoofing | Match OS properties | High |
| 4 | Plugin Mocking | Fake PDF plugins | High |
| 5 | MIME Types | Plugin associations | Medium |
| 6 | Chrome Runtime | Extension object | High |
| 7 | Permissions API | Block suspicious requests | Medium |
| 8 | Languages/Locales | Timezone awareness | Medium |
| 9 | WebGL Masking | GPU fingerprinting | Critical |
| 10 | Canvas Randomization | Break fingerprints | High |
| 11 | Navigator Properties | Hardware specs | Medium |
| 12 | Screen Properties | Display metrics | Medium |
| 13 | Timezone Spoofing | Locale detection | Medium |
| 14 | Media Devices | Camera/mic obfuscation | Medium |
| 15 | Geolocation | Mock GPS data | Medium |
| 16 | Fetch Interception | Header management | High |
| 17 | XHR Interception | Request patching | Medium |

---

## 🤖 8 Browser Profiles

Pre-configured realistic browser fingerprints:

```
1. Windows Chrome 120         → Most common (1920x1080, Intel)
2. MacOS Chrome 120           → Intel Mac (1440x900)
3. MacOS M1 Chrome 120        → Apple Silicon (1680x1050)
4. Linux Chrome 120           → Developer (1920x1080, 4 cores)
5. Windows Edge 120           → Business user (High-end GPU)
6. Windows Firefox 121        → Privacy-focused Windows
7. MacOS Firefox 121          → Privacy-focused Mac
8. Linux Firefox 121          → Privacy-focused Linux
```

### Automatic Rotation
```go
// Single request with random profile
profile := GetRandomProfile()

// All available profiles
profiles := GetAllProfiles()

// Specific profile
profile := GetProfileByName("MacOS M1 Chrome 120")
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Container                       │
│              browserless/chrome:latest                  │
│  (Chrome 120 with optimized launch arguments)          │
└────────────────┬────────────────────────────────────────┘
                 │ ws://127.0.0.1:3000
                 │
┌────────────────▼────────────────────────────────────────┐
│              Go Application Layer                        │
│  ┌─────────────────────────────────────────────┐       │
│  │  main.go: Core Stealth Implementation       │       │
│  │  • 17 Anti-detection mechanisms             │       │
│  │  • Stealth script generation                │       │
│  │  • Single-site automation                   │       │
│  └─────────────────────────────────────────────┘       │
│  ┌─────────────────────────────────────────────┐       │
│  │  profiles.go: Browser Profiles & Agents     │       │
│  │  • 8 pre-configured profiles                │       │
│  │  • AIAgent system with headers              │       │
│  │  • Timezone & language rotation             │       │
│  └─────────────────────────────────────────────┘       │
│  ┌─────────────────────────────────────────────┐       │
│  │  multi_agent.go: Orchestration              │       │
│  │  • Agent pool management                    │       │
│  │  • Task queue processing                    │       │
│  │  • Parallel execution                       │       │
│  └─────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
         ┌────▼────┐          ┌────▼────┐
         │ Targets │          │ Proxies  │
         │  Sites  │          │ (Optional)
         └─────────┘          └──────────┘
```

---

## 💻 System Requirements

### Minimum
- 2 CPU cores
- 2GB RAM
- Docker + Docker Compose
- Go 1.21+

### Recommended (Production)
- 8+ CPU cores
- 8GB+ RAM
- 1Gbps network
- Residential proxy service
- Kubernetes cluster (optional)

---

## 🔧 Configuration

### Docker Compose Environment Variables

```yaml
# Debug logging
DEBUG: browserless*

# Browser launch arguments (25+ hardening flags)
DEFAULT_LAUNCH_ARGS: "--disable-blink-features=AutomationControlled ..."

# Timeouts
CONNECTION_TIMEOUT: 30000         # milliseconds
FUNCTION_CALL_TIMEOUT: 60000      # milliseconds

# Resource limits
MAX_CONCURRENT_SESSIONS: 10       # Parallel browsers
QUEUE_LENGTH: 20                  # Queued tasks
```

### Runtime Configuration

```go
// Stealth configuration
config := StealthConfig{
    UserAgent:       "Mozilla/5.0...",
    Platform:        "Win32",
    Language:        "en-US",
    TimeZoneID:      "America/New_York",
    ScreenWidth:     1920,
    ScreenHeight:    1080,
    WebGLVendor:     "Google Inc. (Google)",
    WebGLRenderer:   "ANGLE (Intel HD Graphics 630, OpenGL 4.1)",
    MaxTouchPoints:  0,
}

// Apply configuration
stealthScript := BuildStealthScript(config)
```

---

## 📚 Usage Examples

### Example 1: Single Site with Stealth
```go
allocContext, _ := chromedp.NewRemoteAllocator(ctx, "ws://127.0.0.1:3000")
browserCtx, _ := chromedp.NewContext(allocContext)

config := DefaultStealthConfig()
stealthScript := BuildStealthScript(config)

chromedp.Run(browserCtx,
    chromedp.ActionFunc(func(ctx context.Context) error {
        _, err := page.AddScriptToEvaluateOnNewDocument(stealthScript).Do(ctx)
        return err
    }),
    chromedp.Navigate("https://example.com"),
    chromedp.Sleep(5 * time.Second),
    // ... continue ...
)
```

### Example 2: Multi-Agent Processing
```go
pool := NewAgentPool(5)  // 5 concurrent agents
ctx, cancel := context.WithCancel(context.Background())
pool.Start(ctx)

for _, url := range urls {
    pool.SubmitTask(&AgentTask{
        URL:     url,
        Timeout: 30 * time.Second,
    })
}

pool.Wait()
```

### Example 3: Profile Rotation
```go
for _, site := range sites {
    profile := GetRandomProfile()  // Different profile each time
    
    config := StealthConfig{
        UserAgent:     profile.UserAgent,
        Platform:      profile.Platform,
        Language:      profile.Language,
        TimeZoneID:    profile.TimeZone,
        // ... more config ...
    }
    
    // Navigate with profile
}
```

See **QUICK_REFERENCE.md** for 10+ complete examples.

---

## 🌐 Testing Against Detection Systems

### Cloudflare Challenge
```go
// Stealth injection automatically handles JS challenge
chromedp.Run(ctx,
    chromedp.ActionFunc(injectStealth),
    chromedp.Navigate(url),
    chromedp.Sleep(8 * time.Second),  // Challenge resolves in 3-5s
    chromedp.Title(&title),
)
```

### Akamai Bot Manager
- Timing randomization ✓
- Real browser headers ✓
- DOM access patterns ✓
- Network behavior ✓

### General Bot Detection
All 17 features work together to evade:
- JavaScript-based detection
- Fingerprinting (canvas, WebGL)
- Automation flags
- Behavioral patterns

---

## 🚀 Production Deployment

### Docker
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
```

### With Proxy Rotation
```bash
docker run -e PROXY_URL="http://proxy:8080" \
  browserless/chrome:latest
```

See **DEPLOYMENT_GUIDE.md** for full enterprise setup.

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Page Load Time | 3-8 seconds |
| Stealth Injection | <50ms |
| Memory per Session | 100-200MB |
| CPU per Session | 1-2 cores |
| Concurrent Sessions | 1-10 (depending on hardware) |
| Requests/minute | 6-60 (depending on site complexity) |

---

## ⚠️ Important Notes

### Legal & Ethical Use

✅ **Permitted:**
- Testing your own infrastructure
- Scraping public data where authorized
- Security research
- Academic projects
- Competitive intelligence (within bounds)

❌ **Prohibited:**
- Unauthorized access
- Data theft or fraud
- Violating Terms of Service
- Illegal activity
- Rate-limiting evasion for malicious purposes

**Always check:**
1. robots.txt and Terms of Service
2. Local laws regarding web scraping
3. Server's rate limits
4. Your intended use legality

### Detection Prevention Best Practices

1. **Respect rate limits** - Add delays between requests
2. **Rotate profiles** - Different browser signature each time
3. **Use proxies** - For large-scale operations
4. **Clean sessions** - Clear cookies between targets
5. **Monitor blocks** - Implement fallback strategies
6. **Randomize patterns** - No predictable behavior

---

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs stealth-browserless

# Verify port availability
lsof -i :3000

# Restart
docker-compose restart
```

### Connection refused
```bash
# Ensure container is healthy
docker-compose ps

# Test connection
curl http://localhost:3000/json/version
```

### Detection still failing
1. Check stealth script injection
2. Increase wait times
3. Rotate profiles
4. Add proxy layer
5. Review target site detection mechanism

See **DEPLOYMENT_GUIDE.md** > Troubleshooting for detailed solutions.

---

## 📖 Documentation

- **DEPLOYMENT_GUIDE.md** - Full deployment guide with Kubernetes examples
- **QUICK_REFERENCE.md** - Common usage patterns and examples
- **main.go** - Source code with detailed comments
- **profiles.go** - Browser profiles and agent system
- **multi_agent.go** - Agent orchestration system

---

## 🔗 Dependencies

```go
github.com/chromedp/chromedp v0.9.5     // Browser automation
github.com/chromedp/cdproto v0.0.0      // Chrome DevTools Protocol
```

All dependencies managed via `go.mod` and `docker-compose.yml`.

---

## 🎓 Learning Resources

- [Browserless Documentation](https://docs.browserless.io/)
- [Chromedp Guide](https://github.com/chromedp/chromedp)
- [Bot Detection Evasion](https://blog.apify.com/evasion-techniques/)
- [Cloudflare Challenge](https://support.cloudflare.com/hc/en-us/articles/200170006)
- [Akamai Bot Manager](https://www.akamai.com/us/en/products/security/bot-manager/)

---

## 🤝 Contributing

Improvements and contributions are welcome:

1. Test against new detection systems
2. Add new browser profiles
3. Improve stealth mechanisms
4. Optimize performance
5. Fix bugs and issues

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🎯 Roadmap

- [ ] Playwright backend support
- [ ] Advanced behavioral simulation
- [ ] Machine learning detection evasion
- [ ] WebRTC leak prevention
- [ ] DNS over HTTPS integration
- [ ] TLS fingerprinting randomization
- [ ] HTTP/2 fingerprinting
- [ ] Advanced proxy integration

---

## 🆘 Support

For issues and questions:

1. Check **DEPLOYMENT_GUIDE.md** troubleshooting section
2. Review Docker logs: `docker-compose logs`
3. Test stealth features: `go run main.go profiles.go`
4. Verify connection: `curl http://localhost:3000/json/version`
5. Check source code comments for detailed explanations

---

## ✅ Verification Checklist

Before production deployment:

- [ ] Docker and Docker Compose installed
- [ ] Go 1.21+ installed
- [ ] Port 3000 available
- [ ] Sufficient disk space (1GB minimum)
- [ ] Container health check passing
- [ ] Stealth script injection working
- [ ] Test screenshot generated
- [ ] All 17 features listed in output
- [ ] No error messages in logs
- [ ] Ready for testing against real targets

---

## 🎉 Ready to Deploy?

```bash
# 1. Start container
docker-compose up -d

# 2. Verify connection
curl http://localhost:3000/json/version

# 3. Run application
go run main.go profiles.go

# 4. Check screenshot
open /tmp/stealth-browserless-test.png
```

---

**Happy automating! 🚀**

For detailed setup and enterprise deployment, see **DEPLOYMENT_GUIDE.md**
