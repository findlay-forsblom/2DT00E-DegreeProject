'use strict'

const axios = require('axios')
const forecaster = require('../libs/forecast')
const Pitch = require('../models/pitchModel')
const Action = require('../models/actionModel.js')

const weatherSymb = [
  { id: 1, type: 'Clear sky', type_se: 'Klart', icon: '1.png' },
  { id: 2, type: 'Nearly clear sky', type_se: 'Lätt molnighet', icon: '2.png' },
  { id: 3, type: 'Variable cloudiness', type_se: 'Halvklart', icon: '3.png' },
  { id: 4, type: 'Halfclear sky', type_se: 'Molnigt', icon: '4.png' },
  { id: 5, type: 'Cloudy sky', type_se: 'Mycket moln', icon: '5.png' },
  { id: 6, type: 'Overcast', type_se: 'Mulet', icon: '6.png' },
  { id: 7, type: 'Fog', type_se: 'Dimma', icon: '7.png' },
  { id: 8, type: 'Light rain showers', type_se: 'Lätt regn', icon: '8.png' },
  { id: 9, type: 'Moderate rain showers', type_se: 'Regn', icon: '9.png' },
  { id: 10, type: 'Heavy rain showers', type_se: 'Kraftigt regn', icon: '10.png' },
  { id: 11, type: 'Thunderstorm', type_se: 'Åskskur', icon: '11.png' },
  { id: 12, type: 'Light sleet showers', type_se: 'Lätt by av regn och snö', icon: '12.png' },
  { id: 13, type: 'Moderate sleet showers', type_se: 'By av regn och snö', icon: '13.png' },
  { id: 14, type: 'Heavy sleet showers', type_se: 'Kraftig by av regn och snö', icon: '14.png' },
  { id: 15, type: 'Light snow showers', type_se: 'Lätt snöby', icon: '15.png' },
  { id: 16, type: 'Moderate snow showers', type_se: 'Snöby', icon: '16.png' },
  { id: 17, type: 'Heavy snow showers', type_se: 'Kraftig snöby', icon: '17.png' },
  { id: 18, type: 'Light rain', type_se: 'Lätt regn', icon: '18.png' },
  { id: 19, type: 'Moderate rain', type_se: 'Regn', icon: '19.png' },
  { id: 20, type: 'Heavy rain', type_se: 'Kraftigt regn', icon: '20.png' },
  { id: 21, type: 'Thunder', type_se: 'Åska', icon: '21.png' },
  { id: 22, type: 'Light sleet', type_se: 'Lätt snöblandat regn', icon: '22.png' },
  { id: 23, type: 'Moderate sleet', type_se: 'Snöblandat regn', icon: '23.png' },
  { id: 24, type: 'Heavy sleet', type_se: 'Kraftigt snöblandat regn', icon: '24.png' },
  { id: 25, type: 'Light snowfall', type_se: 'Lätt snöfall', icon: '25.png' },
  { id: 26, type: 'Moderate snowfall', type_se: 'Snöfall', icon: '26.png' },
  { id: 27, type: 'Heavy snowfall', type_se: 'Ymnigt snöfall', icon: '27.png' }
]

function formatDate (date) {
  var d = new Date(date)
  var month = '' + (d.getMonth() + 1)
  var day = '' + d.getDate()
  var year = d.getFullYear()

  if (month.length < 2) { month = '0' + month }
  if (day.length < 2) { day = '0' + day }

  return [year, month, day].join('%2D')
}

const actionController = {}

// app.use('/action', require('./routes/actionRouter.js'))

/**
 * Adds an action to database
 */
// const tester = async () => {
//   const Action = require('./models/actionModel.js')
//   const today = new Date()
//   const oneDay = new Date()
//   oneDay.setDate(oneDay.getDate() + 1)
//   const twoDays = new Date()
//   twoDays.setDate(oneDay.getDate() + 2)

//   const action = new Action({
//     id: 'test_2',
//     bookings: 'test_bookings_2',
//     date: today.toDateString(),
//     oneDay: oneDay.toDateString(),
//     twoDays: twoDays.toDateString(),
//     forecast: 'rainy'
//   })

//   await action.save()
// }

actionController.index = async (req, res, next) => {
  // Fetch Action history
  const action = await Action.find({})

  // collection.find().sort({datefield: -1}, function(err, cursor){...});
  // OMman vill sortera efter datum

  const today = new Date()
  const oneDay = new Date()
  oneDay.setDate(oneDay.getDate() + 1)
  const twoDays = new Date()
  twoDays.setDate(oneDay.getDate() + 2)

  // Must create new object to be able to render page with information.
  const context = {
    actions: action.map(act => {
      return {
        id: act._id,
        name: act.name,
        bookings: act.bookings,
        date: act.date
      }
    })
  }

  // Fetch Action in request.
  const current = await Action.findOne({ _id: req.params.id })
  const currentArr = []
  let currentContext
  let data
  let bookings

  if (current) {
    currentArr.push(current)

    currentContext = {
      currentAction: currentArr.map(act => {
        return {
          id: act._id,
          name: act.name,
          bookings: act.bookings,
          forecast: act.forecast
        }
      })
    }
    currentContext.currentAction[0].today = today.toDateString()
    currentContext.currentAction[0].oneDay = oneDay.toDateString()
    currentContext.currentAction[0].twoDays = twoDays.toDateString()

    data = await fetchBookings(today, current.id)
    bookings = handleInfo(data.bookings, data.contact)
  }

  const forecast = await getForecast([today.toDateString(), oneDay.toDateString(), twoDays.toDateString()], [['11', 'pm'], ['8', 'am'], ['8', 'am']])

  const cast = []
  forecast.forEach(forecast => {
    const symbol = weatherSymb.filter(symb => {
      return symb.id === forecast.params[4].values[0]
    })

    cast.push({ temp: forecast.params[0].values[0], humid: forecast.params[1].values[0], symb: symbol[0], date: forecast.date })
  })

  res.render('action/decision', { current: current ? currentContext.currentAction[0] : null, data: context.actions, bookings: bookings, forecast: cast })
}

