/**
 * add a selection field to the /compare plot.
 */
function addField() {
  let selector = document.getElementById("selectors");
  let additional_selector = document.createElement("div");
  let index = document.getElementsByClassName("selector").length;
  let id = `selector_${index + 1}`;
  additional_selector.innerHTML = `
      <div id="${id}" class="selector">
        <label for="station">Station:</label>
          <select id="station" class="station" onchange="updatePlot()">
            <option value="1">Station 1 - Schloßbrücke</option>
            <option value="2">Station 2 - Berliner Platz</option>
            <option value="3">Station 3 - Leineweber Straße</option>
            <option value="4">Station 4 - Forumsgebäude</option>
            <option value="5">Station 5- Forumsgebäude Brücke</option>
            <option value="6">Station 6 - Dickswall</option>
            <option value="7">Station 7 - Buggenbeck</option>
            <option value="8">Station 8 - Essener Straße</option>
            <option value="9">Station 9 - Hölterstraße</option>
            <option value="10">Station 10 - Walkmühlenstraße</option>
            <option value="11">Station 11 - Rumbachtal Kreuzung</option>
            <option value="12">Station 12 - Rumbachtal</option>
          </select>
        <label for="param">Parameter:</label>
          <select id="param" class="param" onchange="updatePlot()">
            <option value="lufttemp_200">Lufttemperatur 2 m</option>
            <option value="lufttemp_5">Lufttemperatur 0,05 m</option>
            <option value="relhum">rel. Feuchte 0,05 m</option>
            <option value="oberfl_temp_unten">Oberfl. Temperatur unten</option>
            <option value="oberfl_temp_oben">Oberfl. Temperatur oben</option>
            <option value="oberfl_temp_links">Oberfl. Temperatur Nord</option>
            <option value="oberfl_temp_rechts">Oberfl. Temperatur Süd</option>
            <option value="windgeschw_5">Windgeschwindigkeit 0,05 m</option>
            <option value="windgeschw_200">Windgeschwindigkeit 2 m</option>
          </select>
        <label for="plot_axis_0">Y-Achse:</label>
        <select id="plot_axis_${index}" onchange="updatePlot()">
          <option value="y1">links</option>
          <option value="y2" selected="selected">rechts</option>
        </select>
        <button type="button" class="btn btn-danger btn-sm" onclick="removeField('${id}');">X</button>
      </div>`;
  selector.appendChild(additional_selector);
}

/**
 * remove a field from the /compare plot and update the plot.
 *
 * @param {string} id - the id of the field to remove
 */
function removeField(id) {
  let to_remove = document.getElementById(id);
  to_remove.parentNode.removeChild(to_remove);
  updatePlot();
}

/**
 * create an info panel on the / page with all plots for all parameters
 *
 * @param {event} e
 */
function createInfoPane(e) {
  let map = document.getElementById("map_row");
  let info_html = `
    <div class="info-box">
        <button type="button" class="btn btn-light" onclick="removeInfoPane();">X</button>
        <h3 style="text-align: center;">Station Nr. ${e.layer.feature.properties.station} - ${e.layer.feature.properties.name}</h3>
        <div class="text-center addScroll" style="height: 600px;">
          <p>Lufttemperatur 2 m [°C]<p>
          <div class="m-2" id="temperature"></div>
          <h5>Relative Feuchte [%]<p>
          <div class="m-2" id="relhum"></div>
          <p>Oberflächentemperatur [°C]</p>
          <div class="m-2" id="surf_temp"></div>
          <p>Windgeschwindigkeit [m/s]</p>
          <div class="m-2" id="wind_speed"><div>
          <p>Windrichtungshäufigkeit [%]</p>
          <div class="m-2" id="wind_dir"><div>
        </div>
    </div>
      `;
  if (document.getElementById("info_pane") == null) {
    let info = document.createElement("div");
    info.className = "col-lg-5";
    info.id = "info_pane";
    info.innerHTML = info_html;
    map.appendChild(info);
  } else {
    let info = document.getElementById("info_pane");
    info.innerHTML = info_html;
  }
}

