import unittest
from mobula import Mobula, MobulaAPIError

class TestMobula(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = Mobula("e26c7e73-d918-44d9-9de3-7cbe55b63b99")

    def test_initialization(self):
        """Test proper initialization of Mobula client."""
        self.assertEqual(self.client.api_key, "e26c7e73-d918-44d9-9de3-7cbe55b63b99")
        self.assertEqual(self.client.BASE_URL, "https://api.mobula.io/api/1")
        self.assertEqual(self.client.session.headers["Authorization"], self.client.api_key)

    def test_get_market_data(self):
        """Test getting market data for Bitcoin."""
        data = self.client.get_market_data(symbol="BTC")
        
        self.assertIsInstance(data, dict)
        self.assertIn("price", data)
        self.assertIn("market_cap", data)
        self.assertIn("volume", data)
        self.assertIn("liquidity", data)
        self.assertEqual(data["symbol"], "BTC")

    def test_get_all_assets(self):
        """Test getting all assets."""
        assets = self.client.get_all_assets()
        
        self.assertIsInstance(assets, list)
        self.assertGreater(len(assets), 0)
        self.assertIn("id", assets[0])
        self.assertIn("name", assets[0])
        self.assertIn("symbol", assets[0])

    def test_get_blockchains(self):
        """Test getting blockchain information."""
        blockchains = self.client.get_blockchains()
        
        self.assertIsInstance(blockchains, list)
        self.assertGreater(len(blockchains), 0)
        self.assertIn("name", blockchains[0])
        self.assertIn("chainId", blockchains[0])
        self.assertIn("evmChainId", blockchains[0])

    def test_get_market_pairs(self):
        """Test getting trading pairs."""
        pairs = self.client.get_market_pairs(limit="10")
        
        self.assertIsInstance(pairs, dict)
        if "pairs" in pairs:
            pairs_list = pairs["pairs"]
        else:
            # Handle case where response is direct list of pairs
            pairs_list = pairs
            
        self.assertIsInstance(pairs_list, list)
        if len(pairs_list) > 0:
            first_pair = pairs_list[0]
            self.assertTrue(
                "token0" in first_pair or 
                "baseToken" in first_pair or 
                "base_token" in first_pair
            )

    def test_get_market_multi_data(self):
        """Test getting multi-asset market data."""
        data = self.client.get_market_multi_data(symbols="BTC,ETH")
        
        self.assertIsInstance(data, dict)
        self.assertIn("data", data)
        self.assertIn("dataArray", data)
        self.assertGreater(len(data["dataArray"]), 0)

    def test_invalid_parameters(self):
        """Test handling of invalid parameters."""
        with self.assertRaises(ValueError):
            self.client.get_market_data()

    def test_api_error(self):
        """Test API error handling with invalid symbol."""
        with self.assertRaises(MobulaAPIError):
            self.client.get_market_data(symbol="NONEXISTENTCOIN123456789")

if __name__ == '__main__':
    unittest.main()
