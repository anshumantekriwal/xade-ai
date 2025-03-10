const axios = require("axios");
const OpenAI = require("openai");
const coins = require("./coins.json");

// Initialize OpenAI
const openai = new OpenAI({
  apiKey: process.env.REACT_APP_OPENAI_API_KEY,
});

// Add portfolioAddresses if not defined
const portfolioAddresses = ["0x0000000000000000000000000000000000000000"];

// Add LunarCrush API constant
const LUNARCRUSH_API_KEY = "deb9mcyuk3wikmvo8lhlv1jsxnm6mfdf70lw4jqdk";

// API Functions
const fetchPriceHistory = async (coinname, from = null, to = null) => {
  const response = await axios.get(
    `https://api.mobula.io/api/1/market/history`,
    {
      params: {
        asset: coinname,
        from: from,
        to: to,
      },
      headers: {
        Authorization:
          process.env.MOBULA_API_KEY || "e26c7e73-d918-44d9-9de3-7cbe55b63b99",
      },
    }
  );
  return response.data?.data?.price_history;
};

const fetchCryptoPanicData = async (coinname) => {
  const response = await axios.get(
    `https://cryptopanic.com/api/free/v1/posts/`,
    {
      params: {
        auth_token:
          process.env.CRYPTOPANIC_API_KEY ||
          "2c962173d9c232ada498efac64234bfb8943ba70",
        public: "true",
        currencies: coinname,
      },
    }
  );
  return response.data?.results;
};

const fetchMarketData = async (coinname) => {
  const response = await axios.get(
    `https://api.mobula.io/api/1/market/data?asset=${coinname}`,
    {
      headers: {
        Authorization: "e26c7e73-d918-44d9-9de3-7cbe55b63b99",
      },
    }
  );
  return response.data?.data;
};

const fetchMetadata = async (coinname) => {
  const response = await axios.get(
    `https://api.mobula.io/api/1/metadata?asset=${coinname}`,
    {
      headers: {
        Authorization: "e26c7e73-d918-44d9-9de3-7cbe55b63b99",
      },
    }
  );
  return response.data?.data;
};

const fetchHistoricPortfolioData = async (from, to, addresses) => {
  const response = await axios.get(
    `https://api.mobula.io/api/1/wallet/history`,
    {
      params: {
        wallets: addresses.join(","),
        from: from,
        to: to,
      },
      headers: {
        Authorization: "e26c7e73-d918-44d9-9de3-7cbe55b63b99",
      },
    }
  );
  return response.data;
};

const fetchWalletPortfolio = async (address) => {
  const response = await axios.get(
    `https://api.mobula.io/api/1/wallet/multi-portfolio`,
    {
      params: {
        wallets: address,
      },
      headers: {
        Authorization: "e26c7e73-d918-44d9-9de3-7cbe55b63b99",
      },
    }
  );
  return response.data?.data[0];
};

// Helper Functions
const getTokenName = (input) => {
  const lowercaseInput = input.toLowerCase();
  const matchedCoin = coins.find(
    (coin) =>
      coin.name.toLowerCase() === lowercaseInput ||
      coin.symbol.toLowerCase() === lowercaseInput
  );
  return matchedCoin ? matchedCoin.name.toLowerCase() : lowercaseInput;
};

const calculateSMA = (prices, period) => {
  const sum = prices.slice(-period).reduce((a, b) => a + b, 0);
  return sum / period;
};

const calculateRSI = (prices, period) => {
  let gains = 0;
  let losses = 0;
  for (let i = prices.length - period; i < prices.length; i++) {
    const difference = prices[i] - prices[i - 1];
    if (difference >= 0) gains += difference;
    else losses -= difference;
  }
  const avgGain = gains / period;
  const avgLoss = losses / period;
  const rs = avgGain / avgLoss;
  return 100 - 100 / (1 + rs);
};

