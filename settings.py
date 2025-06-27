from PySide6.QtCore import QSettings


def get_settings() -> QSettings:
    """获取全局配置

    Returns:
        QSettings: QSettings配置对象
    """
    return QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, "jiek", "live-caption-py")
