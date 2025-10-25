from abc import ABC, abstractmethod
from django.utils import timezone

#Observer Interface 
class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

# Subject Interface
class Subject(ABC):
    def __init__(self):
        self._observers = [] 

    def register(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self) 

# Concrete Observers
class PostTakedownObserver(Observer):
    def update(self, subject):
        from .models import PostReportSubject 
        
        state = subject.get_state()
        post = state['post']
        
        if post.is_active:
            post.is_active = False
            post.save()
            print(f"Post {post.id} taken down.")


class AuthorNotificationObserver(Observer):

    def update(self, subject):
        from .models import Notification, PostReportSubject
        
        state = subject.get_state()
        post = state['post']
        reporter = state['reporter']
        
        Notification.objects.create(
            user=post.author,
            post=post,
            message=f"Your post '{post.title}' is currently under review after being reported by {reporter.username}.",
            is_new=True 
        )
        print(f"Notification created for author {post.author.username}.")