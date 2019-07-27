function buildPlot() {
    /* data route */
  var url = "/movies_api";

  d3.json(url).then(function(response) {

    console.log(response);

    var movie = response.map(row => row.movie);
    var gross = response.map(row => row.gross);
    var like_count = response.map(row => row.like_count);

   console.log(movie);
   console.log(gross);
   console.log(like_count);

    var trace = {
        x : like_count, 
        y : gross,
        text: movie,
        mode: 'markers',
        type: 'scatter'
    };

    var data = [trace];

    var layout = {
        title: "Youtube Like Count vs Movie Gross (2018)", 
        xaxis: { title: "Youtube Like Count",  automargin: true, ticks: "outside"},
        yaxis: { title: "Movie Gross ($)"},
    };
   
    Plotly.newPlot("plot", data, layout);
    });
};

buildPlot();
