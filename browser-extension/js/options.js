onload = async () => {
    let {titles, newTitles} = await chrome.storage.local.get({titles: [], newTitles: []})

    let titlesMarkup = titles.map(title => `<tr><td>${title}</td></tr>`)
    let newTitlesMarkup = newTitles.map(title => `<tr><td>${title}</td></tr>`)

    if(titlesMarkup.length || newTitlesMarkup.length) {
        document.querySelector('tbody').innerHTML = titlesMarkup.join('') + newTitlesMarkup.join('')
    }
}