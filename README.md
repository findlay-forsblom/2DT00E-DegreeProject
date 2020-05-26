# 2DT00E-DegreeProject
This thesis project was assigned by dizparc on behalv of Växjö Kommun. The participants of this project were students at Linnaeus University. The problem at hand was to limit the number of snow clearances at artificial grass pitches in Växjö, due to rubber granulates leaking into the environment. This included automating the snow depth measurement, testing different [sensor techniques](/Sensor), predicting snow depth in the near future using [Random Forrest as machine learning model](/Algorithm) and present the measured and predicted data in a [web application](/Server). 

## Process
To restrict the number of snow clearances, Växjö county decided to close the pitch upon snow depths above 2cm and one additional criterion is fulfilled: If there is snowfall or the snow will melt in the near future. Else, the pitch will be cleared. This is done by presenting weather API data, along with the measured and predicted data at the web application, to let the authorities make a decision. Upon a confirmed decision, this information is dispersed to the appropriate persons/teams. The image below shows the project flowchart.

![The project process.](/img/flowchart.eps)
<br>
Flowchart of the project process.

## Machine learning algorithm
