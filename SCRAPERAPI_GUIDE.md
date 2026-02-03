# ScraperAPI Integration Guide

## Overview

ScraperAPI is the easiest way to bypass Cloudflare and other anti-bot systems. It handles:
- ✅ Cloudflare challenges automatically
- ✅ Residential IP rotation
- ✅ CAPTCHA solving
- ✅ Session management
- ✅ Browser fingerprinting

## Getting Started

### Step 1: Create Free Account
1. Go to: https://www.scraperapi.com/signup
2. Enter email and password
3. No credit card required!
4. Verify email

### Step 2: Get Your Free API Key
After signup, you'll see your dashboard with:
```
Free API Key: xxxxxxxxxxxxxxxxxxxxx
Free monthly requests: 1,000
```

### Step 3: Copy Your API Key
Keep this safe - you'll need it for configuration.

## How ScraperAPI Works

### Architecture
```
Your Code
    ↓
ScraperAPI Endpoint
    ↓
Their Residential Proxies
    ↓
Cloudflare Check
    ↓
Their Anti-Bot Evasion
    ↓
Target Website
    ↓
Return Clean HTML
```

### API Format
```
http://api.scraperapi.com?api_key=YOUR_KEY&url=TARGET_URL
```

## Integration with Your Go Code

### Method 1: Use ScraperAPI as HTTP Proxy

```bash
# Set environment variable
export PROXY_URL="http://api.scraperapi.com?api_key=YOUR_KEY"

# Run tests
go run main.go profiles.go behavior.go config.go
```

### Method 2: Direct Integration in Go

Modify your test code to use ScraperAPI directly:
```go
// Instead of accessing target URL directly
scraperURL := fmt.Sprintf(
    "http://api.scraperapi.com?api_key=%s&url=%s",
    os.Getenv("SCRAPER_API_KEY"),
    url.QueryEscape(testURL),
)

// Use scraperURL instead of testURL
```

### Method 3: Chrome Extension Mode

Use their Residential Proxy format for Chrome:
```bash
export PROXY_URL="http://scraperapi.render:YOURKEY@api.scraperapi.com:8001"
```

## Configuration

### Environment Variables

Create `.env` file in your project:
```bash
# ScraperAPI Configuration
SCRAPER_API_KEY=your_free_api_key_here
SCRAPER_API_ENABLED=true

# Or use as proxy
PROXY_URL=http://api.scraperapi.com?api_key=your_free_api_key_here
```

### Docker Compose

Update docker-compose.yml:
```yaml
environment:
  SCRAPER_API_KEY: ${SCRAPER_API_KEY}
  PROXY_URL: "http://api.scraperapi.com?api_key=${SCRAPER_API_KEY}"
```

## Usage Examples

### Example 1: Test Booking.com

```bash
export SCRAPER_API_KEY="your_free_api_key"
export PROXY_URL="http://api.scraperapi.com?api_key=${SCRAPER_API_KEY}"

go run main.go profiles.go behavior.go config.go
```

### Example 2: Direct URL to ScraperAPI

```go
func TestWithScraperAPI(testURL string, apiKey string) error {
    scraperURL := fmt.Sprintf(
        "http://api.scraperapi.com?api_key=%s&url=%s",
        apiKey,
        url.QueryEscape(testURL),
    )
    
    // Navigate to scraperURL instead of testURL
    chromedp.Navigate(scraperURL)
    
    return nil
}
```

### Example 3: Python Equivalent (if needed)

```python
import requests

api_key = "your_free_api_key"
url = "https://booking.com"

response = requests.get(
    "http://api.scraperapi.com",
    params={
        'api_key': api_key,
        'url': url
    }
)

print(response.text)
```

## API Request Parameters

### Basic
- `api_key` - Your API key (required)
- `url` - URL to scrape (required)

### Advanced
```
http://api.scraperapi.com?
  api_key=YOUR_KEY&
  url=https://booking.com&
  render=true&
  timeout=10000&
  country_code=US
```

### Available Parameters
- `render=true` - Render JavaScript
- `premium=true` - Use premium proxies (paid)
- `country_code=US` - US IP location
- `timeout=10000` - Timeout in ms
- `keep_headers=true` - Keep original headers

## Troubleshooting

### Issue: "Unauthorized" Error
```
Error: 401 Unauthorized
```
**Solution:** Check API key is correct
- Copy from dashboard again
- Verify no spaces/typos
- Check key has NOT been copied incorrectly

### Issue: "Rate Limited"
```
Error: 429 Too Many Requests
```
**Solution:** Free tier has limits
- Free: 1,000 requests/month
- ~33 requests/day
- Space out tests
- Or upgrade to paid plan

### Issue: Still Blocked by Cloudflare
```
Page: "Checking your browser"
```
**Solution:** Use render parameter
```
http://api.scraperapi.com?
  api_key=KEY&
  url=TARGET&
  render=true
```

### Issue: Slow Response
```
Takes 10+ seconds
```
**Solution:** Normal for ScraperAPI
- They solve challenges
- Takes 5-15 seconds per request
- Free tier is slower than paid

## Cost Analysis

### Free Tier
- **Requests**: 1,000/month
- **Cost**: FREE
- **Duration**: Unlimited
- **Cloudflare**: ✅ YES
- **Speed**: Standard

### Paid Plans (If needed later)
- **Hobby**: $29/month (10,000 requests)
- **Professional**: $99/month (100,000 requests)
- **Business**: Custom pricing

## Testing Your Integration

### Quick Test
```bash
curl "http://api.scraperapi.com?api_key=YOUR_KEY&url=https://httpbin.org/ip"
```

Expected response:
```json
{
  "origin": "123.45.67.89"  // ScraperAPI's IP
}
```

### Test Cloudflare Bypass
```bash
curl "http://api.scraperapi.com?api_key=YOUR_KEY&url=https://booking.com" | head -20
```

Should return HTML, not "Checking your browser"

## Limitations & Notes

### Free Tier Limits
- 1,000 requests/month
- Standard speed
- Shared proxies
- No priority support

### What Works
- ✅ Cloudflare bypass
- ✅ All tested sites
- ✅ JavaScript rendering
- ✅ Cookie handling
- ✅ Header manipulation

### What Doesn't Work
- ❌ CAPTCHA solving (requires OCR)
- ❌ Very slow sites
- ❌ WebSocket connections
- ❌ File downloads

## Next Steps

1. Sign up and get API key
2. Test with curl command above
3. Set environment variable
4. Run your Go tests
5. Monitor usage dashboard
6. If you exceed free tier, upgrade or wait for next month

## Support & Documentation

- Website: https://www.scraperapi.com
- Docs: https://www.scraperapi.com/documentation
- Dashboard: https://dashboard.scraperapi.com
- Status: https://status.scraperapi.com
