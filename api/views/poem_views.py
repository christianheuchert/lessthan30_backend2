from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models.poem import Poem
from api.serializers import PoemSerializer


class Poems(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PoemSerializer

    def get(self, request):
        """Index request"""
        # Get all the poems:
        # poems = Poems.objects.all()
        # Filter the poems by owner, so you can only see your owned Poems
        poems = Poem.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = PoemSerializer(poems, many=True).data
        return Response({'poems': data})

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['poem']['owner'] = request.user.id
        # Serialize/create poem
        poem = PoemSerializer(data=request.data['poem'])
        # If the poem data is valid according to our serializer...
        if poem.is_valid():
            # Save the created poem & send a response
            poem.save()
            return Response({'poem': poem.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(poem.errors, status=status.HTTP_400_BAD_REQUEST)


class PoemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """Show request"""
        # Locate the poem to show
        poem = get_object_or_404(Poem, pk=pk)
        # Only want to show owned poems?
        if request.user != poem.owner:
            raise PermissionDenied('Unauthorized, you do not own this poem')

        # Run the data through the serializer so it's formatted
        data = PoemSerializer(poem).data
        return Response({'poem': data})

    def delete(self, request, pk):
        """Delete request"""
        # Locate poem to delete
        poem = get_object_or_404(Poem, pk=pk)
        # Check the poem's owner against the user making this request
        if request.user != poem.owner:
            raise PermissionDenied('Unauthorized, you do not own this poem')
        # Only delete if the user owns the  poem
        poem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate poem
        # get_object_or_404 returns a object representation of our poem
        poem = get_object_or_404(Poem, pk=pk)
        # Check the poem's owner against the user making this request
        if request.user != poem.owner:
            raise PermissionDenied('Unauthorized, you do not own this poem')

        # Ensure the owner field is set to the current user's ID
        request.data['poem']['owner'] = request.user.id
        # Validate updates with serializer
        data = PoemSerializer(poem, data=request.data['poem'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicPoems(generics.ListCreateAPIView):
    def get(self, request):
        """Index request"""
        # Get all the poems:
        poems = Poem.objects
        # Run the data through the serializer
        data = PoemSerializer(poems, many=True).data
        return Response({'poems': data})
