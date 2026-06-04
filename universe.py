# universe.py — Every stock and ETF to scan

# ── US SECTOR ETFs ────────────────────────────────────────────
SECTOR_ETFS = {
    # Tech & Semiconductors
    "SMH":  "VanEck Semiconductor ETF",
    "SOXX": "iShares Semiconductor ETF",
    "XLK":  "Technology Select Sector SPDR",
    "ARKK": "ARK Innovation ETF",
    "ARKQ": "ARK Autonomous Tech ETF",
    "ARKG": "ARK Genomic Revolution ETF",
    "ARKF": "ARK Fintech Innovation ETF",
    "ARKX": "ARK Space Exploration ETF",
    "IGV":  "iShares Software ETF",
    "WCLD": "WisdomTree Cloud Computing",
    "CLOU": "Global X Cloud Computing ETF",
    "HACK": "ETFMG Prime Cyber Security",
    "CIBR": "First Trust Cybersecurity ETF",
    "ROBT": "First Trust Nasdaq AI & Robotics",
    "BOTZ": "Global X Robotics & AI ETF",
    "AIQ":  "Global X AI & Technology ETF",

    # Energy
    "XLE":  "Energy Select Sector SPDR",
    "XOP":  "SPDR S&P Oil & Gas Exploration",
    "OIH":  "VanEck Oil Services ETF",
    "AMLP": "Alerian MLP ETF",
    "UNG":  "United States Natural Gas",
    "USO":  "United States Oil Fund",

    # Defence & Aerospace
    "ITA":  "iShares US Aerospace & Defense",
    "XAR":  "SPDR S&P Aerospace & Defense",
    "PPA":  "Invesco Aerospace & Defense",
    "DFEN": "Direxion Daily Aerospace 3x Bull",

    # Healthcare & Biotech
    "XLV":  "Health Care Select Sector SPDR",
    "IBB":  "iShares Biotechnology ETF",
    "XBI":  "SPDR S&P Biotech ETF",
    "LABD": "Direxion Daily S&P Biotech Bear",
    "LABU": "Direxion Daily S&P Biotech Bull",

    # Financials & Banking
    "XLF":  "Financial Select Sector SPDR",
    "KBE":  "SPDR S&P Bank ETF",
    "KRE":  "SPDR S&P Regional Banking",
    "IAI":  "iShares US Broker-Dealers ETF",

    # Consumer
    "XLY":  "Consumer Discretionary SPDR",
    "XLP":  "Consumer Staples SPDR",
    "XRT":  "SPDR S&P Retail ETF",
    "AMZN": "Amazon",

    # Materials & Metals
    "XME":  "SPDR S&P Metals & Mining",
    "GDX":  "VanEck Gold Miners ETF",
    "GDXJ": "VanEck Junior Gold Miners",
    "SLV":  "iShares Silver Trust",
    "GLD":  "SPDR Gold Shares",
    "COPX": "Global X Copper Miners ETF",
    "REMX": "VanEck Rare Earth/Strategic Metals",

    # Industrials & Infrastructure
    "XLI":  "Industrial Select Sector SPDR",
    "PAVE": "Global X US Infrastructure Dev",
    "IGF":  "iShares Global Infrastructure",

    # Real Estate
    "XLRE": "Real Estate Select Sector SPDR",
    "VNQ":  "Vanguard Real Estate ETF",

    # Broad Market
    "QQQ":  "Invesco QQQ (Nasdaq 100)",
    "SPY":  "SPDR S&P 500 ETF",
    "IWM":  "iShares Russell 2000 (Small Cap)",
    "DIA":  "SPDR Dow Jones Industrial",
    "VTI":  "Vanguard Total Stock Market",

    # International
    "EEM":  "iShares MSCI Emerging Markets",
    "EWJ":  "iShares MSCI Japan",
    "KWEB": "KraneShares China Internet",
    "FXI":  "iShares China Large-Cap",
    "INDA": "iShares MSCI India ETF",

    # Bull/Leveraged ETFs (for you)
    "TQQQ": "ProShares UltraPro QQQ 3x",
    "SOXL": "Direxion Daily Semi Bull 3x",
    "TECL": "Direxion Daily Tech Bull 3x",
    "UPRO": "ProShares UltraPro S&P500 3x",
    "SPXL": "Direxion Daily S&P500 Bull 3x",
    "LABU": "Direxion Daily Biotech Bull 3x",
    "TNA":  "Direxion Daily Small Cap Bull 3x",
    "FAS":  "Direxion Daily Financial Bull 3x",
    "NAIL": "Direxion Daily Homebuilders Bull 3x",
    "FNGU": "MicroSectors FANG+ 3x Leveraged",

    # Crypto-adjacent
    "IBIT": "iShares Bitcoin Trust",
    "FBTC": "Fidelity Wise Origin Bitcoin",
    "GBTC": "Grayscale Bitcoin Trust",

    # Bonds/Rates
    "TLT":  "iShares 20+ Year Treasury Bond ETF",
    "EDV":  "Vanguard Extended Duration Treasury ETF",
    "IEF":  "iShares 7-10 Year Treasury Bond ETF",
    "SHY":  "iShares 1-3 Year Treasury Bond ETF",
    "TBT":  "ProShares UltraShort 20+ Year Treasury",
    "HYG":  "iShares iBoxx High Yield Corp Bond",
    "IEV":  "iShares Europe ETF",
    "AGG":  "iShares Core US Aggregate Bond ETF",
}

