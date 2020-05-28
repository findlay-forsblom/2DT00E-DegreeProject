#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox = Adafruit_VL53L0X();
long calibrated;
long depth;
long measured;
int counter;

void setup() {
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }
  
  Serial.println("Adafruit VL53L0X test");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  // power 
  Serial.println(F("VL53L0X API Simple Ranging example\n\n"));
    VL53L0X_RangingMeasurementData_t measure;
  long calibration = 0;
  int iter = 30;

  for(int i = 0; i < iter; i++){
    Serial.println("Reading a measurement... ");
    lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!
  
    if (measure.RangeStatus != 4) {  // phase failures have incorrect data
      calibration = calibration + measure.RangeMilliMeter;
    } else {
      Serial.println(" out of range ");
    }
    delay(100);
  }

  calibrated = calibration / iter;
  Serial.print("Calibrated distance: ");Serial.println(calibrated);
  

    
  delay(8000); 
}


void loop() {
  //Serial.print("Reading a measurement... ");
  int arr[200];
  int cnt = 0;
  for(int j=0; j<10;j++){
    for(int i=0; i < 20; i++){
        counter = 0;
        measured = 0;
        for(int k = 0; k < 10; k++){
          VL53L0X_RangingMeasurementData_t measure;
      
          lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!
        
          if (measure.RangeStatus != 4) {  // phase failures have incorrect data
            measured = measured + measure.RangeMilliMeter;
            counter = counter + 1;
            
          } else {
            Serial.println(" out of range ");
          }
          delay(100);
        }
        //Serial.println(counter);
        //Serial.println("Distance: ");
        Serial.println(measured/counter);
        //Serial.println("Depth: ");
        arr[cnt] = (measured/counter);
        cnt = cnt + 1;
    }
    //Serial.println(arr)
    Serial.print("[");
    for(int k = 0; k < j*10; k++){
      Serial.print(arr[k]);Serial.print(", ");
    }
        Serial.println("]");

  }



  
    
  delay(500);
}