const calculateMACD = (prices) => {
  const ema12 = calculateEMA(prices, 12);
  const ema26 = calculateEMA(prices, 26);
  const macdLine = ema12 - ema26;
  const signalLine = calculateEMA([macdLine], 9);
  const histogram = macdLine - signalLine;
  return { macdLine, signalLine, histogram };
};

const calculateEMA = (prices, period) => {
  const multiplier = 2 / (period + 1);
  let ema = prices[0];
  for (let i = 1; i < prices.length; i++) {
    ema = (prices[i] - ema) * multiplier + ema;
  }
  return ema;
};

const determineTrend = (sma, rsi, macd) => {
  let signals = [];
  if (rsi > 70) signals.push("Overbought");
  else if (rsi < 30) signals.push("Oversold");
  if (macd.macdLine > macd.signalLine) signals.push("Bullish MACD Crossover");
  else if (macd.macdLine < macd.signalLine)
    signals.push("Bearish MACD Crossover");
  return signals.join(", ") || "Neutral";
};

const calculateVolatility = (values) => {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const squaredDiffs = values.map((value) => Math.pow(value - mean, 2));
  const variance = squaredDiffs.reduce((a, b) => a + b, 0) / values.length;
  return Math.sqrt(variance);
};

const calculateTrend = (values) => {
  const firstValue = values[0];
  const lastValue = values[values.length - 1];
  const change = ((lastValue - firstValue) / firstValue) * 100;
  if (change > 5) return "Upward";
  if (change < -5) return "Downward";
  return "Sideways";
};

// Perplexity API
const usePerplexity = async (content) => {
  try {
    const response = await axios.post(
      "https://api.perplexity.ai/chat/completions",
      {
        model: "llama-3.1-sonar-small-128k-online",
        messages: [{ role: "user", content }],
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.REACT_APP_PERPLEXITY_API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error("Perplexity API error:", error);
    return "Unable to fetch data from Perplexity API";
  }
};

// Constants
const API_KEYS = {
  MOBULA: process.env.MOBULA_API_KEY || "e26c7e73-d918-44d9-9de3-7cbe55b63b99",
  CRYPTOPANIC:
    process.env.CRYPTOPANIC_API_KEY ||
    "2c962173d9c232ada498efac64234bfb8943ba70",
};

const TIME_PERIODS = {
  "1d": 24 * 60 * 60 * 1000,
  "7d": 7 * 24 * 60 * 60 * 1000,
  "30d": 30 * 24 * 60 * 60 * 1000,
  "1y": 365 * 24 * 60 * 60 * 1000,
};

// Token Information Functions
const website = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);
  return metadata?.website || "N/A";
};

const twitter = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);
  return metadata?.twitter || "N/A";
};

const telegram = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);
  return metadata?.telegram || "N/A";
};

const discord = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);
  return metadata?.discord || "N/A";
};

const description = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);
  return metadata?.description || "N/A";
};

// Market Data Functions
const price = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data?.price !== undefined ? `$${data.price.toFixed(2)}` : "N/A";
};

const volume = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data?.volume !== undefined ? `$${data.volume.toFixed(2)}` : "N/A";
};

const marketCap = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data?.market_cap !== undefined
    ? `$${data.market_cap.toFixed(2)}`
    : "N/A";
};

const marketCapDiluted = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `$${data?.market_cap_diluted?.toFixed(2) || "N/A"}`;
};

// Token Metrics Functions
const liquidity = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `$${data?.liquidity?.toFixed(2) || "N/A"}`;
};

const liquidityChange24h = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data?.liquidity_change_24h
    ? `${data.liquidity_change_24h.toFixed(2)}%`
    : "N/A";
};

const offChainVolume = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `$${data?.off_chain_volume?.toFixed(2) || "N/A"}`;
};

const volume7d = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `$${data?.volume_7d?.toFixed(2) || "N/A"}`;
};

