
// save previous resize function if it existed
var previous_resize = window.onresize;

// setting new resize function
window.onresize = resize;


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
            var append_to = "#" + zeeguu_graph.getAttribute("id");
            // line graph resizing (1200 px for full year , 100 px per month)
            var months_to_show = Math.min(12, Math.round(width / 100));
            zeeguu_graph.setAttribute("months_to_show", months_to_show);
            var temp_input_data = zeeguu_graph.getAttribute("input_data");
            display_months(months_to_show, append_to, window[temp_input_data]);
        }
    }
    // end of line graph resizing
}

// function for redrawing line graph
function display_months(months_to_show, append_to, input_data){
    var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);

    d3.selectAll(append_to + ' > svg').remove();
    line_graph(input_data, append_to, width, months_to_show);
}

// increasing/decreasing month amount displayed
function change_months_showed_by_x_amount (append_to, input_data, amount){
    var zeeguu_graph = document.getElementById(append_to);
    var months_to_show = parseInt(zeeguu_graph.getAttribute("months_to_show")) + parseInt(amount);

    if (isNaN(months_to_show)){
        months_to_show = 11;
    }

    months_to_show = Math.max(5, months_to_show);

    zeeguu_graph.setAttribute("months_to_show", months_to_show);
    display_months(months_to_show, "#"+append_to, input_data);
}


