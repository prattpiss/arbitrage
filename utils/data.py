# ============================================================
# YAHOO FINANCE UNIVERSAL CLIENT
# MIT COOKIE + CRUMB AUTHENTICATION
# ============================================================

import sys 
sys.path.insert(0, r"C:\Users\Labor\Desktop\Plans\Investment\Analysen\Mathematische_Modelle\Modelling\Arbitrage\utils\data.py")
sys.path.insert(0, r"C:\Users\Labor\Desktop\Plans\Investment\Analysen\Mathematische_Modelle\Modelling\Arbitrage\utils")

"""
======================================================================
YAHOO FINANCE UNIVERSAL CLIENT
======================================================================

ZWECK
-----
Diese Klasse stellt eine einheitliche Python-Schnittstelle zu
verschiedenen Yahoo-Finance-Web-Endpunkten bereit.

Die Klasse ist bewusst nicht auf eine einzelne Datenart beschränkt.
Sie kann unter anderem:

    - historische Preisreihen
    - OHLCV-Daten
    - Adjusted Close
    - aktuelle Quotes
    - Unternehmensinformationen
    - Fundamentaldaten
    - Bilanzdaten
    - Gewinn- und Verlustrechnung
    - Cashflows
    - Earnings
    - Analysteninformationen
    - Insidertransaktionen
    - institutionelle Eigentümer
    - Fondsbesitz
    - Optionsketten
    - Unternehmenssuche

abrufen.

Die Klasse arbeitet direkt mit HTTP-Requests gegen Yahoo-Finance-
Endpunkte und benötigt deshalb nicht die Bibliothek "yfinance".


======================================================================
GRUNDARCHITEKTUR
======================================================================

Die Klasse besitzt mehrere unterschiedliche Datenwege:

                         Yahoo Finance
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
          CHART          QUOTE SUMMARY       QUOTE
             │                │                │
             ▼                ▼                ▼
        Preisreihen       Fundamentaldaten   aktuelle Kurse
             │                │
             │                ├── Bilanz
             │                ├── Income
             │                ├── Cashflow
             │                ├── Insider
             │                ├── Eigentümer
             │                └── usw.
             │
             ▼
        pandas DataFrame


Zusätzlich:

    SEARCH
        └── Unternehmenssuche

    OPTIONS
        └── Optionsketten


======================================================================
AUTHENTICATION
======================================================================

Einige Yahoo-Endpunkte akzeptieren einfache Requests nicht mehr.

Insbesondere können folgende Endpunkte eine Yahoo-Session benötigen:

    - quote
    - quoteSummary
    - options

Dafür verwendet die Klasse:

    1. Yahoo-Cookie
    2. Yahoo-Crumb

Der Ablauf ist:

    Yahoo Cookie
        ↓
    Session Cookie
        ↓
    Crumb
        ↓
    authentifizierter Request
        ↓
    JSON-Antwort


Die historische CHART-API benötigt diesen Mechanismus normalerweise
nicht.


======================================================================
WICHTIGER HINWEIS
======================================================================

Yahoo Finance stellt diese Endpunkte nicht als stabile, offiziell
dokumentierte öffentliche API für beliebige externe Programme bereit.

Daher können:

    - URLs
    - Module
    - Parameter
    - Authentifizierung
    - Rate Limits
    - Antwortstrukturen

zukünftig geändert werden.

Die Klasse ist deshalb als flexibler Forschungs-/Analyse-Client
gedacht und nicht als garantiert dauerhaft stabile Produktions-API.


======================================================================
1. __init__()
======================================================================

SIGNATUR:

    YahooFinance(
        timeout=20,
        retries=3,
        pause=0.5,
        auto_auth=True
    )


AUFGABE
-------
Erstellt eine Yahoo-Finance-Session.

Dabei werden:

    - requests.Session()
    - HTTP-Header
    - Timeout
    - Retry-Anzahl
    - Wartezeit
    - Crumb

initialisiert.


PARAMETER
---------

timeout : int
    Maximale Wartezeit eines HTTP-Requests in Sekunden.

retries : int
    Anzahl der erneuten Versuche bei einem Fehler.

pause : float
    Grundwartezeit zwischen Requests bzw. Retries.

auto_auth : bool
    Wenn True, wird beim Erstellen des Objekts automatisch
    Cookie + Crumb geladen.


BEISPIEL:

    yf = YahooFinance(
        timeout=20,
        retries=3,
        pause=1,
        auto_auth=True
    )


======================================================================
2. authenticate()
======================================================================

SIGNATUR:

    yf.authenticate()


AUFGABE
-------
Initialisiert bzw. erneuert die Yahoo-Authentifizierung.

Dabei werden:

    1. Cookie von Yahoo angefordert
    2. Cookie in der Session gespeichert
    3. Crumb angefordert
    4. Crumb in self.crumb gespeichert


ERGEBNIS:

    self.crumb

enthält anschließend den aktuell verwendeten Yahoo-Crumb.


WIRD VERWENDET FÜR:

    - quote()
    - get()
    - options()


BEISPIEL:

    yf.authenticate()


======================================================================
3. _ensure_auth()
======================================================================

INTERNE FUNKTION


AUFGABE
-------
Prüft, ob bereits ein Crumb vorhanden ist.

Wenn kein Crumb vorhanden ist:

    authenticate()

wird automatisch aufgerufen.


WARUM?
------
Damit muss der Benutzer die Authentifizierung nicht bei jedem
Request manuell durchführen.


======================================================================
4. _request()
======================================================================

INTERNE KERNFUNKTION


SIGNATUR:

    _request(
        url,
        params=None,
        authenticated=False
    )


AUFGABE
-------
Führt tatsächlich den HTTP-Request aus.

Fast alle anderen Funktionen verwenden diese Funktion.


ABLAUF:

    URL + Parameter
          ↓
    Session verwenden
          ↓
    ggf. Crumb hinzufügen
          ↓
    HTTP GET
          ↓
    Statuscode prüfen
          ↓
    JSON zurückgeben


BEHANDELT:

    normale Antworten
    HTTP-Fehler
    401 Unauthorized
    403 Forbidden
    429 Too Many Requests
    Retry
    erneute Authentifizierung


BEI 401/403:

    Cookie + Crumb werden erneuert.


BEI 429:

    Die Funktion wartet und versucht es erneut.


RÜCKGABE:

    Python-Dictionary / JSON-Daten


======================================================================
5. available_modules()
======================================================================

SIGNATUR:

    yf.available_modules()


AUFGABE
-------
Gibt alle bekannten Aliasnamen der Quote-Summary-Module zurück.


BEISPIEL:

    yf.available_modules()


ERGEBNIS z.B.:

    [
        "balance",
        "cashflow",
        "financial",
        "income",
        "insiders",
        "statistics",
        ...
    ]


NÜTZLICH FÜR:

    - Übersicht
    - Jupyter
    - Exploration
    - Debugging


======================================================================
6. _resolve_modules()
======================================================================

INTERNE FUNKTION


AUFGABE
-------
Übersetzt benutzerfreundliche Aliasnamen in die tatsächlichen
Yahoo-Modulnamen.


BEISPIEL:

    "financial"

wird zu:

    "financialData"


oder:

    "cashflow"

wird zu:

    "cashflowStatementHistory"


Dadurch muss der Benutzer die technischen Yahoo-Namen nicht kennen.


SONDERFALL:

    "all"


führt dazu, dass alle bekannten Module angefordert werden.


======================================================================
7. get()
======================================================================

SIGNATUR:

    yf.get(
        symbol,
        modules
    )


AUFGABE
-------
Universeller Zugriff auf Quote-Summary-Daten.


BEISPIEL:

    yf.get(
        "AAPL",
        "financial"
    )


oder:

    yf.get(
        "AAPL",
        [
            "financial",
            "balance",
            "cashflow",
            "insiders"
        ]
    )


oder:

    yf.get(
        "AAPL",
        "all"
    )


DATENFLUSS:

    Symbol
      ↓
    Modulname
      ↓
    _resolve_modules()
      ↓
    Yahoo quoteSummary
      ↓
    _request()
      ↓
    JSON


RÜCKGABE:

    Rohes JSON / Python-Dictionary


WICHTIG:
--------
Diese Funktion gibt bewusst die Rohdaten zurück.

Damit gehen keine Informationen verloren.


======================================================================
8. df()
======================================================================

SIGNATUR:

    yf.df(
        symbol,
        module
    )


AUFGABE
-------
Wie get(), aber die Antwort wird direkt in einen
pandas.DataFrame umgewandelt.


BEISPIEL:

    df = yf.df(
        "AAPL",
        "financial"
    )


NÜTZLICH FÜR:

    - pandas
    - Statistik
    - Visualisierung
    - Jupyter
    - Datenanalyse


INTERN:

    get()
        ↓
    quoteSummary
        ↓
    JSON
        ↓
    pandas.json_normalize()
        ↓
    DataFrame


======================================================================
9. history()
======================================================================

SIGNATUR:

    yf.history(
        symbol,
        interval="1d",
        range="1y",
        start=None,
        end=None,
        events="div,splits",
        prepost=False
    )


AUFGABE
-------
Lädt historische Marktdaten.


GELIEFERTE DATEN:

    timestamp
    open
    high
    low
    close
    volume
    adj_close


OHLCV:

    O = Open
    H = High
    L = Low
    C = Close
    V = Volume


BEISPIEL:

    prices = yf.history(
        "AAPL",
        interval="1d",
        range="10y"
    )


MÖGLICHE INTERVALLE:

    1m
    2m
    5m
    15m
    30m
    60m
    90m
    1h
    1d
    5d
    1wk
    1mo
    3mo


BEISPIEL MIT DATUM:

    yf.history(
        "AAPL",
        start="2015-01-01",
        end="2025-01-01",
        interval="1d"
    )


RÜCKGABE:

    pandas.DataFrame


INDEX:

    timestamp


======================================================================
10. quote()
======================================================================

SIGNATUR:

    yf.quote(
        symbols
    )


AUFGABE
-------
Lädt aktuelle Marktdaten für einen oder mehrere Ticker.


BEISPIEL:

    yf.quote("AAPL")


oder:

    yf.quote(
        [
            "AAPL",
            "MSFT",
            "NVDA"
        ]
    )


RÜCKGABE:

    pandas.DataFrame


NÜTZLICH FÜR:

    - aktueller Preis
    - Marktkapitalisierung
    - Bid/Ask
    - Volumen
    - Börseninformationen
    - aktuelle Kennzahlen


======================================================================
11. search()
======================================================================

SIGNATUR:

    yf.search(
        query
    )


AUFGABE
-------
Sucht nach Unternehmen, Aktien und anderen Yahoo-Finance-Symbolen.


BEISPIEL:

    yf.search(
        "Nvidia"
    )


NÜTZLICH FÜR:

    - Ticker finden
    - Unternehmen suchen
    - Symbolauflösung


RÜCKGABE:

    Rohes JSON


======================================================================
12. options()
======================================================================

SIGNATUR:

    yf.options(
        symbol,
        expiration=None
    )


AUFGABE
-------
Lädt die Optionskette eines Unternehmens.


BEISPIEL:

    yf.options(
        "AAPL"
    )


MIT BESTIMMTEM VERFALLSDATUM:

    yf.options(
        "AAPL",
        expiration=UNIX_TIMESTAMP
    )


RÜCKGABE:

    Rohes JSON


ENTHÄLT TYPISCHERWEISE:

    Calls
    Puts
    Strike
    Bid
    Ask
    Last Price
    Volume
    Open Interest
    Implied Volatility
    Expiration


======================================================================
13. options_df()
======================================================================

SIGNATUR:

    yf.options_df(
        symbol,
        expiration=None
    )


AUFGABE
-------
Wie options(), aber die Optionsdaten werden direkt in DataFrames
umgewandelt.


RÜCKGABE:

    {
        "calls": DataFrame,
        "puts": DataFrame,
        "expiration_dates": [...]
    }


BEISPIEL:

    options = yf.options_df(
        "AAPL"
    )

    calls = options["calls"]

    puts = options["puts"]


NÜTZLICH FÜR:

    - Optionsanalyse
    - Volatilitätsanalyse
    - Put/Call-Vergleiche
    - Implied Volatility
    - Open Interest
    - Optionsarbitrage


======================================================================
14. many()
======================================================================

SIGNATUR:

    yf.many(
        symbols,
        module,
        as_dataframe=False
    )


AUFGABE
-------
Führt dieselbe Datenabfrage für viele Unternehmen aus.


BEISPIEL:

    data = yf.many(
        [
            "AAPL",
            "MSFT",
            "NVDA",
            "GOOG"
        ],
        "financial"
    )


MIT DATAFRAMES:

    data = yf.many(
        [
            "AAPL",
            "MSFT",
            "NVDA"
        ],
        "financial",
        as_dataframe=True
    )


RÜCKGABE:

    Dictionary

    {
        "AAPL": DataFrame,
        "MSFT": DataFrame,
        "NVDA": DataFrame
    }


WICHTIG:
--------
Ein Fehler bei einem einzelnen Unternehmen stoppt nicht automatisch
den gesamten Batch.


======================================================================
15. history_many()
======================================================================

SIGNATUR:

    yf.history_many(
        symbols,
        interval="1d",
        range="1y"
    )


AUFGABE
-------
Lädt historische Preisreihen für mehrere Unternehmen.


BEISPIEL:

    prices = yf.history_many(
        [
            "AAPL",
            "MSFT",
            "NVDA",
            "GOOG"
        ],
        interval="1d",
        range="10y"
    )


RÜCKGABE:

    {
        "AAPL": DataFrame,
        "MSFT": DataFrame,
        "NVDA": DataFrame,
        "GOOG": DataFrame
    }


BESONDERS NÜTZLICH FÜR:

    - Korrelation
    - Cointegration
    - Pairs Trading
    - Statistical Arbitrage
    - Faktoranalysen
    - Portfolioanalyse


======================================================================
16. save_csv()
======================================================================

SIGNATUR:

    yf.save_csv(
        df,
        filename
    )


AUFGABE
-------
Speichert einen DataFrame als CSV.


BEISPIEL:

    yf.save_csv(
        prices,
        "AAPL_prices.csv"
    )


======================================================================
17. save_parquet()
======================================================================

SIGNATUR:

    yf.save_parquet(
        df,
        filename
    )


AUFGABE
-------
Speichert einen DataFrame im Parquet-Format.


BEISPIEL:

    yf.save_parquet(
        prices,
        "AAPL_prices.parquet"
    )


WARUM PARQUET?
--------------
Parquet ist für große quantitative Datenmengen meist deutlich
geeigneter als CSV.

Vorteile:

    - kompakter
    - schneller
    - Datentypen bleiben erhalten
    - geeignet für große Zeitreihen


======================================================================
18. info()
======================================================================

SIGNATUR:

    yf.info()


AUFGABE
-------
Zeigt Informationen über den aktuellen Client.


AUSGABE:

    - Timeout
    - Retries
    - Authentication Status
    - verfügbare Module


======================================================================
DATENMODULE
======================================================================

Die Aliasnamen der Klasse entsprechen folgenden Yahoo-Daten:


PREIS
-----

    price
        Preisübersicht


UNTERNEHMEN
-----------

    profile
        Unternehmensprofil


FUNDAMENTALS
------------

    financial
        Finanzkennzahlen

    statistics
        statistische Kennzahlen


BILANZ
------

    balance
        historische Bilanz

    balance_q
        quartalsweise Bilanz


INCOME STATEMENT
----------------

    income
        historische Gewinn-/Verlustrechnung

    income_q
        quartalsweise Gewinn-/Verlustrechnung


CASHFLOW
--------

    cashflow
        historische Cashflows

    cashflow_q
        quartalsweise Cashflows


EARNINGS
--------

    earnings
        Earnings

    earnings_history
        historische Earnings

    earnings_trend
        Earnings-Trends


INSIDER
-------

    insiders
        Insidertransaktionen

    insider_holders
        Insider-Beteiligungen


EIGENTÜMER
----------

    institutional
        institutionelle Eigentümer

    funds
        Fondsbesitz

    holders
        größere Eigentümer


ANALYSTEN
---------

    recommendations
        Analystenempfehlungen

    upgrades
        Upgrades / Downgrades


OPTIONEN
--------

    options()
    options_df()


KALENDER
--------

    calendar
        Unternehmensereignisse


ESG
---

    esg


SEC
---

    sec


======================================================================
TYPISCHER WORKFLOW
======================================================================

Ein einfacher Research-Workflow sieht beispielsweise so aus:


    yf = YahooFinance()


    # 1. Preisreihe

    prices = yf.history(
        "AAPL",
        range="10y"
    )


    # 2. Fundamentaldaten

    fundamentals = yf.df(
        "AAPL",
        "financial"
    )


    # 3. Bilanz

    balance = yf.df(
        "AAPL",
        "balance"
    )


    # 4. Cashflow

    cashflow = yf.df(
        "AAPL",
        "cashflow"
    )


    # 5. Insider

    insiders = yf.df(
        "AAPL",
        "insiders"
    )


    # 6. Optionen

    options = yf.options_df(
        "AAPL"
    )


======================================================================
FÜR ARBITRAGE-ANALYSEN
======================================================================

Der Client kann anschließend als Datenquelle für quantitative
Analysen verwendet werden.


BEISPIEL:

    symbols = [
        "AAPL",
        "MSFT",
        "GOOG",
        "AMZN",
        "META",
        "NVDA"
    ]


    prices = yf.history_many(
        symbols,
        interval="1d",
        range="10y"
    )


Darauf können anschließend beispielsweise angewendet werden:


    Renditen
        ↓
    Volatilität
        ↓
    Korrelation
        ↓
    Rolling Correlation
        ↓
    Regression
        ↓
    Hedge Ratio
        ↓
    Spread
        ↓
    Stationarität
        ↓
    ADF / KPSS
        ↓
    Cointegration
        ↓
    Half-Life
        ↓
    Hurst Exponent
        ↓
    Z-Score
        ↓
    Entry / Exit
        ↓
    Backtest
        ↓
    Out-of-Sample-Test


======================================================================
WICHTIGE UNTERSCHEIDUNG
======================================================================

Es gibt drei Ebenen der Datenverarbeitung:


1. RAW
-------

    yf.get(...)

liefert möglichst unveränderte Yahoo-Daten.


2. DATAFRAME
------------

    yf.df(...)

wandelt die Daten in pandas DataFrames um.


3. ANALYSE
----------

Die eigentliche quantitative Analyse sollte anschließend getrennt
vom Yahoo-Client stattfinden.

Beispielsweise:


    YahooFinance
          ↓
    Data Acquisition
          ↓
    Data Cleaning
          ↓
    Feature Engineering
          ↓
    Statistical Tests
          ↓
    Model
          ↓
    Backtest
          ↓
    Risk Analysis


Dadurch bleibt der Datenzugriff unabhängig von der späteren
Handelsstrategie.


======================================================================
GRUNDIDEE DER KLASSE
======================================================================

Die Klasse ist bewusst als DATA-ACCESS-LAYER konzipiert.

Sie soll nicht selbst entscheiden:

    "Welche Aktie soll ich kaufen?"

sondern nur zuverlässig Daten bereitstellen.

Damit kann dieselbe Datenbasis später für verschiedene Modelle
verwendet werden:

    - Arbitrage
    - Statistical Arbitrage
    - Pairs Trading
    - Momentum
    - Mean Reversion
    - Faktorstrategien
    - Event Studies
    - Fundamentalanalyse
    - Optionsanalyse
    - Portfoliooptimierung
    - Machine Learning


======================================================================
END
======================================================================
"""


