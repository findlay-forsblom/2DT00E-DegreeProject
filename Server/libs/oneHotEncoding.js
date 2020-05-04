const data = require('../data.json')
var OneHot = require('one-hot')
const obj = JSON.parse(data)
var oneHot = new OneHot();
// oneHot.encode(obj)

let counter = 0
const dict = {}
obj.forEach(element => {
  let i = 0
  const arr = []
  for (i = 0; i < obj.length; i++) {
    if (counter === i) {
      arr[i] = 1
    } else {
      arr[i] = 0
    }
  }
  dict[element] = arr
  counter++
})

const values = { 0: 'none', 1: 'snowfall', 2: 'snöblandat regn', 3: 'regn', 4: 'duggregn', 5: 'underkyld nederbörd' }

module.exports.encode = (precip) => {
  try {
    const type = values[precip]
    return dict[type]
  } catch (error) {
    console.log(error)
  }
}
