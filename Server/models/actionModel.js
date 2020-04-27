const mongoose = require('mongoose')

const actionSchema = mongoose.Schema({
  id: { type: String, required: true },
  name: { type: String, required: true },
  bookings: { type: String, required: true },
  today: { type: String, required: true },
  oneDay: { type: String, required: true },
  twoDays: { type: String, required: true },
  sensor: { type: String, required: true },
  prediction: { type: String, required: true }
})

const Schema = mongoose.model('Action', actionSchema)

module.exports = Schema
