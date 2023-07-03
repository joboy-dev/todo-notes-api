from rest_framework import serializers
import re

from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    '''Todo serializer for creating a new todo item'''

    owner = serializers.StringRelatedField()

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['id', 'is_completed']

    def validate(self, data):
        # if data['name'] == data['content']:
        #     raise serializers.ValidationError({'error': 'Name and Content cannot be the same'})
        if len(data['name']) >= 30:
            raise serializers.ValidationError({'error':'Name is too long'})
        else:
            return data
        
    def create(self, validated_data):
        # get current user
        owner = self.context['request'].user

        name  = validated_data.get('name')
        # content  = validated_data.get('content')
        due_date  = validated_data.get('due_date')

        todo = Todo(
            name=name,
            # content=content,
            due_date=due_date,
            is_completed=False,
            owner=owner
        )

        todo.save()

        return todo

class UpdateTodoSerializer(serializers.ModelSerializer):
    '''Serializer to update todo item'''

    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        # if data['name'] == data['content']:
        #     raise serializers.ValidationError({'error': 'Name and Content cannot be the same'})
        if len(data['name']) >= 30:
            raise serializers.ValidationError({'error':'Name is too long'})
        else:
            return data
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance