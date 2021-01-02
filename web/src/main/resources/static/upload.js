const url = 'http://localhost:8080/upload';

const handleImageUpload = event => {
  let pre = document.getElementById('output');
  pre.textContent = '';

  const files = event.target.files
  const formData = new FormData()
  formData.append('file', files[0])
  
  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then(function (response) {
    return response.json();
  }) 
  .then(function (result) {
    console.log(result)
    // adapted from https://stackoverflow.com/questions/38380462/syntaxerror-unexpected-token-o-in-json-at-position-1
    var jsonData = JSON.parse(JSON.stringify(result));
    var text = ''
    for (var i = 0; i < jsonData.length; i++) {
        var rank = jsonData[i];
        text += (rank.rank + '. ' +  rank.result + '\n')

    }
    pre.textContent = text;
  })
  .catch(function (error) {
    console.error(error)
  })

  let reader = new FileReader();
  reader.onload = function() {
    document.getElementById("imageThumb").src = reader.result;
  };

  if(files[0]) {
    reader.readAsDataURL(files[0]);
  }
}

document.querySelector('#imageUpload').addEventListener('change', event => {
  handleImageUpload(event)
})