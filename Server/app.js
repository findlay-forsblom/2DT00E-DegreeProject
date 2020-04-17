const express = require('express')
const hbs = require('express-hbs')
const path = require('path')
const mongoose = require('./config/mongoose.js')
const dotenv = require('dotenv')
const ttn = require('ttn')

dotenv.config({
  path: './.env'
})

mongoose.connect().catch(error => {
  console.log(error)
  process.exit(1)
})

const port = 8000

const app = express()

app.use(express.static(path.join(__dirname, 'public')))

app.engine('hbs', hbs.express4({
  defaultLayout: path.join(__dirname, 'views', 'layouts', 'default'),
  partialsDir: path.join(__dirname, 'views', 'partials')
}))

app.set('view engine', 'hbs')

app.use(express.urlencoded({ extended: false }))

app.use('/', require('./routes/homeRouter.js'))

app.use((req, res, next) => {
  const err = {}
  err.status = 404
  next(err)
})

app.use((err, req, res, next) => {
  if (err.status === 404) {
    res.status(404)
    return res.sendFile(path.join(__dirname, 'public', 'assets', 'html', '404.html'))
  } else if (err.status === 403) {
    res.status(403)
    return res.sendFile(path.join(__dirname, 'public', 'assets', 'html', '403.html'))
  }
  res.status(err.status || 500)
  res.sendFile(path.join(__dirname, 'public', 'assets', 'html', '500.html'))
})
// const detections = {}

// Listen for changes on application from TTN.
// ttn.data(process.env.appID, process.env.accessKey)
//   .then((client) => {
//     client.on('uplink', async (devID, payload) => {
//       const value = payload.payload_fields
//       console.log(value, ': IS THE VALUE!!')

//       // const isAck = value.includes('ack')

//       // isAck ? console.log('Received ack from ', devID) : console.log('Received uplink from ', devID)

//       // if (isAck) {
//       //   // If ack was received => Extract message and delete from object.
//       //   const ack = value.substring(3)
//       //   delete detections[ack]
//       // } else if (detections[value] === undefined) {
//       //   // Notify video server and client through detectedLoRa function
//       //   console.log('YAAAAY!')
//       //   // detectedLora(STREAM_SERVER, client, io, payload, detections, value)
//       // } else if (detections[value]) {
//       //   // Add counts of detections. If 2 counts found send another ack.
//       //   detections[value] = detections[value]++
//       //   if (detections[value] > 2) {
//       //     client.send(payload.dev_id, [value.substring(value.length - 2)])
//       //     console.log('Sent new ack to node.')
//       //   }
//       // }
//     })
//   })
//   .catch((err) => {
//     console.log(err)
//   })

// const nodeMailer = require('nodemailer')
// const transporter = nodeMailer.createTransport({
//   // pool: 'smtps://ullvante_alf@hotmail.com:annaanna@smtp.live.com /?pool=true',
//   host: 'smtp.live.com',
//   port: 587,
//   secure: false,
//   auth: {
//     user: 'ullvante_alf@hotmail.com',
//     pass: process.env.email
//   }
// })

// transporter.verify(function (error, success) {
//   if (error) {
//     console.log(error)
//   } else {
//     console.log('Server is ready to take our messages')
//   }
// })
// const mailOptions = {
//   from: '"Artificial grass center" <ullvante_alf@hotmail.com>', // sender address
//   to: 'ullvante_alf@hotmail.com', // list of receivers
//   subject: 'Plan stängd!', // Subject line
//   text: 'Araby konstgräsplan är nu tyvärr stängd pga dåliga sensorer som tror att det är snö.', // plain text body
//   html:
//   '<p>Araby konstgräsplan är nu tyvärr stängd pga dåliga sensorer som tror att det är snö.</p><img src="data:image/png;base64,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" />'
// }

// transporter.sendMail(mailOptions, (error, info) => {
//   if (error) {
//     return console.log(error)
//   }
//   console.log('EMAIL SENT!:D')
// })

app.listen(port, () => console.log('Server running at http://localhost:' + port))

// Booking string
// `https://vaxjo.ibgo.se/BookingApi/GetBookings?start=${fromDate}+00%3A00&end=${toDate}+00%3A00&isPublic=true&resources%5B0%5D=50`

// Register string
// https://vaxjo.ibgo.se/AssociationRegister/GetAssociationsList?sEcho=2&iColumns=6&sColumns=Name%2CAssociationCategory%2CCustomerOccupations%2CWebSite%2CDistrict%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=Name&bSortable_0=true&mDataProp_1=AssociationCategoryName&bSortable_1=true&mDataProp_2=CustomerOccupationsText&bSortable_2=true&mDataProp_3=WebSite&bSortable_3=true&mDataProp_4=DistrictName&bSortable_4=true&mDataProp_5=5&bSortable_5=true&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1&CustomerName=Östers IF&DistrictId=&ActivityId=&AssociationCategoryId=&_=1586949943738
