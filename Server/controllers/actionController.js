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
  const action = await Action.find({})

  const today = new Date()
  const oneDay = new Date()
  oneDay.setDate(oneDay.getDate() + 1)
  const twoDays = new Date()
  twoDays.setDate(oneDay.getDate() + 2)

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

  // console.log(currentContext.currentAction[0])
  res.render('action/decision', { current: current ? currentContext.currentAction[0] : null, data: context.actions })
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
    console.log(booking.start + '-' + booking.end + '. Team: ' + booking.description + '. Status: ' + booking.status)
  })

  res.redirect('back')

  // const fetch = require('node-fetch')
  // const data = await fetch(url)
  // console.log(data.headers)
  // config.headers = { Cookie: data.headers.get('set-cookie'), method: 'GET' }
  // console.log(config)
  // const bookings = await fetch(url, config)
  // console.log(bookings)
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

module.exports = actionController
