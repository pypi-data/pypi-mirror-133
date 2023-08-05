import setuptools 

setuptools.setup( 
    name='VCIBD2', 
    version='2.0.0', 
    author="Deo Krishna", 
    author_email="deo2k09@gmail.com", 
    description="You will be able to make a program which can take input in the form of audio.",
    long_description="Please visit at-'https://github.com/Deo-Krishna/VCIBD2/blob/main/README.md'",  
    packages=["VCIBD2"], 
    install_requires=["SpeechRecognition","pyaudio","pyttsx3"],  
    classifiers=[ "Programming Language :: Python :: 3", 
    "License :: OSI Approved :: MIT License", 
    "Operating System :: OS Independent", 
    ]
)