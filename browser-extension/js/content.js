addEventListener('load', async () => {
    let {results} = await chrome.storage.local.get({results: []})
    
    let headlines = document.querySelectorAll('h3')
    let newTitles = []
    
    for (const headline of headlines) {
        let title = headline.innerText.trim()
        let result = results.find(result => result.title === title)

        if (result) {
            headline.style = 'border: 2px solid green;display: flex;flex-direction: column;'
            headline.insertAdjacentHTML('beforeend', `<strong style="align-self: end;border-top: 2px solid green;border-left: 2px solid green;">${result.hate_speech}</strong>`)    
        }
        else {
            newTitles.push(title)
        }
    }

    if (newTitles.length) {
        chrome.runtime.sendMessage({newTitles})
    }
})
