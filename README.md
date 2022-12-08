# Pellet-Printer-GCODE
Repository for code that converts relative, filament based GCODE into absolute GCODE that can be read and used by WWU's pellet printer.

Instructions:
1) You must have the latest version of python installed on your computer
2) Download the file titled "post_process.py" to the same directory as your unmodified GCODE file
3) Modify line 56 by inputting the name of your original GCODE file. Do not remove quotation marks ![image](https://user-images.githubusercontent.com/8853298/206346341-585b9993-ec6a-4805-93e6-fd41a49051d2.png)
4) Since we only want to modify a certain block / chunk of the code, we need to tell the program where to start and stop modification. This is defined as the variables titled "startPattern" and "stopPattern" on line 12 & 11. Open your original GCODE file and find the last instance of the recorded time. This should look something like "TIME_ELAPSED:XXXXX". Replace the X's with your numerical value. The start pattern will not need to be changed.![image](https://user-images.githubusercontent.com/8853298/206347077-ca4fc6ad-ab0f-4a6a-b721-ee838623a60f.png)
5) Save the python file and open either Command Prompt (PC) or Terminal (Apple)
6) Move directories until you are in the same directory as your GCODE and Python files
7) Run the Python file by typing py post_process.py or python post_process.py
8) A new file will be generated in this directory titled, "result.gcode"