// Price Change Functions
const volumeChange24h = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `${data?.volume_change_24h?.toFixed(2) || "N/A"}%`;
};

const priceChange24h = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `${data?.price_change_24h?.toFixed(2) || "N/A"}%`;
};

const priceChange1h = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `${data?.price_change_1h?.toFixed(2) || "N/A"}%`;
};

const priceChange7d = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `${data?.price_change_7d?.toFixed(2) || "N/A"}%`;
};

const priceChange1m = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `${data?.price_change_1m?.toFixed(2) || "N/A"}%`;
};

// Add missing priceChange30d function (alias for priceChange1m)
const priceChange30d = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `${data?.price_change_1m?.toFixed(2) || "N/A"}%`;
};

const priceChange1y = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `${data?.price_change_1y?.toFixed(2) || "N/A"}%`;
};

// Token Stats Functions
const ath = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `$${data?.ath?.toFixed(2) || "N/A"}`;
};

const atl = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return `$${data?.atl?.toFixed(2) || "N/A"}`;
};

const rank = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data?.rank || "N/A";
};

const totalSupply = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data?.total_supply || "N/A";
};

const circulatingSupply = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data?.circulating_supply || "N/A";
};

// Advanced Token Analysis Functions
const cexs = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);

  if (!metadata?.cexs || !Array.isArray(metadata.cexs)) {
    return "No CEX listing information available";
  }

  const formattedCexs = metadata.cexs
    .filter((cex) => cex.id)
    .map((cex) => ({
      name: cex.name || cex.id,
      logo: cex.logo || null,
    }));

  return {
    totalListings: formattedCexs.length,
    exchanges: formattedCexs,
  };
};

const investors = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);

  if (!metadata?.investors || !Array.isArray(metadata.investors)) {
    return "No investor information available";
  }

  const formattedInvestors = metadata.investors.map((investor) => ({
    name: investor.name,
    type: investor.type,
    isLead: investor.lead,
    country: investor.country_name || "Unknown",
    image: investor.image,
  }));

  return {
    totalInvestors: formattedInvestors.length,
    leadInvestors: formattedInvestors
      .filter((inv) => inv.isLead)
      .map((inv) => inv.name),
    vcInvestors: formattedInvestors.filter(
      (inv) => inv.type === "Ventures Capital"
    ).length,
    angelInvestors: formattedInvestors.filter(
      (inv) => inv.type === "Angel Investor"
    ).length,
    allInvestors: formattedInvestors,
  };
};

const distribution = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);

  if (!metadata?.distribution || !Array.isArray(metadata.distribution)) {
    return "No distribution information available";
  }

  return metadata.distribution.map((item) => ({
    category: item.name,
    percentage: item.percentage,
  }));
};

const releaseSchedule = async (token) => {
  const normalizedToken = getTokenName(token);
  const metadata = await fetchMetadata(normalizedToken);

  if (
    !metadata?.release_schedule ||
    !Array.isArray(metadata.release_schedule)
  ) {
    return "No release schedule information available";
  }

  const schedule = metadata.release_schedule.map((item) => ({
    date: new Date(item.unlock_date).toISOString(),
    tokensToUnlock: item.tokens_to_unlock,
    allocation: item.allocation_details,
  }));

  return {
    totalTokensInSchedule: schedule.reduce(
      (sum, item) => sum + item.tokensToUnlock,
      0
    ),
    totalUnlockEvents: schedule.length,
    upcomingUnlocks: schedule
      .filter((item) => new Date(item.date) > new Date())
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .slice(0, 5),
    fullSchedule: schedule,
  };
};

// Add missing priceHistoryData function
const priceHistoryData = async (token, period) => {
  const normalizedToken = getTokenName(token);
  const now = Date.now();
  const from = now - TIME_PERIODS[period];
  return await fetchPriceHistory(normalizedToken, from, now);
};

