const $ = (el, props = {}, ...contents) => {
  const $el = document.createElement(el);
  for (const prop of Object.keys(props)) {
    if (prop === "listeners") {
      props.listeners.forEach(({type, handler}) => $el.addEventListener(type, handler));
    } else if (prop === "dataset") {
      Object.keys(props.dataset).forEach((key) => $el.dataset[key] = props.dataset[key]);
    } else {
      $el[prop] = props[prop];
    }
  }
  for (let child of contents) {
    if (typeof child === "string") {
      child = document.createTextNode(child);
    }
    if (child) $el.appendChild(child);
  }
  return $el;
}

const $searchBox = document.getElementById("searchBox");
const $results = document.getElementById("searchResults");

let searchTimeout = -1;
let lastSearch;

$searchBox.addEventListener('input', function(evt) {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(doSearch, 500);
})

function clearSearch() {
  while ($results.lastElementChild) {
    $results.removeChild($results.lastElementChild)
  }
}

async function doSearch() {
  const search = encodeURIComponent($searchBox.value);
  lastSearch = search;
  if (search === "") {
    return clearSearch();
  }
  fetch("/api/search?q=" + search + "&limit=25")
    .then(res => res.json())
    .then(data => buildSearchResults(data))
}

function buildSearchResults(data) {
  clearSearch();
  list = [...data.artists.items, ...data.tracks.items];
  console.log(list)
  list = list.sort((l, r) => {
    return r.popularity - l.popularity
  }).splice(0, 8)
  list.forEach(dat => {
    let info = {
      primary: dat.name
    };
    let imageList;
    if (dat.type === "artist") {
      imageList = dat.images;
    } else {
      imageList = dat.album.images;
      info.secondary = dat.artists[0].name;
    }
    if (imageList.length) {
      info.imageURL = imageList[imageList.length - 1].url;
    }
    $results.appendChild(buildResultTile(info));
  })
}

function buildResultTile({imageURL, primary, secondary, handler}) {
  return $('div', {className: 'result-tile'},
    $('div', {className: 'result-tile-image'},
      imageURL && $('img', {src: imageURL})
    ),
    $('div', {className: 'result-tile-body'},
      $('h2', {}, primary),
      secondary && $('p', {}, secondary)
    ),
  )
}