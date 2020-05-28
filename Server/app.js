const express = require('express')
const hbs = require('express-hbs')
const path = require('path')
const mongoose = require('./config/mongoose.js')
const dotenv = require('dotenv')
const session = require('express-session')
const redis = require('redis')
const redisClient = redis.createClient()
const RedisStore = require('connect-redis')(session)
const ttn = require('ttn')
const predictor = require('./libs/predictor.js')
const Pitch = require('./models/pitchModel.js')

const siteUrl = 'http://localhost:8000'

dotenv.config({
  path: './.env'
})

const longlatGen = require('./libs/longLatGen.js')

const app = express()
app.use(express.json())
app.use(express.urlencoded({ extended: false }))

const sessionStore = new RedisStore({ host: 'localhost', port: 6379, client: redisClient, ttl: 86400 })

const sessionOptions = {
  name: process.env.SESSION_NAME,
  secret: process.env.SESSION_SECRET,
  resave: false, // Resave even if a request is not changing the session.
  saveUninitialized: false, // Don't save a created but not modified session.
  cookie: {
    maxAge: 1000 * 60 * 60, // % 1 hours
    sameSite: 'lax', // change to lax maybe
    HttpOnly: true
  },
  store: sessionStore
}

app.use(session(sessionOptions))

// const lol2 = async () => {
//   const longlatGen = require('./libs/longLatGen.js')
//   const lol = await longlatGen.gen('Bollgatan 1 Växjö', '35246')
//   const data = { snow: 0.05, temp: -5, humudity: 80 }
//   const prediction = await predictor.predict(data, lol)
//   console.log('PREDICTION: ', prediction)
// }

// lol2()

mongoose.connect().catch(error => {
  console.log(error)
  process.exit(1)
})

const port = 8000

app.use('/public', express.static(path.join(__dirname, '/public')))
app.use(express.static(path.join(__dirname, '/public')))

app.engine('hbs', hbs.express4({
  defaultLayout: path.join(__dirname, 'views', 'layouts', 'default'),
  partialsDir: path.join(__dirname, 'views', 'partials')
}))

app.set('view engine', 'hbs')

// Helper to check if strings are equal when rendering view.
hbs.registerHelper('ifAvailable', function (arg1, arg2, options) {
  return (arg1 !== arg2) ? options.fn(this) : options.inverse(this)
})

app.use(express.urlencoded({ extended: false }))

app.use((req, res, next) => {
  // flash messages - survives only a round trip
  if (req.session.flash) {
    res.locals.flash = req.session.flash
    delete req.session.flash
  }
  if (req.session.userId) {
    const user = {}
    const navbar = {}
    navbar.username = req.session.username
    navbar.type = req.session.role
    user.id = req.session.userId
    res.locals.loggedIn = user
    res.locals.navBar = navbar
  }

  next()
})

app.use('/action', require('./routes/actionRouter.js'))
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

async function newAction (sensor = { temp: 0.3, humid: 42.2, depth: 2.1, pitch: 85 }, predict = { first: 2.4, second: 1.1 }) {
  const today = new Date()

  const book = require('./libs/bookings')
  const data = await book.fetchBookings(today.toDateString(), sensor.pitch)
  const bookings = book.handleInfo(data.bookings, data.contact)

  const Action = require('./models/actionModel.js')
  const days = require('./libs/threeDates').consecutiveDays()

  const action = new Action({
    id: sensor.pitch,
    name: data.pitch.name,
    names: data.pitch.mult_names,
    clearEmail: data.pitch.clear_email,
    bookings: JSON.stringify(bookings),
    today: days.today.toDateString(),
    oneDay: days.oneDay.toDateString(),
    twoDays: days.twoDays.toDateString(),
    sensor: JSON.stringify(sensor),
    prediction: JSON.stringify(predict)
  })

  const savedAction = await action.save()

  const mailer = require('./libs/mailer')
  mailer.sendMail(
    [process.env.pitch_email],
    'Detekterad snö!',
    `<p>${data.pitch.name} kan behövas att skottas eller stängas. Följ länken nedan för att ta beslut.<br><br> <a href="${siteUrl}/action/${savedAction._id}">Beslut för ${data.pitch.name}</a> <br><br>Mvh, <br> Växjö Kommun.</p>`,
    `${data.pitch.name} kan behövas att skottas eller stängas. \n\n Gå till hemsidan ${siteUrl}/action/${savedAction._id} för att ta beslut.\n Mvh, \n Växjö Kommun.`
  )
}

// // newAction()

// async function addPitch () {
//   const Pitch = require('./models/pitchModel.js')
//   const pitch = new Pitch({
//     id: 85,
//     name: 'Värendsvallen Konstgräsplan',
//     mult_id: JSON.stringify([85, 212, 213]),
//     mult_names: JSON.stringify(['Plan C', 'Plan C - Halvplan 1', 'Plan C - Halvplan 2'])
//   })
//   await pitch.save()
// }

// addPitch()
// TTN =>
const detections = {}

// Listen for changes on application from TTN.
ttn.data(process.env.appID, process.env.accessKey)
  .then((client) => {
    client.on('uplink', async (devID, payload) => {
      const value = payload.payload_fields

      const isAck = value.values.includes('ack')

      isAck ? console.log('Received ack from ', devID) : console.log('Received uplink from ', devID)
      if (isAck) {
        // If ack was received => Extract message and delete from object.
        const ack = value.values.substring(3)
        delete detections[ack]
      } else if (detections[value.values] === undefined) {
        // Message received was not previously seen => Predict and send mail.
        // Send ack to client.
        client.send(payload.dev_id, [value.values.substring(value.values.length - 3)])
        detections[value.values] = 1
        console.log('Sent ack to node.')

        // Fetch pitch address and lat/long geodata.
        const pitch = await Pitch.findOne({ id: value.pitch })
        const geo = await longlatGen.gen(pitch.address, pitch.zip)

        // Format data for prediction.
        const data = { snow: value.depth / 100, temp: value.temp, humudity: value.humid }
        const prediction = await predictor.predict(data, geo)

        // Convert predictions to cm and create new action.
        const first = Math.round(prediction[0].snowlevel * 1000) / 10
        const second = Math.round(prediction[1].snowlevel * 1000) / 10
        newAction(value, { first: first, second: second })
      } else if (detections[value.values]) {
        // Add counts of detections. If 2 counts found send another ack.
        detections[value.valuess] = detections[value.values]++
        if (detections[value.values] > 2) {
          client.send(payload.dev_id, [value.values.substring(value.values.length - 3)])
          console.log('Sent new ack to node.')
        }
      }
    })
  })
  .catch((err) => {
    console.log(err)
  })

app.listen(port, () => console.log('Server running at http://localhost:' + port))
