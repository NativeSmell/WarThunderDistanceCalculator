# WarThunderDistanceCalculator

Press Middle Mouse Button to calculate distance between you and Squad Mark. (In War Thunder you need change a Squad Mark button to Middle Mouse Button too)

> Middle Button + Left Alt: Distance between you and Cursor (put cursor on map)


> Middle Button + Left Ctrl: Distance between your team mate and Squad Mark (if you use this with Left alt: Distance between your team mate and Cursor)


If you see, what disntance isn't work fine. Try to check in "set scale manualy" and enter the distance to Scale field 


# To download

> https://disk.yandex.ru/d/S99Wt6OtqR_BQQ

> https://drive.google.com/file/d/14zhPAg9OwGeJdgpTx3HFjUJPts9uOyPl/view?usp=share_link


# For create exe:

> pyinstaller --noconfirm --onedir --windowed --icon "D:/PythonProjects/PyQT/WarThunderDistanceCalculator/assets/map.ico" --hidden-import "xml.etree.ElementTree" --hidden-import "sklearn"  "D:/PythonProjects/PyQT/WarThunderDistanceCalculator/main.py"