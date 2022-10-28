onload = async () => {
    let results = []

    try {
        let response = await fetch('https://localhost:3000/results')
        let data = await response.json()

        console.log(data)

        if(data.success) {
            results = data.results.map(result => `<tr><td>${result}</td></tr>`)
        }
    } 
    catch (error) {
        console.log(error)
    }

    if(results.length) { // if there are results received from the server show them
        document.querySelector('tbody').innerHTML = results.join('')
    }
    else {
        let {titles, newTitles} = await chrome.storage.local.get({titles: [], newTitles: []})
    
        let titlesMarkup = titles.map(title => `<tr><td>${title}</td></tr>`)
        let newTitlesMarkup = newTitles.map(title => `<tr><td>${title}</td></tr>`)
    
        if(titlesMarkup.length || newTitlesMarkup.length) {
            document.querySelector('tbody').innerHTML = titlesMarkup.join('') + newTitlesMarkup.join('')
        }
    }
}