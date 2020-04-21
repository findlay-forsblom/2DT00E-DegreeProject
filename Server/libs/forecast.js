const fetch = require('node-fetch')
const moment = require('moment')

module.exports.forecast = async () => {
  const longlatGen = require('../libs/longLatGen.js')
  const lol = longlatGen.gen('Araby Växjö', '35260')
  lol.then(async (results) => {
    const lat = (results.lat).toFixed(3)
    const lon = (results.long).toFixed(3)
    const SMHI = `https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/${lon}/lat/${lat}/data.json`

    const casts = await getForecasts(SMHI)
    console.log(casts[0].params[0])
  })
}

async function getForecasts (SMHI) {
  const response = await fetch(SMHI)
  const data = await response.json()
  const arr = data.timeSeries

  const casts = []
  // console.log(arr)
  console.log(moment(moment().add(1, 'days')).format('MMMM Do YYYY, h:mm:ss a'))
  arr.forEach(element => {
    let time = moment(element.validTime).format('MMMM Do YYYY, h:mm:ss a')
    time = time.split(',')
    const params = element.parameters
    const filtered = params.filter(e => e.name === 'pmean' || e.name === 't' || e.name === 'r' || e.name === 'pcat')
    casts.push({ date: time[0], time: time[1], params: filtered })
    // console.log(element)
  })
  return casts
}
