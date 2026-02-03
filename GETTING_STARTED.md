# Getting Started with ScraperAPI Integration

## Quick Setup (3 Steps)

### Step 1: Sign Up for Free ScraperAPI Account
1. Go to: **https://www.scraperapi.com/signup**
2. No credit card required for free tier
3. You'll get **1,000 free API calls/month** instantly
4. Copy your API key from the dashboard

### Step 2: Set Environment Variable
```bash
# Linux/macOS
export SCRAPER_API_KEY="your_api_key_here"

# Or add to .env file
echo "SCRAPER_API_KEY=your_api_key_here" > .env
```

### Step 3: Run the Project with Docker
```bash
# Start browserless Chrome container
docker-compose up -d

# Wait 2 seconds for container to start
sleep 2

# Run tests with ScraperAPI enabled
go run main.go profiles.go behavior.go config.go scraperapi.go
```

---

## What Happens Now?

### Before ScraperAPI:
```
[1] ❌ | https://www.booking.com/ (Blocked by Cloudflare)
[2] ❌ | https://www.indeed.com/ (Blocked by Cloudflare)
```

### After ScraperAPI:
```
[1] ✅ | https://www.booking.com/ (SUCCESS - Cloudflare bypassed!)
[2] ✅ | https://www.indeed.com/ (SUCCESS - Cloudflare bypassed!)
```

---

## How It Works

1. **scraperapi.go** loads your `SCRAPER_API_KEY` from environment
2. When enabled, requests are automatically routed through ScraperAPI
3. ScraperAPI's residential proxies bypass IP-based Cloudflare detection
4. JavaScript stealth features handle browser fingerprinting
5. You get 2 layers of bot evasion working together!

---

## Verify Configuration

Run without Docker to see current status:
```bash
# Just compile and show config (needs Docker on localhost:3000)
go run main.go profiles.go behavior.go config.go scraperapi.go
```

Look for this output:
```
🔗 ScraperAPI Configuration:
   • Status: ✅ ENABLED
   • API Key: your_key_here...
   • Render JS: false
   • Country: US
```

---

## Troubleshooting

### "SCRAPER_API_KEY not configured"
```bash
# Check if env var is set
echo $SCRAPER_API_KEY

# If empty, set it:
export SCRAPER_API_KEY="your_key_from_signup"
```

### "Connection refused to localhost:3000"
```bash
# Make sure Docker container is running:
docker-compose ps

# If not running, start it:
docker-compose up -d

# Check logs:
docker-compose logs browserless
```

### "API call limit exceeded"
- Free tier: 1,000 calls/month
- Upgrade at: https://www.scraperapi.com/pricing
- Or wait until next month for reset

---

## Next Steps

1. ✅ Sign up at https://www.scraperapi.com/signup
2. ✅ Copy your free API key
3. ✅ Set `SCRAPER_API_KEY` environment variable
4. ✅ Run `docker-compose up -d`
5. ✅ Run tests with `go run main.go profiles.go behavior.go config.go scraperapi.go`

---

## Support

- **ScraperAPI Docs:** https://www.scraperapi.com/documentation
- **Project Repo:** https://github.com/Ravikant2003/docktesting
- **Issues:** Check PROXY_INTEGRATION.md for advanced proxy setups

---

## Current Test Results

| Site | Difficulty | Status | Notes |
|------|-----------|--------|-------|
| Flipkart.com | MEDIUM | ✅ Working | Stealth features enough |
| eBay.com | MEDIUM | ✅ Working | Stealth features enough |
| Booking.com | MEDIUM | 🛡️ Blocked | Needs ScraperAPI (IP detection) |
| Indeed.com | MEDIUM | 🛡️ Blocked | Needs ScraperAPI (IP detection) |
| Reddit.com | EASY-MEDIUM | ⚠️ Partial | Content loaded but slow |
| Example.com | EASY | ⚠️ Partial | Cloudflare but allowed |

**With ScraperAPI enabled:** Booking.com and Indeed.com should show ✅ SUCCESS

