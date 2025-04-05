import asyncio
from playwright.async_api import async_playwright

import asyncio
from playwright.async_api import async_playwright
import asyncio
from playwright.async_api import async_playwright

async def main6():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Inject JavaScript to monitor variables starting with 'game4padel_'
        await page.add_init_script("""
            (function() {
                const interceptGlobalAssign = (target, prop) => {
                    let value = target[prop];
                    Object.defineProperty(target, prop, {
                        get() {
                            return value;
                        },
                        set(newValue) {
                            // Only log variables that start with 'game4padel_'
                            if (prop.startsWith('game4padel_')) {
                                console.log(`%c🔑 ${prop} set to: ` + newValue, 'color: blue; font-weight: bold;');
                                console.trace();  // This will print where the key is set
                            }
                            value = newValue;
                        }
                    });
                };

                // Intercept all window properties
                for (let prop in window) {
                    interceptGlobalAssign(window, prop);
                }

                // In case new properties are added dynamically (e.g. in modern JS frameworks)
                const originalDefineProperty = Object.defineProperty;
                Object.defineProperty = function(target, prop, descriptor) {
                    interceptGlobalAssign(target, prop);
                    return originalDefineProperty.apply(this, arguments);
                };
            })();
        """)

        # Go to the page you are testing
        await page.goto("https://www.game4padel.com/hove-beach-park")  # Replace with your actual page

        # Allow time for the script to load and for the key to be set
        await page.wait_for_timeout(10000)

        await browser.close()


async def main5():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Inject JavaScript to watch for changes to a possible global 'apiKey' variable
        await page.add_init_script("""
            (function() {
                const originalDefineProperty = Object.defineProperty;

                // Intercept and watch for changes to any object with apiKey in it
                Object.defineProperty(window, 'apiKey', {
                    set(value) {
                        console.log('%c🔑 API Key set to: ' + value, 'color: blue; font-weight: bold;');
                        console.trace();  // Get a stack trace
                    },
                    get() {
                        return this._apiKey;
                    }
                });

                // Allow the variable to be set normally
                Object.defineProperty(window, '_apiKey', {
                    set(value) {
                        this._apiKey = value;
                    }
                });
            })();
        """)

        # Go to the page you are testing
        await page.goto("https://www.game4padel.com/hove-beach-park")  # Replace with your actual page

        # Allow time for the script to load and for the key to be set
        await page.wait_for_timeout(10000)

        await browser.close()


async def main4():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True to run headless
        context = await browser.new_context()
        page = await context.new_page()

        # Inject JavaScript to monitor XMLHttpRequest
        await page.add_init_script("""
            (function() {
                const originalOpen = XMLHttpRequest.prototype.open;
                const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

                XMLHttpRequest.prototype.setRequestHeader = function(name, value) {
                    if (name.toLowerCase() === 'x-api-key') {
                        console.log('%c🔐 XHR x-api-key SET: ' + value, 'color: green; font-weight: bold;');
                        console.trace();  // View stack trace in DevTools
                    }
                    return originalSetRequestHeader.apply(this, arguments);
                };

                XMLHttpRequest.prototype.open = function() {
                    this._requestUrl = arguments[1]; // Save URL
                    return originalOpen.apply(this, arguments);
                };
            })();
        """)

        # Go to the actual page (replace with target)
        await page.goto("https://www.game4padel.com/hove-beach-park")

        # Wait for JS to load and API calls to happen
        await page.wait_for_timeout(30000)

        await browser.close()



async def main3():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Inject JavaScript to override fetch and XHR
        await page.add_init_script("""
            (function() {
                const originalFetch = window.fetch;
                window.fetch = async function(...args) {
                    const [resource, config] = args;
                    if (config && config.headers) {
                        for (const [key, value] of Object.entries(config.headers)) {
                            if (key.toLowerCase() === 'x-api-key') {
                                console.log('🔎 FETCH x-api-key SET:', value);
                                console.trace();  // <-- This prints the stack trace!
                            }
                        }
                    }
                    return originalFetch.apply(this, args);
                };

                const originalOpen = XMLHttpRequest.prototype.open;
                const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

                XMLHttpRequest.prototype.setRequestHeader = function(name, value) {
                    if (name.toLowerCase() === 'x-api-key') {
                        console.log('🔎 XHR x-api-key SET:', value);
                        console.trace();  // <-- Stack trace again
                    }
                    return originalSetRequestHeader.apply(this, arguments);
                };
            })();
        """)

        # Navigate to your real page
        await page.goto("https://www.game4padel.com/hove-beach-park")  # Replace with actual page

        # Allow time for widget + JS to load and API key to be set
        await page.wait_for_timeout(10000)

        await browser.close()



async def main2():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True to hide
        context = await browser.new_context()
        page = await context.new_page()

        # Intercept requests and look for 'x-api-key'
        async def handle_request(request):
            headers = request.headers
            for k, v in headers.items():
                if k.lower() == "x-api-key":
                    print(f"🔑 Found x-api-key in request to {request.url}: {v}")

        page.on("request", handle_request)

        # Go to the actual page
        await page.goto("https://www.game4padel.com/hove-beach-park")  # Replace with real URL


        # Wait for things to settle
        await page.wait_for_timeout(10000)

        await browser.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True to run in background
        context = await browser.new_context()
        page = await context.new_page()

        # 🧠 Inject JavaScript before page loads to hook into MatchiWidget.init
        await page.add_init_script("""
            window.__interceptedApiKey = null;

            const originalInit = window.MatchiWidget?.init;
            window.MatchiWidget = {
                init: function(options) {
                    console.log("Intercepted options:", options);
                    if (options?.apiKey) {
                        window.__interceptedApiKey = options.apiKey;
                        console.log("🎯 API Key found:", options.apiKey);
                    }
                    if (originalInit) {
                        return originalInit.apply(this, arguments);
                    }
                }
            };
        """)

        # 🌐 Navigate to the page with the widget
        await page.goto("https://www.game4padel.com/hove-beach-park")  # Replace with real URL

        # ⏳ Wait for a bit to allow the widget to load
        await page.wait_for_timeout(5000)

        # 🔍 Read the intercepted API key from the page
        api_key = await page.evaluate("window.__interceptedApiKey")
        print("\n🚀 Extracted API Key:", api_key)

        await browser.close()

asyncio.run(main2())

