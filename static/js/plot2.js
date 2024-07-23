var columnIndex;
var columnIndex2;

document.getElementById('column-selector').addEventListener('change', function() {
    columnIndex = this.selectedIndex;
});

document.getElementById('column-selector2').addEventListener('change', function() {
    columnIndex2 = this.selectedIndex;
});

document.getElementById('plot-button').addEventListener('click', function() {
    plotGraph(columnIndex, 'graph', 'DEPT', document.getElementById('column-selector').value);
});

document.getElementById('plot-button2').addEventListener('click', function() {
    plotGraph(columnIndex2, 'graph2', 'DEPT', document.getElementById('column-selector2').value);
});

document.getElementById('add-graph-button').addEventListener('click', function() {
    document.getElementById('second-graph-container').style.display = 'block';
    this.style.display = 'none';
});

function plotGraph(index, containerId, xAxisLabel, yAxisLabel) {
    var deptData = [];
    var otherData = [];

    var table = document.getElementById('data-table');
    for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i];
        var deptValue = parseFloat(row.cells[1].innerHTML);
        var otherValue = parseFloat(row.cells[index].innerHTML);

        deptData.push(deptValue);
        otherData.push(otherValue);
    }

    var trace = {
        x: deptData,
        y: otherData,
        mode: 'lines',
        type: 'scatter'
    };

    var layout = {
        xaxis: {
            title: {
                text: xAxisLabel,
                font: {
                    family: 'Verdana',
                    size: 16,
                    color: '#007bff'
                }
            }
        },
        yaxis: {
            title: {
                text: yAxisLabel,
                font: {
                    family: 'Verdana',
                    size: 16,
                    color: '#007bff'
                }
            }
        }
    };

    var data = [trace];

    Plotly.newPlot(containerId, data, layout);
}
