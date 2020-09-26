import matplotlib.pyplot as plt # Plotting
import numpy as np # Arrays

loading = True
points = np.array([]) # Array of plotting points
perm = np.array([]) # Helping array
line_counter = 0 # Lines counter

while loading == True: # Cycle along all files  
  path = input('Input path: ')
  file_name = path.split('\\')[-1]
  with open(path) as file:  
    for line in file: # Cycle along lines in files=
      line_counter += 1 # Counting lines
      if line_counter > 2: # Skip 3 first lines
        line = np.array(line.strip(' ').split()) # Splitting by spaces
        if line[0] == 'I=': # New line
          perm = perm.flatten() # 1D array
          if len(points) == 0: 
            points = np.append(points, perm) # Append if it is empty
          else:
            points = np.vstack((points, perm)) # Stack if not empty
          perm = np.array([]) # Nulling array
        else:
          line = line.astype(float) # Needed data type
          perm = np.append(perm, line) # Fill in helping array

    # Append last line
    perm = perm.flatten()
    if len(points) == 0:
      points = np.append(points, perm)
    else:
      points = np.vstack((points, perm))

    plt.figure(figsize=(8,8))
    plt.imshow(points.T, cmap='hot', interpolation='nearest') 
    cbar = plt.colorbar() # Color bar
    cbar.ax.tick_params(labelsize=16) # Digits size
    cbar.ax.yaxis.get_offset_text().set(size=16) # Size of power on colorbar
    cbar.set_label('E-field amplitude', fontsize=16) # Size of label and label itself on colorbar
    plt.title(file_name) # Title
    plt.xlabel('z (nm)', fontsize=16) # Size and title of X
    plt.ylabel('x (nm)', fontsize=16) # Size and title of Y
    h, w = points.shape # Boundaries of picture
    print()
    plt.xlim(0,h) # X limits
    plt.ylim(w,0) # Y limits
    plt.show() # Show plot

    print('Max value for ', file_name,' = "{:.2e}"'.format(np.amax(points))) # Max value in points 
    print('To save picture press right button of mouse -> "Save as..."')
    print('Picture format is .png, it will be transparent')

    # Nulling variables 
    perm = np.array([])
    points = np.array([])
    line_counter = 0
    
    answer = input('More files? (+/-): ')
    if answer == '-':
      loading = False
    print()
print('The program is finished!')
input('Press ENTER to quit...')
