'use strict'

const forecaster = require('../libs/forecast')
const Action = require('../models/actionModel.js')
const Pitch = require('../models/pitchModel.js')
const weatherSymb = require('../libs/weatherSymbols')
const mailer = require('../libs/mailer')
const actionController = {}
const err = {}

// Run development functions if true
const development = true

actionController.index = async (req, res, next) => {
  // Fetch Action history if query, else fetch only todays actions
  const action = req.query.all === 'true' ? await Action.find({}) : await Action.find({ today: new Date().toDateString() })

  // Must create new object from database to be able to render page with information.
  const context = { actions: arrangeAction(action.reverse()) }

  // Fetch Action in request and create a new object to access rendering options.
  const current = await Action.findOne({ _id: req.params.id })

  // Parameters to pass for rendering
  const currentArr = []
  let currentContext, bookings, sensor, prediction, emails
  let pitch = { address: 'Växjö', zip: '35232' }

  if (current) {
    currentArr.push(current)
    pitch = await Pitch.findOne({ id: current.id })
    currentContext = { currentAction: arrangeAction(currentArr) }

    // If action found => Add to objects outside if-statement.
    bookings = currentContext.currentAction[0].bookings
    sensor = currentContext.currentAction[0].sensor
    prediction = currentContext.currentAction[0].prediction

    // Append missing dates to prediction for rendering.
    prediction.dateFirst = currentContext.currentAction[0].oneDay
    prediction.dateSecond = currentContext.currentAction[0].twoDays

    // Filter to unique emails to form rendering
    emails = bookings.map(booking => { return booking.contact }).filter(onlyUnique)
  }
  // Get current dates, filtered forecasts with corresponding symbols.
  const days = require('../libs/threeDates').consecutiveDays()
  let forecast = await getForecast([days.today.toDateString(), days.oneDay.toDateString(), days.twoDays.toDateString()], { address: pitch.address, zip: pitch.zip })
  forecast = forecast.filter((element) => {
    // Filter out undefined values
    return element !== undefined
  })
  const forecastSymbols = weatherSymb.getSymbol(forecast)

  res.render('action/decision', {
    current: current ? currentContext.currentAction[0] : null,
    data: context.actions,
    bookings: bookings,
    forecast: forecastSymbols,
    sensor: sensor,
    predict: prediction,
    emails: emails,
    all: req.query.all === 'true' ? true : undefined
  })
}

actionController.ensureAuthenticated = async (req, res, next) => {
  if (req.session.userId) {
    next()
  } else {
    req.session.actionId = req.body.id ? req.body.id : req.params.id
    const redirector = req.session.actionId ? `/${req.params.id}` : '/'
    res.redirect(redirector)
  }
}

actionController.authorize = async (req, res, next) => {
  const type = req.session.role
  if (type === 'Admin') {
    next()
  } else {
    err.status = 403
    next(err)
  }
}

/**
 * Sends emails to all recipients filled in form
 */
actionController.decision = async (req, res, next) => {
  if (req.session.role === 'Admin') {
    mailer.sendMail([development ? process.env.dev_email : process.env.dev_email2], req.body.title, msgToHTML(req.body.message), req.body.message)
    req.session.flash = { type: 'success', text: `Email(s) successfully sent to ${req.body.email}` }
  } else {
    req.session.flash = { type: 'danger', text: `Could not send email to ${req.body.email}` }
  }

  res.redirect(`/action/${req.body.id}`)
}

/**
 * Gets forecast and filter out the days and times requested.
 * @param {Array} days Array of dates.
 * @param {Array} time Array of time.
 */
async function getForecast (days, geo) {
  const forecast = await forecaster.forecast(geo)
  const result = []

  for (let i = 0; i < days.length; i++) {
    const day = days[i].split(' ')
    day[2] = parseInt(day[2], 10).toString()

    const dayArr = forecast.filter(cast => {
      return cast.date.includes(day[1]) && cast.date.includes(day[2])
    })

    // Initialize the return object
    const weather = {
      date: dayArr[0].date,
      lowTemp: dayArr[0].params[0].values[0],
      highTemp: dayArr[0].params[0].values[0],
      lowHumid: dayArr[0].params[1].values[0],
      highHumid: dayArr[0].params[1].values[0],
      symbol: []
    }

    // Find lowest/highest temp/humidity and add weather symbols.
    dayArr.forEach((item, idx) => {
      const temp = item.params[0].values[0]
      const humid = item.params[1].values[0]
      if (temp < weather.lowTemp) {
        weather.lowTemp = temp
      } else if (temp > weather.highTemp) {
        weather.highTemp = temp
      }

      if (humid < weather.lowHumid) {
        weather.lowHumid = humid
      } else if (humid > weather.highHumid) {
        weather.highHumid = humid
      }

      weather.symbol.push(item.params[4].values[0])
    })

    // Find most common weather symbol and push to result
    weather.commonSymbol = mode(weather.symbol)
    result.push(weather)
  }

  return result
}

/**
 * Finds the most common element in an array.
 * @param {Array} arr Array
 */
function mode (arr) {
  return arr.sort((a, b) =>
    arr.filter(v => v === a).length -
      arr.filter(v => v === b).length
  ).pop()
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
      names: JSON.parse(act.names),
      clearEmail: act.clearEmail,
      bookings: JSON.parse(act.bookings),
      today: act.today,
      oneDay: act.oneDay,
      twoDays: act.twoDays,
      sensor: JSON.parse(act.sensor),
      prediction: JSON.parse(act.prediction)
    }
  })
}

/**
 * Checks if an array only consists of unique entries. Used in filter function.
 */
function onlyUnique (value, index, self) {
  return self.indexOf(value) === index
}

/**
 * Adds the line break tag to each linebreak string occurance.
 * @param {String} message Message to add HTML line breaks
 */
function msgToHTML (message) {
  return message.split('\r\n').join('<br>')
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
//      .log(booking.start + '-' + booking.end + '. Team: ' + booking.description.replace('<br><br>', ' ') + '. Status: ' + booking.status)
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
