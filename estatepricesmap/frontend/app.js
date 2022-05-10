import {GoogleMapsOverlay as DeckOverlay} from '@deck.gl/google-maps';
import {ColumnLayer} from '@deck.gl/layers';
import {HexagonLayer} from '@deck.gl/aggregation-layers';
import {mean, quantileSeq, min, max} from 'mathjs';

require('file-loader?name=[name].[ext]!./index.html');
// Set your Google Maps API key here or via environment variable
const GOOGLE_MAPS_API_KEY = "AIzaSyAKcerlw9vs-spzoGujzVmGNNDcNwMLGbs"; // eslint-disable-line
const GOOGLE_MAP_ID = 'f52ed2dd8b0fe113'; // eslint-disable-line
const GOOGLE_MAPS_API_URL = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&v=beta&map_ids=${GOOGLE_MAP_ID}`;


function loadScript(url) {
  let script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = url;
  let head = document.querySelector('head');
  head.appendChild(script);
  return new Promise(resolve => {
    script.onload = resolve;
  });
}


function loadMap(response){
  let responseParsed = response;
  let pricesqmArray= responseParsed.map(element => element.pricesqm);
  let pricesqmArrayQuantiles = {
    lowerTen : quantileSeq(pricesqmArray, 0.1),
    lowerTwenty : quantileSeq(pricesqmArray, 0.2),
    half : quantileSeq(pricesqmArray, 0.5),
    higherTwenty : quantileSeq(pricesqmArray, 0.8),
    higherTen : quantileSeq(pricesqmArray, 0.5)
  };
  let latArray = responseParsed.map(element => element.lat);
  let lngArray = responseParsed.map(element => element.lng);
  let centerLat = quantileSeq(latArray, 0.5);
  let centerLng = quantileSeq(lngArray, 0.5);

  loadScript(GOOGLE_MAPS_API_URL).then(() => {
    let map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: centerLat, lng: centerLng},
      zoom: 13,
      tilt: 45,
      heading: 0,
      mapId: GOOGLE_MAP_ID
    });
  
    let overlay = new DeckOverlay({
      layers: [
        new HexagonLayer({
          id: 'column-layer',
          data: responseParsed,
          filled: true,
          radius: 30,
          extruded: true,
          pickable: true,
          elevationScale: 100,
          getPosition: d => [d.lng, d.lat],
          getFillColor: d => adjustFillColor(d.pricesqm, pricesqmArrayQuantiles),
          getLineColor: [0, 0, 0],
          getElevation: d => d.pricesqm/5000,
          autoHighlight: true,
          onClick: info => info.object && window.open(info.object.link, '_blank'),
        })
      ],
      getTooltip: ({object}) => object && {
        html: 
          `<div style="display:grid; grid-template-columns: 100px 130px;>
              <div style="float:left;">
                <img src='${object.picture}' style="width:90px; height:100px; border-radius:5px">
              <div>
              <div>
                <p>${object.location}</p>
                <p>CENA ZA M^2: <b>${object.pricesqm} ZŁ</b></p>
              </div>
          </div>`,
        style: {
          'border-radius' : '5px',
        },
      },
    });
  
    overlay.setMap(map);
  });
}


function adjustFillColor(pricesqm, pricesqmArrayQuantiles){
  let returnColor = [];
  switch(true){
    case pricesqm <= pricesqmArrayQuantiles.lowerTen:
      returnColor.push(1, 152, 189);
    case pricesqmArrayQuantiles.lowerTen < pricesqm && pricesqm <= pricesqmArrayQuantiles.lowerTwenty:
      returnColor.push(73, 227, 206);
    case pricesqmArrayQuantiles.lowerTwenty < pricesqm && pricesqm <= pricesqmArrayQuantiles.half:
      returnColor.push(216, 254, 181);
    case pricesqmArrayQuantiles.half < pricesqm && pricesqm <= pricesqmArrayQuantiles.higherTwenty:
      returnColor.push(254, 237, 177);
    case pricesqmArrayQuantiles.higherTwenty < pricesqm && pricesqm <= pricesqmArrayQuantiles.higherTen:
      returnColor.push(254, 173, 84);
    case pricesqmArrayQuantiles.higherTen < pricesqm:
      returnColor.push(209, 55, 78);
  }
  return returnColor;
}


window.showOffers = function(inputId) {
  let city = String(document.getElementById(inputId).value);
  fetch(`http://estateprices.martyngodlewski.com/api/?city=${city}`)
    .then(async response => {
      let contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        let data = await response.json();
        loadMap(data);
        if(document.getElementById("displayError").innerText != ''){
          document.getElementById("displayError").innerText = '';
        }
      } else {
        let text = await response.text();
        document.getElementById("displayError").innerText = text;
      }})
    .catch(async error => console.log(error));
};


window.addEventListener("keydown", (event) =>{
  if(event.key == "Enter"){
    event.preventDefault;
    setTimeout(document.getElementById("searchBttn").click());
  }
});