/**
 * close the info panel and update the map.
 */
function removeInfoPane() {
  let to_remove = document.getElementById("info_pane");
  to_remove.parentNode.removeChild(to_remove);
  map.invalidateSize();
}

/**
 * call the API for data for one station for one parameter
 *
 * @param {integer} station - the station number
 * @param {string} param - the parameter id as specified in the db
 * @returns - a json object with all data fields needed to create a plot
 */
async function getData(station, param) {
  let request = "/api/data?station=" + station + "&param=" + param;
  let data = fetch(request).then((response) => {
    return response.json()
  })
  return data;
}

/**
 * call the API to get wind data. The data is returned as an array of objects
 * one object for each wind speed class.
 *
 * @param {integer} station - the station number
 * @returns {array[object, ...]}
 */
async function getWindData(station) {
  let request = "/api/data/wind?station=" + station;
  let data = fetch(request).then((response) => {
    return response.json()
  })
  return data;
}

/**
 * create all plots for the info panel for one station
 *
 * @param {integer} station - the station number
 */
async function createPlot(station) {
  let temp_200 = getData(station, "lufttemp_5");
  let temp_5 = getData(station, "lufttemp_200");
  let relhum = getData(station, "relhum");
  let surf_temp_top = getData(station, "oberfl_temp_unten");
  let surf_temp_bot = getData(station, "oberfl_temp_oben");
  let surf_temp_left = getData(station, "oberfl_temp_links");
  let surf_temp_right = getData(station, "oberfl_temp_rechts");
  let wind_speed_200 = getData(station, "windgeschw_200");
  let wind_speed_5 = getData(station, "windgeschw_5");
  let wind_dir = getWindData(station);
  let config = { responsive: true };
  let layout = {
    xaxis: {
      title: "Datum",
      tickformat: "%Y~%m~%d %H:%M",
      tickangle: 15,
    },
    yaxis: {
      title: "",
    },
    height: 250,
    margin: {
      l: 40,
      r: 40,
      b: 10,
      t: 10,
      pad: 4,
    },
    showlegend: true,
    legend: {
      orientation: "h",
      x: 0.5,
      y: -0.5,
      xanchor: "center",
    },
  };
  let layout_temp = layout;
  layout_temp.yaxis.title = temp_200.unit;
  Plotly.newPlot("temperature", [await temp_200, await temp_5], layout_temp, config);
  let layout_relhum = layout;
  layout_temp.yaxis.title = relhum.unit;
  Plotly.newPlot("relhum", [await relhum], layout_relhum, config);
  let layout_surf_temp = layout;
  layout_surf_temp.yaxis.title = surf_temp_top.unit;
  layout_surf_temp.height = 300;
  Plotly.newPlot(
    "surf_temp",
    [await surf_temp_top, await surf_temp_bot, await surf_temp_left, await surf_temp_right],
    layout_surf_temp,
    config
  );
  let layout_wind_speed = layout;
  layout_wind_speed.yaxis.title = wind_speed_200.unit;
  Plotly.newPlot(
    "wind_speed",
    [await wind_speed_200, await wind_speed_5],
    layout_wind_speed,
    config
  );

  let layout_wind_dir = {
    margin: {
      l: 40,
      r: 40,
      b: 10,
      t: 10,
      pad: 4,
    },
    legend: {
      orientation: "h",
      x: 0.5,
      xanchor: "center",
    },
    polar: {
      barmode: "overlay",
      bargap: 0,
      radialaxis: { ticksuffix: "%", angle: 45, dtick: 20 },
      angularaxis: { direction: "clockwise" },
    },
  };
  Plotly.newPlot("wind_dir", await wind_dir, layout_wind_dir);
}