# ── US STOCKS BY SECTOR ───────────────────────────────────────
US_STOCKS = {
    # AI & Semiconductors
    "NVDA": "NVIDIA Corporation",
    "AMD":  "Advanced Micro Devices",
    "INTC": "Intel Corporation",
    "QCOM": "Qualcomm",
    "AVGO": "Broadcom",
    "TSM":  "Taiwan Semiconductor",
    "MU":   "Micron Technology",
    "SNDK": "SanDisk Corp",
    "AMAT": "Applied Materials",
    "LRCX": "Lam Research",
    "KLAC": "KLA Corporation",
    "ASML": "ASML Holding",
    "ARM":  "ARM Holdings",
    "MRVL": "Marvell Technology",
    "SMCI": "Super Micro Computer",
    "PLTR": "Palantir Technologies",

    # Big Tech
    "AAPL": "Apple Inc",
    "MSFT": "Microsoft Corporation",
    "GOOGL":"Alphabet (Google)",
    "META": "Meta Platforms",
    "AMZN": "Amazon.com",
    "TSLA": "Tesla Inc",
    "NFLX": "Netflix",
    "CRM":  "Salesforce",
    "NOW":  "ServiceNow",
    "SNOW": "Snowflake",
    "DDOG": "Datadog",
    "NET":  "Cloudflare",
    "CRWD": "CrowdStrike",
    "PANW": "Palo Alto Networks",
    "FTNT": "Fortinet",
    "ZS":   "Zscaler",
    "OKTA": "Okta",

    # Defence & Aerospace
    "LMT":  "Lockheed Martin",
    "RTX":  "Raytheon Technologies",
    "NOC":  "Northrop Grumman",
    "BA":   "Boeing",
    "GD":   "General Dynamics",
    "LHX":  "L3Harris Technologies",
    "LDOS": "Leidos Holdings",
    "BAH":  "Booz Allen Hamilton",
    "SAIC": "Science Applications Intl",
    "CACI": "CACI International",
    "HII":  "Huntington Ingalls",
    "TDG":  "TransDigm Group",
    "HEI":  "HEICO Corporation",
    "KTOS": "Kratos Defense",
    "RKLB": "Rocket Lab USA",
    "RDW":  "Redwire Corporation",
    "ACHR": "Archer Aviation (Drones)",
    "JOBY": "Joby Aviation (Drones)",
    "LILM": "Lilium (Drones)",

    # Energy & Oil
    "XOM":  "ExxonMobil",
    "CVX":  "Chevron",
    "COP":  "ConocoPhillips",
    "EOG":  "EOG Resources",
    "PXD":  "Pioneer Natural Resources",
    "DVN":  "Devon Energy",
    "HAL":  "Halliburton",
    "SLB":  "SLB (Schlumberger)",
    "BKR":  "Baker Hughes",
    "OXY":  "Occidental Petroleum",
    "MPC":  "Marathon Petroleum",
    "VLO":  "Valero Energy",

    # Healthcare & Biotech
    "JNJ":  "Johnson & Johnson",
    "PFE":  "Pfizer",
    "MRK":  "Merck",
    "ABBV": "AbbVie",
    "LLY":  "Eli Lilly",
    "BMY":  "Bristol-Myers Squibb",
    "GILD": "Gilead Sciences",
    "REGN": "Regeneron",
    "MRNA": "Moderna",
    "BNTX": "BioNTech",
    "VRTX": "Vertex Pharmaceuticals",
    "BIIB": "Biogen",
    "ILMN": "Illumina",
    "ISRG": "Intuitive Surgical",

    # Financials
    "JPM":  "JPMorgan Chase",
    "BAC":  "Bank of America",
    "GS":   "Goldman Sachs",
    "MS":   "Morgan Stanley",
    "WFC":  "Wells Fargo",
    "BLK":  "BlackRock",
    "BX":   "Blackstone",
    "KKR":  "KKR & Co",
    "APO":  "Apollo Global Management",
    "V":    "Visa",
    "MA":   "Mastercard",
    "PYPL": "PayPal",
    "SQ":   "Block (Square)",
    "COIN": "Coinbase",

    # Consumer & Retail
    "WMT":  "Walmart",
    "COST": "Costco",
    "TGT":  "Target",
    "HD":   "Home Depot",
    "LOW":  "Lowe's",
    "NKE":  "Nike",
    "SBUX": "Starbucks",
    "MCD":  "McDonald's",
    "ABNB": "Airbnb",
    "UBER": "Uber",
    "LYFT": "Lyft",

    # Industrials & Infrastructure
    "CAT":  "Caterpillar",
    "DE":   "Deere & Company",
    "GE":   "GE Aerospace",
    "HON":  "Honeywell",
    "MMM":  "3M Company",
    "UPS":  "United Parcel Service",
    "FDX":  "FedEx",
    "DAL":  "Delta Air Lines",
    "UAL":  "United Airlines",

    # EV & Clean Energy
    "RIVN": "Rivian Automotive",
    "LCID": "Lucid Group",
    "NIO":  "NIO Inc",
    "LI":   "Li Auto",
    "XPEV": "XPeng",
    "CHPT": "ChargePoint",
    "BLNK": "Blink Charging",
    "ENPH": "Enphase Energy",
    "FSLR": "First Solar",
    "SEDG": "SolarEdge Technologies",

    # Telecom & Media
    "T":    "AT&T",
    "VZ":   "Verizon",
    "TMUS": "T-Mobile US",
    "DIS":  "Walt Disney",
    "CMCSA":"Comcast",
    "NFLX": "Netflix",
    "SPOT": "Spotify",

    # Dell & Storage (your interest)
    "DELL": "Dell Technologies",
    "HPE":  "Hewlett Packard Enterprise",
    "HPQ":  "HP Inc",
    "WDC":  "Western Digital",
    "STX":  "Seagate Technology",
    "NTAP": "NetApp",
}

