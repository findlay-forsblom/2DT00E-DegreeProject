# Web application
<b>The current version is only suitable for development at this stage.</b> [Read more](#security)

The intended functionality of this web application was to present sensor and predicted data, along with weather API data, to restrict the number of snow clearances at artificial grass pitches in Växjö county. The application should also handle the information dispersing upon pitch closure or clearance. The web application was written in JavaScript with Node.js. The framework used was Express.js, along with numerous modules to build up functionality. The view engine used was Express-hbs (handlebars). Information was dispersed through email, using the nodemailer module. The different functionalities are explained below.

## Starting the web application
To start the web application, the following commands should be used. Make sure the latest version of Node.js is installed. Redis is used for storing session variables. Make sure the Redis server is up and running, upon starting the application, [read more](https://redis.io/topics/quickstart).

### Using Node

The following command installs the node modules used in this application.
```
npm install
```

To run the application in development mode:
```
npm run devstart
```

The following command will run the application in production mode:
```
npm start
```

### Environment variables
The server uses environent variables for sensitive information, such as API keys, etc. They are store in a file named .env, which is not uploaded to the repository and therefore needs to be created before running the application. Upon clarity of how the variables are defined, please visit the documentation respectively.

| Environment variable | Description |
| --- | --- |
| SESSION_NAME | The session name used for Express-session |
| SESSION_SECRET | Used for Express-session to sign the session name cookie |
| CONNECTION_STRING | Used to connect to MongoDB database |
| APIkey  | Google GeoCoding API key  |
|  appID | The application ID at The Things Network  |
|  accessKey | The access key to the application at The Things Network  |
| dev_email  | Email to send when using development in actionController.js  |
| dev_email2 | Email to send when using development in actionController.js  |
| pitch_email | Email address to send email upon snow level detection |
| EMAIL  | Email address that nodemailer uses to send emails from   |

## Application usage
Upon detections of snow levels above 2 cm, a notification email is sent to the county authority (user) responsible for pitch actions. The user follows a link to the application page. If the user is not logged in already, the login page is rendered and upon successful login a redirect to the pitch page, as seen in the image below. Based on the sensor data ("Mätdata"), predicted upcoming snow levels ("Förväntat snödjup") and weather forecasts, a decision is made. Upon pitch clearance (yellow button), an email is sent to the responsible for clearing the particular pitch. Upon pitch closure (red button) an email is sent to all contacts found in the bookings section, fetched from the [IBGO API](#ibgo-api).

![Application page](/img/application.jpg)
<br>
The application page, rendered upon successful login.

## The Things Network (TTN)
As the sensor data was sent over LoRaWAN to The Things Network, to make the data available to the web application. The server received the information from TTN, using the ttn module along with the application keys needed to receive data. 

## Weather forecasts (SMHI API)
The weather forcasts were fetched from the [Swedish Meteorological and Hydrological Institute (SMHI) API](http://opendata.smhi.se/apidocs/metfcst/index.html) upon snow level detections above threshold. This was then sent into the machine learning algorithm.

## Machine Learning
The machine learning algorithm used Random Forrest to predict the upcoming snow depth, using the measured snow depth and weather forecasts as input parameters. The algorithm was written in Python, why the JavaScript had to be spawned into Python. When predictions were made, an email was sent to the authority handeling the decision making process.

### Versions for machine learning
When running the server and using the predefined machine learning models in the models folder, then you should make sure that the  versions of the following libraries are used:

* scikit-learn - 0.22.1
* numpy - 1.18.1
* joblib - 0.14.1

## Nodemailer
The emails dispersing was implemented with nodemailer. This was used both upon notifying authorities that decision might be needed, upon snow level detections, and upon dispersing information upon a confirmed decision. 

## Authentication and authorization
Simple authentication/authorization handeling was implemented. Only logged in users gained access to resources. All passwords were hashed, and user login details were stored in a database.

## Databases (MongoDB and Redis)
The user login data, along with pitch information and detection data were stored in MongoDb. All session data were stored in Redis.

## Security
This implementation were only made to create the intended functionalities for the web application. Therefore, numerous security implementations have to be made before putting the web application into production. Also, GDPR regulations are not implemented. <b>The current version is only suitable for development at this stage.</b>

## IBGO API
IBGO is a platform where bookings are handled for Växjö countys sport facilities. The usage of this API was made through reverse engineering, using Postman to find API calls, since it is not an open API. Both bookings and contact informations for the application was fetched using this API. 