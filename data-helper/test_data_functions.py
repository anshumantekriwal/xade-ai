import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_functions import *

class TestDataFunctions(unittest.TestCase):
    def setUp(self):
        """Set up test data that matches API response formats"""
        # Sample price history data (matches Mobula API format)
        # Generate enough data points for MACD (need at least 26 for slow period)
        # and price stability (need at least 20)
        self.price_history = [
            100.0, 105.0, 95.0, 98.0, 103.0, 107.0, 104.0, 110.0, 115.0, 112.0,
            108.0, 111.0, 116.0, 120.0, 118.0, 122.0, 125.0, 121.0, 124.0, 128.0,
            126.0, 130.0, 135.0, 132.0, 128.0, 131.0, 136.0, 140.0, 138.0, 142.0
        ]
        
        # Sample market data (matches Mobula API format)
        self.market_data = {
            "price": 120.0,
            "volume": 1000000.0,
            "market_cap": 10000000.0,
            "off_chain_volume": 500000.0
        }
        
        # Sample market history data
        self.history_data = {
            "price": 100.0
        }
        
        # Sample pair data (matches Mobula pair format)
        self.pair_data = {
            "liquidity": 500000.0
        }
        
        # Sample trades data (matches Mobula trades format)
        self.trades_data = [
            {"timestamp": 1625097600, "price": 100.0},
            {"timestamp": 1625184000, "price": 105.0},
            {"timestamp": 1625270400, "price": 95.0}
        ]
        
        # Sample social data (matches LunarCrush format)
        self.social_data = {
            "sentiment": 0.75,
            "galaxy_score": 85,
            "alt_rank": 25,
            "interactions_24h": 10000,
            "num_posts": 1000
        }
        
        # Sample token holders data (matches Mobula format)
        self.token_holders = {
            "data": [
                {"holding": 1000000},
                {"holding": 500000},
                {"holding": 250000}
            ]
        }

    def test_calculateSMA(self):
        """Test Simple Moving Average calculation"""
        sma = calculateSMA(self.price_history, 5)
        self.assertIsInstance(sma, float)
        self.assertTrue(100.0 <= sma <= 120.0)  # Should be within price range

    def test_calculateEMA(self):
        """Test Exponential Moving Average calculation"""
        ema = calculateEMA(self.price_history, 5)
        self.assertIsInstance(ema, float)
        self.assertTrue(100.0 <= ema <= 120.0)  # Should be within price range

    def test_calculateRSI(self):
        """Test Relative Strength Index calculation"""
        rsi = calculateRSI(self.price_history)
        self.assertIsInstance(rsi, float)
        self.assertTrue(0 <= rsi <= 100)  # RSI should be between 0 and 100

    def test_calculateMACD(self):
        """Test Moving Average Convergence Divergence calculation"""
        macd = calculateMACD(self.price_history, 12, 26, 9)
        self.assertIsInstance(macd, dict)
        self.assertIn("macd_line", macd)
        self.assertIn("signal_line", macd)
        self.assertIn("histogram", macd)

    def test_calculateVolatility(self):
        """Test volatility calculation"""
        volatility = calculateVolatility(self.price_history)
        self.assertIsInstance(volatility, float)
        self.assertTrue(volatility >= 0)  # Volatility should be non-negative

    def test_determineTrend(self):
        """Test trend determination"""
        trend = determineTrend(self.price_history, 5, 10)
        self.assertIn(trend, ["up", "down", "sideways"])

    def test_price(self):
        """Test price extraction"""
        p = price(self.market_data)
        self.assertEqual(p, 120.0)

    def test_volume(self):
        """Test volume extraction"""
        vol = volume(self.market_data)
        self.assertEqual(vol, 1000000.0)

    def test_marketCap(self):
        """Test market cap calculation"""
        cap = marketCap(self.market_data, 100000.0)
        self.assertEqual(cap, 120.0 * 100000.0)

    def test_offChainVolume(self):
        """Test off-chain volume extraction"""
        off_vol = offChainVolume(self.market_data)
        self.assertEqual(off_vol, 500000.0)

    def test_liquidity(self):
        """Test liquidity extraction"""
        liq = liquidity(self.pair_data)
        self.assertEqual(liq, 500000.0)

    def test_liquidityChange24h(self):
        """Test liquidity change calculation"""
        change = liquidityChange24h(500000.0, 400000.0)
        self.assertEqual(change, 25.0)

    def test_socialSentimentScore(self):
        """Test social sentiment score extraction"""
        score = socialSentimentScore(self.social_data)
        self.assertEqual(score, 0.75)

    def test_galaxyScore(self):
        """Test Galaxy Score extraction"""
        score = galaxyScore(self.social_data)
        self.assertEqual(score, 85)

    def test_altRank(self):
        """Test AltRank extraction"""
        rank = altRank(self.social_data)
        self.assertEqual(rank, 25)

    def test_socialEngagementRate(self):
        """Test social engagement rate calculation"""
        rate = socialEngagementRate(self.social_data)
        self.assertEqual(rate, 10)  # 10000/1000

    def test_decentralizationScore(self):
        """Test decentralization score calculation"""
        score = decentralizationScore(self.token_holders)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 1)  # Score should be between 0 and 1

    def test_marketMomentumScore(self):
        """Test market momentum score calculation"""
        score = marketMomentumScore(self.price_history, 5, 10)
        self.assertIsInstance(score, float)

    def test_priceChange24h(self):
        """Test 24h price change calculation"""
        change = priceChange24h(self.market_data, self.history_data)
        self.assertEqual(change, 20.0)  # (120-100)/100 * 100

    def test_ath(self):
        """Test all-time high calculation"""
        high = ath(self.price_history)
        self.assertEqual(high, 120.0)

    def test_atl(self):
        """Test all-time low calculation"""
        low = atl(self.price_history)
        self.assertEqual(low, 95.0)

    def test_marketCapToVolumeRatio(self):
        """Test market cap to volume ratio calculation"""
        ratio = marketCapToVolumeRatio(self.market_data)
        self.assertEqual(ratio, 10.0)  # 10000000/1000000

    def test_riskAdjustedReturn(self):
        """Test risk-adjusted return calculation"""
        rar = riskAdjustedReturn(self.price_history)
        self.assertIsInstance(rar, float)

    def test_priceStabilityScore(self):
        """Test price stability score calculation"""
        score = priceStabilityScore(self.price_history)
        self.assertIsInstance(score, float)
        self.assertTrue(0 <= score <= 1)  # Score should be between 0 and 1

    def test_tradeActivityIntensity(self):
        """Test trade activity intensity calculation"""
        intensity = tradeActivityIntensity(self.trades_data)
        self.assertEqual(intensity, 3.0)  # Length of trades_data

if __name__ == '__main__':
    unittest.main()
