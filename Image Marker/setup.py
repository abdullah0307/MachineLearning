from cx_Freeze import setup, Executable
packages = ["numpy","tkinter"]
includes=["tkinter"]
setup(name="Image_Marker",
      version="0.1",
      description="",
      options = {"build_exe": {"packages":packages}},
      executables=[Executable("ImageMarker.py")])