# ── MACRO INDICATORS (Yahoo Finance tickers) ──────────────────
MACRO_TICKERS = {
    "^VIX":   "CBOE Volatility Index (VIX)",
    "^TNX":   "10-Year Treasury Yield",
    "^TYX":   "30-Year Treasury Yield",
    "^FVX":   "5-Year Treasury Yield",
    "DX-Y.NYB":"US Dollar Index (DXY)",
    "GC=F":   "Gold Futures",
    "CL=F":   "Crude Oil Futures",
    "^GSPC":  "S&P 500",
    "^IXIC":  "Nasdaq Composite",
    "^DJI":   "Dow Jones Industrial",
    "^RUT":   "Russell 2000",
}

# ── NSE INDIA STOCKS ──────────────────────────────────────────
NSE_STOCKS = {
    # Nifty 50
    "RELIANCE.NS":   "Reliance Industries",
    "TCS.NS":        "Tata Consultancy Services",
    "HDFCBANK.NS":   "HDFC Bank",
    "BHARTIARTL.NS": "Bharti Airtel",
    "ICICIBANK.NS":  "ICICI Bank",
    "INFOSYS.NS":    "Infosys",
    "SBIN.NS":       "State Bank of India",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "ITC.NS":        "ITC",
    "LT.NS":         "Larsen & Toubro",
    "KOTAKBANK.NS":  "Kotak Mahindra Bank",
    "AXISBANK.NS":   "Axis Bank",
    "BAJFINANCE.NS": "Bajaj Finance",
    "MARUTI.NS":     "Maruti Suzuki",
    "TITAN.NS":      "Titan Company",
    "SUNPHARMA.NS":  "Sun Pharmaceutical",
    "WIPRO.NS":      "Wipro",
    "ONGC.NS":       "ONGC",
    "NTPC.NS":       "NTPC",
    "TATAMOTORS.NS": "Tata Motors",
    "HCLTECH.NS":    "HCL Technologies",
    "JSWSTEEL.NS":   "JSW Steel",
    "TATASTEEL.NS":  "Tata Steel",
    "ADANIPORTS.NS": "Adani Ports",
    "DRREDDY.NS":    "Dr Reddy's",
    "CIPLA.NS":      "Cipla",
    "EICHERMOT.NS":  "Eicher Motors",
    "HEROMOTOCO.NS": "Hero MotoCorp",
    "DIVISLAB.NS":   "Divi's Laboratories",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "BAJAJ-AUTO.NS": "Bajaj Auto",
    "NESTLEIND.NS":  "Nestle India",
    "ADANIENT.NS":   "Adani Enterprises",
    "HINDALCO.NS":   "Hindalco Industries",
    "TRENT.NS":      "Trent",

    # Defence & PSU
    "HAL.NS":        "Hindustan Aeronautics",
    "BEL.NS":        "Bharat Electronics",
    "IRCTC.NS":      "Indian Railway Catering",
    "IRFC.NS":       "Indian Railway Finance",
    "RECLTD.NS":     "REC Limited",
    "PFC.NS":        "Power Finance Corp",
    "NHPC.NS":       "NHPC",
    "COALINDIA.NS":  "Coal India",
    "SAIL.NS":       "Steel Authority of India",
    "NMDC.NS":       "NMDC",

    # IT & Tech
    "TECHM.NS":      "Tech Mahindra",
    "LTIM.NS":       "LTIMindtree",
    "PERSISTENT.NS": "Persistent Systems",
    "COFORGE.NS":    "Coforge",
    "MPHASIS.NS":    "Mphasis",

    # Banking & Finance
    "INDUSINDBK.NS": "IndusInd Bank",
    "BANDHANBNK.NS": "Bandhan Bank",
    "FEDERALBNK.NS": "Federal Bank",
    "IDFCFIRSTB.NS": "IDFC First Bank",
    "PNB.NS":        "Punjab National Bank",
    "CANBK.NS":      "Canara Bank",
    "BANKBARODA.NS": "Bank of Baroda",
    "ABCAPITAL.NS":  "Aditya Birla Capital",
    "BAJAJFINSV.NS": "Bajaj Finserv",

    # Consumer & FMCG
    "TATACONSUM.NS": "Tata Consumer Products",
    "BRITANNIA.NS":  "Britannia Industries",
    "DABUR.NS":      "Dabur India",
    "MARICO.NS":     "Marico",
    "GODREJCP.NS":   "Godrej Consumer Products",

    # Auto
    "M&M.NS":        "Mahindra & Mahindra",
    "BALKRISIND.NS": "Balkrishna Industries",
    "MOTHERSON.NS":  "Samvardhana Motherson",
    "BOSCHLTD.NS":   "Bosch",

    # New Age Tech
    "ZOMATO.NS":     "Zomato",
    "NYKAA.NS":      "FSN E-Commerce (Nykaa)",
    "DELHIVERY.NS":  "Delhivery",
    "DIXON.NS":      "Dixon Technologies",
    "TATAPOWER.NS":  "Tata Power",
    "ADANIGREEN.NS": "Adani Green Energy",

    # NSE Futures (underlying)
    "^NSEI":         "Nifty 50 Index",
    "^NSEBANK":      "Bank Nifty Index",
}

