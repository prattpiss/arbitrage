const fetchButton = document.getElementById("fetchButton");

const output = document.getElementById("output");

const assetElement = document.getElementById("asset");
const priceElement = document.getElementById("price");
const currencyElement = document.getElementById("currency");
const previousCloseElement = document.getElementById("previousClose");
const timestampElement = document.getElementById("timestamp");
const sourceElement = document.getElementById("source");

const rawDataElement = document.getElementById("rawData");

const statusElement = document.getElementById("status");
const statusDot = document.getElementById("statusDot");

const symbolInput = document.getElementById("symbolInput");


/*
 * Yahoo Finance Chart API
 *
 * Beispiel:
 *
 * https://query1.finance.yahoo.com/v8/finance/chart/AAPL
 *
 * Parameter:
 *
 * interval=1m
 * range=1d
 *
 * 
 * 
 *
 * 
 */

async function fetchYahooData(symbol) {

    symbol = symbol.trim().toUpperCase();

    if (!symbol) {
        throw new Error("Kein Ticker angegeben.");
    }


    const encodedSymbol = encodeURIComponent(symbol);


    const url =
        `https://query1.finance.yahoo.com/v8/finance/chart/${encodedSymbol}` +
        `?interval=1m` +
        `&range=1d` +
        `&includePrePost=true`;


    console.log("Yahoo URL:");
    console.log(url);


    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    });


    console.log("HTTP Status:", response.status);


    if (!response.ok) {

        throw new Error(
            `Yahoo Finance HTTP ${response.status}`
        );

    }


    const data = await response.json();


    console.log("Yahoo Response:");
    console.log(data);


    if (
        !data.chart ||
        !data.chart.result ||
        !data.chart.result[0]
    ) {

        throw new Error(
            "Yahoo Finance hat keine gültigen Chartdaten zurückgegeben."
        );

    }


    return data;

}


/*
 * Daten aus der Yahoo-Antwort extrahieren
 */

function processYahooData(data) {

    const result = data.chart.result[0];

    const meta = result.meta;


    const symbol =
        meta.symbol || "---";


    const price =
        meta.regularMarketPrice;


    const currency =
        meta.currency || "---";


    const previousClose =
        meta.previousClose;


    const marketTime =
        meta.regularMarketTime;


    return {

        symbol: symbol,

        price: price,

        currency: currency,

        previousClose: previousClose,

        marketTime: marketTime

    };

}


/*
 * Button
 */

fetchButton.addEventListener("click", async () => {

    const symbol = symbolInput.value;


    /*
     * UI zurücksetzen
     */

    output.textContent =
        `Lade ${symbol.toUpperCase()} ...`;

    statusElement.textContent =
        "Lade Daten...";


    statusDot.classList.remove("error");


    fetchButton.disabled = true;


    try {

        /*
         * Yahoo Finance abrufen
         */

        const data =
            await fetchYahooData(symbol);


        /*
         * Daten verarbeiten
         */

        const marketData =
            processYahooData(data);


        /*
         * Dashboard aktualisieren
         */

        assetElement.textContent =
            marketData.symbol;


        priceElement.textContent =
            marketData.price !== undefined
                ? marketData.price
                : "---";


        currencyElement.textContent =
            marketData.currency;


        previousCloseElement.textContent =
            marketData.previousClose !== undefined
                ? marketData.previousClose
                : "---";


        timestampElement.textContent =
            marketData.marketTime
                ? new Date(
                    marketData.marketTime * 1000
                  ).toLocaleString("de-DE")
                : "---";


        sourceElement.textContent =
            "Yahoo Finance";


        /*
         * Status
         */

        output.textContent =
            "Yahoo-Finance-Daten erfolgreich abgerufen.";


        statusElement.textContent =
            "Online";


        /*
         * komplette Antwort anzeigen
         */

        rawDataElement.textContent =
            JSON.stringify(data, null, 2);


        /*
         * Debugging
         */

        console.log("Verarbeitete Marktdaten:");
        console.log(marketData);


    } catch (error) {

        console.error(
            "Yahoo Finance Fehler:",
            error
        );


        output.textContent =
            "Fehler: " + error.message;


        statusElement.textContent =
            "Fehler";


        statusDot.classList.add("error");


        rawDataElement.textContent =
            error.stack || error.toString();


    } finally {

        fetchButton.disabled = false;

    }

});