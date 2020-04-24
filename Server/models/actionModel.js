const mongoose = require('mongoose')

const actionSchema = mongoose.Schema({
  id: { type: String, required: true },
  name: { type: String, required: true },
  forecast: { type: String, required: true },
  bookings: { type: String, required: true },
  date: { type: String, required: true }
})

const Schema = mongoose.model('Action', actionSchema)

module.exports = Schema
