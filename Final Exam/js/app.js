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

    $("#search").on("change", function(event) {
      $.ajax({
        url: DEBUG ? "sample-data.json" : "names",
        method: "GET",
        data: event.target.value.strip(", ").split(/, */),
        dataType: "json"
      }).done(function(rawData) {
        if (rawData == "No entered names found") {
          $("#name-not-found")
            .text("No entered names found")
            .parent()
            .show();
          $("#search").addClass("has-error");
        } else {
          $("#name-not-found")
            .parent()
            .hide();
          $("#search").removeClass("has-error");
        }

        //Map an array of name data (a name datum being in the form: [name, 1900 rating, 1910 rating, etc.])
        //to an array that google charts can work with, namely:
        //[
        //  ["Year", name0, name1, etc.],
        //  ["1900", name0 rating for 1900, name1 rating for 1900, etc.],
        //  ["1910", name0 rating for 1910, name1 rating for 1910, etc.],
        //  ...
        //  ["2000", name0 rating for 2000, name1 rating for 2000, etc.]
        //]
        const formattedData = [["Year"]];
        for (let i = startYear; i <= endYear; i += censusInterval) {
          formattedData.push([i]);
        }
        rawData.forEach(function(name, index, array) {
          formattedData[0].push("" + name[0]);
          for (let i = 1; i < name.length; ++i) {
            formattedData[i].push(name[i] || 1001);
          }
        });
        chart.draw(google.visualization.arrayToDataTable(formattedData), options);
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
