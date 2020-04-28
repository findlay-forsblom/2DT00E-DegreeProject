const fetch = require('node-fetch')
const moment = require('moment')
const pipeine = require('../libs/mlPipeline.js')

const test = [0.1, -0.5, 0.0, 79.06, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]

module.exports.predict = async (data, geocode, threshold = 0) => {
  const snowDepth = data.snow

  const lat = (geocode.lat).toFixed(3)
  const lon = (geocode.long).toFixed(3)
  const SMHI = `https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/${lon}/lat/${lat}/data.json`
  const casts = await getForecasts(SMHI)
  const date = moment().format('MMMM Do YYYY')

  if (snowDepth > 0) {
    console.log(date)
    const temp = getAverageTemp(casts, date).toFixed(1)
    const humid = getAverageHumid(casts, date).toFixed(1)
    const precip = getAveragePrecip(casts, date)
    console.log(temp)
    console.log(humid)
    console.log(precip)
    const snowDepthDay1 = await pipeine.getData(test)
    /**
     * Predicting two days in the future
     */
    if (snowDepthDay1 > threshold) {
      let i
      for (i = 1; i < 3; i++) {
        const day = moment(moment().add(i, 'days')).format('MMMM Do YYYY')
        console.log(day)
        const temp = getAverageTemp(casts, day).toFixed(1)
        const humid = getAverageHumid(casts, day).toFixed(1)
        const precip = getAveragePrecip(casts, day)
        console.log(temp)
        console.log(humid)
        console.log(precip)
        /**
         * const snowDepthDay1 = await pipeine.getData(test)
         */
      }
    }
  } else {
    const result = checkForSnow(casts, date)
    const times = result.map(a => a.time) // Time to check again
    console.log(times)
  }
}

function checkForSnow (data, day) {
  let results = []
  const arr = data.filter(e => e.date === day)
  arr.forEach(element => {
    const param = element.params.filter(e => e.name === 'pmean' || e.name === 'pcat')
    results.push({ day: element.date, time: element.time, type: param[0].values[0], value: param[1].values[0] })
  })
  results = results.filter(e => e.type === 1 || e.type === 0) // should be changed to 1 and 2 when in production
  return results
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
    // const avg = (sum / val.length) || 0
    dict[i] = sum
  }
  return dict
}

async function getForecasts (SMHI) {
  const response = await fetch(SMHI)
  const data = await response.json()
  const arr = data.timeSeries

  const casts = []
  // console.log(arr)
  // console.log(moment(moment().add(1, 'days')).format('MMMM Do YYYY, h:mm:ss a'))
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
