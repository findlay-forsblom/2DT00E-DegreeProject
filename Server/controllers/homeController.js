const passwordChecker = require('../libs/passwordChecker.js')

const homeController = {}
const roles = ['User', 'Admin']
const User = require('../models/user.js')

homeController.index = async (req, res, next) => {
  res.render('home/home')
}

homeController.register = async (req, res, next) => {
  res.render('home/register')
}

homeController.logout = async (req, res, next) => {
  delete req.session.userId
  req.session.flash = { type: 'success', text: 'Succesfully logged out' }
  res.redirect('/')
  req.session.cookie.maxAge = 0
}

homeController.redirectAuthenticated = async (req, res, next) => {
  if (req.session.userId) {
    res.redirect('/action')
  } else {
    next()
  }
}

homeController.login = async (req, res, next) => {
  // Fetch and process request parameters.
  let email = req.body.username
  const password = req.body.password
  email = email.trim()
  email = email.toLowerCase()

  try {
    // Check if user exist
    const user = await User.findOne({ email })
    if (!user) {
      req.session.flash = { type: 'danger', text: 'Log in failed. Username or password is incorrect.' }
      res.redirect('/')
      return
    }
    const result = await user.comparePassword(password)

    if (result) {
      req.session.userId = user.id
      req.session.username = user.username
      req.session.role = user.role
      req.session.flash = { type: 'success', text: `Welcome ${user.username}. You have succesfully logged in` }
      res.redirect('/action')
    } else {
      req.session.flash = { type: 'danger', text: 'Log in failed. username or password is incorrect' }
      res.redirect('/')
    }
  } catch (error) {
    console.log(error.message)
    req.session.flash = { type: 'danger', text: 'An error ocuured while logging in. Please try again later' }
    res.redirect('/')
  }
}

homeController.registerPost = async (req, res, next) => {
  console.log('I am here boi')
  let username = req.body.username
  let email = req.body.email
  const password = req.body.password
  const confirmPassword = req.body.confirmPassword

  // Process fetched parameters.
  username = username.trim()
  username = username.toLowerCase()
  username = username.charAt(0).toUpperCase() + username.slice(1)
  email = email.trim()
  const match = passwordChecker.check(password, confirmPassword)

  if (match) {
    try {
      const user = new User({
        username: username,
        email: email,
        password: password,
        role: roles[1]
      })

      await user.save()

      req.session.flash = { type: 'success', text: 'User succesfully created' }
      req.session.userId = user.id
      req.session.username = user.username
      req.session.role = user.role
      res.redirect('/action/test')
    } catch (error) {
      req.session.flash = { type: 'danger', text: error.message }
      res.redirect('/register')
    }
  }
}

module.exports = homeController