# ── ETF → RELATED STOCKS mapping ─────────────────────────────
# When a stock gets a catalyst, also flag these ETFs
STOCK_TO_ETF = {
    "NVDA": ["SMH", "SOXX", "QQQ", "SOXL", "FNGU"],
    "AMD":  ["SMH", "SOXX", "QQQ", "SOXL"],
    "INTC": ["SMH", "SOXX"],
    "MU":   ["SMH", "SOXX"],
    "SNDK": ["SMH"],
    "TSLA": ["QQQ", "ARKK"],
    "AAPL": ["QQQ", "SPY", "XLK"],
    "MSFT": ["QQQ", "SPY", "XLK"],
    "PLTR": ["QQQ", "ARKK"],
    "LMT":  ["ITA", "XAR", "PPA"],
    "RTX":  ["ITA", "XAR", "PPA"],
    "NOC":  ["ITA", "XAR", "PPA"],
    "BA":   ["ITA", "XAR"],
    "XOM":  ["XLE", "XOP"],
    "CVX":  ["XLE", "XOP"],
    "MRNA": ["IBB", "XBI", "ARKG"],
    "PFE":  ["XLV", "IBB"],
    "JPM":  ["XLF", "KBE"],
    "BAC":  ["XLF", "KBE"],
    "GS":   ["XLF", "IAI"],
    "COIN": ["IBIT", "FBTC"],
}

# All tickers combined for US scan
ALL_US = {**US_STOCKS, **SECTOR_ETFS}

# ── BOTTLENECK STOCKS ─────────────────────────────────────────
# These are the picks-and-shovels plays — companies that supply
# critical components to the AI/tech mega-trend.
# When chips run, these run HARDER because they're capacity constraints.

