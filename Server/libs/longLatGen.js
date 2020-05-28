/**
 * Fetches Geodata using node-geocoder.
 *
 * @author Findlay Forsblom, Linnaeus University.
 */

const NodeGeocoder = require('node-geocoder')

const options = {
  provider: 'google',
  // Optional depending on the providers
  apiKey: process.env.APIkey // for Mapquest, OpenCage, Google Premier
}

module.exports.gen = async (address, zipcode) => {
  const geocoder = NodeGeocoder(options)
  const res = await geocoder.geocode({
    address,
    country: 'Sweden',
    zipcode
  })
  return { lat: res[0].latitude, long: res[0].longitude }
}
