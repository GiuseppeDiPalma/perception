const capitalize = (str) => {
    return `${str[0].toUpperCase()}${str.slice(1)}`
}

addEventListener('load', async () => {
    let {results} = await chrome.storage.local.get({results: []})


    let headlines = document.querySelectorAll('h3')
    let newTitles = []

    for (const headline of headlines) {
        let title = headline.innerText.trim()
        let result = results.find(result => result.title.trim() === title.trim())

        if (result) {
            let sentiment = capitalize(result.sentiment.toLowerCase())
            if (result.hate_speech === "NO HS") {
                headline.style = 'border: 2px solid green;display: flex;flex-direction: column;'
                headline.insertAdjacentHTML('beforeend', `<strong style="align-self: end;border-top: 2px solid green;border-left: 2px solid green;">${sentiment}</strong>`)
            } else { 
                headline.style = 'border: 2px solid red;display: flex;flex-direction: column;'
                headline.insertAdjacentHTML('beforeend', `<strong style="align-self: end;border-top: 2px solid red;border-left: 2px solid red;">${sentiment}</strong>`)
            }
        } else {
            newTitles.push(title)
        }
    }

    if (newTitles.length) {
        chrome.runtime.sendMessage({newTitles})
    }
})
