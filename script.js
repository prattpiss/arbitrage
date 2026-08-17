```javascript
const fetchButton = document.getElementById("fetchButton");

const output = document.getElementById("output");

const assetElement = document.getElementById("asset");
const priceElement = document.getElementById("price");
const timestampElement = document.getElementById("timestamp");


fetchButton.addEventListener("click", () => {

    output.textContent = "JavaScript funktioniert!";

    assetElement.textContent = "TEST";
    priceElement.textContent = "100.00";
    timestampElement.textContent = new Date().toLocaleString("de-DE");

});
```
