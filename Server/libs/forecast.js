const fetch = require('node-fetch')
const moment = require('moment')

async function forecast (geoInfo) {
  const longlatGen = require('../libs/longLatGen.js')
  const geo = longlatGen.gen(geoInfo.address, geoInfo.zip)

  return geo.then(async (results) => {
    const lat = (results.lat).toFixed(3)
    const lon = (results.long).toFixed(3)
    const SMHI = `https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/${lon}/lat/${lat}/data.json`
    const forecast = await getForecasts(SMHI)
    return forecast
  })
}

async function getForecasts (SMHI) {
  const response = await fetch(SMHI)
  const data = await response.json()
  const arr = data.timeSeries

  const casts = []
  arr.forEach(element => {
    let time = moment(element.validTime).format('MMMM Do YYYY, h:mm:ss a')
    time = time.split(',')
    const params = element.parameters
    const filtered = params.filter(e => e.name === 'pmean' || e.name === 't' || e.name === 'r' || e.name === 'pcat' || e.name === 'Wsymb2')
    casts.push({ date: time[0], time: time[1], params: filtered })
  })

  return casts
}

module.exports = { forecast }
