function showSearch() {
    const element = document.getElementById('search-list');
    element.style.display = 'inline'

}

function hideSearch() {
    const element = document.getElementById('search-list');
    element.style.display = 'none'
}

function getValue() {
    const carList = ['TOYOTA58', 'TOYOTA59', 'TOYOTA60', 'TOYOTA62', 'TOYOTA63', 'TOYOTA64', 'TOYOTA66', 'TOYOTA67', 'TOYOTA68', 'TOYOTA70', 'TOYOTA75', 'TOYOTA78', 'TOYOTA79', 'TOYOTA82', 'TOYOTA84', 'TOYOTA85', 'TOYOTA86', 'TOYOTA87', 'TOYOTA88', 'TOYOTA89', 'TOYOTA90', 'TOYOTA91', 'TOYOTA92', 'TOYOTA93', 'TOYOTA95', 'EL7S234', 'EL7S238', 'EL7S239', 'EL7S240', 'EL7S241', 'EL7S236', 'EL7S242', 'EL7S237', 'EL7S233', 'EL7S235', 'EL7S243', 'EL7S244', 'EL7S245', 'EL7S246', 'EL1T890', 'WY6794L', 'WY6795L', 'WY6796L', 'WY6797L', 'WY6798L', 'WY6799L', 'WY9392K', 'WY9794K', 'WY9544K', '34BYS070', '34BYT370', '34BYU787', '34BYU794', '51G67188', 'ABF8551', 'B-2797-PKA', 'CZU60P', 'THA-8937', 'THA-3253', 'TWN-0755', '539ZWU', 'E43BAR', 'FRN-0681', 'FZT-6579', 'KGCT-50', 'CW24YYGP', 'CW24ZFGP', 'B038HT799', 'B060HT799', 'B087HT799', 'O527MH799', 'O690MH799', 'O789MH799', 'O789MH799'];
    carList.sort()
    const regions = ['us', 'eu', 'apac', 'lam', 'zaf', 'rus&ukr']
    const element = document.getElementById('search').value.toUpperCase();
    const carsList = document.getElementById('search-car-lists');
    carsList.innerHTML = ''
    let listt = carList.filter((item) => item.includes(element))

    listt.forEach((item) => {
        let li = document.createElement('li')
        li.innerHTML = `<div class="car-element"><a href="http://127.0.0.1:5000/home/us/${item}">${item}<a/><div/>`
        carsList.appendChild(li)

    })


}

const carList = ['THA', 'CWA56', 'TOYOTA']
const search = document.getElementById('search')
search.addEventListener('focus', showSearch)
const main = document.getElementById('main-site-container')
main.addEventListener('click', hideSearch)
search.addEventListener('keyup', getValue)

const key = 'bbf02f6c2bc9cf7676e9928e294b82b3'

function connToAPI(city, key) {
    axios.get(`http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${key}`)
        .then(
            response => console.log(response.data),
            reason => console.log(reason)
        )

}


q