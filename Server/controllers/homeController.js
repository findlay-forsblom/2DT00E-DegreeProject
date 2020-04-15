const homeController = {}

homeController.index = async (req, res, next) => {
  res.render('home/home')
}

homeController.register = async (req, res, next) => {
  res.render('home/register')
}

module.exports = homeController
