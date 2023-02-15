from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    """Модель Group(группы)."""
    title = models.CharField(max_length=200, verbose_name='Название',
                             help_text='Введите название группы')
    slug = models.SlugField(unique=True, verbose_name='Номер группы')
    description = models.TextField(verbose_name='Описание',
                                   help_text='Введите описание группы')

    def __str__(self):
        """Вывод названия группы."""
        return self.title


class Post(models.Model):
    """Модель Post(посты)."""
    text = models.TextField(verbose_name='Текст',
                            help_text='Введите текст поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', verbose_name='Автор')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='posts', blank=True, null=True,
                              verbose_name='Группа',
                              help_text='Выбирите группу')
    image = models.ImageField(verbose_name='Картинка',
                              help_text='Загрузите изображение',
                              upload_to='posts/', blank=True)

    def __str__(self):
        """Вывод текста поста."""
        return self.text[:15]

    class Meta:
        """Мета класс, для отображения сразу упорядоченых постов."""
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    """Модель комментария к посту."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comment',
                             verbose_name='Пост', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comment',
                               verbose_name='Автор', null=True)
    text = models.TextField(verbose_name='Комментарий',
                            help_text='Введите комментарий')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата комментария',
                                   help_text='Укажите дату')


class Follow(models.Model):
    """Модель подписки на автора."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', null=True,
                             verbose_name='Пользователь',
                             help_text='Укажите пользователя')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', null=True,
                               verbose_name='Избранный автор',
                               help_text='Укажите автора поста')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            )
        ]
