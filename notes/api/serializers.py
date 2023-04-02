from rest_framework import serializers
from notes.models import Note

class NoteSerializer(serializers.ModelSerializer):
    '''Create note serializer'''
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        '''Validate user input'''

        if data['title'] == data['content']:
            raise serializers.ValidationError({'error':'Title and content cannot be the same'})
        if len(data['title']) < 5:
            raise serializers.ValidationError({'error':'Title cannot be less than five characters'})
        else:
            return data
    
    def create(self, validated_data):
        '''Create a new note'''

        author = self.context['request'].user

        title = validated_data['title']
        content = validated_data['content']

        note = Note(
            title=title,
            content=content,
            author=author,
        )
        note.save()
        return note
    

class UpdateNoteSerializer(serializers.ModelSerializer):
    '''Update note serializer'''

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        '''Validate user input'''

        if data['title'] == data['content']:
            raise serializers.ValidationError({'error':'Title and content cannot be the same'})
        if len(data['title']) < 5:
            raise serializers.ValidationError({'error':'Title cannot be less than five characters'})
        else:
            return data
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
    