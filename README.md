# CheckerDistance

This Python Script was created to utilize a circle object of a known diameter (a US Quarter is used for my example) and measure the distance of a checker on a table. The script requires the known diameter of the circular object to obtain the correct pixel/in ratio. This was created because my group needed a more accurate measuring device and by utilizing an Iphone 8's high megapixel camera and photo quality accurate measurements could be attained. This automated the measurement process improving the speed at which we captured data as well as removed human errors. Measurements could be made down to roughly ~0.0005 inches in my usage but higher precision is possible I would assume.

The cv2.Canny value needs to be adjusted depending on the quality of the photos, shadows and lighting of the photos.

This script gave me great experience with utilizing cv, an open computer vision library that can be used in Python. I was able to put into real world use my programming skills by automating the measurement and analyzing process for my group.

The Week 13 folder contains some photos used for my project. Directing the script to the folder will analyze the data and give the results in csv file.

Install the required Python libraries by running "pip install -r requirements.txt" in the Python directory.

The Week 5 Histogram Excel file is where I computed and analyzed all the data that we collected each week. This was a project for a Six Sigma Green Belt and we had to use tools such as 3D Histograms, Control Charts and Individual Sheets. This helped us determine factors that affected our data and allowed us to improve each week.
