data_examples = [
"""
USER QUERY: 
Create an agent that talks about the top ReFi projects and gives a buy or sell rating about the same and help the user answer questions about different ReFi projects.


MASTER LLM OUTPUT:
  - Agent Bio & Naming:
    - Proposed Name: "ReFi Alpha"
    - Bio: ReFi Alpha is a state-of-the-art AI analyst that delivers comprehensive insights into the top 5 Regenerative Finance (ReFi) projects in crypto. Combining advanced market analytics, social sentiment tracking, and on-chain data examination, ReFi Alpha empowers investors with actionable, reliable buy/sell recommendations. Focused on sustainability and innovation, it transforms complex data into clear, strategic insights for optimal decision-making.

  - High-Level Execution Plan:
    1. Identification Phase:
        - Recognize that “ReFi” is a niche topic not covered in the predefined sectors.
        - Specify that the Data Agent must use the LunarCrush Topics API solely for identifying the top 5 ReFi coins (identification-only).
    2. Data Retrieval Phase:
        - Once the coins are identified, instruct the Data Agent to collect detailed market and on-chain data via the Mobula API.
        - Retrieve social sentiment data using the LunarCrush Coin V1 API.
    3. Analysis Phase:
        - Direct the Analysis Agent to integrate these data streams to generate comprehensive insights and actionable recommendations.

  - Rationale & Chain-of-Thought:
    - Isolating the identification step is critical because ReFi isn’t a predefined sector.
    - Using distinct APIs ensures that each agent specializes—one for identifying coins and the other for gathering detailed data—avoiding redundancy.

  - Execution Flow Overview:
    - The plan flows as follows: Query assessment → Identification (via LunarCrush Topics API) → Data retrieval (via Mobula and LunarCrush Coin V1) → Analysis synthesis.

OUTPUT:
    
DATA AGENT CHAIN-OF-THOUGHT:
- The query requires an in-depth analysis of the top 5 ReFi projects, including buy/sell ratings.
- Since “ReFi” is a niche topic and not part of the predefined sectors, I must first identify the relevant coins using the LunarCrush Topics API.
- In this identification step, only coin symbols (e.g., "REFA", "REFB", "REFC", "REFD", "REFE") should be used—not asset names, addresses, or IDs.
- After identification, I need to generate nested API calls:
  - A Mobula API call (using `/market/multi-data`) to fetch detailed market and on-chain data for these coins.
  - Individual LunarCrush Coins v1 API calls to fetch social sentiment for each coin.
- This approach aligns with the Master LLM’s suggestion but is tailored to my role: output only the API call structure and my reasoning for data retrieval.


FINAL API CALL STRUCTURE:
[
  {
    "provider": "lunarcrush",
    "endpoint": "/public/topic/refi/v1",
    "description": "Identify trending topics related to ReFi and extract the top 5 ReFi coin symbols (identification-only).",
    "nested_calls": [
      {
        "provider": "mobula",
        "endpoint": "/market/multi-data?symbols=REFA,REFB,REFC,REFD,REFE",
        "description": "Retrieve detailed market and on-chain data for the identified ReFi coins using their symbols."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/REFA/v1",
        "description": "Retrieve social sentiment data for coin REFA."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/REFB/v1",
        "description": "Retrieve social sentiment data for coin REFB."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/REFC/v1",
        "description": "Retrieve social sentiment data for coin REFC."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/REFD/v1",
        "description": "Retrieve social sentiment data for coin REFD."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/REFE/v1",
        "description": "Retrieve social sentiment data for coin REFE."
      }
    ]
  }
]

""",
"""
USER QUERY:
Give me the latest news updates on Ethereum, Arbitrum, Injective, and Stacks.


MASTER LLM OUTPUT :
  - Agent Bio & Naming:
    - Proposed Name: "NewsFi"
    - Bio: NewsFi is a cutting-edge AI analyst engineered for rapid aggregation and deep analysis of cryptocurrency news. It meticulously filters through vast amounts of data to extract crucial headlines, regulatory developments, and market shifts for coins like Ethereum, Arbitrum, Injective, and Stacks. By integrating real-time news with social sentiment analytics, NewsFi delivers clear, actionable insights that keep users informed and ahead of market trends.

  - High-Level Execution Plan:
    1. Query Assessment:
        - Identify that the query is coin-specific and centers on retrieving the latest news and social sentiment.
    2. Data Retrieval Phase:
        - Direct the Data Agent to fetch the latest news updates for each specified coin using the appropriate LunarCrush news endpoints.
    3. Analysis Phase:
        - Instruct the Analysis Agent to distill and synthesize the news data, identifying key trends and correlating them with market sentiment.

  - Rationale & Chain-of-Thought:
    - Direct coin queries bypass the need for an identification phase, enabling a streamlined approach.
    - This focused strategy ensures that news aggregation is current and precisely targeted for each coin.

  - Execution Flow Overview:
    - The execution flow: Query assessment → Direct news retrieval via LunarCrush → Analysis and summarization.

    
OUTPUT:

DATA AGENT CHAIN-OF-THOUGHT:
- The query requires fetching the latest news updates and social sentiment for four specified coins.
- Since the query is coin-specific, there is no need for an identification phase; I will directly use the coin symbols.
- It is critical to use coin symbols exclusively: Ethereum (ETH), Arbitrum (ARB), Injective (INJ), and Stacks (STX) — never asset names, addresses, or IDs.
- I will construct individual API calls for each coin using the appropriate LunarCrush news endpoint.
- This approach follows the Master LLM suggestion as guidance while ensuring my role is strictly limited to orchestrating the API calls.


FINAL API CALL STRUCTURE:
[
  {
    "provider": "lunarcrush",
    "endpoint": "/public/news/ETH/v1",
    "description": "Retrieve the latest news updates and social sentiment for Ethereum (ETH)."
  },
  {
    "provider": "lunarcrush",
    "endpoint": "/public/news/ARB/v1",
    "description": "Retrieve the latest news updates and social sentiment for Arbitrum (ARB)."
  },
  {
    "provider": "lunarcrush",
    "endpoint": "/public/news/INJ/v1",
    "description": "Retrieve the latest news updates and social sentiment for Injective (INJ)."
  },
  {
    "provider": "lunarcrush",
    "endpoint": "/public/news/STX/v1",
    "description": "Retrieve the latest news updates and social sentiment for Stacks (STX)."
  }
]
""",
"""
USER QUERY:
What are the top projects on Polygon right now?


MASTER LLM OUTPUT:
- Agent Bio & Naming:
  - Proposed Name: "PolygonTrend"
  - Bio: PolygonTrend is an advanced AI analyst specializing in the dynamic ecosystem of the Polygon blockchain. By fusing real-time market data, on-chain activity, and social engagement metrics, PolygonTrend identifies the most promising projects with rising momentum. Its analytical prowess enables users to understand liquidity, trading volumes, and network interactions, ensuring a clear picture of Polygon’s top projects and growth potential.

- High-Level Execution Plan:
  1. Query Assessment:
      - Recognize that the query is blockchain-specific (Polygon) and that Polygon is not part of the predefined LunarCrush sectors.
  2. Data Retrieval Phase:
      - Instruct the Data Agent to use the Mobula Blockchain Pairs API exclusively to identify the top projects on Polygon based on the most-appropriate
  3. Analysis Phase:
      - Direct the Analysis Agent to rank these projects based on metrics such as trading volume, liquidity, and on-chain interactions.

- Rationale & Chain-of-Thought:
  - For blockchain-specific queries outside of predefined sectors, relying solely on Mobula avoids data redundancy.
  - A clear, linear process ensures targeted data retrieval and accurate project ranking.

- Execution Flow Overview:
  - The process flows as follows: Query assessment → Data retrieval via Mobula → Analysis and ranking.

OUTPUT:

DATA AGENT CHAIN-OF-THOUGHT:
- The query demands an analysis of trending projects on Polygon, which requires both identification and detailed data retrieval.
- Polygon is not part of the predefined LunarCrush sectors; thus, I must use the Mobula Blockchain Pairs API to first identify the relevant projects.
- The query implies that projects should be sorted by a key metric (e.g., trading volume). I will incorporate a sorting parameter (defaulting to trading volume) in the API call.
- After identification, I will fetch detailed data using:
  - The LunarCrush Coins v1 API to gather social sentiment and market details for each project (using coin symbols exclusively).
  - The Mobula Multi-Market API to obtain comprehensive market metrics.
- This structured, two-step approach ensures precision and avoids redundant calls.


FINAL API CALL STRUCTURE:
[
  {
    "provider": "mobula",
    "endpoint": "/market/blockchain/pairs?blockchain=Polygon&sortBy=volume_5min&sortOrder=desc",
    "description": "Retrieve a list of trending projects on the Polygon blockchain, sorted by trading volume (or the most relevant metric inferred from the query).",
    "nested_calls": [
      {
        "provider": "mobula",
        "endpoint": "/market/multi-data?symbols=coin1,coin2,coin3",
        "description": "Retrieve comprehensive market metrics for the identified projects using their coin symbols."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin1/v1",
        "description": "Retrieve detailed social sentiment data for coin1."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin2/v1",
        "description": "Retrieve detailed social sentiment data for coin1."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin3/v1",
        "description": "Retrieve detailed social sentiment data for coin3."
      }
    ]
  }
]
""",
"""
USER QUERY:
Give me a detailed analysis of the DeSci (Decentralized Science) sector in crypto.


MASTER LLM OUTPUT:
- Agent Bio & Naming:
  - Proposed Name: "DeSciVision"
  - Bio: DeSciVision is a pioneering AI analyst that delves into the innovative realm of Decentralized Science (DeSci). It excels in examining funding trends, project innovation, and community sentiment within the DeSci ecosystem. By leveraging advanced market analytics and real-time social data, DeSciVision offers comprehensive insights into how blockchain is revolutionizing scientific research and collaboration, guiding stakeholders with data-driven perspectives.

- High-Level Execution Plan:
  1. Query Assessment:
      - Recognize that DeSci is a predefined sector within LunarCrush.
  2. Data Retrieval Phase:
      - Instruct the Data Agent to retrieve sector-specific data (coins, posts, and news) using the LunarCrush Coins V2 API, filtered to DeSci.
      - Supplement this with detailed market data via the Mobula API.
  3. Analysis Phase:
      - Direct the Analysis Agent to integrate market, social, and news data to produce a thorough analysis, highlighting trends, risks, and opportunities in the DeSci sector.

- Rationale & Chain-of-Thought:
  - Leveraging predefined sector endpoints enhances efficiency and accuracy.
  - Separating social/news data (via LunarCrush) from market data (via Mobula) ensures a robust, multidimensional analysis.

- Execution Flow Overview:
  - The blueprint is: Query assessment → Data retrieval (using LunarCrush Sector API & Mobula API) → Data synthesis and comprehensive analysis.

OUTPUT:

DATA AGENT CHAIN-OF-THOUGHT:
- The query targets a predefined sector: DeSci.
- I will use the LunarCrush Coins V2 API to identify the top coins related to DeSci as well as their social metrics.
- Supplement this with detailed market and on-chain metrics via the Mobula API for the identified coins.
- Remember: Use coin symbols only.
- This approach ensures efficiency by leveraging predefined sector endpoints without requiring an identification phase.


FINAL API CALL STRUCTURE:
[
  {
    "provider": "lunarcrush",
    "endpoint": "/public/coins/list/v2?filter=DeSci",
    "description": "Retrieve coins, posts, and news related to the DeSci sector using coin symbols.",
    nested_calls: [
      {
        "provider": "mobula",
        "endpoint": "/market/multi-data?symbols=coin1,coin2,coin3",
        "description": "Retrieve detailed market and on-chain data for the identified DeSci coins."
      }
    ],
  }
]
""",
"""
USER QUERY:
Provide an analysis of the latest trends in both the NFTs and DeFi sectors.


MASTER LLM BLUEPRINT OUTPUT:
- Agent Bio & Naming:
- Proposed Name: "TrendFusion"
- Bio: TrendFusion is an innovative AI analyst that seamlessly integrates insights from both the NFTs and DeFi sectors. It excels at capturing and comparing trends across these distinct domains, delivering a unified perspective on market dynamics, social sentiment, and on-chain activity for enhanced strategic decision-making.

- High-Level Execution Plan:
1. Query Assessment:
   - Identify that the query targets two distinct, predefined sectors: NFTs and DeFi.
   - Since both sectors are predefined, there is no need for identification APIs.
2. Data Retrieval Phase:
   - Instruct the Data Agent to retrieve sector-specific data (coins, posts, and news) for NFTs and DeFi using the LunarCrush Sector API.
   - Supplement with relevant market data from the Mobula API if necessary.
3. Analysis Phase:
   - Direct the Analysis Agent to independently analyze the data from each sector and then synthesize comparative insights to highlight similarities, differences, and overall trends.

- Rationale & Chain-of-Thought:
- Handling multi-sector queries requires parallel processing to ensure clear and distinct data streams for each sector.
- This separation allows for accurate comparative analysis and prevents data conflation, ensuring robust insights.

- Execution Flow Overview:
- The process flows as follows: Query assessment → Retrieve data for NFTs and DeFi separately → Synthesize and compare insights.


OUTPUT:

DATA AGENT CHAIN-OF-THOUGHT:

1. **Query Assessment**:
   - The user query requests an analysis of trends in the NFTs and DeFi sectors.
   - Both NFTs and DeFi are predefined sectors in the available resources, so there is no need to use identification APIs.

2. **Data Retrieval Phase**:
   - Use the LunarCrush Coins v2 API to retrieve sector-specific data for both NFTs and DeFi. This includes coins, posts, and news related to each sector.
   - Supplement the data with detailed market and on-chain metrics from the Mobula API for the identified coins in each sector.

3. **Analysis Phase**:
   - The Analysis Agent will independently analyze the data from each sector.
   - Comparative insights will be synthesized to highlight similarities, differences, and overall trends between the NFTs and DeFi sectors.

4. **Rationale & Execution Flow**:
   - By handling the NFTs and DeFi sectors separately, we ensure clear and distinct data streams, which allows for accurate comparative analysis.
   - This approach prevents data conflation and ensures robust insights, aligning with the Master LLM's blueprint for handling multi-sector queries.

   
FINAL API CALL STRUCTURE:
[
  {
    "provider": "lunarcrush",
    "endpoint": "/public/coins/list/v2?filter=NFT",
    "description": "Retrieve coins, posts, and news related to the NFT sector using coin symbols.",
    "nested_calls": [
      {
        "provider": "mobula",
        "endpoint": "/market/multi-data?symbols=coin1,coin2,coin3",
        "description": "Retrieve detailed market and on-chain data for the identified NFT coins."
      }
    ]
  },
  {
    "provider": "lunarcrush",
    "endpoint": "/public/coins/list/v2?filter=DeFi",
    "description": "Retrieve coins, posts, and news related to the DeFi sector using coin symbols.",
    "nested_calls": [
      {
        "provider": "mobula",
        "endpoint": "/market/multi-data?symbols=coin4,coin5,coin6",
        "description": "Retrieve detailed market and on-chain data for the identified DeFi coins."
      }
    ]
  }
]
""",
"""
    USER QUERY:
    Give me a historical trend analysis of Bitcoin over the past 5 years.

    
    MASTER LLM BLUEPRINT OUTPUT:
    - Agent Bio & Naming:
      - Proposed Name: "BitcoinHistorian"
      - Bio: BitcoinHistorian is a seasoned AI analyst specializing in long-term trend analysis. With deep expertise in examining historical market data and correlating trends with key events, BitcoinHistorian provides a comprehensive perspective on Bitcoin’s evolution and future potential.

    - High-Level Execution Plan:
      1. Query Assessment:
         - Recognize that the query is coin-specific and requires an analysis of historical trends spanning 5 years.
      2. Data Retrieval Phase:
         - Direct the Data Agent to retrieve historical time-series market data for Bitcoin using Mobula and/or LunarCrush time-series endpoints.
         - Instruct retrieval of historical social sentiment data, if available, to provide contextual insights.
      3. Analysis Phase:
         - Direct the Analysis Agent to conduct a detailed trend analysis, correlating market data with major historical events and shifts in community sentiment.
         - Emphasize the identification of long-term trends, cycles, and potential catalysts for future movements.

    - Rationale & Chain-of-Thought:
      - Historical analysis demands robust, continuous data and careful correlation with past events.
      - This approach ensures that trends are interpreted within a broader historical context, yielding reliable insights.

    - Execution Flow Overview:
      - The blueprint is: Query assessment → Retrieve historical market and sentiment data → Perform trend analysis and event correlation.

      OUTPUT:

      DATA AGENT CHAIN-OF-THOUGHT:
      1. **Query Assessment**:
         - The user query is specific to Bitcoin and requires a historical trend analysis over a 5-year period.
         - The analysis should include both market data and social sentiment to provide a comprehensive view.

      2. **Data Retrieval Phase**:
         - **Market Data**: Use the LunarCrush `/public/coins/BTC/time-series/v2` endpoint to fetch historical market data for Bitcoin. This endpoint provides both market and social data, which is ideal for a comprehensive analysis.
         - **Social Sentiment**: The same LunarCrush endpoint will also provide historical social sentiment data, which is crucial for understanding community trends and reactions over time.
         - **Supplementary Market Data**: Use the Mobula `/market/history` endpoint to ensure a robust dataset by retrieving additional historical market metrics for Bitcoin. This will help in cross-verifying data and providing a more detailed analysis.

      3. **Parameters**:
         - For LunarCrush, set the `bucket` to "day" to aggregate data daily, and use the `interval` "all" to cover the entire 5-year period.
         - For Mobula, specify the `from` and `to` timestamps to cover the 5-year period from January 1, 2018, to January 1, 2023, with a `period` of "1h" for detailed hourly data.

      4. **Analysis Phase**:
         - The Analysis Agent will use the retrieved data to conduct a detailed trend analysis, correlating market data with major historical events and shifts in community sentiment.
         - The focus will be on identifying long-term trends, cycles, and potential catalysts for future movements.

      This structured approach ensures that the analysis is comprehensive, leveraging both market and social data to provide a holistic view of Bitcoin's historical trends.

      
      FINAL API CALL STRUCTURE:
      [
         {
            "provider": "lunarcrush",
            "endpoint": "/public/coins/BTC/time-series/v2",
            "description": "Retrieve historical market and social data for Bitcoin over the past 5 years.",
            "parameters": {
               "coin": "BTC",
               "bucket": "day",
               "interval": "all"
            }
         },
         {
            "provider": "mobula",
            "endpoint": "/market/history",
            "description": "Retrieve historical market metrics for Bitcoin over the past 5 years.",
            "parameters": {
               "asset": "Bitcoin",
               "from": "1514764800000",  // January 1, 2018, in milliseconds
               "to": "1704067200000",    // January 1, 2023, in milliseconds
               "period": "1h"
            }
         }
      ]
      """
    ,
    """
USER QUERY:
Provide a detailed analysis of the wallet portfolio for wallet address 0xABC123XYZ.


MASTER LLM OUTPUT:
- Proposed Name: "PortfolioPulse"
- Bio: PortfolioPulse is a cutting-edge AI analyst dedicated to in-depth wallet portfolio analysis. It excels at assessing asset distribution, market valuations, and historical performance to deliver a clear, actionable overview of a wallet's crypto holdings.

- High-Level Execution Plan:
  1. Query Assessment:
      - Recognize that the query is wallet-specific, focusing on detailed portfolio analysis for a given wallet address.
      - Note that the analysis should include current holdings and, optionally, historical trends.
  2. Data Retrieval Phase:
      - Instruct the Data Agent to retrieve current wallet portfolio data using Mobula’s Wallet Explorer API (e.g., /wallet/portfolio endpoint).
      - Optionally, specify the retrieval of historical balance data (/wallet/history) or transaction counts (/warehouse/wallet-transactions-count) for added context.
  3. Analysis Phase:
      - Direct the Analysis Agent to integrate the portfolio data with current market metrics from the Mobula Market API.
      - Instruct the Analysis Agent to analyze asset distribution, overall valuation, and historical trends.
      - If data is insufficient, mandate that the Analysis Agent clearly state: "Insufficient data available for reliable insights."

- Rationale & Chain-of-Thought:
  - Wallet analysis requires a specialized approach, distinct from coin or sector analysis.
  - Leveraging the Mobula Wallet Explorer API ensures detailed retrieval of portfolio information, while supplementary data enhances context.
  - Transparent handling of data limitations is essential to maintain analytical integrity.

- Execution Flow Overview:
  - The blueprint outlines: Query assessment → Retrieve wallet portfolio (and supplementary) data via Mobula → Integrate market data → Synthesize a comprehensive wallet analysis.

OUTPUT:

DATA AGENT CHAIN-OF-THOUGHT:
- The query is wallet-specific and requires detailed portfolio analysis.
- I will use the Mobula Wallet Explorer API to retrieve current portfolio data for the given wallet address.
- Additionally, if required, I will supplement this with historical balance data using the Mobula Wallet History endpoint.
- This ensures a comprehensive view of the wallet's holdings and trends over time.
- The wallet address is provided directly; however, coin symbols should still be used when fetching coin-specific data.


FINAL API CALL STRUCTURE:
[
  {
    "provider": "mobula",
    "endpoint": "/wallet/portfolio?wallet=0xABC123XYZ",
    "description": "Retrieve current portfolio holdings for wallet address 0xABC123XYZ."
  },
  {
    "provider": "mobula",
    "endpoint": "/wallet/history?wallet=0xABC123XYZ",
    "description": "Retrieve historical balance data for wallet address 0xABC123XYZ for additional context."
  }
]
    """,

    """
USER QUERY:
Provide a comprehensive analysis of trending projects in crypto.


MASTER LLM OUTPUT :
- Proposed Name: "MarketMaven"
- Bio: MarketMaven is a visionary AI analyst specializing in the analysis of trending crypto projects. It leverages advanced market analytics and real-time social sentiment data to identify emerging trends and evaluate project performance. By integrating insights from both LunarCrush and Mobula APIs, MarketMaven empowers users with actionable intelligence to navigate the dynamic crypto landscape.

- High-Level Execution Plan:
  1. Query Assessment:
     - Recognize that the query targets trending projects across the entire crypto market, necessitating a broad, integrated view.
     - Identify that the LunarCrush Coins v2 API is ideal for capturing a comprehensive snapshot of trending projects (via aggregated market cap, social engagement, and trading volume metrics).
     - Note: For detailed individual project analysis, LunarCrush Coin v1 can be used; however, the focus here is on market-wide trends.
  2. Data Retrieval Phase:
     - Instruct the Data Agent to use the LunarCrush Coins v2 API to retrieve a full list of trending projects, ensuring the API call is filtered and sorted based on user-specified criteria (e.g., highest social engagement, market cap, or trading volume).
     - Additionally, direct the Data Agent to supplement this data with detailed market metrics from the Mobula API to capture trading dynamics, liquidity, and on-chain activity.
  3. Analysis Phase:
     - Direct the Analysis Agent to synthesize the aggregated data into a comprehensive report.
     - The report should identify key trending projects, highlight emerging market trends, and evaluate overall market sentiment, thereby providing a holistic view of the crypto market.
  
- Rationale & Chain-of-Thought:
  - Utilizing the LunarCrush Coins v2 API as the identifier ensures broad coverage of trending projects across the market.
  - Integrating supplementary data from Mobula deepens the analysis by adding insights into trading volumes, liquidity, and on-chain behavior.
  - Filtering and sorting the data according to user-defined parameters focuses the analysis on the most significant projects, reducing noise and enhancing actionable insights.
  
- Execution Flow Overview:
  - The blueprint flows as follows: Query assessment → Retrieve trending projects using LunarCrush Coins v2 (filtered/sorted as per criteria) + Supplement with Mobula market data → Synthesize and deliver a comprehensive analysis of trending crypto projects.

OUTPUT:

DATA AGENT CHAIN-OF-THOUGHT:
- The query requires an analysis of trending projects across the entire crypto market.
- I will use the LunarCrush Coins v2 API as an identifier to fetch a comprehensive snapshot of trending projects, filtered and sorted according to user criteria (e.g., highest social engagement or market cap).
- Since this endpoint provides a market-wide view, I must ensure only coin symbols are used.
- Then, I will supplement the identified projects with detailed market metrics from the Mobula Multi-Market API and detailed social sentiment data via the LunarCrush Coins v1 API.
- This two-step approach ensures robust identification followed by comprehensive data retrieval.

FINAL API CALL STRUCTURE:
[
  {
    "provider": "lunarcrush",
    "endpoint": "/public/coins/list/v2?sort=alt_rank&desc=true",
    "description": "Retrieve a broad snapshot of trending crypto projects, sorted by AltRank (or another key metric), using coin symbols exclusively.",
    "nested_calls": [
      {
        "provider": "mobula",
        "endpoint": "/market/multi-data?symbols=coin1,coin2,coin3,coin4,coin5",
        "description": "Retrieve detailed market and on-chain data for the identified trending projects using their coin symbols."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin1/v1",
        "description": "Retrieve detailed social sentiment data for project coin1."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin2/v1",
        "description": "Retrieve detailed social sentiment data for project coin2."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin3/v1",
        "description": "Retrieve detailed social sentiment data for project coin3."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin4/v1",
        "description": "Retrieve detailed social sentiment data for project coin4."
      },
      {
        "provider": "lunarcrush",
        "endpoint": "/public/coins/coin5/v1",
        "description": "Retrieve detailed social sentiment data for project coin5."
      }
    ]
  }
]
    """
]

