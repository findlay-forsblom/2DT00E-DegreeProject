const mongoose = require('mongoose')

const pitchSchema = mongoose.Schema({
  id: { type: String, required: true, unique: true },
  name: { type: String, required: true }
})

const Schema = mongoose.model('Pitch', pitchSchema)
console.log('change')

module.exports = Schema
