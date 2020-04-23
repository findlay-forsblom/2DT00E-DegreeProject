'use strict'

const axios = require('axios')

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
  // console.log(req.params.id)
  const Action = require('../models/actionModel.js')

  // Fetch Action history
  const action = await Action.find({})

  const today = new Date()
  const oneDay = new Date()
  oneDay.setDate(oneDay.getDate() + 1)
  const twoDays = new Date()
  twoDays.setDate(oneDay.getDate() + 2)

  // Must create new object to be able to render page with information.
  const context = {
    actions: action.map(act => {
      return {
        id: act.id,
        bookings: act.bookings,
        date: act.date
      }
    })
  }

  // Fetch Action in request.
  const current = await Action.findOne({ id: req.params.id })
  const currentArr = []
  let currentContext

  if (current) {
    currentArr.push(current)

    currentContext = {
      currentAction: currentArr.map(act => {
        return {
          id: act.id,
          bookings: act.bookings,
          forecast: act.forecast
        }
      })
    }
    currentContext.currentAction[0].today = today.toDateString()
    currentContext.currentAction[0].oneDay = oneDay.toDateString()
    currentContext.currentAction[0].twoDays = twoDays.toDateString()
  }

  const data = await fetchBookings(today)
  const bookings = handleInfo(data.bookings, data.contact)

  console.log(data)

  // console.log(currentContext.currentAction[0])
  res.render('action/decision', { current: current ? currentContext.currentAction[0] : null, data: context.actions, bookings: bookings })
}

async function fetchBookings (date) {
  const fromDate = formatDate(date)
  const toDate = fromDate
  const url = `https://vaxjo.ibgo.se/BookingApi/GetBookings?start=${fromDate}+00%3A00&end=${toDate}+00%3A00&isPublic=true&resources%5B0%5D=50`

  const bookings = await requestBookings(url)

  // Print out the unique bookings.
  // bookings.forEach(booking => {
  //   console.log(booking.start + '-' + booking.end + '. Team: ' + booking.description.replace('<br><br>', ' ') + '. Status: ' + booking.status)
  // })

  // console.log(bookings)
  const teams = bookings.map(booking => booking.description.replace('<br><br>', ' ').split(' '))
  const contacts = []

  for (let i = 0; i < teams.length; i++) {
    const contact = await getContact(teams[i][0])
    contact.forEach(team => {
      if (teams.length > 2 && team.Name.includes(teams[i][1]) && team.CustomerOccupationsText.includes(teams[i][teams[i].length - 1])) {
        // Team name with extensions.
        contacts.push({ name: team.Name, contact: team.Email })
      } else if (teams.length === 2 && team.CustomerOccupationsText.includes(teams[i][teams[i].length - 1])) {
        // Team name without extensions.
        contacts.push({ name: team.Name, contact: team.Email })
      }
    })
  }

  // console.log(contacts, 'Contacts')
  return { bookings: bookings, contact: contacts }
}

function handleInfo (bookings, contact) {
  const info = []
  console.log('Got to Handleinfo', bookings.length)
  for (let i = 0; i < bookings.length; i++) {
    const temp = contact[i]
    temp.time = bookings[i].title
    info.push(temp)
    console.log(temp, 'IN HANDLEDATA')
  }
  return info
}

actionController.clear = (req, res, next) => {
  res.send('Clear')
}

actionController.close = async (req, res, next) => {
  const fromDate = formatDate(req.params.date)
  const toDate = fromDate
  const url = `https://vaxjo.ibgo.se/BookingApi/GetBookings?start=${fromDate}+00%3A00&end=${toDate}+00%3A00&isPublic=true&resources%5B0%5D=50`

  const bookings = await requestBookings(url)

  // Print out the unique bookings.
  bookings.forEach(booking => {
    console.log(booking.start + '-' + booking.end + '. Team: ' + booking.description.replace('<br><br>', ' ') + '. Status: ' + booking.status)
  })

  console.log(bookings)
  const teams = bookings.map(booking => booking.description.replace('<br><br>', ' ').split(' '))
  const contacts = []

  for (let i = 0; i < teams.length; i++) {
    const contact = await getContact(teams[i][0])
    contact.forEach(team => {
      if (teams.length > 2 && team.Name.includes(teams[i][1]) && team.CustomerOccupationsText.includes(teams[i][teams[i].length - 1])) {
        // Team name with extensions.
        contacts.push({ name: team.Name, contact: team.Email })
      } else if (teams.length === 2 && team.CustomerOccupationsText.includes(teams[i][teams[i].length - 1])) {
        // Team name without extensions.
        contacts.push({ name: team.Name, contact: team.Email })
      }
    })
  }

  console.log(contacts, 'Contacts')

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
    url: `https://vaxjo.ibgo.se/AssociationRegister/GetAssociationsList?sEcho=2&iColumns=6&sColumns=Name%2CAssociationCategory%2CCustomerOccupations%2CWebSite%2CDistrict%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=Name&bSortable_0=true&mDataProp_1=AssociationCategoryName&bSortable_1=true&mDataProp_2=CustomerOccupationsText&bSortable_2=true&mDataProp_3=WebSite&bSortable_3=true&mDataProp_4=DistrictName&bSortable_4=true&mDataProp_5=5&bSortable_5=true&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&CustomerName=${team}&DistrictId=&ActivityId=&AssociationCategoryId=&_=1586949943738`
  }
  const data = await axios.request(config)
  const contactCookie = data.headers['set-cookie'].toString()
  config.headers = { Cookie: contactCookie }

  const resp = await axios.request(config)
  const contact = resp.data
  console.log(contact.aaData.Customers, ': IN getContact')
  return contact.aaData.Customers
}

module.exports = actionController
