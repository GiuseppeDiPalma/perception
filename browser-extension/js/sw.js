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
        console.log(json)
    } 
    catch (error) {
        console.log(error)
    }
})