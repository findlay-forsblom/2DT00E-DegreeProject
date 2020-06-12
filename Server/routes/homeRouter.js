const controller = require('../controllers/homeController.js')
const express = require('express')

const router = express.Router()

router.post('/login', controller.login)
router.post('/logout', controller.logout)

// Uncomment this route if no registrations should be possible.
router.route('/register')
  .get(controller.register)
  .post(controller.registerPost)

router.get('/:id', controller.index)
router.get('/', controller.redirectAuthenticated, controller.index) // Login page

module.exports = router
