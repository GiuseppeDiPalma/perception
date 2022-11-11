onload = async () => {
    let {results} = await chrome.storage.local.get({results: []})
    const clearBtn = document.querySelector('.clear-btn')
    let rows = []

    console.log("Provo retrive dati...")
    try {
        console.log("Dentro-1")
        let response = await fetch('http://localhost:5000/results')
        let json = await response.json()
        console.log(json)

        if (json.success) {
            results.push(...json.results)
            chrome.storage.local.set({results})

            rows = json.results.map(result => {
                return `<tr>
                    <td>${result.title}</td>
                    <td>${result.hate_speech}</td>
                    <td>${result.sentiment}</td>
                    </tr>`
                }
            )
        }
    }
    catch (error) {
        console.log(error)
    }

    if (rows.length) { // if there are results received from the server show them
        document.querySelector('tbody').innerHTML = rows.join('')
        
        clearBtn.disabled = false
        clearBtn.addEventListener('click', clear)
    }
    else {
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
}

function clear() {
    this.disabled = true
    chrome.storage.local.set({results: []})
    document.querySelector('tbody').innerHTML = '<tr><td>No Headlines</td><td>No hate</td><td>No sentiment</td></tr>'
}