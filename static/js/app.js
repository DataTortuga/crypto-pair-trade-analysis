// const data_loc = 'samples.json';


// Function updates Demographic info panel when subject id is changed
// function update_panel(index, data) {

//     var sample_panel = d3.select('#sample-metadata')
//     sample_panel.selectAll('ul').remove()
//     sample_panel.append('ul')

//     var panel_list = sample_panel.select('ul')
//     panel_list.append('li').text('ID: ' + data.metadata[index].id);
//     panel_list.append('li').text('Ethnicity: ' + data.metadata[index].ethnicity);
//     panel_list.append('li').text('Gender: ' + data.metadata[index].gender);
//     panel_list.append('li').text('Age: ' + data.metadata[index].age);
//     panel_list.append('li').text('Location: ' + data.metadata[index].location);
// }

// // Function updates plotly graph when subject id is changed
// function update_plot(index, data) {
 
//     otu_value = data.samples[index].sample_values.slice(0, 10);
//     otu_id = data.samples[index].otu_ids.slice(0,10);
//     otu_label = data.samples[index].otu_labels.slice(0,10);

//     otu_id1 = [];
//     for (let i = 0; i < otu_id.length; i++) {
//         otu_id1.push('OTU_ID: ' + otu_id[i])
//     }

//     let trace1 = {
//         x: otu_value,
//         y: otu_id1,
//         text: otu_label,
//         type: 'bar',
//         orientation: 'h'
//     };
      
//     otu_value = data.samples[index].sample_values;
//     otu_id = data.samples[index].otu_ids;
//     otu_label = data.samples[index].otu_labels;

//     let trace2 = {
//         x: otu_id,
//         y: otu_value,
//         mode: 'markers',
//         text: otu_label,
//         marker: {
//         size: otu_value,
//         color: otu_id
//         }
//     };

//     let data1 = [trace1];
//     let data2 = [trace2];
      
//     let layout = {
//         title: "Belly Button Creatures",
//         showgrid: true,
//         showticklabels: true,
//         showline: true
//     };
      
//     Plotly.newPlot("bar", data1, layout);
//     Plotly.newPlot("bubble", data2, layout);
// }

// Defines what to do when subject ID is changed
function optionChanged(sam_id) {
    d3.json(`/pair/${sam_id}`).then(function (data) {
        console.log(data)
        let trace = {
        x: [Array(data.length).keys()],
        y: data,

        type: 'line',

    };
    let ret_data = [trace]
        Plotly.newPlot("plot",ret_data)
    })
}

// Initializes webpage with data
function init() {
    for (let i = 0;  i < 10; i++) {
        select.append('option').text(i)
    }
    update_panel(0, data)
    update_plot(0, data)

}

init()
