const mongoose = require('mongoose')

const actionSchema = mongoose.Schema({
  id: { type: String, required: true, unique: true, minlength: 3 },
  forecast: { type: String, required: true },
  bookings: { type: String, required: true },
  date: { type: String, required: true }
})

const Schema = mongoose.model('Action', actionSchema)

module.exports = Schema
