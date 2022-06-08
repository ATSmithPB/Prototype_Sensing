//Semantics:
//Temperature Sensor == TS
//Rotary Encoder == RE
//Rotary Encoder CCW Pin = CLK
//Rotary Encoder CW Pin = DT

// Include Libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// Define Inputs and Outputs
  const int RECount = 6;
  const int TSCount = 6;
  const int DStartPin = 22;
  const int TSStartPin = 2;

  int tempIteration = 0;
  long tempEvery = 9999; //read TS every n loops
  int writeEvery = 100;//serial write every n loops
  int REIndex [RECount];
  int TSIndex [TSCount];
  int RECLKPin [RECount];
  int REDTPin [RECount];
  int TSDATAPin [TSCount];
  int previousStateCLK [RECount];
  int currentStateCLK [RECount];
  int REcounter [RECount];
  int currentStateDT [RECount];
  String encdir [RECount];
  double detentCirDist = 1.50; // Circum/nDetents (48mm/32) 
  float TempC [TSCount];
  float RETravel[TSCount];

  //Setup oneWire instances to communicate w/ sensors & pass to Dallas Temperature
  #define ONE_WIRE_BUS_0 2
  #define ONE_WIRE_BUS_1 3
  #define ONE_WIRE_BUS_2 4
  #define ONE_WIRE_BUS_3 5
  #define ONE_WIRE_BUS_4 6
  #define ONE_WIRE_BUS_5 7
  OneWire oneWire0(ONE_WIRE_BUS_0);
  OneWire oneWire1(ONE_WIRE_BUS_1);
  OneWire oneWire2(ONE_WIRE_BUS_2);
  OneWire oneWire3(ONE_WIRE_BUS_3);
  OneWire oneWire4(ONE_WIRE_BUS_4);
  OneWire oneWire5(ONE_WIRE_BUS_5);
  DallasTemperature TS0(&oneWire0);
  DallasTemperature TS1(&oneWire1);
  DallasTemperature TS2(&oneWire2);
  DallasTemperature TS3(&oneWire3);
  DallasTemperature TS4(&oneWire4);
  DallasTemperature TS5(&oneWire5);
  
void setup() { // put your setup code here, to run once:
  //Populate Arrays for I/Os
    for (int i = 0; i < RECount; i++){
    REIndex[i] = i;
    TSIndex[i] = i;
    RECLKPin[i] = DStartPin + (i*2);//even -- YELLOW/PURPLE -- GREEN
    REDTPin[i] = DStartPin + ((i*2)+1);//odd -- ORANGE -- BLUE
    TSDATAPin[i] = TSStartPin + i;
  //Set-Up Pins 
    pinMode (RECLKPin[i],INPUT);
    pinMode (REDTPin[i],INPUT);
    }
  
  //Set-Up Serial Moniter
    Serial.begin(115200);

  //Set-Up Previous States
    for (int i = 0; i < RECount; i++){
    previousStateCLK[i] = digitalRead(RECLKPin[i]);
    }
  //Set-up Temp Sensor libraries  
    TS0.begin();
    TS1.begin();
    TS2.begin();
    TS3.begin();
    TS4.begin();
    TS5.begin();
}
  
void loop() {  // put your main code here, to run repeatedly:
    String dataStringCSV;
    
    //update the temperature values every n loops
    if (tempIteration == 0){
    TS0.requestTemperatures();
    TS1.requestTemperatures();
    TS2.requestTemperatures();
    TS3.requestTemperatures();
    TS4.requestTemperatures();
    TS5.requestTemperatures();
    
    TempC[0] = TS0.getTempCByIndex(0);
    TempC[1] = TS1.getTempCByIndex(0);
    TempC[2] = TS2.getTempCByIndex(0);
    TempC[3] = TS3.getTempCByIndex(0);
    TempC[4] = TS4.getTempCByIndex(0);
    TempC[5] = TS5.getTempCByIndex(0);
    }
    
    
  //Read the current state of RE CLK pins
    for (int i = 0; i < RECount; i++){
    currentStateCLK[i] = digitalRead(RECLKPin[i]);

    if (currentStateCLK[i] != previousStateCLK[i]){
      currentStateDT[i] = digitalRead(REDTPin[i]);
      if (digitalRead(REDTPin[i]) != currentStateCLK[i]){
        REcounter[i] --;
        encdir[i] = "C";
        }else{
        REcounter[i] ++;
        encdir[i] = "E";
        }
      }//end pin

      if (tempIteration % writeEvery == 0){
        RETravel[i] = REcounter[i] * detentCirDist;// Calculate travel distance
        //Concat RE and TS values to CSV string
        dataStringCSV.concat(RETravel[i]);
        dataStringCSV.concat(',');
        dataStringCSV.concat(TempC[i]);
        if (i < RECount - 1){
          dataStringCSV.concat(',');
          }
        }
      previousStateCLK[i] = currentStateCLK[i];
    }//end pins
  
  //Serial Write
    if (tempIteration % writeEvery == 0){
    Serial.println(dataStringCSV);
    }

  //iterate and/or reset tempIteration
    tempIteration++;
    if (tempIteration == tempEvery){
    tempIteration = 0;
    }
    delay(5);
}//end loop
