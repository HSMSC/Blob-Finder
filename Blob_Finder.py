Python 3.10.7 (v3.10.7:6cc6b13308, Sep  5 2022, 14:02:52) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> # Package imports
... import cv2 
... import numpy as np
... import matplotlib.pyplot as plt
... import os 
... import pandas as pd
... import csv
... import plotly.express as px
... import kaleido
... 
... 
... # Process an image and compute blob sizes and number
... 
... # Read image
... def Process_Image(imgfile):
...         im = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)
... 
...         # Setup SimpleBlobDetector parameters.
...         params = cv2.SimpleBlobDetector_Params()
... 
...         # Change thresholds
...         params.minThreshold = 10
...         params.maxThreshold = 200


        # Filter by Area.
        params.filterByArea = True
        params.minArea = 50

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.87
            
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.01

        # Create a detector with the parameters
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3 :
                detector = cv2.SimpleBlobDetector(params)
        else : 
                detector = cv2.SimpleBlobDetector_create(params)


        # Detect blobs.
        keypoints = detector.detect(im)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        # the size of the circle corresponds to the size of blob

        im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # Compute average size and number of blobs detected
        avg_size = sum([x.size for x in keypoints]) / len(keypoints)
        num_points = len(keypoints)

        return (avg_size, num_points)

#Note: all above are indented (inside the function, after defining process_image). If you get an indentation error, type ipython and try again.

# Read one image

imgloc = '/Users/Hazel/Documents/BLOB/Clump_Images/P1_S1_D.png'
(sz, num) = Process_Image(imgloc)
print(sz, num)


# Find a way to get a list of all files within some directory
# Create a for loop that processes each file in the list (omitting DS_Store files)
# Print the size and number for each file


file_path = '/Users/Hazel/Documents/BLOB/Clump_Images/'
files = os.listdir(file_path)
files = [f for f in files if f != '.DS_Store']
sizes = []
for file in files:
        if file == ".DS_Store":
                continue
        full_path = file_path + file
        (sz, num) = Process_Image(full_path)
        print(file, sz, num)
        sizes.append(sz)

#Quick plotting of the results above.
plt.scatter(files, sizes)
plt.show()

        
# Exercise: print a data frame

file_path = '/Users/Hazel/Documents/BLOB/Clump_Images/'
files = os.listdir(file_path)
files = [f for f in files if f != '.DS_Store']
sizes = []
nums = []
for file in files:
        full_path = file_path + file
        (sz, num) = Process_Image(full_path)
        print(file, sz, num)
        sizes.append(sz)
        nums.append(num)

BlobDataFrame = pd.DataFrame(data=(files, sizes, nums), index=['Sample', 'Size', 'Number'])

print(BlobDataFrame)

#Transpose

BlobDataFrame_transposed=BlobDataFrame.T
print(BlobDataFrame.T)


#Exporting dataframe as csv 

BlobDataFrame.T.to_csv('/Users/Hazel/Documents/BLOB/Blob.csv')

#This exports fine. For now, added external ELISA and other data to a copy of this CSV.


#To Graph: number of large clumps performance

df = pd.read_csv('/Users/Hazel/Documents/BLOB/BlobELISA.csv')

fig = px.scatter(df, x = 'ELISA', y = 'Blob', color='Sample')

fig.update_layout(
   title="Correlation to large clumps",
   xaxis_title="S1 IgG (µg,ml)",
   yaxis_title="Number of large clumps")

fig.show()
fig.write_image(fig.write_image('/Users/Hazel/Documents/BLOB/Graphs/BlobNumber.png'))


#Show correlations with MAT
df = pd.read_csv('/Users/Hazel/Documents/BLOB/BlobELISA.csv')

fig = px.scatter(df, x = 'LOGELISA', y = 'MAT', color='Sample')

fig.update_layout(
   title="Agglutination of human serum",
   xaxis_title="Log10 IgG Concentration",
   yaxis_title="Agglutination Score")

fig.show()

#Show original Mat over ELISA

df = pd.read_csv('/Users/Hazel/Documents/BLOB/BlobELISA.csv')

fig = px.scatter(df, x = 'LOGELISA', y = 'MAT', color="Sample")

fig.update_layout(
   title="Original Correlation",
   xaxis_title="Log10 IgG Concentration",
   yaxis_title="Agglutination Score")

fig.show()

#Plot Standard Curve
df = pd.read_csv('/Users/Hazel/Documents/BLOB/STDMM.csv')

fig = px.scatter(df, x = 'id', y = 'Average', error_y="STD")

fig.update_layout(
   #title="Agglutination of S1 IgG Versus Antibody Concentration",
   xaxis_title="IgG Concentration (µg/ml)",
   yaxis_title="Agglutination Score",
   plot_bgcolor="white")

fig.update_traces(marker_color='magenta')
fig.update_layout(xaxis=dict(showgrid=True),
              yaxis=dict(showgrid=True))
fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
fig.update_traces(marker={'size': 10}) 
#fig.update_layout(title="<b>Agglutination of S1 IgG Versus Antibody Concentration</b>")
fig.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=18,  # Set the font size here
        color="black"))

fig.show()

#Export graphs as PNGs

fig.write_image(fig.write_image('/Users/Hazel/Documents/BLOB/Graphs/STD.png'))

#make bar plot for specificity test
df = pd.read_csv('/Users/Hazel/Documents/BLOB/SPC.csv')

fig = px.bar(df, x = 'id', y = 'Average', error_y="STD")

fig.update_layout(
   title="S1-Coated Beads are Specific for SARS-CoV-2 IgG ",
   xaxis_title="Sample",
   yaxis_title="Agglutination Score",
   plot_bgcolor="white")
fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
fig.update_traces(marker_color='grey', width=0.5)

fig.show()

fig.write_image(fig.write_image('/Users/Hazel/Documents/BLOB/Graphs/SPC.png'))

#Pretty graphs for publication

#Show original Mat over ELISA

df = pd.read_csv('/Users/Hazel/Documents/BLOB/BlobELISA.csv')

fig = px.scatter(df, x = 'LOGELISA', y = 'MAT', color="Category")

fig.update_layout(
   #title="Agglutination of S1-IgG in Human Plasma ",
   xaxis_title="Log10 IgG Concentration (µg/ml)",
   yaxis_title="Agglutination Score",
   plot_bgcolor="white",
   legend=dict(
        bordercolor="Black",
        borderwidth=1))
fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
fig.update_traces(marker={'size': 10}) 
#fig.update_layout(title="<b>Agglutination of S1 IgG Versus Antibody Concentration</b>")
fig.update_layout(
    font=dict(
        #family="Courier New, monospace",
        size=18,  # Set the font size here
        color="black"))


fig.show()

fig.write_image(fig.write_image('/Users/Hazel/Documents/BLOB/Graphs/ALLPLASMA.png'))

