chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log(request)
    chrome.storage.local.set({newTitles: request.newTitles}).then(sendTitles)
})

async function sendTitles() {
    let {newTitles} = await chrome.storage.local.get({newTitles: []})
    if(!newTitles.length) return console.log('No new titles')

    try {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({titles: newTitles})
        }

        let response = await fetch('http://localhost:3000/titles', options)
        let json = await response.json()

        if (json.success) {
            let {titles} = await chrome.storage.local.get({titles: []})
            titles = [...titles, ...newTitles]

            chrome.storage.local.set({titles, newTitles: []})
            console.log('✅ Titles sent')
        }
        else {
            console.log('❌ Titles not sent', json)
        }
    } 
    catch (error) {
        console.log(error)
    }
}