# social-distancing-v2

https://youtu.be/1NOkuQelV7E

<img width="1148" alt="image" src="https://user-images.githubusercontent.com/41614960/166265315-2370a242-3673-4e7b-a397-dbcb33082c20.png">

<img width="1148" alt="image" src="https://user-images.githubusercontent.com/41614960/166265400-46a11b69-b121-44e6-9946-6e068a5da466.png">

<img width="1148" alt="image" src="https://user-images.githubusercontent.com/41614960/166545484-3072f5f5-da0b-4a45-907d-8fbaa5990140.png">

---

Это приложение предназначено для контроля социальной дистанции. 

Как это работает:

1. Сверточная сеть обнаруживает людей
1. Координаты преобразуются в абсолютные
1. Перебираеются все пары координат и вычисляются расстояния

Использованные технологии:

- [YOLOv3](https://pjreddie.com/darknet/yolo/)
- [OpenCV](https://opencv.org/)
- [Qt 6](https://www.qt.io/product/qt6)

В мастере настройки можно указать путь к видеофайлу, 0 для веб-камеры и url любой rtsp камеры.

---

pyinstaller build command
```bash
pyinstaller main.py --onefile -n 'SocialDistancing' --windowed --icon=icon.png
```