async function getForecast (days, time) {
  const forecast = await forecaster.forecast()
  const result = []

  for (let i = 0; i < days.length; i++) {
    const day = days[i].split(' ')
    const dayArr = forecast.filter(cast => {
      return cast.date.includes(day[1]) && cast.date.includes(day[2]) && cast.time.includes(time[i][0]) && cast.time.includes(time[i][1])
    })
    result.push(dayArr[0])
  }

  return result
}

async function fetchBookings (date, pitchID) {
  const fromDate = formatDate(date)
  const toDate = fromDate
  const pitch = await Pitch.findOne({ id: pitchID })

  const url = `https://vaxjo.ibgo.se/BookingApi/GetBookings?start=${fromDate}+00%3A00&end=${toDate}+00%3A00&isPublic=true&resources%5B0%5D=${pitchID}`

  const bookings = await requestBookings(url)

  // Print out the unique bookings.
  bookings.forEach(booking => {
    console.log(booking.start + '-' + booking.end + '. Team: ' + booking.description.replace('<br><br>', ' ') + '. Status: ' + booking.status)
  })

  const teams = bookings.map(booking => booking.description.replace('<br><br>', ' ').split(' '))
  const teamNames = teams.map(team => {
    if (team.length >= 2) {
      const temp = team.join(' ')
      return [temp.substring(0, temp.length - team[team.length - 1].length - 1), team[team.length - 1]]
    } else {
      return [team.toString(), null]
    }
  })
  const contacts = []

  for (let i = 0; i < teamNames.length; i++) {
    const contact = await getContact(teamNames[i][0])

    if (contact.length > 0) {
      contact.forEach(team => {
        contacts.push({ name: team.Name, contact: team.Email })
      })
    } else {
      contacts.push({ name: teamNames[i][0], contact: 'N/A' })
    }
  }

  return { pitch: pitch, bookings: bookings, contact: contacts }
}

function handleInfo (bookings, contact) {
  const info = []

  for (let i = 0; i < bookings.length; i++) {
    const temp = contact[i] ? contact[i] : {}
    temp.time = bookings[i].title
    info.push(temp)
  }

  return info
}

actionController.clear = async (req, res, next) => {
  res.send('Clear')
}

actionController.close = async (req, res, next) => {
  // const fromDate = formatDate(req.params.date)
  // const toDate = fromDate
  // const url = `https://vaxjo.ibgo.se/BookingApi/GetBookings?start=${fromDate}+00%3A00&end=${toDate}+00%3A00&isPublic=true&resources%5B0%5D=50`

  // const bookings = await requestBookings(url)

  // const teams = bookings.map(booking => booking.description.replace('<br><br>', ' ').split(' '))
  // const contacts = []

  // for (let i = 0; i < teams.length; i++) {
  //   const contact = await getContact(teams[i][0])
  //   contact.forEach(team => {
  //     if (teams.length > 2 && team.Name.includes(teams[i][1]) && team.CustomerOccupationsText.includes(teams[i][teams[i].length - 1])) {
  //       // Team name with extensions.
  //       contacts.push({ name: team.Name, contact: team.Email })
  //     } else if (teams.length === 2 && team.CustomerOccupationsText.includes(teams[i][teams[i].length - 1])) {
  //       // Team name without extensions.
  //       contacts.push({ name: team.Name, contact: team.Email })
  //     }
  //   })
  // }

  res.redirect('back')
}

async function requestBookings (url) {
  const config = {
    url: url
  }
  // Request for cookie
  const data = await axios.request(config)
  const cookie = data.headers['set-cookie'].toString()
  config.headers = { Cookie: cookie }

  // Request for bookings with cookie
  const resp = await axios.request(config)
  const bookings = resp.data.filter((booking) => {
    return booking.status === 'booked'
  })

  // Remove duplicates in array.
  const uniqueBookings = []
  bookings.forEach(booking => {
    const uniques = uniqueBookings.filter(item => {
      return item.start === booking.start && item.description === booking.description
    })
    if (uniques.length === 0) {
      uniqueBookings.push(booking)
    }
  })

  return uniqueBookings
}

async function getContact (team) {
  const config = {
    url: `https://vaxjo.ibgo.se/AssociationRegister/GetAssociationsList?sEcho=2&iColumns=6&sColumns=Name%2CAssociationCategory%2CCustomerOccupations%2CWebSite%2CDistrict%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=Name&bSortable_0=true&mDataProp_1=AssociationCategoryName&bSortable_1=true&mDataProp_2=CustomerOccupationsText&bSortable_2=true&mDataProp_3=WebSite&bSortable_3=true&mDataProp_4=DistrictName&bSortable_4=true&mDataProp_5=5&bSortable_5=true&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&CustomerName=${encodeURI(team)}&DistrictId=&ActivityId=&AssociationCategoryId=&_=1586949943738`
  }

  const data = await axios.request(config)
  const contactCookie = data.headers['set-cookie'].toString()
  config.headers = { Cookie: contactCookie }

  const resp = await axios.request(config)
  const contact = resp.data

  return contact.aaData.Customers
}

module.exports = actionController
