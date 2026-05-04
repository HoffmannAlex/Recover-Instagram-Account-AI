import requests
import aiohttp
import asyncio
import re
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Optional
import logging
import time
from logging_config import setup_logger

logger = setup_logger('CSRFManager')

class CSRFManager:
    """Manages CSRF tokens for secure API interactions"""
    
    def __init__(self, login_url="https://www.instagram.com/accounts/login/", timeout=15, cache_duration=10):
        self.login_url = login_url
        self.timeout = timeout
        self.cache_duration = timedelta(minutes=cache_duration)
        self.token_cache = {}
        self.last_request_time = None
        self.session_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    @lru_cache(maxsize=100)
    def get_csrf_token(self, use_proxy=False, proxy=None):
        """Fetch CSRF token with caching for performance"""
        cached_token = self.get_cached_token()
        if cached_token:
            logger.info("Returning cached CSRF token")
            return cached_token

        proxies = proxy if use_proxy else None
        try:
            logger.info("Fetching CSRF token...")
            response = requests.get(
                self.login_url,
                headers=self.session_headers,
                proxies=proxies,
                timeout=self.timeout
            )
            if response.status_code == 200:
                # Try cookies first
                csrf_token = response.cookies.get('csrftoken')
                if not csrf_token:
                    # Try extracting from HTML
                    csrf_token = self._extract_token_from_html(response.text)
                if csrf_token:
                    logger.info("CSRF token successfully fetched")
                    self.cache_token(csrf_token)
                    return csrf_token
                else:
                    logger.error("Failed to extract CSRF token from cookies or HTML")
            else:
                logger.error(f"Failed to fetch CSRF token. HTTP Status: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Exception fetching CSRF token: {e}")
        return None
    
    def _extract_token_from_html(self, html: str) -> Optional[str]:
        """Extract CSRF token from HTML response"""
        patterns = [
            r'"csrf_token":"([^"]+)"',
            r'<meta name="csrf_token" content="([^"]+)"',
            r'csrftoken=([^;]+)',
            r'"csrf_token"\s*:\s*"([^"]+)"',
        ]
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        return None

    def cache_token(self, token: str):
        """Cache CSRF token with timestamp"""
        self.token_cache = {
            'token': token,
            'timestamp': datetime.now()
        }
        logger.info("CSRF token cached")

    def get_cached_token(self) -> Optional[str]:
        """Retrieve cached token if still valid"""
        if not self.token_cache:
            return None
            
        if datetime.now() - self.token_cache['timestamp'] < self.cache_duration:
            return self.token_cache['token']
        else:
            logger.info("Cached CSRF token expired")
        return None

    def refresh_csrf_token(self, use_proxy=False, proxy=None):
        """Refresh CSRF token"""
        logger.info("Refreshing CSRF token...")
        return self.get_csrf_token(use_proxy, proxy)

    def validate_csrf_token(self, csrf_token, use_proxy=False, proxy=None):
        """Validate CSRF token authenticity"""
        headers = self.session_headers.copy()
        headers['X-CSRFToken'] = csrf_token
        proxies = proxy if use_proxy else None
        try:
            response = requests.get(self.login_url, headers=headers, proxies=proxies, timeout=self.timeout)
            if response.status_code == 200:
                logger.info("CSRF token is valid")
                return True
            else:
                logger.error(f"CSRF token validation failed. HTTP Status: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Exception validating CSRF token: {e}")
        return False

    def retry_request(self, func, retries=3, delay=2, *args, **kwargs):
        """Retry failed requests with exponential backoff"""
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                logger.warning(f"Request failed: {e}. Retrying {attempt + 1}/{retries}...")
                time.sleep(delay * (2 ** attempt))
        logger.error("All retries failed")
        return None
    
    async def get_csrf_token_async(self, use_proxy=False, proxy=None):
        """Fetch CSRF token asynchronously"""
        cached_token = self.get_cached_token()
        if cached_token:
            logger.info("Returning cached CSRF token (async)")
            return cached_token
        
        try:
            async with aiohttp.ClientSession(headers=self.session_headers) as session:
                async with session.get(self.login_url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                    if response.status == 200:
                        html = await response.text()
                        # Try cookies
                        csrf_token = None
                        for cookie in session.cookie_jar:
                            if cookie.key == 'csrftoken':
                                csrf_token = cookie.value
                                break
                        # Try HTML extraction
                        if not csrf_token:
                            csrf_token = self._extract_token_from_html(html)
                        if csrf_token:
                            logger.info("CSRF token successfully fetched (async)")
                            self.cache_token(csrf_token)
                            return csrf_token
                        else:
                            logger.error("Failed to extract CSRF token (async)")
                    else:
                        logger.error(f"Failed to fetch CSRF token (async). HTTP Status: {response.status}")
        except Exception as e:
            logger.error(f"Exception fetching CSRF token (async): {e}")
        return None

def get_csrf_token(use_proxy=False, proxy=None):
    """Convenience function to get CSRF token"""
    csrf_manager = CSRFManager()
    return csrf_manager.get_csrf_token(use_proxy, proxy)

if __name__ == "__main__":
    csrf_manager = CSRFManager()
    csrf_token = csrf_manager.get_csrf_token()
    if csrf_token:
        logger.info(f"Fetched CSRF Token: {csrf_token}")
        if csrf_manager.validate_csrf_token(csrf_token):
            refreshed_token = csrf_manager.refresh_csrf_token()
            logger.info(f"Refreshed CSRF Token: {refreshed_token}")
        else:
            logger.error("Invalid CSRF token")
    else:
        logger.error("Failed to fetch CSRF token")