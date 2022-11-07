onload = async () => {
    let {titles, newTitles} = await chrome.storage.local.get({titles: [], newTitles: []})

    let allTitlesEl = document.querySelector('.all-titles .card-title')
    let sentTitlesEl = document.querySelector('.sent-titles .card-title')

    allTitlesEl.innerText = (titles.length + newTitles.length).toLocaleString()
    sentTitlesEl.innerText = (titles.length).toLocaleString()

    let optionsBtn = document.querySelector('.options-btn')
    optionsBtn.addEventListener('click', () => {
        chrome.runtime.openOptionsPage()
    })
}