const mongoose = require('mongoose')

const pitchSchema = mongoose.Schema({
  id: { type: String, required: true, unique: true },
  name: { type: String, required: true },
  mult_id: { type: String },
  mult_names: { type: String },
  clear_email: { type: String },
  address: { type: String },
  zip: { type: String }
})

const Schema = mongoose.model('Pitch', pitchSchema)

module.exports = Schema
