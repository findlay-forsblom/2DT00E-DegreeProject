const fetch = require('node-fetch')
const moment = require('moment')
const pipeine = require('../libs/mlPipeline.js')
const encoder = require('../libs/oneHotEncoding.js')

// const test = [0.07, 2, 0.5, 80, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
// const yolo = { 1: 4, 2: 6, 3: 9 }

module.exports.predict = async (data, geocode, threshold = 0) => {
  const snowDepth = data.snow

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
    const arr = [snowDepth, parseInt(temp), parseInt(tempTmr), parseInt(humid), precipAmount]
    let encoded = encoder.encode(precip)
    encoded = arr.concat(encoded)
    encoded.shift()
    encoded = [snowDepthDay1].concat(encoded)
    snowDepthDay1 = await pipeine.getData(encoded)
    snowDepthDay1 = parseFloat(snowDepthDay1)
    results.push({ date: dayTmr, snowlevel: snowDepthDay1 })
  }
  console.log(results)
  return results
  

  // if (snowDepth > 0) {
   /*  console.log(date)
    const dayTmr = moment(moment().add(1, 'days')).format('MMMM Do YYYY')
    const temp = getAverageTemp(casts, date).toFixed(1)
    const tempTmr = getAverageTemp(casts, dayTmr).toFixed(1)
    const humid = getAverageHumid(casts, date).toFixed(1)
    const precip = getAveragePrecip(casts, date)
    console.log(temp)
    console.log(humid)
    console.log(tempTmr)
    console.log('precip is ', precip)
    const yolo = { 1: 4, 2: 6, 3: 9 }
    const precipAmount = getTotalPrecip(precip)
    const arr = [snowDepth, parseInt(temp), parseInt(tempTmr), parseInt(humid), precipAmount]
    let encoded = encoder.encode(precip)
    encoded = arr.concat(encoded)
    console.log(encoded)
    const snowDepthDay1 = await pipeine.getData(encoded)
    console.log('The depth tmrw is ', snowDepthDay1) */

    /**
     * Predicting two days in the future
     */

/*     let snowDepthDay1 = snowDepth
    let i
    const results = []
    for (i = 0; i < 3; i++) {
      const date = moment(moment().add(i, 'days')).format('MMMM Do YYYY')
      console.log(date)
      const dayTmr = moment(moment().add(i + 1, 'days')).format('MMMM Do YYYY')
      const temp = getAverageTemp(casts, date).toFixed(1)
      const tempTmr = getAverageTemp(casts, dayTmr).toFixed(1)
      const humid = getAverageHumid(casts, date).toFixed(1)
      const precip = getAveragePrecip(casts, date)
      console.log(temp)
      console.log(humid)
      console.log(tempTmr)
      console.log('precip is ', precip)
      const yolo = { 1: 4, 2: 6, 3: 9 }
      const precipAmount = getTotalPrecip(precip)
      const arr = [snowDepth, parseInt(temp), parseInt(tempTmr), parseInt(humid), precipAmount]
      let encoded = encoder.encode(precip)
      encoded = arr.concat(encoded)
      encoded.shift()
      encoded = [snowDepthDay1].concat(encoded)
      console.log(encoded)
      snowDepthDay1 = await pipeine.getData(encoded)
      snowDepthDay1 = parseFloat(snowDepthDay1)
      console.log('The depth tmrw is ', snowDepthDay1)
      results.push({ date: dayTmr, snowlevel: snowDepthDay1 })
    }
    console.log(results) */

/*     if (snowDepthDay1 > threshold) {
      let i
      for (i = 1; i < 3; i++) {
        const day = moment(moment().add(i, 'days')).format('MMMM Do YYYY')
        console.log(day)
        let temp = getAverageTemp(casts, day).toFixed(1)
        let humid = getAverageHumid(casts, day).toFixed(1)
        temp = parseFloat(temp.replace(',', '.'))
        humid = parseFloat(humid.replace(',', '.'))
        const precip = getAveragePrecip(casts, day)
        // console.log(temp)
        // console.log(humid)
        console.log('here ', precip)
        const arr = [snowDepth, temp, humid]
        // console.log(precip)
        for (const i in precip) {
          // console.log(i)
          let encoded = encoder.encode(i)
          const value = parseFloat(precip[i].replace(',', '.'))
          encoded = [value].concat(encoded)
          encoded = arr.concat(encoded)
          encoded = encoded.slice(0, 18)
          let snowDepthDay1 = await pipeine.getData(encoded)
          snowDepthDay1 = parseFloat(snowDepthDay1)
          encoded.shift()
          encoded = [snowDepthDay1].concat(encoded)
          console.log(snowDepthDay1)
        }
          // const snowDepthDay1 = await pipeine.getData(test)
      }
    } */
  // } else {
    /**
     * const result = checkForSnow(casts, date)
    const times = result.map(a => a.time) // Time to check again
    console.log(times)
     */
  // }
}

function DummyVariableEncoder (data) {

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
  // console.log('temp is', sum)
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