// Add missing getHistoricPortfolioData function
const getHistoricPortfolioData = async (addresses, period) => {
  const now = Date.now();
  const from = now - TIME_PERIODS[period];
  return await fetchHistoricPortfolioData(from, now, addresses);
};

// Add missing isListed function
const isListed = async (token) => {
  const normalizedToken = getTokenName(token);
  const data = await fetchMarketData(normalizedToken);
  return data ? "Listed" : "Not Listed";
};

// Add missing getPriceHistory function (wrapper for fetchPriceHistory)
const getPriceHistory = async (token, period) => {
  const normalizedToken = getTokenName(token);
  const now = Date.now();
  const from = now - TIME_PERIODS[period];
  return await fetchPriceHistory(normalizedToken, from, now);
};

// Add social data function
const getSocialData = async (token) => {
  try {
    const normalizedToken = getTokenName(token);
    const response = await axios.get(
      `https://lunarcrush.com/api4/public/topic/${normalizedToken}/v1`,
      {
        headers: {
          Authorization: `Bearer ${LUNARCRUSH_API_KEY}`,
        },
      }
    );

    const socialData = response.data?.data;
    if (!socialData) {
      return "No social data available";
    }

    return {
      topic: socialData.topic,
      title: socialData.title,
      topicRank: socialData.topic_rank,
      relatedTopics: socialData.related_topics,
      postCounts: socialData.types_count,
      interactions: {
        total24h: socialData.interactions_24h,
        byType: socialData.types_interactions,
      },
      sentiment: {
        byType: socialData.types_sentiment,
        details: socialData.types_sentiment_detail,
      },
      contributors: socialData.num_contributors,
      totalPosts: socialData.num_posts,
      categories: socialData.categories,
      trend: socialData.trend,
    };
  } catch (error) {
    console.error("Error fetching social data:", error);
    return "Failed to fetch social data";
  }
};

