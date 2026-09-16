print('===Peripheral Test Tool===')
try:
  user=int(input("Please select usb option 1/2: "))
  if user == 1:
    print("Starting USB test...")
  elif user == 2:
    print("Exit")
  else:
    print("Invalid option")
except ValueError:
  print("Invalid option")
  