import requests
import pandas as pd
import time
from typing import Union, List, Optional


class YahooFinance:

    # ========================================================
    # ENDPOINTS
    # ========================================================

    CHART_URL = (
        "https://query1.finance.yahoo.com"
        "/v8/finance/chart"
    )

    QUOTE_URL = (
        "https://query1.finance.yahoo.com"
        "/v7/finance/quote"
    )

    SEARCH_URL = (
        "https://query1.finance.yahoo.com"
        "/v1/finance/search"
    )

    OPTIONS_URL = (
        "https://query2.finance.yahoo.com"
        "/v7/finance/options"
    )

    QUOTE_SUMMARY_URL = (
        "https://query2.finance.yahoo.com"
        "/v10/finance/quoteSummary"
    )

    COOKIE_URL = (
        "https://fc.yahoo.com"
    )

    CRUMB_URL = (
        "https://query1.finance.yahoo.com"
        "/v1/test/getcrumb"
    )

    # ========================================================
    # MODULE
    # ========================================================

    MODULES = {

        "price":
            "price",

        "summary":
            "summaryDetail",

        "profile":
            "assetProfile",

        "financial":
            "financialData",

        "financialData":
            "financialData",

        "statistics":
            "defaultKeyStatistics",

        "keyStats":
            "defaultKeyStatistics",

        "balance":
            "balanceSheetHistory",

        "balance_q":
            "balanceSheetHistoryQuarterly",

        "balanceQuarter":
            "balanceSheetHistoryQuarterly",

        "income":
            "incomeStatementHistory",

        "income_q":
            "incomeStatementHistoryQuarterly",

        "incomeQuarter":
            "incomeStatementHistoryQuarterly",

        "cashflow":
            "cashflowStatementHistory",

        "cashflow_q":
            "cashflowStatementHistoryQuarterly",

        "cashflowQuarter":
            "cashflowStatementHistoryQuarterly",

        "earnings":
            "earnings",

        "earnings_history":
            "earningsHistory",

        "earningsHistory":
            "earningsHistory",

        "earnings_trend":
            "earningsTrend",

        "earningsTrend":
            "earningsTrend",

        "calendar":
            "calendarEvents",

        "recommendations":
            "recommendationTrend",

        "recommendationTrend":
            "recommendationTrend",

        "upgrades":
            "upgradeDowngradeHistory",

        "upgradeDowngradeHistory":
            "upgradeDowngradeHistory",

        "insiders":
            "insiderTransactions",

        "insiderTransactions":
            "insiderTransactions",

        "insider_holders":
            "insiderHolders",

        "insiderHolders":
            "insiderHolders",

        "institutional":
            "institutionOwnership",

        "institutionOwnership":
            "institutionOwnership",

        "funds":
            "fundOwnership",

        "fundOwnership":
            "fundOwnership",

        "holders":
            "majorHoldersBreakdown",

        "majorHolders":
            "majorHoldersBreakdown",

        "majorHoldersBreakdown":
            "majorHoldersBreakdown",

        "esg":
            "esgScores",

        "sec":
            "secFilings",
    }

        # ============================================================
    # FINANCIAL DATA FIELD CATALOG
    # ============================================================

    FINANCIAL_FIELDS = {

        # --------------------------------------------------------
        # PREIS / BEWERTUNG
        # --------------------------------------------------------

        "currentPrice":
            "Aktueller Aktienkurs",

        "targetHighPrice":
            "Höchstes Analystenkursziel",

        "targetLowPrice":
            "Niedrigstes Analystenkursziel",

        "targetMeanPrice":
            "Durchschnittliches Analystenkursziel",

        "targetMedianPrice":
            "Median des Analystenkursziels",

        "recommendationMean":
            "Numerischer Analysten-Empfehlungswert",

        "recommendationKey":
            "Analystenempfehlung",

        "numberOfAnalystOpinions":
            "Anzahl der Analystenmeinungen",


        # --------------------------------------------------------
        # CASH
        # --------------------------------------------------------

        "totalCash":
            "Gesamter Cashbestand",

        "totalCashPerShare":
            "Cash pro Aktie",


        # --------------------------------------------------------
        # SCHULDEN
        # --------------------------------------------------------

        "totalDebt":
            "Gesamte verzinsliche Verschuldung",

        "debtToEquity":
            "Verhältnis Schulden zu Eigenkapital",


        # --------------------------------------------------------
        # GEWINN
        # --------------------------------------------------------

        "ebitda":
            "EBITDA",

        "grossProfits":
            "Bruttogewinn",


        # --------------------------------------------------------
        # UMSATZ
        # --------------------------------------------------------

        "totalRevenue":
            "Gesamtumsatz",

        "revenuePerShare":
            "Umsatz pro Aktie",


        # --------------------------------------------------------
        # CASHFLOW
        # --------------------------------------------------------

        "freeCashflow":
            "Free Cash Flow",

        "operatingCashflow":
            "Operativer Cashflow",


        # --------------------------------------------------------
        # WACHSTUM
        # --------------------------------------------------------

        "earningsGrowth":
            "Gewinnwachstum",

        "revenueGrowth":
            "Umsatzwachstum",


        # --------------------------------------------------------
        # MARGEN
        # --------------------------------------------------------

        "grossMargins":
            "Bruttomarge",

        "ebitdaMargins":
            "EBITDA-Marge",

        "operatingMargins":
            "Operative Marge",

        "profitMargins":
            "Gewinnmarge",


        # --------------------------------------------------------
        # RENTABILITÄT
        # --------------------------------------------------------

        "returnOnAssets":
            "Return on Assets (ROA)",

        "returnOnEquity":
            "Return on Equity (ROE)",


        # --------------------------------------------------------
        # LIQUIDITÄT
        # --------------------------------------------------------

        "quickRatio":
            "Quick Ratio",

        "currentRatio":
            "Current Ratio",


        # --------------------------------------------------------
        # META
        # --------------------------------------------------------

        "financialCurrency":
            "Währung der Finanzdaten",

        "maxAge":
            "Alter der Yahoo-Daten in Sekunden"
    }

        # ============================================================
    # STATISTICS FIELD CATALOG
    # ============================================================

    STATISTICS_FIELDS = {

        # --------------------------------------------------------
        # UNTERNEHMENSWERT
        # --------------------------------------------------------

        "enterpriseValue": {
            "name": "Enterprise Value",
            "unit": "USD",
            "category": "Bewertung",
            "description":
                "Unternehmenswert inklusive Nettofinanzverschuldung."
        },

        # --------------------------------------------------------
        # BEWERTUNG
        # --------------------------------------------------------

        "forwardPE": {
            "name": "Forward P/E",
            "unit": "x",
            "category": "Bewertung",
            "description":
                "Kurs-Gewinn-Verhältnis auf Basis des erwarteten Gewinns."
        },

        "priceToBook": {
            "name": "Price-to-Book",
            "unit": "x",
            "category": "Bewertung",
            "description":
                "Verhältnis von Marktkapitalisierung zu Buchwert."
        },

        "priceToSalesTrailing12Months": {
            "name": "Price-to-Sales",
            "unit": "x",
            "category": "Bewertung",
            "description":
                "Kurs-Umsatz-Verhältnis auf Basis der letzten 12 Monate."
        },

        "pegRatio": {
            "name": "PEG Ratio",
            "unit": "x",
            "category": "Bewertung",
            "description":
                "P/E-Verhältnis relativ zum erwarteten Gewinnwachstum."
        },

        "enterpriseToRevenue": {
            "name": "Enterprise Value / Revenue",
            "unit": "x",
            "category": "Bewertung",
            "description":
                "Enterprise Value relativ zum Umsatz."
        },

        "enterpriseToEbitda": {
            "name": "Enterprise Value / EBITDA",
            "unit": "x",
            "category": "Bewertung",
            "description":
                "Enterprise Value relativ zum EBITDA."
        },

        # --------------------------------------------------------
        # GEWINN
        # --------------------------------------------------------

        "profitMargins": {
            "name": "Profit Margin",
            "unit": "%",
            "category": "Profitabilität",
            "description":
                "Nettogewinnmarge."
        },

        "netIncomeToCommon": {
            "name": "Net Income to Common",
            "unit": "USD",
            "category": "Gewinn",
            "description":
                "Nettogewinn, der den Stammaktionären zuzurechnen ist."
        },

        # --------------------------------------------------------
        # EPS
        # --------------------------------------------------------

        "trailingEps": {
            "name": "Trailing EPS",
            "unit": "USD/Aktie",
            "category": "Gewinn",
            "description":
                "Gewinn je Aktie auf Basis der vergangenen Periode."
        },

        "forwardEps": {
            "name": "Forward EPS",
            "unit": "USD/Aktie",
            "category": "Gewinn",
            "description":
                "Erwarteter zukünftiger Gewinn je Aktie."
        },

        # --------------------------------------------------------
        # AKTIEN
        # --------------------------------------------------------

        "floatShares": {
            "name": "Float Shares",
            "unit": "Aktien",
            "category": "Aktienstruktur",
            "description":
                "Anzahl der frei handelbaren Aktien."
        },

        "sharesOutstanding": {
            "name": "Shares Outstanding",
            "unit": "Aktien",
            "category": "Aktienstruktur",
            "description":
                "Anzahl der ausstehenden Aktien."
        },

        "impliedSharesOutstanding": {
            "name": "Implied Shares Outstanding",
            "unit": "Aktien",
            "category": "Aktienstruktur",
            "description":
                "Von Yahoo ermittelte implizite Aktienanzahl."
        },

        # --------------------------------------------------------
        # SHORT INTEREST
        # --------------------------------------------------------

        "sharesShort": {
            "name": "Shares Short",
            "unit": "Aktien",
            "category": "Short Interest",
            "description":
                "Anzahl der leerverkauften Aktien."
        },

        "sharesShortPriorMonth": {
            "name": "Shares Short Previous Month",
            "unit": "Aktien",
            "category": "Short Interest",
            "description":
                "Short-Positionen im vorherigen Monat."
        },

        "sharesPercentSharesOut": {
            "name": "Short Shares / Shares Outstanding",
            "unit": "%",
            "category": "Short Interest",
            "description":
                "Anteil der leerverkauften Aktien an allen Aktien."
        },

        "shortPercentOfFloat": {
            "name": "Short Percent of Float",
            "unit": "%",
            "category": "Short Interest",
            "description":
                "Anteil der leerverkauften Aktien am Free Float."
        },

        "shortRatio": {
            "name": "Short Ratio",
            "unit": "Tage",
            "category": "Short Interest",
            "description":
                "Short Interest relativ zum durchschnittlichen Handelsvolumen."
        },

        # --------------------------------------------------------
        # EIGENTÜMER
        # --------------------------------------------------------

        "heldPercentInsiders": {
            "name": "Insider Ownership",
            "unit": "%",
            "category": "Eigentümerstruktur",
            "description":
                "Aktienanteil, der von Insidern gehalten wird."
        },

        "heldPercentInstitutions": {
            "name": "Institutional Ownership",
            "unit": "%",
            "category": "Eigentümerstruktur",
            "description":
                "Aktienanteil, der von Institutionen gehalten wird."
        },

        # --------------------------------------------------------
        # BETA / RISIKO
        # --------------------------------------------------------

        "beta": {
            "name": "Beta",
            "unit": "dimensionslos",
            "category": "Risiko",
            "description":
                "Sensitivität der Aktie gegenüber dem Gesamtmarkt."
        },

        "beta3Year": {
            "name": "3-Year Beta",
            "unit": "dimensionslos",
            "category": "Risiko",
            "description":
                "Beta über einen längeren Zeitraum."
        },

        # --------------------------------------------------------
        # BUCHWERT
        # --------------------------------------------------------

        "bookValue": {
            "name": "Book Value per Share",
            "unit": "USD/Aktie",
            "category": "Bilanz",
            "description":
                "Buchwert je Aktie."
        },

        # --------------------------------------------------------
        # WACHSTUM
        # --------------------------------------------------------

        "earningsQuarterlyGrowth": {
            "name": "Quarterly Earnings Growth",
            "unit": "%",
            "category": "Wachstum",
            "description":
                "Quartalsweises Gewinnwachstum."
        },

        "revenueQuarterlyGrowth": {
            "name": "Quarterly Revenue Growth",
            "unit": "%",
            "category": "Wachstum",
            "description":
                "Quartalsweises Umsatzwachstum."
        },

        # --------------------------------------------------------
        # RENDITE
        # --------------------------------------------------------

        "52WeekChange": {
            "name": "52-Week Change",
            "unit": "%",
            "category": "Performance",
            "description":
                "Kursveränderung über 52 Wochen."
        },

        "SandP52WeekChange": {
            "name": "S&P 500 52-Week Change",
            "unit": "%",
            "category": "Performance",
            "description":
                "Vergleichbare 52-Wochen-Veränderung des S&P 500."
        },

        "ytdReturn": {
            "name": "YTD Return",
            "unit": "%",
            "category": "Performance",
            "description":
                "Rendite seit Jahresbeginn."
        },

        "qtdReturn": {
            "name": "QTD Return",
            "unit": "%",
            "category": "Performance",
            "description":
                "Rendite seit Quartalsbeginn."
        },

        # --------------------------------------------------------
        # DIVIDENDE
        # --------------------------------------------------------

        "lastDividendValue": {
            "name": "Last Dividend",
            "unit": "USD/Aktie",
            "category": "Dividende",
            "description":
                "Zuletzt gezahlte Dividende je Aktie."
        },

        "lastDividendDate": {
            "name": "Last Dividend Date",
            "unit": "Datum",
            "category": "Dividende",
            "description":
                "Datum der letzten Dividendenzahlung."
        },

        # --------------------------------------------------------
        # SPLITS
        # --------------------------------------------------------

        "lastSplitFactor": {
            "name": "Last Split Factor",
            "unit": "Verhältnis",
            "category": "Corporate Actions",
            "description":
                "Verhältnis des letzten Aktiensplits."
        },

        "lastSplitDate": {
            "name": "Last Split Date",
            "unit": "Datum",
            "category": "Corporate Actions",
            "description":
                "Datum des letzten Aktiensplits."
        },

        # --------------------------------------------------------
        # FISCAL
        # --------------------------------------------------------

        "lastFiscalYearEnd": {
            "name": "Last Fiscal Year End",
            "unit": "Datum",
            "category": "Unternehmensdaten",
            "description":
                "Ende des letzten Geschäftsjahres."
        },

        "nextFiscalYearEnd": {
            "name": "Next Fiscal Year End",
            "unit": "Datum",
            "category": "Unternehmensdaten",
            "description":
                "Voraussichtliches Ende des nächsten Geschäftsjahres."
        },

        "mostRecentQuarter": {
            "name": "Most Recent Quarter",
            "unit": "Datum",
            "category": "Unternehmensdaten",
            "description":
                "Ende des zuletzt verfügbaren Quartals."
        }
    }

    # ========================================================
    # INIT
    # ========================================================

    def __init__(
        self,
        timeout: int = 20,
        retries: int = 3,
        pause: float = 0.5,
        auto_auth: bool = True
    ):

        self.timeout = timeout
        self.retries = retries
        self.pause = pause

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0 "
                "Safari/537.36",

            "Accept":
                "application/json,text/plain,*/*",

            "Accept-Language":
                "en-US,en;q=0.9",

            "Connection":
                "keep-alive"
        })

        self.crumb = None

        if auto_auth:

            self.authenticate()

    # ========================================================
    # AUTHENTICATION
    # ========================================================

    def authenticate(self):

        """
        Holt Yahoo-Cookie und Crumb.
        """

        print("Yahoo Session wird initialisiert...")

        # ----------------------------------------------------
        # 1. Cookie holen
        # ----------------------------------------------------

        try:

            response = self.session.get(
                self.COOKIE_URL,
                timeout=self.timeout
            )

            # Yahoo kann hier 404 liefern.
            # Wichtig ist primär das gesetzte Cookie.

            print(
                f"Cookie-Request: HTTP {response.status_code}"
            )

        except Exception as e:

            raise RuntimeError(
                f"Yahoo Cookie konnte nicht geladen werden: {e}"
            )

        # ----------------------------------------------------
        # Prüfen, ob Cookie vorhanden
        # ----------------------------------------------------

        cookies = self.session.cookies.get_dict()

        if len(cookies) == 0:

            print(
                "Warnung: Yahoo hat kein Cookie geliefert."
            )

        # ----------------------------------------------------
        # 2. Crumb holen
        # ----------------------------------------------------

        try:

            response = self.session.get(
                self.CRUMB_URL,
                timeout=self.timeout
            )

            response.raise_for_status()

            crumb = response.text.strip()

        except Exception as e:

            raise RuntimeError(
                f"Yahoo Crumb konnte nicht geladen werden: {e}"
            )

        # ----------------------------------------------------
        # Crumb validieren
        # ----------------------------------------------------

        if not crumb:

            raise RuntimeError(
                "Yahoo hat einen leeren Crumb geliefert."
            )

        if "too many requests" in crumb.lower():

            raise RuntimeError(
                "Yahoo hat statt des Crumbs "
                "'Too Many Requests' geliefert. "
                "Die IP wurde vermutlich temporär begrenzt."
            )

        self.crumb = crumb

        print("Yahoo Authentication erfolgreich.")
        print(
            f"Crumb: {self.crumb[:10]}..."
        )

        return True

    # ========================================================
    # AUTH CHECK
    # ========================================================

    def _ensure_auth(self):

        if self.crumb is None:

            self.authenticate()

    # ========================================================
    # REQUEST
    # ========================================================

    def _request(
        self,
        url: str,
        params: Optional[dict] = None,
        authenticated: bool = False
    ):

        if params is None:

            params = {}

        params = params.copy()

        # ----------------------------------------------------
        # Crumb hinzufügen
        # ----------------------------------------------------

        if authenticated:

            self._ensure_auth()

            params["crumb"] = self.crumb

        last_error = None

        for attempt in range(
            self.retries
        ):

            try:

                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )

                # =================================================
                # 401 / 403
                # =================================================

                if response.status_code in (
                    401,
                    403
                ):

                    # Session erneuern

                    if authenticated:

                        print(
                            "Yahoo Session abgelehnt "
                            f"(HTTP {response.status_code}). "
                            "Erneuere Cookie + Crumb..."
                        )

                        self.authenticate()

                        params["crumb"] = self.crumb

                        response = self.session.get(
                            url,
                            params=params,
                            timeout=self.timeout
                        )

                # =================================================
                # 429
                # =================================================

                if response.status_code == 429:

                    wait = (
                        self.pause *
                        (attempt + 1) *
                        3
                    )

                    print(
                        f"Yahoo Rate Limit (429). "
                        f"Warte {wait:.1f}s..."
                    )

                    time.sleep(wait)

                    continue

                # =================================================
                # Fehler
                # =================================================

                response.raise_for_status()

                return response.json()

            except Exception as e:

                last_error = e

                if attempt < self.retries - 1:

                    time.sleep(
                        self.pause *
                        (attempt + 1)
                    )

        raise RuntimeError(
            "\nYahoo Finance Request fehlgeschlagen.\n"
            f"URL: {url}\n"
            f"Fehler: {last_error}"
        )

    # ========================================================
    # MODULE
    # ========================================================

    def available_modules(self):

        return sorted(
            set(self.MODULES.keys())
        )

    # ========================================================
    # MODULE RESOLVER
    # ========================================================

    def _resolve_modules(
        self,
        modules
    ):

        if modules == "all":

            modules = list(
                set(
                    self.MODULES.values()
                )
            )

        elif isinstance(
            modules,
            str
        ):

            modules = [
                self.MODULES.get(
                    modules,
                    modules
                )
            ]

        else:

            modules = [

                self.MODULES.get(
                    module,
                    module
                )

                for module in modules
            ]

        return sorted(
            set(modules)
        )

    # ========================================================
    # QUOTE SUMMARY
    # ========================================================

    def get(
        self,
        symbol: str,
        modules: Union[
            str,
            List[str]
        ]
    ):

        symbol = symbol.upper()

        modules = self._resolve_modules(
            modules
        )

        url = (
            f"{self.QUOTE_SUMMARY_URL}"
            f"/{symbol}"
        )

        params = {

            "modules":
                ",".join(modules)
        }

        return self._request(
            url,
            params=params,
            authenticated=True
        )

    # ========================================================
    # DATAFRAME
    # ========================================================

    def df(
        self,
        symbol: str,
        module: str
    ):

        data = self.get(
            symbol,
            module
        )

        try:

            result = (
                data
                ["quoteSummary"]
                ["result"]
            )

            if not result:

                return pd.DataFrame()

            result = result[0]

        except Exception:

            return pd.DataFrame()

        return pd.json_normalize(
            result
        )

    # ========================================================
    # HISTORY
    # ========================================================

    def history(
        self,
        symbol: str,
        interval: str = "1d",
        range: str = "1y",
        start: Optional[str] = None,
        end: Optional[str] = None,
        events: str = "div,splits",
        prepost: bool = False
    ):

        symbol = symbol.upper()

        url = (
            f"{self.CHART_URL}"
            f"/{symbol}"
        )

        params = {

            "interval":
                interval,

            "events":
                events,

            "includePrePost":
                str(prepost).lower()
        }

        # ----------------------------------------------------
        # Zeitraum
        # ----------------------------------------------------

        if start is not None:

            start_dt = pd.Timestamp(
                start,
                tz="UTC"
            )

            params["period1"] = int(
                start_dt.timestamp()
            )

            if end is not None:

                end_dt = pd.Timestamp(
                    end,
                    tz="UTC"
                )

                params["period2"] = int(
                    end_dt.timestamp()
                )

        else:

            params["range"] = range

        # chart braucht keinen Crumb

        data = self._request(
            url,
            params=params,
            authenticated=False
        )

        try:

            result = (
                data
                ["chart"]
                ["result"]
            )

            if not result:

                return pd.DataFrame()

            result = result[0]

        except Exception:

            return pd.DataFrame()

        timestamps = result.get(
            "timestamp",
            []
        )

        indicators = result[
            "indicators"
        ]

        quote = indicators[
            "quote"
        ][0]

        df = pd.DataFrame({

            "timestamp":
                pd.to_datetime(
                    timestamps,
                    unit="s",
                    utc=True
                ),

            "open":
                quote.get("open"),

            "high":
                quote.get("high"),

            "low":
                quote.get("low"),

            "close":
                quote.get("close"),

            "volume":
                quote.get("volume")
        })

        # ----------------------------------------------------
        # Adjusted Close
        # ----------------------------------------------------

        adjclose = indicators.get(
            "adjclose"
        )

        if adjclose:

            df["adj_close"] = (
                adjclose[0]
                .get("adjclose")
            )

        df = df.set_index(
            "timestamp"
        )

        return df

    # ========================================================
    # QUOTE
    # ========================================================

    def quote(
        self,
        symbols: Union[
            str,
            List[str]
        ]
    ):

        if isinstance(
            symbols,
            str
        ):

            symbols = [
                symbols
            ]

        symbols = [

            s.upper()
            for s in symbols
        ]

        params = {

            "symbols":
                ",".join(symbols)
        }

        data = self._request(

            self.QUOTE_URL,

            params=params,

            authenticated=True
        )

        results = (

            data
            .get(
                "quoteResponse",
                {}
            )
            .get(
                "result",
                []
            )
        )

        return pd.DataFrame(
            results
        )

    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query: str
    ):

        params = {
            "q":
                query
        }

        # search funktioniert normalerweise
        # ohne Crumb

        return self._request(
            self.SEARCH_URL,
            params=params,
            authenticated=False
        )

    # ========================================================
    # OPTIONS
    # ========================================================

    def options(
        self,
        symbol: str,
        expiration: Optional[int] = None
    ):

        symbol = symbol.upper()

        url = (
            f"{self.OPTIONS_URL}"
            f"/{symbol}"
        )

        params = {}

        if expiration is not None:

            params["date"] = expiration

        return self._request(
            url,
            params=params,
            authenticated=True
        )

    # ========================================================
    # OPTIONS DATAFRAME
    # ========================================================

    def options_df(
        self,
        symbol: str,
        expiration: Optional[int] = None
    ):

        data = self.options(
            symbol,
            expiration
        )

        try:

            result = (
                data
                ["optionChain"]
                ["result"][0]
            )

        except Exception:

            return {

                "calls":
                    pd.DataFrame(),

                "puts":
                    pd.DataFrame(),

                "expiration_dates":
                    []
            }

        expiration_dates = \
            result.get(
                "expirationDates",
                []
            )

        options = result.get(
            "options",
            []
        )

        if not options:

            return {

                "calls":
                    pd.DataFrame(),

                "puts":
                    pd.DataFrame(),

                "expiration_dates":
                    expiration_dates
            }

        options = options[0]

        calls = pd.DataFrame(
            options.get(
                "calls",
                []
            )
        )

        puts = pd.DataFrame(
            options.get(
                "puts",
                []
            )
        )

        return {

            "calls":
                calls,

            "puts":
                puts,

            "expiration_dates":
                expiration_dates
        }

    # ========================================================
    # BATCH
    # ========================================================

    def many(
        self,
        symbols: List[str],
        module: Union[
            str,
            List[str]
        ],
        as_dataframe: bool = False
    ):

        results = {}

        for symbol in symbols:

            try:

                if as_dataframe:

                    results[symbol] = \
                        self.df(
                            symbol,
                            module
                        )

                else:

                    results[symbol] = \
                        self.get(
                            symbol,
                            module
                        )

            except Exception as e:

                results[symbol] = {

                    "error":
                        str(e)
                }

        return results

    # ========================================================
    # HISTORY MANY
    # ========================================================

    def history_many(
        self,
        symbols: List[str],
        interval: str = "1d",
        range: str = "1y"
    ):

        results = {}

        for symbol in symbols:

            try:

                results[symbol] = \
                    self.history(
                        symbol,
                        interval=interval,
                        range=range
                    )

            except Exception as e:

                results[symbol] = {

                    "error":
                        str(e)
                }

        return results

    # ========================================================
    # SAVE
    # ========================================================

    def save_csv(
        self,
        df: pd.DataFrame,
        filename: str
    ):

        df.to_csv(
            filename
        )

    def save_parquet(
        self,
        df: pd.DataFrame,
        filename: str
    ):

        df.to_parquet(
            filename
        )

    # ========================================================
    # INFO
    # ========================================================

    def info(self):

        print(
            "Yahoo Finance Universal Client"
        )

        print(
            "================================"
        )

        print(
            f"Timeout: {self.timeout}s"
        )

        print(
            f"Retries: {self.retries}"
        )

        print(
            f"Authenticated: "
            f"{self.crumb is not None}"
        )

        print()

        print(
            "Verfügbare Module:"
        )

        for module in self.available_modules():

            print(
                f"  - {module}"
            )

        # ============================================================
    # GENERISCHE FINANCIAL-DATENWERKZEUGE
    # ============================================================

    def financial_raw(self, symbol: str):
        """
        Gibt den kompletten financialData-Block zurück.

        Beispiel:
            data = yf.financial_raw("MSFT")
        """

        data = self.get(
            symbol=symbol,
            modules="financial"
        )

        try:
            return (
                data["quoteSummary"]
                    ["result"][0]
                    ["financialData"]
            )

        except (KeyError, IndexError, TypeError):
            return {}


    def financial_keys(self, symbol: str = None):
        """
        Gibt alle verfügbaren Keys des financialData-Moduls zurück.

        Wenn symbol angegeben wird:
            werden die tatsächlich von Yahoo gelieferten Keys
            dieses Unternehmens angezeigt.

        Beispiel:
            yf.financial_keys("MSFT")
        """

        if symbol is None:
            return list(self.FINANCIAL_FIELDS.keys())

        data = self.financial_raw(symbol)

        return list(data.keys())


    def financial_info(self, symbol: str):
        """
        Zeigt alle verfügbaren Financial-Keys inklusive
        einer kurzen Beschreibung.
        """

        available = self.financial_keys(symbol)

        rows = []

        for key in available:

            rows.append({
                "key": key,
                "description":
                    self.FINANCIAL_FIELDS
                    .get(key, "")
            })

        return pd.DataFrame(rows)


    def financial_get(
        self,
        symbol: str,
        keys=None,
        raw=False,
        formatted=False
    ):
        """
        Allgemeiner Financial-Filter.

        keys kann sein:

            "totalDebt"

        oder:

            ["totalDebt", "totalRevenue", "ebitda"]

        oder:

            None

        None gibt alle verfügbaren Werte zurück.
        """

        data = self.financial_raw(symbol)

        if keys is None:

            selected = data

        else:

            if isinstance(keys, str):
                keys = [keys]

            selected = {
                key: data[key]
                for key in keys
                if key in data
            }

        # --------------------------------------------------------
        # RAW
        # --------------------------------------------------------

        if raw:
            return selected

        # --------------------------------------------------------
        # Werte extrahieren
        # --------------------------------------------------------

        result = {}

        for key, value in selected.items():

            if isinstance(value, dict):

                if "raw" in value:

                    if formatted:
                        result[key] = value.get(
                            "fmt",
                            value["raw"]
                        )

                    else:
                        result[key] = value["raw"]

                else:
                    result[key] = value

            else:

                result[key] = value

        return result


    def financial_df(
        self,
        symbol: str,
        keys=None
    ):
        """
        Gibt ausgewählte Financial-Daten als DataFrame zurück.
        """

        data = self.financial_get(
            symbol=symbol,
            keys=keys
        )

        rows = []

        for key, value in data.items():

            rows.append({
                "key": key,
                "value": value
            })

        return pd.DataFrame(rows)


        # ============================================================
    # SPEZIELLE ANALYSTEN-FUNKTIONEN
    # ============================================================

    def financial_field(
        self,
        symbol: str,
        field: str,
        formatted: bool = False
    ):
        """
        Holt genau EIN Financial-Feld.

        Beispiel:

            yf.financial_field(
                "MSFT",
                "totalDebt"
            )
        """

        return self.financial_get(
            symbol=symbol,
            keys=field,
            formatted=formatted
        ).get(field)


    # ============================================================
    # UMSATZ
    # ============================================================

    def revenue(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "totalRevenue",
            formatted
        )


    def revenue_growth(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "revenueGrowth",
            formatted
        )


    # ============================================================
    # SCHULDEN
    # ============================================================

    def debt(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "totalDebt",
            formatted
        )


    def debt_to_equity(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "debtToEquity",
            formatted
        )


    # ============================================================
    # CASH
    # ============================================================

    def cash(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "totalCash",
            formatted
        )


    def cash_per_share(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "totalCashPerShare",
            formatted
        )


    # ============================================================
    # EBITDA
    # ============================================================

    def ebitda(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "ebitda",
            formatted
        )


    # ============================================================
    # GEWINN
    # ============================================================

    def gross_profit(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "grossProfits",
            formatted
        )


    # ============================================================
    # CASHFLOW
    # ============================================================

    def cashflow(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "operatingCashflow",
            formatted
        )


    def free_cashflow(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "freeCashflow",
            formatted
        )


    # ============================================================
    # MARGEN
    # ============================================================

    def gross_margin(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "grossMargins",
            formatted
        )


    def operating_margin(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "operatingMargins",
            formatted
        )


    def ebitda_margin(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "ebitdaMargins",
            formatted
        )


    def profit_margin(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "profitMargins",
            formatted
        )


    # ============================================================
    # RENTABILITÄT
    # ============================================================

    def roe(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "returnOnEquity",
            formatted
        )


    def roa(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "returnOnAssets",
            formatted
        )


    # ============================================================
    # LIQUIDITÄT
    # ============================================================

    def current_ratio(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "currentRatio",
            formatted
        )


    def quick_ratio(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "quickRatio",
            formatted
        )


    # ============================================================
    # WACHSTUM
    # ============================================================

    def earnings_growth(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "earningsGrowth",
            formatted
        )


    # ============================================================
    # ANALYSTEN
    # ============================================================

    def analyst_target(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "targetMeanPrice",
            formatted
        )


    def analyst_target_high(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "targetHighPrice",
            formatted
        )


    def analyst_target_low(
        self,
        symbol: str,
        formatted: bool = False
    ):

        return self.financial_field(
            symbol,
            "targetLowPrice",
            formatted
        )


        # ============================================================
    # STATISTICS RAW
    # ============================================================

    def statistics_raw(self, symbol: str):
        """
        Gibt den kompletten defaultKeyStatistics-Block zurück.
        """

        data = self.get(
            symbol=symbol,
            modules="statistics"
        )

        try:

            return (
                data
                ["quoteSummary"]
                ["result"][0]
                ["defaultKeyStatistics"]
            )

        except (KeyError, IndexError, TypeError):

            return {}


    # ============================================================
    # STATISTICS KEYS
    # ============================================================

    def statistics_keys(self, symbol: str = None):
        """
        Gibt verfügbare Statistics-Keys zurück.

        Ohne Symbol:
            bekannte Keys des Clients.

        Mit Symbol:
            tatsächlich von Yahoo gelieferte Keys.
        """

        if symbol is None:

            return list(
                self.STATISTICS_FIELDS.keys()
            )

        data = self.statistics_raw(
            symbol
        )

        return list(
            data.keys()
        )


    # ============================================================
    # STATISTICS INFO
    # ============================================================

    def statistics_info(
        self,
        symbol: str
    ):
        """
        Zeigt verfügbare Statistics-Felder
        inklusive Beschreibung und Kategorie.
        """

        available = self.statistics_keys(
            symbol
        )

        rows = []

        for key in available:

            info = self.STATISTICS_FIELDS.get(
                key,
                {}
            )

            rows.append({

                "key":
                    key,

                "name":
                    info.get(
                        "name",
                        key
                    ),

                "category":
                    info.get(
                        "category",
                        ""
                    ),

                "unit":
                    info.get(
                        "unit",
                        ""
                    ),

                "description":
                    info.get(
                        "description",
                        ""
                    )
            })

        return pd.DataFrame(rows)

        # ============================================================
    # STATISTICS GET
    # ============================================================

    def statistics_get(
        self,
        symbol: str,
        keys=None,
        raw=False,
        formatted=False
    ):
        """
        Allgemeiner Filter für defaultKeyStatistics.

        Beispiel:

            yf.statistics_get(
                "AAPL",
                [
                    "beta",
                    "forwardPE",
                    "pegRatio"
                ]
            )
        """

        data = self.statistics_raw(
            symbol
        )

        if keys is None:

            selected = data

        else:

            if isinstance(keys, str):

                keys = [keys]

            selected = {

                key: data[key]

                for key in keys

                if key in data
            }

        if raw:

            return selected

        result = {}

        for key, value in selected.items():

            if isinstance(value, dict):

                if "raw" in value:

                    if formatted:

                        result[key] = value.get(
                            "fmt",
                            value["raw"]
                        )

                    else:

                        result[key] = value["raw"]

                else:

                    result[key] = value

            else:

                result[key] = value

        return result

        # ============================================================
    # STATISTICS FIELD
    # ============================================================

    def statistics_field(
        self,
        symbol: str,
        field: str,
        verbose: bool = True
    ):
        """
        Holt genau ein Statistics-Feld.

        Rückgabe:
            reiner numerischer Rohwert

        Zusätzlich:
            lesbare Informationen auf stdout.
        """

        data = self.statistics_raw(
            symbol
        )

        if field not in data:

            if verbose:

                print(
                    f"'{field}' wurde für "
                    f"{symbol} nicht gefunden."
                )

            return None

        value = data[field]

        # --------------------------------------------------------
        # Metadaten
        # --------------------------------------------------------

        info = self.STATISTICS_FIELDS.get(
            field,
            {}
        )

        name = info.get(
            "name",
            field
        )

        unit = info.get(
            "unit",
            "unbekannt"
        )

        category = info.get(
            "category",
            "unbekannt"
        )

        description = info.get(
            "description",
            ""
        )

        # --------------------------------------------------------
        # Yahoo-Objekt
        # --------------------------------------------------------

        if isinstance(value, dict):

            raw_value = value.get(
                "raw"
            )

            formatted_value = value.get(
                "fmt"
            )

            long_formatted = value.get(
                "longFmt"
            )

        else:

            raw_value = value

            formatted_value = value

            long_formatted = value

        # --------------------------------------------------------
        # Ausgabe
        # --------------------------------------------------------

        if verbose:

            print()
            print(
                "═" * 60
            )

            print(
                f"{name}"
            )

            print(
                "─" * 60
            )

            print(
                f"Ticker:       {symbol}"
            )

            print(
                f"Key:          {field}"
            )

            print(
                f"Kategorie:    {category}"
            )

            print(
                f"Wert:         {formatted_value}"
            )

            print(
                f"Rohwert:      {raw_value}"
            )

            print(
                f"Datentyp:     {type(raw_value).__name__}"
            )

            print(
                f"Einheit:      {unit}"
            )

            if long_formatted is not None:

                print(
                    f"Langformat:   {long_formatted}"
                )

            if description:

                print(
                    f"Bedeutung:    {description}"
                )

            print(
                "Quelle:       Yahoo Finance"
            )

            print(
                "═" * 60
            )

        # --------------------------------------------------------
        # WICHTIG:
        # Reiner Wert wird zurückgegeben
        # --------------------------------------------------------

        return raw_value


        # ============================================================
    # STATISTICS SHORTCUTS
    # ============================================================

    def beta(self, symbol):
        return self.statistics_field(
            symbol,
            "beta"
        )


    def beta_3y(self, symbol):
        return self.statistics_field(
            symbol,
            "beta3Year"
        )


    def enterprise_value(self, symbol):
        return self.statistics_field(
            symbol,
            "enterpriseValue"
        )


    def forward_pe(self, symbol):
        return self.statistics_field(
            symbol,
            "forwardPE"
        )


    def peg(self, symbol):
        return self.statistics_field(
            symbol,
            "pegRatio"
        )


    def price_to_book(self, symbol):
        return self.statistics_field(
            symbol,
            "priceToBook"
        )


    def price_to_sales(self, symbol):
        return self.statistics_field(
            symbol,
            "priceToSalesTrailing12Months"
        )


    def ev_to_revenue(self, symbol):
        return self.statistics_field(
            symbol,
            "enterpriseToRevenue"
        )


    def ev_to_ebitda(self, symbol):
        return self.statistics_field(
            symbol,
            "enterpriseToEbitda"
        )


    def eps(self, symbol):
        return self.statistics_field(
            symbol,
            "trailingEps"
        )


    def forward_eps(self, symbol):
        return self.statistics_field(
            symbol,
            "forwardEps"
        )


    def book_value(self, symbol):
        return self.statistics_field(
            symbol,
            "bookValue"
        )


    def shares_outstanding(self, symbol):
        return self.statistics_field(
            symbol,
            "sharesOutstanding"
        )


    def float_shares(self, symbol):
        return self.statistics_field(
            symbol,
            "floatShares"
        )


    def shares_short(self, symbol):
        return self.statistics_field(
            symbol,
            "sharesShort"
        )


    def short_ratio(self, symbol):
        return self.statistics_field(
            symbol,
            "shortRatio"
        )


    def short_percent_float(self, symbol):
        return self.statistics_field(
            symbol,
            "shortPercentOfFloat"
        )


    def insider_ownership(self, symbol):
        return self.statistics_field(
            symbol,
            "heldPercentInsiders"
        )


    def institutional_ownership(self, symbol):
        return self.statistics_field(
            symbol,
            "heldPercentInstitutions"
        )


    def profit_margin(self, symbol):
        return self.statistics_field(
            symbol,
            "profitMargins"
        )


    def earnings_growth(self, symbol):
        return self.statistics_field(
            symbol,
            "earningsQuarterlyGrowth"
        )


    def revenue_growth(self, symbol):
        return self.statistics_field(
            symbol,
            "revenueQuarterlyGrowth"
        )


    def net_income(self, symbol):
        return self.statistics_field(
            symbol,
            "netIncomeToCommon"
        )


    def last_dividend(self, symbol):
        return self.statistics_field(
            symbol,
            "lastDividendValue"
        )


    def performance_52w(self, symbol):
        return self.statistics_field(
            symbol,
            "52WeekChange"
        )


    def market_performance_52w(self, symbol):
        return self.statistics_field(
            symbol,
            "SandP52WeekChange"
        )


    def split_factor(self, symbol):
        return self.statistics_field(
            symbol,
            "lastSplitFactor"
        )