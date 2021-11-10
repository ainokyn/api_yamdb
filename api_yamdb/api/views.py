from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from reviews.models import Title


class ReviewsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        title_id = self.kwargs['title_id']
        get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(title.reviews.all, id=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        get_object_or_404(title.reviews.all, id=review_id)
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        get_object_or_404(title.reviews.all, id=review_id)
        serializer.save(author=self.request.user)