master_example_output = [
    # Example 1 – In-Depth Analysis of Top 5 ReFi Agents
    """
    USER QUERY:
    Give me in-depth analysis of the top 5 ReFi agents in the market.

    MASTER LLM BLUEPRINT OUTPUT:

    - Agent Bio & Naming:
      - Proposed Name: "ReFi Alpha"
      - Bio: ReFi Alpha is a state-of-the-art AI analyst that delivers comprehensive insights into the top 5 Regenerative Finance (ReFi) projects in crypto. Combining advanced market analytics, social sentiment tracking, and on-chain data examination, ReFi Alpha empowers investors with actionable, reliable buy/sell recommendations. Focused on sustainability and innovation, it transforms complex data into clear, strategic insights for optimal decision-making.

    - High-Level Execution Plan:
      1. Identification Phase:
         - Recognize that “ReFi” is a niche topic not covered in the predefined sectors.
         - Specify that the Data Agent must use the LunarCrush Topics API solely for identifying the top 5 ReFi coins (identification-only).
      2. Data Retrieval Phase:
         - Once the coins are identified, instruct the Data Agent to collect detailed market and on-chain data via the Mobula API.
         - Retrieve social sentiment data using the LunarCrush Coin V1 API.
      3. Analysis Phase:
         - Direct the Analysis Agent to integrate these data streams to generate comprehensive insights and actionable recommendations.

    - Rationale & Chain-of-Thought:
      - Isolating the identification step is critical because ReFi isn’t a predefined sector.
      - Using distinct APIs ensures that each agent specializes—one for identifying coins and the other for gathering detailed data—avoiding redundancy.

    - Execution Flow Overview:
      - The plan flows as follows: Query assessment → Identification (via LunarCrush Topics API) → Data retrieval (via Mobula and LunarCrush Coin V1) → Analysis synthesis.
    """,

    # Example 2 – Latest News Updates on Specific Coins
    """
    USER QUERY:
    Give me the latest news updates on Ethereum, Arbitrum, Injective, and Stacks.

    MASTER LLM BLUEPRINT OUTPUT:

    - Agent Bio & Naming:
      - Proposed Name: "NewsFi"
      - Bio: NewsFi is a cutting-edge AI analyst engineered for rapid aggregation and deep analysis of cryptocurrency news. It meticulously filters through vast amounts of data to extract crucial headlines, regulatory developments, and market shifts for coins like Ethereum, Arbitrum, Injective, and Stacks. By integrating real-time news with social sentiment analytics, NewsFi delivers clear, actionable insights that keep users informed and ahead of market trends.

    - High-Level Execution Plan:
      1. Query Assessment:
         - Identify that the query is coin-specific and centers on retrieving the latest news and social sentiment.
      2. Data Retrieval Phase:
         - Direct the Data Agent to fetch the latest news updates for each specified coin using the appropriate LunarCrush news endpoints.
      3. Analysis Phase:
         - Instruct the Analysis Agent to distill and synthesize the news data, identifying key trends and correlating them with market sentiment.

    - Rationale & Chain-of-Thought:
      - Direct coin queries bypass the need for an identification phase, enabling a streamlined approach.
      - This focused strategy ensures that news aggregation is current and precisely targeted for each coin.

    - Execution Flow Overview:
      - The execution flow: Query assessment → Direct news retrieval via LunarCrush → Analysis and summarization.
    """,

    # Example 3 – Top Projects on Polygon
    """
    USER QUERY:
    What are the top projects on Polygon right now?

    MASTER LLM BLUEPRINT OUTPUT:

    - Agent Bio & Naming:
      - Proposed Name: "PolygonTrend"
      - Bio: PolygonTrend is an advanced AI analyst specializing in the dynamic ecosystem of the Polygon blockchain. By fusing real-time market data, on-chain activity, and social engagement metrics, PolygonTrend identifies the most promising projects with rising momentum. Its analytical prowess enables users to understand liquidity, trading volumes, and network interactions, ensuring a clear picture of Polygon’s top projects and growth potential.

    - High-Level Execution Plan:
      1. Query Assessment:
         - Recognize that the query is blockchain-specific (Polygon) and that Polygon is not part of the predefined LunarCrush sectors.
      2. Data Retrieval Phase:
         - Instruct the Data Agent to use the Mobula Blockchain Pairs API exclusively to identify the top projects on Polygon based on the most-appropriate
      3. Analysis Phase:
         - Direct the Analysis Agent to rank these projects based on metrics such as trading volume, liquidity, and on-chain interactions.

    - Rationale & Chain-of-Thought:
      - For blockchain-specific queries outside of predefined sectors, relying solely on Mobula avoids data redundancy.
      - A clear, linear process ensures targeted data retrieval and accurate project ranking.

    - Execution Flow Overview:
      - The process flows as follows: Query assessment → Data retrieval via Mobula → Analysis and ranking.
    """,

    # Example 4 – Detailed Analysis of the DeSci Sector
    """
    USER QUERY:
    Give me a detailed analysis of the DeSci (Decentralized Science) sector in crypto.

    MASTER LLM BLUEPRINT OUTPUT:

    - Agent Bio & Naming:
      - Proposed Name: "DeSciVision"
      - Bio: DeSciVision is a pioneering AI analyst that delves into the innovative realm of Decentralized Science (DeSci). It excels in examining funding trends, project innovation, and community sentiment within the DeSci ecosystem. By leveraging advanced market analytics and real-time social data, DeSciVision offers comprehensive insights into how blockchain is revolutionizing scientific research and collaboration, guiding stakeholders with data-driven perspectives.

    - High-Level Execution Plan:
      1. Query Assessment:
         - Recognize that DeSci is a predefined sector within LunarCrush.
      2. Data Retrieval Phase:
         - Instruct the Data Agent to retrieve sector-specific data (coins, posts, and news) using the LunarCrush Sector API.
         - Supplement this with detailed market data via the Mobula API.
      3. Analysis Phase:
         - Direct the Analysis Agent to integrate market, social, and news data to produce a thorough analysis, highlighting trends, risks, and opportunities in the DeSci sector.

    - Rationale & Chain-of-Thought:
      - Leveraging predefined sector endpoints enhances efficiency and accuracy.
      - Separating social/news data (via LunarCrush) from market data (via Mobula) ensures a robust, multidimensional analysis.

    - Execution Flow Overview:
      - The blueprint is: Query assessment → Data retrieval (using LunarCrush Sector API & Mobula API) → Data synthesis and comprehensive analysis.
    """,
    
        # Example 5 – Multi-Sector Query: NFTs and DeFi
    """
    USER QUERY:
    Provide an analysis of the latest trends in both the NFTs and DeFi sectors.

    MASTER LLM BLUEPRINT OUTPUT:

    - Agent Bio & Naming:
      - Proposed Name: "TrendFusion"
      - Bio: TrendFusion is an innovative AI analyst that seamlessly integrates insights from both the NFTs and DeFi sectors. It excels at capturing and comparing trends across these distinct domains, delivering a unified perspective on market dynamics, social sentiment, and on-chain activity for enhanced strategic decision-making.

    - High-Level Execution Plan:
      1. Query Assessment:
         - Identify that the query targets two distinct, predefined sectors: NFTs and DeFi.
         - Since both sectors are predefined, there is no need for identification APIs.
      2. Data Retrieval Phase:
         - Instruct the Data Agent to retrieve sector-specific data (coins, posts, and news) for NFTs and DeFi using the LunarCrush Sector API.
         - Supplement with relevant market data from the Mobula API if necessary.
      3. Analysis Phase:
         - Direct the Analysis Agent to independently analyze the data from each sector and then synthesize comparative insights to highlight similarities, differences, and overall trends.

    - Rationale & Chain-of-Thought:
      - Handling multi-sector queries requires parallel processing to ensure clear and distinct data streams for each sector.
      - This separation allows for accurate comparative analysis and prevents data conflation, ensuring robust insights.

    - Execution Flow Overview:
      - The process flows as follows: Query assessment → Retrieve data for NFTs and DeFi separately → Synthesize and compare insights.
    """,

    # Example 6 – Historical Analysis of Bitcoin
    """
    USER QUERY:
    Give me a historical trend analysis of Bitcoin over the past 5 years.

    MASTER LLM BLUEPRINT OUTPUT:

    - Agent Bio & Naming:
      - Proposed Name: "BitcoinHistorian"
      - Bio: BitcoinHistorian is a seasoned AI analyst specializing in long-term trend analysis. With deep expertise in examining historical market data and correlating trends with key events, BitcoinHistorian provides a comprehensive perspective on Bitcoin’s evolution and future potential.

    - High-Level Execution Plan:
      1. Query Assessment:
         - Recognize that the query is coin-specific and requires an analysis of historical trends spanning 5 years.
      2. Data Retrieval Phase:
         - Direct the Data Agent to retrieve historical time-series market data for Bitcoin using Mobula and/or LunarCrush time-series endpoints.
         - Instruct retrieval of historical social sentiment data, if available, to provide contextual insights.
      3. Analysis Phase:
         - Direct the Analysis Agent to conduct a detailed trend analysis, correlating market data with major historical events and shifts in community sentiment.
         - Emphasize the identification of long-term trends, cycles, and potential catalysts for future movements.

    - Rationale & Chain-of-Thought:
      - Historical analysis demands robust, continuous data and careful correlation with past events.
      - This approach ensures that trends are interpreted within a broader historical context, yielding reliable insights.

    - Execution Flow Overview:
      - The blueprint is: Query assessment → Retrieve historical market and sentiment data → Perform trend analysis and event correlation.
    """,

    # Example 7 – Wallet Portfolio Analysis via Mobula's Wallet Explorer API
    """
    USER QUERY:
    Provide a detailed analysis of the wallet portfolio for wallet address 0xABC123XYZ.

    MASTER LLM BLUEPRINT OUTPUT:

    - Agent Bio & Naming:
      - Proposed Name: "PortfolioPulse"
      - Bio: PortfolioPulse is a cutting-edge AI analyst dedicated to in-depth wallet portfolio analysis. It excels at assessing asset distribution, market valuations, and historical performance to deliver a clear, actionable overview of a wallet's crypto holdings.

    - High-Level Execution Plan:
      1. Query Assessment:
         - Recognize that the query is wallet-specific, focusing on detailed portfolio analysis for a given wallet address.
         - Note that the analysis should include current holdings and, optionally, historical trends.
      2. Data Retrieval Phase:
         - Instruct the Data Agent to retrieve current wallet portfolio data using Mobula’s Wallet Explorer API (e.g., /wallet/portfolio endpoint).
         - Optionally, specify the retrieval of historical balance data (/wallet/history) or transaction counts (/warehouse/wallet-transactions-count) for added context.
      3. Analysis Phase:
         - Direct the Analysis Agent to integrate the portfolio data with current market metrics from the Mobula Market API.
         - Instruct the Analysis Agent to analyze asset distribution, overall valuation, and historical trends.
         - If data is insufficient, mandate that the Analysis Agent clearly state: "Insufficient data available for reliable insights."
    
    - Rationale & Chain-of-Thought:
      - Wallet analysis requires a specialized approach, distinct from coin or sector analysis.
      - Leveraging the Mobula Wallet Explorer API ensures detailed retrieval of portfolio information, while supplementary data enhances context.
      - Transparent handling of data limitations is essential to maintain analytical integrity.

    - Execution Flow Overview:
      - The blueprint outlines: Query assessment → Retrieve wallet portfolio (and supplementary) data via Mobula → Integrate market data → Synthesize a comprehensive wallet analysis.
    """,
    """
USER QUERY:
Provide a comprehensive analysis of trending projects in crypto.

MASTER LLM BLUEPRINT OUTPUT:

- Agent Bio & Naming:
  - Proposed Name: "MarketMaven"
  - Bio: MarketMaven is a visionary AI analyst specializing in the analysis of trending crypto projects. It leverages advanced market analytics and real-time social sentiment data to identify emerging trends and evaluate project performance. By integrating insights from both LunarCrush and Mobula APIs, MarketMaven empowers users with actionable intelligence to navigate the dynamic crypto landscape.

- High-Level Execution Plan:
  1. Query Assessment:
     - Recognize that the query targets trending projects across the entire crypto market, necessitating a broad, integrated view.
     - Identify that the LunarCrush Coins v2 API is ideal for capturing a comprehensive snapshot of trending projects (via aggregated market cap, social engagement, and trading volume metrics).
     - Note: For detailed individual project analysis, LunarCrush Coin v1 can be used; however, the focus here is on market-wide trends.
  2. Data Retrieval Phase:
     - Instruct the Data Agent to use the LunarCrush Coins v2 API to retrieve a full list of trending projects, ensuring the API call is filtered and sorted based on user-specified criteria (e.g., highest social engagement, market cap, or trading volume).
     - Additionally, direct the Data Agent to supplement this data with detailed market metrics from the Mobula API to capture trading dynamics, liquidity, and on-chain activity.
  3. Analysis Phase:
     - Direct the Analysis Agent to synthesize the aggregated data into a comprehensive report.
     - The report should identify key trending projects, highlight emerging market trends, and evaluate overall market sentiment, thereby providing a holistic view of the crypto market.
  
- Rationale & Chain-of-Thought:
  - Utilizing the LunarCrush Coins v2 API as the identifier ensures broad coverage of trending projects across the market.
  - Integrating supplementary data from Mobula deepens the analysis by adding insights into trading volumes, liquidity, and on-chain behavior.
  - Filtering and sorting the data according to user-defined parameters focuses the analysis on the most significant projects, reducing noise and enhancing actionable insights.
  
- Execution Flow Overview:
  - The blueprint flows as follows: Query assessment → Retrieve trending projects using LunarCrush Coins v2 (filtered/sorted as per criteria) + Supplement with Mobula market data → Synthesize and deliver a comprehensive analysis of trending crypto projects.
"""
]

