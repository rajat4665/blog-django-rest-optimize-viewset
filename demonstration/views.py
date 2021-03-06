from django.db.models import Prefetch
from rest_framework import viewsets

from .models import BlogPost, Comment
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = (
        BlogPost.objects
        .select_related(
            'author',
        )
        .prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.select_related('author')
            )
        )
    )
    serializer_class = BlogPostSerializer

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)

        # For debugging purposes only.
        from django.db import connection
        print('# of Queries: {}'.format(len(connection.queries)))

        return response
