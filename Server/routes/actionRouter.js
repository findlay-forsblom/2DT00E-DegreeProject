const controller = require('../controllers/actionController.js')
const express = require('express')

const router = express.Router()

router.get('/clear/:id/:date', controller.ensureAuthenticated, controller.authorize, controller.clear)
router.get('/close/:id/:date', controller.ensureAuthenticated, controller.authorize, controller.close)
router.get('/:id', controller.ensureAuthenticated, controller.index)
router.get('/', controller.ensureAuthenticated, controller.index)

module.exports = router
