document.addEventListener('DOMContentLoaded', function() {
    var deptData = [];
    var otherData = [];

    var table = document.getElementById('data-table');
    if (!table) {
        console.error('Таблица не найдена!');
        return;
    }

    for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i];
        var deptValue = parseFloat(row.cells[0].innerHTML);
        var otherValue = parseFloat(row.cells[1].innerHTML);

        deptData.push(deptValue);
        otherData.push(otherValue);
    }

    console.log('deptData:', deptData);
    console.log('otherData:', otherData);

    if (deptData.length === 0 || otherData.length === 0) {
        console.warn('Нет данных для построения графика!');
        return;
    }

    var trace = {
        x: deptData,
        y: otherData,
        mode: 'lines',
        type: 'scatter'
    };

    var data = [trace];

    Plotly.newPlot('graph', data);
});
