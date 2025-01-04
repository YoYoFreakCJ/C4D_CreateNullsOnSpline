# Introduction
This script creates Nulls along a Spline in Cinema 4D. The Nulls are equally spaced based on the desired amount of Nulls. The user will be asked how many Nulls to create. Tested with Cinema 4D 2025.1.1.

# Usage
Select any Spline object and run the script. When prompted, enter the amount of Nulls you wish to create. The Nulls will be inserted under the Spline object.

# Installation
1. Download [CreateNullsOnSpline.py](/CreateNullsOnSpline.py)
2. In Cinema 4D go to **Extensions** -> **Script Manager**.
3. In the Script Manager, go to **File** -> **Import Script...**.
4. Select the downloaded file.

# For Developers
The script is written in a way which allows for easy implementation in other scripts.

This script inserts the Nulls under the Spline object. If you wish to insert them somewhere else you may simply adjust the line in `main` which calls `add_nulls_to_object`.
This script gets the Spline object by using the selected object. If you wish to choose another Spline object you may simply change the implementation of `get_spline`.
This script gets the amount of desired Nulls by asking the user in an input dialog. If you wish to choose another amount you may simply change the implementation of `get_desired_count`.
