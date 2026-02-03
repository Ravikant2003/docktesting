# Proxy Integration Guide for Chrome CDP

## Overview
This guide explains how to integrate proxy support with your Browserless Chrome instance running over Chrome DevTools Protocol (CDP).

## How Chrome CDP Proxy Works

Chrome's remote debugging protocol doesn't directly support HTTP proxies through CDP commands. Instead, proxies are configured at:
1. **Browser launch time** - via Chrome command-line flags
2. **System level** - via environment variables
3. **Browserless service** - via Docker environment variables

## Implementation Methods

### Method 1: Browserless Docker Environment Variables (Recommended)

Browserless supports proxy configuration through environment variables in docker-compose.yml

**Setup:**
```yaml
environment:
  PROXY_URL: "http://username:password@proxy-server:port"
  PROXY_SOCKS: "socks5://username:password@socks-server:port"
```

**Supported Formats:**
- HTTP: `http://[user:pass@]host:port`
- HTTPS: `https://[user:pass@]host:port`
- SOCKS5: `socks5://[user:pass@]host:port`

**Chrome respects via:**
- `--proxy-server=<proxy-url>` flag
- `http_proxy`, `https_proxy`, `all_proxy` environment variables

### Method 2: Direct Chrome Flags in docker-compose

```yaml
DEFAULT_LAUNCH_ARGS: >-
  --proxy-server="http://proxy-ip:port"
  --proxy-bypass-list="localhost;127.0.0.1"
```

### Method 3: Go Application Level Configuration

From your Go code, you can:
1. Detect proxy environment variables
2. Pass them to Browserless via launch arguments
3. Create separate contexts for different proxies

## Current Implementation Status

Your setup currently:
- ✅ Has docker-compose with Browserless
- ✅ Supports environment variables
- ❌ Not using any proxy

## Next Steps

1. Update docker-compose.yml with proxy environment variables
2. Test with free proxy (optional) or paid proxy service
3. Verify Booking.com and Indeed.com can be accessed
4. Implement proxy rotation (cycling through multiple proxies)

## Proxy Services Integration

### Free Proxies (Not Recommended)
- Unreliable
- Often blocked
- Slow speeds

### Paid Proxies (Recommended)

**ScraperAPI ($29/month)**
```
http://api.scraperapi.com?api_key=YOUR_KEY&url=TARGET_URL
```

**Bright Data ($168/month)**
```
http://username-country-US:password@proxy.provider.com:7000
```

**Smartproxy ($39/month)**
```
http://username:password@gate.smartproxy.com:7000
```

## Environment Variables

Set these in your `.env` file or docker-compose:

```bash
# Proxy Configuration
PROXY_URL=http://username:password@proxy.server:port
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
PROXY_SERVER=proxy.server
PROXY_PORT=port
PROXY_TYPE=http  # http, https, socks5

# Rotation Configuration
PROXY_ROTATION_ENABLED=true
PROXY_LIST_FILE=/path/to/proxies.txt
```

## Testing Proxy Configuration

### Step 1: Update docker-compose.yml
Add PROXY_URL environment variable

### Step 2: Restart Browserless
```bash
docker-compose down
docker-compose up -d
```

### Step 3: Test connectivity
```bash
curl -x http://proxy:port https://httpbin.org/ip
```

### Step 4: Run your tests
```bash
go run main.go profiles.go behavior.go
```

## Troubleshooting

**Issue: Proxy connection refused**
- Check proxy credentials
- Verify proxy server is running
- Check firewall rules

**Issue: Bookmarks.com still blocked**
- Proxy may be detected as data-center
- Try different proxy provider
- May need CAPTCHA solver as well

**Issue: Slow responses**
- Proxy server overloaded
- Network latency to proxy
- Try different proxy location

## Security Considerations

1. **Never commit credentials** - Use environment variables
2. **Encrypt in transit** - Use HTTPS/SOCKS5
3. **Audit proxy usage** - Log all requests
4. **Rotate credentials** - Change passwords regularly
5. **Whitelist URLs** - Only proxy necessary requests
