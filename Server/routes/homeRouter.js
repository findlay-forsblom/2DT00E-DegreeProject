const controller = require('../controllers/homeController.js')
const express = require('express')

const router = express.Router()

router.get('/:id', controller.index)
router.get('/', controller.redirectAuthenticated, controller.index) // Login page

router.post('/login', controller.login)
router.post('/logout', controller.logout)

router.route('/register')
  .get(controller.register)
  .post(controller.registerPost)

module.exports = router
