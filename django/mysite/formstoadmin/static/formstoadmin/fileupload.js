$(document).ready(function(){
    function loadHandler(event) {
      var csv = event.target.result;
      processData(csv);
    }

    function processData(csv) {
        var allTextLines = csv.split(/\r\n|\n/);
        var lines = [];
        for (var i=0; i<allTextLines.length; i++) {
            var data = allTextLines[i].split(';');
                var tarr = [];
                for (var j=0; j<data.length; j++) {
                    tarr.push(data[j]);
                }
                lines.push(tarr);
        }
      console.log(lines);
    }

    var fileInput = document.getElementById('exampleFormControlFile1');
    var fileDisplayArea = document.getElementById('fileDisplayArea');

    fileInput.addEventListener('change', function(e) {
        var file = fileInput.files[0];
        var textType = /csv.*/;

        if (file.type.match(textType)) {
            var reader = new FileReader();

            reader.onload = function(e) {
                fileDisplayArea.innerText = reader.result;
            }

            reader.readAsText(file);
        } else {
            fileDisplayArea.innerText = "File not supported!"
        }
    });
})
