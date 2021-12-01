# Mouse using Hand Tracking

Based on the paper published by Hindawi, Deep learning based virtual mouse this recreates the functionality of the paper.

## Demo

![Image](https://github.com/Sarath191181208/paint/blob/master/images/Screenshot.png)

## Features

- Lift only index finger to drag the mouse around.
- Use Thumb finger and Index finger to lift click using a pinch-in gesture.
- Use Middle finger and Index finger to right click using a pinch-in gesture.
- Use Middle finger and Index finger to scroll.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Sarath191181208/mouse-tracking-using-Hand
```

Go to the project directory

```bash
  cd ./mouse-tracking-using-Hand
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

## Requirements

- python `Make sure to add to path, python version == 3.9`
- tkinter `default`
- opencv `pip install opencv-python==4.5.3.56`
- mediapipe `pip install mediapipe==0.8.7.1`
- mouse `pip install mouse==0.7.1`
