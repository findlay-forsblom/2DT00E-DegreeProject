'use strict'

// const axios = require('axios')
const forecaster = require('../libs/forecast')
// const Pitch = require('../models/pitchModel')
const Action = require('../models/actionModel.js')

const weatherSymb = require('../libs/weatherSymbols')

const actionController = {}

actionController.index = async (req, res, next) => {
  // Fetch Action history
  const action = await Action.find({})
  // collection.find().sort({datefield: -1}, function(err, cursor){...});
  // OMman vill sortera efter datum

  // Must create new object from database to be able to render page with information.
  const context = { actions: arrangeAction(action) }

  // Fetch Action in request and create a new object to access rendering options.
  const current = await Action.findOne({ _id: req.params.id })

  // Parameters to pass for rendering
  const currentArr = []
  let currentContext
  let bookings
  let sensor
  let prediction

  if (current) {
    currentArr.push(current)

    currentContext = { currentAction: arrangeAction(currentArr) }

    // If action found => Add to objects outside if-statement.
    bookings = currentContext.currentAction[0].bookings
    sensor = currentContext.currentAction[0].sensor
    prediction = currentContext.currentAction[0].prediction

    // Append missing dates to prediction for rendering.
    prediction.dateFirst = currentContext.currentAction[0].oneDay
    prediction.dateSecond = currentContext.currentAction[0].twoDays
  }

  // Get current dates, filtered forecasts with corresponding symbols.
  const days = require('../libs/threeDates').consecutiveDays()
  const forecast = await getForecast([days.today.toDateString(), days.oneDay.toDateString(), days.twoDays.toDateString()], [['11', 'pm'], ['8', 'am'], ['8', 'am']])
  const forecastSymbols = weatherSymb.getSymbol(forecast)
  console.log(forecastSymbols)

  res.render('action/decision', {
    current: current ? currentContext.currentAction[0] : null,
    data: context.actions,
    bookings: bookings,
    forecast: forecastSymbols,
    sensor: sensor,
    predict: prediction
  })
}

actionController.clear = async (req, res, next) => {
  res.send('Clear')
}

actionController.close = async (req, res, next) => {
  res.redirect('back')
}

/**
 * Gets forecast and filter out the days and times requested.
 * @param {Array} days Array of dates.
 * @param {Array} time Array of time.
 */
async function getForecast (days, time) {
  const forecast = await forecaster.forecast()
  const result = []

  for (let i = 0; i < days.length; i++) {
    const day = days[i].split(' ')
    const dayArr = forecast.filter(cast => {
      return cast.date.includes(day[1]) && cast.date.includes(day[2]) &&
      cast.time.includes(time[i][0]) && cast.time.includes(time[i][1])
    })
    result.push(dayArr[0])
  }

  return result
}

/**
 * Maps an Action object to new object, to gain access for view rendering. Also parses the JSON objects provided.
 * @param {Model Object} action Object from database.
 */
function arrangeAction (action) {
  return action.map(act => {
    return {
      _id: act._id,
      id: act.id,
      name: act.name,
      bookings: JSON.parse(act.bookings),
      today: act.today,
      oneDay: act.oneDay,
      twoDays: act.twoDays,
      sensor: JSON.parse(act.sensor),
      prediction: JSON.parse(act.prediction)
    }
  })
}

module.exports = actionController

// async function requestBookings (url) {
//   const config = {
//     url: url
//   }
//   // Request for cookie
//   const data = await axios.request(config)
//   const cookie = data.headers['set-cookie'].toString()
//   config.headers = { Cookie: cookie }

//   // Request for bookings with cookie
//   const resp = await axios.request(config)
//   const bookings = resp.data.filter((booking) => {
//     return booking.status === 'booked'
//   })

//   // Remove duplicates in array.
//   const uniqueBookings = []
//   bookings.forEach(booking => {
//     const uniques = uniqueBookings.filter(item => {
//       return item.start === booking.start && item.description === booking.description
//     })
//     if (uniques.length === 0) {
//       uniqueBookings.push(booking)
//     }
//   })

//   return uniqueBookings
// }

// async function getContact (team) {
//   const config = {
//     url: `https://vaxjo.ibgo.se/AssociationRegister/GetAssociationsList?sEcho=2&iColumns=6&sColumns=Name%2CAssociationCategory%2CCustomerOccupations%2CWebSite%2CDistrict%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=Name&bSortable_0=true&mDataProp_1=AssociationCategoryName&bSortable_1=true&mDataProp_2=CustomerOccupationsText&bSortable_2=true&mDataProp_3=WebSite&bSortable_3=true&mDataProp_4=DistrictName&bSortable_4=true&mDataProp_5=5&bSortable_5=true&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&CustomerName=${encodeURI(team)}&DistrictId=&ActivityId=&AssociationCategoryId=&_=1586949943738`
//   }

//   const data = await axios.request(config)
//   const contactCookie = data.headers['set-cookie'].toString()
//   config.headers = { Cookie: contactCookie }

//   const resp = await axios.request(config)
//   const contact = resp.data

//   return contact.aaData.Customers
// }

// async function fetchBookings (date, pitchID) {
//   const fromDate = formatDate(date)
//   const toDate = fromDate
//   const pitch = await Pitch.findOne({ id: pitchID })

//   const url = `https://vaxjo.ibgo.se/BookingApi/GetBookings?start=${fromDate}+00%3A00&end=${toDate}+00%3A00&isPublic=true&resources%5B0%5D=${pitchID}`

//   const bookings = await requestBookings(url)

//   // Print out the unique bookings.
//   bookings.forEach(booking => {
//     console.log(booking.start + '-' + booking.end + '. Team: ' + booking.description.replace('<br><br>', ' ') + '. Status: ' + booking.status)
//   })

//   const teams = bookings.map(booking => booking.description.replace('<br><br>', ' ').split(' '))
//   const teamNames = teams.map(team => {
//     if (team.length >= 2) {
//       const temp = team.join(' ')
//       return [temp.substring(0, temp.length - team[team.length - 1].length - 1), team[team.length - 1]]
//     } else {
//       return [team.toString(), null]
//     }
//   })
//   const contacts = []

//   for (let i = 0; i < teamNames.length; i++) {
//     const contact = await getContact(teamNames[i][0])

//     if (contact.length > 0) {
//       contact.forEach(team => {
//         contacts.push({ name: team.Name, contact: team.Email })
//       })
//     } else {
//       contacts.push({ name: teamNames[i][0], contact: 'N/A' })
//     }
//   }

//   return { pitch: pitch, bookings: bookings, contact: contacts }
// }

// function handleInfo (bookings, contact) {
//   const info = []

//   for (let i = 0; i < bookings.length; i++) {
//     const temp = contact[i] ? contact[i] : {}
//     temp.time = bookings[i].title
//     info.push(temp)
//   }

//   return info
// }
