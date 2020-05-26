# 2DT00E-DegreeProject
This thesis project was assigned by dizparc on behalv of Växjö Kommun. The [participants](https://github.com/findlay-forsblom/2DT00E-DegreeProject/graphs/contributors) of this project were students at Linnaeus University. The problem at hand was to limit the number of snow clearances at artificial grass pitches in Växjö, due to rubber granulates leaking into the environment. This included automating the snow depth measurement, testing different [sensor techniques](/Sensor), predicting snow depth in the near future using [Random Forrest as machine learning model](/Algorithm) and present the measured and predicted data in a [web application](/Server). 

## Process
To restrict the number of snow clearances, Växjö county decided to close the pitch upon snow depths above 2cm and one additional criterion is fulfilled: If there is snowfall or the snow will melt in the near future. Else, the pitch will be cleared. This is done by presenting weather API data, along with the measured and predicted data at the web application, to let the authorities make a decision. Upon a confirmed decision, this information is dispersed to the appropriate persons/teams. The image below shows the project flowchart.

![The project process.](/img/flowchart.jpg)
<br>
Flowchart of the project process.

## Machine learning algorithm
Text about the ML algorithm. A more in depth explanation of the web application can be found in the [Algorithm folder](/Algorithm).

## IoT device
The IoT device should handle the snow depth, relative humidity and temperature measurements and send the data via LoRaWAN to the web application server. This was done via The Things Network, which made the data available to the application connected to the server. The sensors techniques tested was ultrasonic, micro LIDAR, IR and a relative humidity and temperature sensor. More in depth information can be found in the [Sensor folder](/Sensor).

## Web application
The web application was written in JavaScript with Node.js. The framework used was Express.js, along with numerous modules to build up functionality. The information was dispersed through email, using the nodemailer module. A more in depth explanation of the web application can be found in the [Server folder](/Server).