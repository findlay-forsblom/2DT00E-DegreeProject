const express = require('express')
const hbs = require('express-hbs')
const path = require('path')
const mongoose = require('./config/mongoose.js')

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

app.listen(port, () => console.log('Server running at http://localhost:' + port))
