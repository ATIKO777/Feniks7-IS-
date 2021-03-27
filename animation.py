from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QGraphicsOpacityEffect

def rise_label (q_object):
    # global fade_effect
    global animation
    fade_effect = QGraphicsOpacityEffect(q_object)
    q_object.setGraphicsEffect(fade_effect)
    animation = QPropertyAnimation(fade_effect, b"opacity")
    animation.setDuration(1500)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.Linear)
    # animation.setEasingCurve(QEasingCurve.InQuad)
    # animation.start()
    animation.start(QPropertyAnimation.DeleteWhenStopped)
    q_object.setVisible(True)
