onload = async () => {
    let {results} = await chrome.storage.local.get({results: []})
    console.log(results)
    const clearBtn = document.querySelector('.clear-btn')

    let savedResults = results.map(result => {
            return `<tr>
                <td>${result.title}</td>
                <td>${result.hate_speech}</td>
                <td>${result.sentiment}</td>
                </tr>`
        }
    )

    if (savedResults.length) {
        document.querySelector('tbody').innerHTML = savedResults.join('')
        clearBtn.disabled = false
        clearBtn.addEventListener('click', clear)
    }

}

function clear() {
    this.disabled = true
    chrome.storage.local.set({results: []})
    document.querySelector('tbody').innerHTML = '<tr><td>No Headlines</td><td>No hate</td><td>No sentiment</td></tr>'
}