BOTTLENECK_STOCKS = {

    # ── Photonics & Optical Interconnects ─────────────────────
    # Data moves between chips at the speed of light — these make that happen
    "LITE":  "Lumentum Holdings (lasers for AI data centres)",
    "COHR":  "Coherent Corp (optical transceivers + components)",
    "MTSI":  "MACOM Technology (RF + optical semiconductors)",
    "FN":    "Fabrinet (manufactures for Lumentum, Coherent)",
    "VIAV":  "VIAVI Solutions (optical network testing)",
    "IPAR":  "InterPlex (precision photonic components)",

    # ── Advanced Packaging ────────────────────────────────────
    # NVDA's H100/H200 uses CoWoS packaging — massive bottleneck
    "AMAT":  "Applied Materials (deposition + packaging equipment)",
    "LRCX":  "Lam Research (etch equipment for advanced packaging)",
    "KLAC":  "KLA Corporation (inspection + metrology)",
    "ONTO":  "Onto Innovation (advanced packaging inspection)",
    "ACMR":  "ACM Research (cleaning equipment for advanced nodes)",

    # ── Power Management & VRMs ───────────────────────────────
    # Every AI chip needs ultra-precise power delivery
    "VICR":  "Vicor Corp (power components for AI servers)",
    "MPWR":  "Monolithic Power Systems (power ICs for data centres)",
    "IREN":  "Iris Energy (AI power infrastructure)",
    "SMCI":  "Super Micro Computer (AI server systems)",

    # ── Liquid Cooling & Thermal ──────────────────────────────
    # AI chips generate enormous heat — cooling is a hard constraint
    "VRT":   "Vertiv Holdings (data centre cooling + power)",
    "MOD":   "Modine Manufacturing (thermal management)",
    "CARR":  "Carrier Global (HVAC + cooling systems)",
    "CIBR":  "Comfort Systems USA (data centre mechanical)",

    # ── Data Centre Power & Grid ──────────────────────────────
    # AI data centres need 10-100x more power than normal ones
    "ETN":   "Eaton Corp (power management for data centres)",
    "POWL":  "Powell Industries (switchgear + transformers)",
    "CEG":   "Constellation Energy (nuclear power for data centres)",
    "VST":   "Vistra Corp (power generation for AI)",
    "NRG":   "NRG Energy (power supply to hyperscalers)",

    # ── Copper & Raw Materials ────────────────────────────────
    # AI data centres use enormous amounts of copper for wiring
    "FCX":   "Freeport-McMoRan (largest US copper producer)",
    "SCCO":  "Southern Copper Corp",
    "COPX":  "Global X Copper Miners ETF",

    # ── Networking & Interconnects ────────────────────────────
    # Moving data between thousands of GPUs requires fast networking
    "ANET":  "Arista Networks (AI data centre networking)",
    "MRVL":  "Marvell Technology (custom AI chips + networking)",
    "INFN":  "Infinera Corp (optical networking)",
    "CIEN":  "Ciena Corp (optical networking equipment)",
    "APH":   "Amphenol (connectors for data centres)",

    # ── PCBs & Substrates ─────────────────────────────────────
    # The boards that everything sits on
    "TTMI":  "TTM Technologies (printed circuit boards)",
    "BHE":   "Benchmark Electronics (EMS for AI hardware)",

    # ── Specialty Chemicals & Gases ───────────────────────────
    # Chip fabs need ultra-pure gases and chemicals
    "APD":   "Air Products (specialty gases for chip fabs)",
    "LIN":   "Linde PLC (industrial gases for semiconductors)",
    "CMC":   "CMC Materials (CMP slurries for chip polishing)",

    # ── HBM Memory (direct NVDA bottleneck) ───────────────────
    "MU":    "Micron Technology (HBM3e for NVDA H200)",
    "WDC":   "Western Digital (NAND for AI storage)",

    # ── Nuclear / Uranium (AI power demand) ───────────────────
    "CCJ":   "Cameco Corp (uranium — nuclear for AI power)",
    "UUUU":  "Energy Fuels (uranium mining)",
    "LEU":   "Centrus Energy (uranium enrichment)",

    # ── EDA & Design Software ─────────────────────────────────
    # Every chip starts as software design — these are monopolies
    "CDNS":  "Cadence Design Systems (chip design EDA)",
    "SNPS":  "Synopsys (chip design + verification)",

    # ── Defence AI bottlenecks ────────────────────────────────
    "KTOS":  "Kratos Defense (autonomous systems + AI drones)",
    "RKLB":  "Rocket Lab (launch vehicles for AI satellites)",
    "ACHR":  "Archer Aviation (autonomous air mobility)",
}
