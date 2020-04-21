const actionController = {}

// app.use('/action', require('./routes/actionRouter.js'))

/**
 * Adds an action to database
 */
// const tester = async () => {
//   const Action = require('./models/actionModel.js')
//   const today = new Date()
//   const oneDay = new Date()
//   oneDay.setDate(oneDay.getDate() + 1)
//   const twoDays = new Date()
//   twoDays.setDate(oneDay.getDate() + 2)

//   const action = new Action({
//     id: 'test_2',
//     bookings: 'test_bookings_2',
//     date: today.toDateString(),
//     oneDay: oneDay.toDateString(),
//     twoDays: twoDays.toDateString(),
//     forecast: 'rainy'
//   })

//   await action.save()
// }

actionController.index = async (req, res, next) => {
  // console.log(req.params.id)
  const Action = require('../models/actionModel.js')
  const action = await Action.find({})

  const today = new Date()
  const oneDay = new Date()
  oneDay.setDate(oneDay.getDate() + 1)
  const twoDays = new Date()
  twoDays.setDate(oneDay.getDate() + 2)

  const current = await Action.findOne({ id: req.params.id })
  const currentArr = []
  let currentContext
  console.log(today.toDateString(), oneDay.toDateString(), twoDays.toDateString())

  if (current) {
    currentArr.push(current)

    currentContext = {
      currentAction: currentArr.map(act => {
        return {
          id: act.id,
          bookings: act.bookings,
          forecast: act.forecast
        }
      })
    }
    currentContext.currentAction[0].today = today.toDateString()
    currentContext.currentAction[0].oneDay = oneDay.toDateString()
    currentContext.currentAction[0].twoDays = twoDays.toDateString()
  }

  console.log(currentContext)

  // Must create new object to be able to render page with information.
  const context = {
    actions: action.map(act => {
      return {
        id: act.id,
        bookings: act.bookings,
        date: act.date
      }
    })
  }

  // console.log(currentContext.currentAction[0])
  res.render('action/decision', { current: current ? currentContext.currentAction[0] : null, data: context.actions })
}

actionController.clear = (req, res, next) => {
  res.send('Clear')
}

actionController.close = (req, res, next) => {
  res.send('Close')
}

module.exports = actionController
