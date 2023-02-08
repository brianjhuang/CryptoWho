#!/usr/bin/python
import os


class Reddit(object):
    """
    Static class that includes configuration for our Reddit Data Scraper
    """

    # GENERAL CONFIG
    SUBREDDITS = [
        "bitcoin",
        "btc",
        "ethereum",
        "dogecoin",
        "CryptoMarkets",
        "CryptoCurrencies",
        "CryptoCurrency",
        "CryptoCurrencyTrading",
        "Crypto_General",
        "binance",
        "CoinBase",
        "ledgerwallet",
        "bitcoinbeginners",
        "altcoin",
        "NFT",
        "NFTsMarketplace",
        "opensea",
        "wallstreetbets",
        "finance",
        "BusinessHub",
        "FinancialPlanning",
        "AskEconomics",
        "investing",
        "povertyfinance",
        "Economics",
        "Trading",
        "StockMarket",
        "Forex",
        "stocks",
        "Economy",
        "options",
        "dividends",
        "SecurityAnalysis",
        "Daytrading",
        "pennystocks",
    ]
    SCRAPE_DEPTH = 1  # How many pages to scrape per subreddit (25 posts per page)

    # SAVE PATHS
    RAW_THREADS = "../../data/raw/reddit/"
    PROCESSED_THREADS = "../../data/processed/reddit/"
    INTERIM_THREADS = "../../data/interim/reddit/"
    EXTERNAL_THREADS = "../../data/external/reddit/"
