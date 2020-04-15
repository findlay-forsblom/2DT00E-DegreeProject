const express = require('express')
const hbs = require('express-hbs')
const path = require('path')
const mongoose = require('./config/mongoose.js')
const dotenv = require('dotenv')
const ttn = require('ttn')

dotenv.config({
  path: './.env'
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
//   host: 'smtp.live.com',
//   port: 587,
//   secure: false,
//   auth: {
//     user: 'ullvante_alf@hotmail.com',
//     pass: process.env.email
//   }
// })
// const mailOptions = {
//   from: '"Lars" <ullvante_alf@hotmail.com>', // sender address
//   to: 'ff222ey@student.lnu.se', // list of receivers
//   subject: 'Hiho', // Subject line
//   text: 'Test yo', // plain text body
//   html: '<b>NodeJS Email Tutorial</b>' // html body
// }

// transporter.sendMail(mailOptions, (error, info) => {
//   if (error) {
//     return console.log(error)
//   }
//   console.log('EMAIL SENT!:D')
// })

app.listen(port, () => console.log('Server running at http://localhost:' + port))
