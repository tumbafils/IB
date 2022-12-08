#!/bin/bash
d=$(dirname $0)
if [ $d = "." ]; then d=$(pwd); fi

# Copy libIBScanUltimate.so 
file=$d/../lib/libIBScanUltimate.so
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

# Copy libIBScanUltimateJNI.so
file=$d/../lib/libIBScanUltimateJNI.so
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

######### PAD Library File copy (If PAD library exist) #########
if [ -e "$d/../lib/libLiveFinger2.so" ] # Check Package has PAD library file
then
    # Copy libIBScanUltimateJNI.so
    file=$d/../lib/libLiveFinger2.so
    dest=/usr/lib
    if cp -f $file $dest ; then
      echo "Copied $file to $dest"
    fi
else
    echo "PAD Library not exist, Skipping.."
    
fi
################################################################

################### Clean libAKXUS and libUVC ##################
# Delete previous Columbo Mini runtime library files
sudo rm -f /usr/lib/libAKXUS*
sudo rm -f /usr/lib/libuvc*

###################### libAKXUS.so #############################
# Copy libAKXUS.so.2.0.10
file=$d/../lib/libAKXUS.so.2.0.10
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"  
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

# Copy libAKXUS.so.2
file=$d/../lib/libAKXUS.so.2
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

# Copy libAKXUS.so
file=$d/../lib/libAKXUS.so
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

###################### libuvc.so #############################
# Copy libuvc.so.0.0.6
file=$d/../lib/libuvc.so.0.0.6
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

# Copy libuvc.so.0
file=$d/../lib/libuvc.so.0
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

# Copy libuvc.so
file=$d/../lib/libuvc.so
dest=/usr/lib
if cp -f $file $dest ; then
  echo "Copied $file to $dest"
else
  echo "Could not copy $file to $dest - check your permissions"
  exit
fi

#Check that we're really running a 2.6 kernel or higher
if [ "`uname -r | cut -f 1,2 -d .`" \< "2.6" ]; then
  echo "A minimum kernel level of 2.6.x is required.  Aborting."
  exit
fi
