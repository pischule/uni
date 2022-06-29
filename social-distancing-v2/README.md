# social-distancing-v2

https://youtu.be/1NOkuQelV7E

<img width="1050" alt="Screenshot 2022-06-29 at 22 24 22" src="https://user-images.githubusercontent.com/41614960/176519330-cd2b8197-dccd-4db8-9a08-c813aac56797.png">

---

Это приложение для контроля социальной дистанции.

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
