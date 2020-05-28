/**
 * Predicts upcoming snow levels, by measured data, weather forecasts at site.
 * Weather forcast precipitation are one hot encoded.
 *
 * @author Findlay Forsblom, Linnaeus University.
 */

const fetch = require('node-fetch')
const moment = require('moment')
const pipeline = require('../libs/mlPipeline.js')
const encoder = require('../libs/oneHotEncoding.js')

module.exports.predict = async (data, geocode, threshold = 0) => {
  const snowDepth = data.snow
  const tempLora = 0.7
  const humidLora = data.humudity

  const lat = (geocode.lat).toFixed(3)
  const lon = (geocode.long).toFixed(3)
  const SMHI = `https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/${lon}/lat/${lat}/data.json`
  const casts = await getForecasts(SMHI)
  let snowDepthDay1 = snowDepth
  let i
  const results = []

  for (i = 0; i < 3; i++) {
    const date = moment(moment().add(i, 'days')).format('MMMM Do YYYY')
    const dayTmr = moment(moment().add(i + 1, 'days')).format('MMMM Do YYYY')
    const temp = getAverageTemp(casts, date).toFixed(1)
    const tempTmr = getAverageTemp(casts, dayTmr).toFixed(1)
    const humid = getAverageHumid(casts, date).toFixed(1)
    const precip = getAveragePrecip(casts, date)
    const precipAmount = getTotalPrecip(precip)

    let arr
    if (i === 0) {
      // Add measured data
      arr = [snowDepth, parseFloat(tempLora), parseFloat(tempTmr), parseFloat(humidLora), precipAmount]
    } else {
      // Add forecast data
      arr = [snowDepth, parseFloat(temp), parseFloat(tempTmr), parseFloat(humid), precipAmount]
    }

    // One hot encode precipitations
    let encoded = encoder.encode(precip)
    encoded = arr.concat(encoded)
    encoded.shift()
    encoded = [snowDepthDay1].concat(encoded)

    // Predict snowdepth of i'th day
    snowDepthDay1 = await pipeline.getData(encoded)
    snowDepthDay1 = parseFloat(snowDepthDay1)
    results.push({ date: dayTmr, snowlevel: snowDepthDay1 })
  }
  return results

  function getTotalPrecip (data) {
    let sum = 0
    for (const i in data) {
      sum += data[i] * Math.pow(10, -2)
    }
    return sum
  }

  function getAverageTemp (data, day) {
    const arr = data.filter(e => e.date === day)
    let sum = 0
    let count = 0
    arr.forEach(element => {
      count++
      const param = element.params.filter(e => e.name === 't')
      sum += param[0].values[0]
    })
    return sum / count
  }

  function getAverageHumid (data, day) {
    const arr = data.filter(e => e.date === day)
    let sum = 0
    let count = 0

    arr.forEach(element => {
      count++
      const param = element.params.filter(e => e.name === 'r')
      sum += param[0].values[0]
    })
    return sum / count
  }

  function getAveragePrecip (data, day) {
    const arr = data.filter(e => e.date === day)
    const dict = {}

    arr.forEach(element => {
      const param = element.params.filter(e => e.name === 'pmean' || e.name === 'pcat')
      const key = param[0].values
      if (!(key in dict)) {
        dict[key] = []
      }
      const arr = dict[key]
      arr.push(param[1].values[0])
    })

    for (const i in dict) {
      const val = dict[i]
      let sum = val.reduce((a, b) => a + b, 0)
      sum = sum.toFixed(1)
      dict[i] = sum
    }
    return dict
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
      const filtered = params.filter(e => e.name === 'pmean' || e.name === 't' || e.name === 'r' || e.name === 'pcat')
      casts.push({ date: time[0], time: time[1], params: filtered })
    })
    return casts
  }
}
