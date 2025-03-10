import unittest
import requests
from social import LunarCrush, SocialAPIError

class TestLunarCrush(unittest.TestCase):
    def setUp(self):
        self.api = LunarCrush("deb9mcyuk3wikmvo8lhlv1jsxnm6mfdf70lw4jqdk")

    def test_get_coin_data(self):
        result = self.api.get_coin_data("BTC")
        self.assertIn("id", result)
        self.assertIn("name", result)
        self.assertIn("symbol", result)
        self.assertEqual(result["symbol"], "BTC")

    def test_get_coin_metadata(self):
        result = self.api.get_coin_metadata("BTC")
        self.assertIn("id", result)
        self.assertIn("name", result)
        self.assertIn("symbol", result)
        self.assertIn("market_categories", result)

    def test_get_nft_data(self):
        result = self.api.get_nft_data("cryptopunks")
        self.assertIn("id", result)
        self.assertIn("name", result)
        self.assertIn("floor_price", result)

    def test_get_topic_news(self):
        result = self.api.get_topic_news("bitcoin")
        self.assertTrue(isinstance(result, list))
        if len(result) > 0:
            self.assertIn("post_type", result[0])
            self.assertIn("post_title", result[0])
            self.assertIn("post_link", result[0])

    def test_get_coins_list(self):
        result = self.api.get_coins_list()
        self.assertTrue(isinstance(result, list))
        if len(result) > 0:
            self.assertIn("id", result[0])
            self.assertIn("symbol", result[0])
            self.assertIn("name", result[0])
            self.assertIn("price", result[0])
            self.assertIn("market_cap", result[0])
            self.assertIn("galaxy_score", result[0])

    def test_get_topic_summary(self):
        result = self.api.get_topic_summary("bitcoin")
        self.assertIn("topic", result)
        self.assertIn("title", result)
        self.assertIn("topic_rank", result)
        self.assertIn("interactions_24h", result)

    def test_api_error(self):
        with self.assertRaises(SocialAPIError):
            self.api.get_coin_data("NONEXISTENTCOIN123456789")

if __name__ == '__main__':
    unittest.main()
