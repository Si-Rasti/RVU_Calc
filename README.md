# RVU_Calc
Calculating detailed physician fee schedule payment for current procedural terminology (CPT) codes can be burdensome due to many applicable regulations. You can calculate detailed RVUs and final fees using an Excel spreadsheet with a column named "CPT" that harbors up to 3 CPT codes separated by comma-space.
The code here is specifically written for radiological diagnostic procedures, but with a bit of manipulation can be generalized in scope. The reference file is published every three months by CMS.gov, but needs some modifications to be further used. Firstly, the headings should be omitted to let the first row contain column names. Then, using the file "CMS_merge_row," you can produce the reference file for further analysis, and finally, run the main.py.

