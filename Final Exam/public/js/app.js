const startYear = 1900;
const endYear = 2000;
const censusInterval = 10;

String.prototype.strip = function(characters) {
  let str = this;
  for (let i = 0; i < characters.length; ++i) {
    str = str.replace(new RegExp(`^[${characters}]+|[${characters}]+$`), "");
  }
  return str;
};

$(function() {
  "use strict";

  $("#name-not-found")
    .parent()
    .hide();

  google.charts.load("current", { packages: ["corechart"] });
  google.charts.setOnLoadCallback(function() {
    const options = {
      hAxis: {
        format: "none"
      },
      height: 400,
      title: "Name Rankings",
      vAxis: { title: "Rank", direction: -1 },
      width: 600
    };
    const chart = new google.visualization.LineChart($("#graph")[0]);
    const chartData = [["Year"]];
    for (let i = startYear; i <= endYear; i += censusInterval) {
      chartData.push([i]);
    }

    $("#search").on("change", function(event) {
      var name = event.target.value;
      $.ajax({
        url: "names/" + name,
        method: "GET",
        data: JSON
      }).done(function(rawData) {
        if (rawData) {
          rawData = JSON.parse(rawData);
          $("#name-not-found")
              .parent()
              .hide();
          $("#search").removeClass("has-error");
        //Map name data provided by the server in the form:
        // {
        //   name: "name",
        //   ratings: [
        //     1900 rating,
        //     1910 rating,
        //     1920 rating,
        //     1930 rating,
        //     1940 rating,
        //     1950 rating,
        //     1960 rating,
        //     1970 rating,
        //     1980 rating,
        //     1990 rating,
        //     2000 rating
        //   ]
        // }
        //to an array that google charts can work with, namely:
        //[
        //  ["Year", name0, name1, etc.],
        //  ["1900", name0 rating for 1900, name1 rating for 1900, etc.],
        //  ["1910", name0 rating for 1910, name1 rating for 1910, etc.],
        //  ...
        //  ["2000", name0 rating for 2000, name1 rating for 2000, etc.]
        //]

        chartData[0].push(rawData.name);
        if (chartData.length !== (rawData.ratings).length + 1) {
          throw new RangeError(
            "Invalid data received from server! Incorrect number of ratings provided."
          );
        }
        for (let i = 1; i < chartData.length; ++i) {
          chartData[i].push(rawData.ratings[i - 1]);
        }
        chart.draw(google.visualization.arrayToDataTable(chartData), options);
        }
        else {
          $("#name-not-found")
              .text("No entered names found")
              .parent()
              .show();
          $("#search").addClass("has-error");
        }
      });
    });
  });
});

// function randomData(name) {
//   function randomRank() {
//     return Math.floor(Math.random() * 1000);
//   }
//   const years = [];
//   for (let i = startYear; i <= endYear; i += censusInterval) {
//     years.push(randomRank());
//   }
//   return `["${name}", ${years.join(", ")}]`;
// }
