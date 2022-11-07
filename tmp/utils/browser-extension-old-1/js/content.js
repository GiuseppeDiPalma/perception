let headlines = document.querySelectorAll('h3')

let newTitles = []

for (const headline of headlines) {
    headline.style.border = '2px solid green'
    newTitles.push(headline.innerText)
}

chrome.runtime.sendMessage({newTitles})