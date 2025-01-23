from abc import ABC, abstractmethod
from pydglab_ws import DGLabLocalClient,DGLabWSClient
class BaseHandler(ABC):
    """处理器基类"""
    def __init__(self):
        pass
    @abstractmethod
    def handle(self, *args, **kwargs):
        """处理方法
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        """
        pass 