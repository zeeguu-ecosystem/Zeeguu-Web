
// save previous resize function if it existed
var previous_resize = window.onresize;

// setting new resize function
window.onresize = resize;

// goes through all the <zeeguu_graph> tags on the page and for each,
// if it has autoresize, then it resizes to the current window size.
function resize() {
    // call previous resize function if it existed
    if (previous_resize != null) {
        previous_resize();
    }

    var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    var all_zeeguu_graphs = document.getElementsByTagName("zeeguu_graph");

    for(var i = 0;i<all_zeeguu_graphs.length;i++){
        var zeeguu_graph = all_zeeguu_graphs[i];
        var autoresize = zeeguu_graph.getAttribute("autoresize");
        if(autoresize == "true"){
            // resize the graph
            var element_id = zeeguu_graph.getAttribute("id");
            // line graph resizing (1200 px for full year , 100 px per month)
            var months_to_show = zeeguu_graph.getAttribute("months_to_show");
            months_to_show = Math.min(Math.min(12, Math.round(width / 100)), months_to_show);
            var input_data = zeeguu_graph.getAttribute("input_data");
            redraw_line_graph(months_to_show, element_id, window[input_data]);
        }
    }
    // end of line graph resizing
}

// function for redrawing line graph
// element_id is the ID of the zeeguu_graph tag
function redraw_line_graph(months_to_show, element_id, input_data){
    var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    d3.selectAll("#" + element_id + ' > svg').remove();
    line_graph(input_data, "#" + element_id, width, months_to_show);
}