// Move getListByCategory function definition before it's used
const getListByCategory = async (
  sort = "social_dominance",
  filter = "",
  limit = 20
) => {
  try {
    const response = await axios.get(
      "https://lunarcrush.com/api4/public/coins/list/v2",
      {
        params: {
          sort,
          filter,
          limit,
        },
        headers: {
          Authorization: `Bearer ${LUNARCRUSH_API_KEY}`,
        },
      }
    );

    if (!response.data?.data) {
      throw new Error("No data received from LunarCrush API");
    }

    // Transform the data to a more usable format
    return response.data.data.map((coin) => ({
      id: coin.id,
      symbol: coin.symbol,
      name: coin.name,
      price: {
        usd: coin.price,
        btc: coin.price_btc,
      },
      volume24h: coin.volume_24h,
      volatility: coin.volatility,
      supply: {
        circulating: coin.circulating_supply,
        max: coin.max_supply,
      },
      priceChange: {
        "1h": coin.percent_change_1h,
        "24h": coin.percent_change_24h,
        "7d": coin.percent_change_7d,
        "30d": coin.percent_change_30d,
      },
      marketCap: {
        value: coin.market_cap,
        rank: coin.market_cap_rank,
        dominance: coin.market_dominance,
        previousDominance: coin.market_dominance_prev,
      },
      social: {
        interactions24h: coin.interactions_24h,
        volume24h: coin.social_volume_24h,
        dominance: coin.social_dominance,
        sentiment: coin.sentiment,
      },
      scores: {
        galaxy: {
          current: coin.galaxy_score,
          previous: coin.galaxy_score_previous,
        },
        altRank: {
          current: coin.alt_rank,
          previous: coin.alt_rank_previous,
        },
      },
      categories: coin.categories ? coin.categories.split(",") : [],
      blockchains: coin.blockchains,
      topic: coin.topic,
      logo: coin.logo,
      lastUpdated: {
        price: coin.last_updated_price,
        source: coin.last_updated_price_by,
      },
    }));
  } catch (error) {
    console.error("Error fetching coin list:", error);
    throw new Error(`Failed to fetch coin list: ${error.message}`);
  }
};
const executeCode = async (code) => {
  try {
    const cleanCode = code
      .replace(/```javascript\n?/, "")
      .replace(/```\n?/, "")
      .trim();

    // Create a safe context with allowed functions
    const context = {
      // Add default coins array to context
      coins: [
        { name: "bitcoin", symbol: "btc" },
        { name: "ethereum", symbol: "eth" },
        { name: "aptos", symbol: "apt" },
        { name: "binance coin", symbol: "bnb" },
        { name: "cardano", symbol: "ada" },
        { name: "solana", symbol: "sol" },
        { name: "ripple", symbol: "xrp" },
        { name: "polkadot", symbol: "dot" },
        // Add more default coins as needed
      ],

      getTokenName: (input) => {
        const lowercaseInput = input.toLowerCase();
        const matchedCoin = context.coins.find(
          (coin) =>
            coin.name.toLowerCase() === lowercaseInput ||
            coin.symbol.toLowerCase() === lowercaseInput
        );
        return matchedCoin ? matchedCoin.name.toLowerCase() : lowercaseInput;
      },

      // Market Data Functions
      price: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.price ? `$${data.price.toFixed(2)}` : "N/A";
      },
      volume: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.volume ? `$${data.volume.toFixed(2)}` : "N/A";
      },
      marketCap: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.market_cap ? `$${data.market_cap.toFixed(2)}` : "N/A";
      },
      marketCapDiluted: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.market_cap_diluted
          ? `$${data.market_cap_diluted.toFixed(2)}`
          : "N/A";
      },
      liquidity: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.liquidity ? `$${data.liquidity.toFixed(2)}` : "N/A";
      },

      // Price Change Functions
      priceChange24h: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.price_change_24h
          ? `${data.price_change_24h.toFixed(2)}%`
          : "N/A";
      },
      priceChange1h: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.price_change_1h
          ? `${data.price_change_1h.toFixed(2)}%`
          : "N/A";
      },
      priceChange7d: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.price_change_7d
          ? `${data.price_change_7d.toFixed(2)}%`
          : "N/A";
      },

      // Historical Data Functions
      getPriceHistory: async (token, period) => {
        return await fetchPriceHistory(token, period);
      },
      getHistoricPortfolioData: async (addresses, period) => {
        return await fetchHistoricPortfolioData(addresses, period);
      },
      getWalletPortfolio: async (address) => {
        return await fetchWalletPortfolio(address);
      },

      // Social Info Functions
      website: async (token) => {
        const metadata = await fetchMetadata(token);
        return metadata?.website || "N/A";
      },
      twitter: async (token) => {
        const metadata = await fetchMetadata(token);
        return metadata?.twitter || "N/A";
      },
      telegram: async (token) => {
        const metadata = await fetchMetadata(token);
        return metadata?.telegram || "N/A";
      },
      discord: async (token) => {
        const metadata = await fetchMetadata(token);
        return metadata?.discord || "N/A";
      },
      description: async (token) => {
        const metadata = await fetchMetadata(token);
        return metadata?.description || "N/A";
      },

      // Advanced Analysis Functions
      usePerplexity: async (query) => {
        return await usePerplexity(query);
      },
      cexs: async (token) => {
        return await cexs(token);
      },
      investors: async (token) => {
        return await investors(token);
      },
      distribution: async (token) => {
        return await distribution(token);
      },
      releaseSchedule: async (token) => {
        return await releaseSchedule(token);
      },

      // Utility Functions
      console: {
        log: (...args) => console.log(...args),
        error: (...args) => console.error(...args),
      },

      // Add missing functions to context
      priceChange30d: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.price_change_1m
          ? `${data.price_change_1m.toFixed(2)}%`
          : "N/A";
      },

      priceHistoryData: async (token, period) => {
        const normalizedToken = context.getTokenName(token);
        const now = Date.now();
        const from = now - TIME_PERIODS[period];
        return await fetchPriceHistory(normalizedToken, from, now);
      },

      liquidityChange24h: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.liquidity_change_24h
          ? `${data.liquidity_change_24h.toFixed(2)}%`
          : "N/A";
      },

      offChainVolume: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.off_chain_volume
          ? `$${data.off_chain_volume.toFixed(2)}`
          : "N/A";
      },

      volume7d: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.volume_7d ? `$${data.volume_7d.toFixed(2)}` : "N/A";
      },

      volumeChange24h: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.volume_change_24h
          ? `${data.volume_change_24h.toFixed(2)}%`
          : "N/A";
      },

      priceChange1m: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.price_change_1m
          ? `${data.price_change_1m.toFixed(2)}%`
          : "N/A";
      },

      priceChange1y: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.price_change_1y
          ? `${data.price_change_1y.toFixed(2)}%`
          : "N/A";
      },

      ath: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.ath ? `$${data.ath.toFixed(2)}` : "N/A";
      },

      atl: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.atl ? `$${data.atl.toFixed(2)}` : "N/A";
      },

      rank: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.rank || "N/A";
      },

      totalSupply: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.total_supply || "N/A";
      },

      circulatingSupply: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data?.circulating_supply || "N/A";
      },

      isListed: async (token) => {
        const normalizedToken = context.getTokenName(token);
        const data = await fetchMarketData(normalizedToken);
        return data ? "Listed" : "Not Listed";
      },

      // Add TIME_PERIODS to context
      TIME_PERIODS: {
        "1d": 24 * 60 * 60 * 1000,
        "7d": 7 * 24 * 60 * 60 * 1000,
        "30d": 30 * 24 * 60 * 60 * 1000,
        "1y": 365 * 24 * 60 * 60 * 1000,
      },

      // Add portfolioAddresses to context
      portfolioAddresses: portfolioAddresses,

      // Add getSocialData function to context
      getSocialData: async (token) => await getSocialData(token),

      // Add getListByCategory to context
      getListByCategory: async (
        sort = "social_dominance",
        filter = "",
        limit = 20
      ) => await getListByCategory(sort, filter, limit),

      // Add getTopicNews to context
      getTopicNews: async (topic) => {
        try {
          const response = await axios.get(
            `https://lunarcrush.com/api4/public/topic/${topic}/news/v1`,
            {
              headers: {
                Authorization: `Bearer ${LUNARCRUSH_API_KEY}`,
              },
            }
          );

          if (!response.data?.data) {
            return "No news data available";
          }

          return response.data.data.map((item) => ({
            id: item.id,
            type: item.post_type,
            title: item.post_title,
            url: item.post_link,
            image: item.post_image,
            created: new Date(item.post_created * 1000).toISOString(),
            sentiment: item.post_sentiment,
            creator: {
              id: item.creator_id,
              name: item.creator_name,
              displayName: item.creator_display_name,
              followers: item.creator_followers,
              avatar: item.creator_avatar,
            },
            interactions: {
              last24h: item.interactions_24h,
              total: item.interactions_total,
            },
          }));
        } catch (error) {
          console.error("Error fetching topic news:", error);
          return "Failed to fetch news data";
        }
      },
    };

    // Create async function from the code
    const AsyncFunction = Object.getPrototypeOf(
      async function () {}
    ).constructor;
    const fn = new AsyncFunction(
      ...Object.keys(context),
      `
      try {
        ${cleanCode}
      } catch (error) {
        console.error('Error in executed code:', error);
        throw error;
      }
    `
    );

    // Execute the function with the context
    const result = await fn(...Object.values(context));
    return result;
  } catch (error) {
    console.error("Error executing code:", error);
    throw new Error(`Code execution failed: ${error.message}`);
  }
};
