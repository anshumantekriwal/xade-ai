import unittest
import requests
from social import LunarCrush, CryptoPanic, SocialAPIError

class TestLunarCrush(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = LunarCrush("deb9mcyuk3wikmvo8lhlv1jsxnm6mfdf70lw4jqdk")

    def test_initialization(self):
        """Test proper initialization of LunarCrush client."""
        self.assertEqual(self.client.api_key, "deb9mcyuk3wikmvo8lhlv1jsxnm6mfdf70lw4jqdk")
        self.assertEqual(self.client.BASE_URL, "https://lunarcrush.com/api4/public")
        self.assertEqual(self.client.session.headers["Authorization"], f"Bearer {self.client.api_key}")

    def test_get_coin_data(self):
        """Test getting coin market data."""
        result = self.client.get_coin_data("BTC")
        
        self.assertIsInstance(result, dict)
        self.assertIn("symbol", result)
        self.assertEqual(result["symbol"], "BTC")
        self.assertIn("name", result)
        self.assertEqual(result["name"], "Bitcoin")
        self.assertIn("price", result)
        self.assertIn("market_cap", result)

    def test_get_coin_metadata(self):
        """Test getting coin metadata."""
        result = self.client.get_coin_metadata("BTC")
        
        self.assertIsInstance(result, dict)
        self.assertIn("symbol", result)
        self.assertEqual(result["symbol"], "BTC")
        self.assertIn("name", result)
        self.assertIn("market_categories", result)

    def test_get_nft_data(self):
        """Test getting NFT collection data."""
        result = self.client.get_nft_data("cryptopunks")
        
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertIn("floor_price", result)

    def test_get_topic_news(self):
        """Test getting topic news."""
        result = self.client.get_topic_news("bitcoin")
        
        self.assertIsInstance(result, list)
        if len(result) > 0:
            self.assertIn("post_type", result[0])
            self.assertIn("post_title", result[0])
            self.assertIn("post_link", result[0])

    def test_get_coins_list(self):
        """Test getting list of all coins."""
        result = self.client.get_coins_list()
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("symbol", result[0])
        self.assertIn("name", result[0])
        self.assertIn("price", result[0])
        self.assertIn("market_cap", result[0])
        self.assertIn("galaxy_score", result[0])

    def test_get_topic_summary(self):
        """Test getting topic summary."""
        result = self.client.get_topic_summary("bitcoin")
        
        self.assertIsInstance(result, dict)
        self.assertIn("topic", result)
        self.assertEqual(result["topic"], "bitcoin")
        self.assertIn("title", result)
        self.assertIn("topic_rank", result)
        self.assertIn("interactions_24h", result)

    def test_api_error(self):
        """Test API error handling with invalid coin."""
        with self.assertRaises(SocialAPIError):
            self.client.get_coin_data("NONEXISTENTCOIN123456789")

class TestCryptoPanic(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = CryptoPanic("2c962173d9c232ada498efac64234bfb8943ba70")

    def test_initialization(self):
        """Test proper initialization of CryptoPanic client."""
        self.assertEqual(self.client.auth_token, "2c962173d9c232ada498efac64234bfb8943ba70")
        self.assertEqual(self.client.BASE_URL, "https://cryptopanic.com/api/v1")

    def test_get_posts(self):
        """Test getting news posts."""
        result = self.client.get_posts(
            public=True,
            filter="hot",
            currencies="BTC,ETH",
            regions="en",
            kind="news"
        )

        self.assertIsInstance(result, dict)
        self.assertIn("results", result)
        self.assertIsInstance(result["results"], list)
        if len(result["results"]) > 0:
            first_post = result["results"][0]
            self.assertIn("kind", first_post)
            self.assertIn("title", first_post)
            self.assertIn("published_at", first_post)
            self.assertIn("url", first_post)


if __name__ == '__main__':
    unittest.main()
