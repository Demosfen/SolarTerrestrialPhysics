This simple script compares substorm onsets 
listed in ASCII file(s) with Kp-index.

--- HOW TO USE ---

1. Download Kp indexes from https://omniweb.gsfc.nasa.gov/form/dx1.html
    (please uncheck all checkboxes and check "Kp*10 Index") 
    
2. Change "kpIndexFilename" variable (line 119)
        according to the name of the downloaded Kp-index file ;
        
3. Put Kp-index data file to ../data directory;

4. Put your substorm onsets list to ../lists directory;
    (download list here: https://supermag.jhuapl.edu/substorms/?tab=download)

5. Change "substormListNames" list variable (line 117)
        according to the name(s) of your substorm(s) list(s);
        
6. Change header of the output file (if needed) (line 101-106)
        
6. Launch the script.

--- Data formats ---

1. No need to change Kp-index data file from OMNIweb;

2. Example of Date and Time columns in the list file:
       '2013 02 13 14 32 ...'
3. This script ignores all other columns and append corresponding Kp
       to the end of the line.
4. If you want to comment some lines in your onsets list,
       use "#" sign at the beginning of the line.
