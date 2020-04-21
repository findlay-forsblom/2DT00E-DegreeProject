const controller = require('../controllers/actionController.js')
const express = require('express')

const router = express.Router()

router.get('/clear/:id', controller.clear)
router.get('/close/:id', controller.close)
router.get('/:id', controller.index)

module.exports = router