sectors = [
    "AI",
    "AI-Agents",
    "Analytics",
    "Base-Ecosystem",
    "Bitcoin-Ecosystem",
    "BRC-20",
    "DAO",
    "DeFAI",
    "DeFi",
    "DePin",
    "DeSci",
    "Events",
    "Exchange-Tokens",
    "Fan Tokens",
    "Gambling",
    "Gaming & Metaverse",
    "Layer-1",
    "Layer-2",
    "Lending/Borrowing",
    "Liquid Staking Derivatives",
    "Made In USA",
    "Memecoins",
    "NFT",
    "Oracles",
    "Real-Estate",
    "Real-World-Assets",
    "Runes",
    "SocialFi",
    "Solana-Ecosystem",
    "Sports",
    "Stablecoin",
    "Stacks-Ecosystem",
    "Storage",
    "Wallets",
    "Zero-Knowledge-Proofs"
]

data_example_output = """
DATA AGENT CHAIN-OF-THOUGHT:
- The query targets a predefined sector: DeSci.
- I will use the LunarCrush Coins V2 API to identify the top coins related to DeSci as well as their social metrics.
- Supplement this with detailed market and on-chain metrics via the Mobula API for the identified coins.
- Remember: Use coin symbols only.
- This approach ensures efficiency by leveraging predefined sector endpoints without requiring an identification phase.

FINAL API CALL STRUCTURE:
```json
[
  {
    "provider": "lunarcrush",
    "endpoint": "/public/coins/list/v2?filter=DeSci",
    "description": "Retrieve coins, posts, and news related to the DeSci sector using coin symbols.",
    nested_calls: [
      {
        "provider": "mobula",
        "endpoint": "/market/multi-data?symbols=coin1,coin2,coin3",
        "description": "Retrieve detailed market and on-chain data for the identified DeSci coins."
      }
    ],
  }
]
```
"""