onload = async () => {
    let {titles, newTitles} = await chrome.storage.local.get({titles: [], newTitles: []})
    console.log(titles, newTitles)
    
    let {results} = await chrome.storage.local.get({results: []})
    console.log(results)
    
    let allTitlesHs = document.querySelector('.all-titles-hs .card-title')
    let allTitleNoHs = document.querySelector('.all-titles-no-hs .card-title')
    
    let allTitlesEl = document.querySelector('.all-titles .card-title')
    let sentTitlesEl = document.querySelector('.sent-titles .card-title')

    let sentimentPositiveTitle = document.querySelector('.positive-sentiment .card-title')
    let sentimentNegativeTitle = document.querySelector('.negative-sentiment .card-title')
    let sentimentNeutralTitle = document.querySelector('.neutral-sentiment .card-title')
    let sentimentMixedTitle = document.querySelector('.mixed-sentiment .card-title')

    // get results from storage
    allTitlesEl.innerText = (titles.length + newTitles.length).toLocaleString()
    sentTitlesEl.innerText = (titles.length).toLocaleString()
    
    // number of hs/no hs titles
    let noHsTitles = results.filter(result => result.hate_speech === "NO HS")
    allTitleNoHs.innerText = noHsTitles.length
    let hsTitles = results.filter(result => result.hate_speech === "HS")
    allTitlesHs.innerText = hsTitles.length
    // number of sentiment for types
    let sentimentPositive = results.filter(result => result.sentiment === "POSITIVE")
    sentimentPositiveTitle.innerText = sentimentPositive.length
    let sentimentNegative = results.filter(result => result.sentiment === "NEGATIVE")
    sentimentNegativeTitle.innerText = sentimentNegative.length
    let sentimentNeutral = results.filter(result => result.sentiment === "NEUTRAL")
    sentimentNeutralTitle.innerText = sentimentNeutral.length
    let sentimentMixed = results.filter(result => result.sentiment === "MIXED")
    sentimentMixedTitle.innerText = sentimentMixed.length


    // serve solo per aprire pagina options
    let optionsBtn = document.querySelector('.options-btn')
    optionsBtn.addEventListener('click', () => {
        chrome.runtime.openOptionsPage()
    })
}