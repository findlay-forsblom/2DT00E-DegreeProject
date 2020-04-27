
const axios = require('axios')
const Pitch = require('../models/pitchModel')

function formatDate (date) {
  var d = new Date(date)
  var month = '' + (d.getMonth() + 1)
  var day = '' + d.getDate()
  var year = d.getFullYear()

  if (month.length < 2) { month = '0' + month }
  if (day.length < 2) { day = '0' + day }

  return [year, month, day].join('%2D')
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

module.exports = { handleInfo, fetchBookings }
