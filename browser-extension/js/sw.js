chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
    try {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({titles: request.newTitles})
        }

        let response = await fetch('http://localhost:5000/titles', options)
        let json = await response.json()

        let titles = json.title_list
        let results = json.engine_results

        chrome.storage.local.set(titles)
        chrome.storage.local.set(results)
    } catch (error) {
        console.log(error)
    }
})