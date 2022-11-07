addEventListener('load', () => {
    let headlines = document.querySelectorAll('h3')
    
    let newTitles = []
    
    for (const headline of headlines) {
        headline.style = 'border: 2px solid green;display: flex;flex-direction: column;'
        headline.insertAdjacentHTML('beforeend', `<strong style="align-self: end;border-top: 2px solid green;border-left: 2px solid green;">Not Suspicious</strong>`)
    
        newTitles.push(headline.innerText)
    }

    chrome.runtime.sendMessage({newTitles})
})
